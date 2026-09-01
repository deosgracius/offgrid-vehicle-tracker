# BLE Link Walkthrough — scan, connect, bond, subscribe, drain (with code)

Companion to [ARCHITECTURE.md §5](ARCHITECTURE.md#5-ble-link-state-machine-the-risky-component-made-explicit).
Every excerpt below is real code from
[`firmware-display/src/protocol/ble_link.cpp`](../firmware-display/src/protocol/ble_link.cpp),
bench- and road-verified against a live Heltec V4 running Meshtastic 2.7.26.

The one-sentence version: **the display is a BLE *central* (client) that finds the
radio, opens an encrypted connection, subscribes to a "new data" doorbell, and
then reads protobuf frames until the radio says "empty" — forever, with automatic
recovery at every step.**

---

## 0. Why BLE at all?

Meshtastic serves its complete API — every position, node record, and config
message — as protobuf frames over BLE GATT. It is the same interface the
official phone apps use, so it is documented, versioned, and cannot silently
rot. Three GATT characteristics make up the whole protocol:

| Characteristic | Direction | Role |
|---|---|---|
| `ToRadio`   | display → radio | commands (we send one: `want_config_id`) |
| `FromRadio` | radio → display | a **queue** of protobuf frames; read until empty |
| `FromNum`   | radio → display | **notify** "the queue has new data" |

```c
static const char *SVC_UUID       = "6ba1b218-15a8-461f-9fa8-5dcae273eafd";
static const char *TORADIO_UUID   = "f75c76d2-129e-4dad-a1dd-7866124401e7";
static const char *FROMRADIO_UUID = "2c55e69e-4993-11ed-b878-0242ac120002"; // fw 2.x
static const char *FROMNUM_UUID   = "ed9da18c-a800-4f66-a670-aa7547e34453";
```

> Bench lesson: the `FromRadio` UUID changed in firmware 2.x. Older tutorials
> list `8ba2bcc2-…` and fail with "missing characteristic".

## 1. SCANNING — find the radio (address first, scan second)

**How.** We do *not* start with a radio scan. The radio's BLE address is
persisted in NVS flash, and the first move is always a **direct connect** to
that remembered address. Only if that fails do we run a 1.5 s active scan
looking for any device advertising the Meshtastic service UUID — and whatever
the scan finds *becomes* the new remembered radio:

```c
// 1) Direct connect to the remembered radio. The connect procedure
//    itself listens ~10 s for that address — our fastest way to
//    catch a brief (or directed-only) advertising window.
if (s_have_addr) {
    attempted = true;
    ok = try_connect(s_known_addr);
    if (!ok) teardown();
}

// 2) Scan pass: first pairing, or the remembered radio is gone /
//    replaced. Whatever we find becomes the new remembered radio.
if (!ok) {
    NimBLEScan *scan = NimBLEDevice::getScan();
    scan->setActiveScan(true);
    NimBLEScanResults results = scan->getResults(1500, false);
    for (int i = 0; i < results.getCount(); i++) {
        const NimBLEAdvertisedDevice *dev = results.getDevice(i);
        if (dev->isAdvertisingService(NimBLEUUID(SVC_UUID))) { found = dev; break; }
    }
    if (found) { remember_radio(found->getAddress()); ok = try_connect(s_known_addr); }
}
```

**Why address-first.** Bench-proven Meshtastic behavior: the radio only
*general-advertises* in a window from boot until its first BLE disconnect, and
a previously-paired radio may only send *directed* advertisements — invisible
to scans. A direct connect by address catches both cases; a scan alone would
never reconnect. This is also why the product flow is "ignition-on": both
units power up together, and the display catches the radio's boot window.

**Why the scan still exists.** First-ever pairing, and radio replacement. If
Victor swaps in radio #2, no reflash is needed — the scan finds it and NVS
learns the new address automatically.

Failures back off exponentially (1 → 2 → 4 → 8 s cap) so a missing radio
doesn't burn the battery, and `node_table_publish(false)` keeps feeding the UI
so the screen shows "LINK SEARCHING…" instead of freezing.

## 2. CONNECTING — open the link (3 tries, 10 s timeout)

```c
s_client = NimBLEDevice::createClient();
s_client->setClientCallbacks(&s_cb, false);
s_client->setConnectTimeout(10000);
for (int attempt = 1; attempt <= 3 && !connected; attempt++) {
    connected = s_client->connect(addr);
    if (!connected) vTaskDelay(pdMS_TO_TICKS(250));
}
```

**Why 3 × 10 s.** The radio's advertising window can be brief; a single
attempt misses it too often, and an unbounded wait would stall the state
machine. Three paced attempts inside one SCANNING pass hit the sweet spot
measured on the bench. Init also sets `setPower(9)` (+9 dBm) because the
default TX power proved marginal for connect handshakes, and `setMTU(517)` so
a full protobuf frame fits in one read.

## 3. BONDING — encrypt the pipe (Just Works, by design)

```c
NimBLEDevice::setSecurityAuth(/*bond*/ false, /*mitm*/ false, /*sc*/ true);
NimBLEDevice::setSecurityIOCap(BLE_HS_IO_NO_INPUT_OUTPUT);
...
s_state = BLE_BONDING;
if (!s_client->secureConnection()) {
    Serial.println("[ble] bonding failed (wrong PIN / rejected?)");
    return false;
}
```

**How.** The Heltec runs `bluetooth.mode NO_PIN`, so pairing is BLE
"Just Works": an encrypted session is negotiated on every connect with no PIN
dialog, no button presses, no stored bond required on our side.

**Why not a stored bond + PIN.** Hard-won: **a bonded Meshtastic peripheral
stops general advertising** — it becomes undiscoverable to everyone,
including (after certain resets) its own peer, and the only cure is a factory
reset. Re-pairing on every connect is fast, still encrypted (LE Secure
Connections), and sidesteps that trap entirely. MITM protection is off
because the threat model is two boards a meter apart inside a locked vehicle.
The same reasoning is behind the hard rule in init: **never
`deleteAllBonds()` at boot.**

## 4. SUBSCRIBED — turn on the doorbell, request the dump

```c
if (!s_fromNum->subscribe(true, notify_cb)) { ... return false; }
s_state = BLE_SUBSCRIBED;

// Handshake: ask for the config + node DB dump.
uint32_t nonce = (uint32_t)esp_random();
size_t n = proto_encode_want_config(buf, sizeof(buf), nonce);
s_toRadio->writeValue(buf, n, /*response*/ true);
```

**How.** Subscribing to `FromNum` asks the radio to *notify* us whenever its
outgoing queue has data — event-driven, no polling. Then we write exactly one
command, `want_config_id` with a random nonce, which tells the radio: "replay
your identity (`MyNodeInfo`), your node database (every node it knows,
including itself and the partner), then echo my nonce back." When the nonce
comes back in `config_complete_id`, we know the snapshot is complete.

**Why.** This handshake means the display never starts blind: even before the
first live packet arrives, it gets the radio's last known picture of the
world. The nonce guards against mixing up dumps from a reconnect.

The notify callback does *one thing* — sets a flag:

```c
static void notify_cb(...) {
    // FromNum notify = "new FromRadio data queued". Drain from the task, never here.
    s_notify_pending = true;
}
```

**Why so lazy?** The callback runs on the BLE stack's own task. Doing GATT
reads from inside it can deadlock the stack. Flag here, drain from our task.

## 5. DRAINING — read until empty, decode every frame

```c
static void drain_from_radio(void) {
    s_state = BLE_DRAINING;
    for (;;) {
        NimBLEAttValue v = s_fromRadio->readValue();
        if (v.size() == 0) break;          // radio says: queue empty
        proto_decode_from_radio(v.data(), v.size());
    }
    s_state = BLE_SUBSCRIBED;
}
```

**How.** `FromRadio` behaves like a vending machine: every read hands over the
next queued protobuf frame; a zero-length read means the queue is empty. Each
frame goes to nanopb, which decodes it into `Position` / `NodeInfo` /
`MyNodeInfo` and updates the node table. Then we drop back to SUBSCRIBED and
wait for the next doorbell.

**Why drain-until-empty instead of one-read-per-notify.** The radio coalesces:
one notify can mean five queued frames (typical after the config dump, or
after a burst of mesh traffic). Reading until empty guarantees we never lag
behind the queue.

## 6. Failure = teardown = back to SCANNING

```c
static void teardown(void) {
    if (s_client) NimBLEDevice::deleteClient(s_client); // also disconnects
    s_toRadio = s_fromRadio = s_fromNum = nullptr;
    proto_reset_config_state();
    s_state = BLE_SCANNING;
}
```

Every failure — connect timeout, pairing rejected, missing characteristic,
mid-session disconnect — funnels through the same teardown into SCANNING.
There is exactly one recovery path, so there is no state where the link can
wedge. Throughout all of it the task keeps publishing `TrackerState` once a
second, so the UI always renders last-known data with an honest age and link
flag. **Link loss degrades the display; it never blanks it.**

Road-proven (Sep 1 drive test): the link dropped while the radio was carried
across the house (`disconnected reason 531`) and re-established itself with no
user action — direct connect caught the radio, re-paired, re-subscribed,
re-drained.

---

# End-to-end data flow — one packet's journey, step by step

The same story as [ARCHITECTURE.md §4](ARCHITECTURE.md#4-end-to-end-data-flow),
told as a single unbroken chain. **Across vehicles:**

1. **GPS fix (partner vehicle).** The GNSS module computes a fix once per
   second and streams it as NMEA sentences **over UART** into Meshtastic B.
2. **Meshtastic B builds a Position packet** — lat/lon (1e-7 deg), ground
   speed (km/h), track, and GPS UTC time — and **broadcasts it over LoRa every
   30–60 s** (60 s timer, or every 30 s / 50 m while moving). ~0.5 s airtime,
   AES-256 on the private Group9 channel, relayed by any mesh node in between.
3. **Meshtastic A receives the packet**, decrypts it, and files it in its node
   database — then queues it on `FromRadio` and rings the `FromNum` doorbell.
4. **`protocol/` (Deo) drains the queue over BLE**: notify → read `FromRadio`
   until empty → **nanopb decodes** each frame → `node_table` stores the
   partner fix with a timestamp. (Our own vehicle's position takes this exact
   path minus steps 2–3's LoRa hop — the local radio streams its own GPS too.)

**Inside the display node:**

5. **`node_table` publishes `TrackerState`** once per second — self fix,
   partner fix, data ages, link flag, GPS clock — into the mutex-protected
   struct. One writer.
6. **The nav engine (Josiah) reads `TrackerState`** — one reader — and computes
   distance (haversine), bearing to partner (θ), and arrow angle = θ − own
   course-over-ground, with a north-up compass fallback when stationary.
7. **`ui_render` redraws the RLCD at 2 Hz**: arrow, distance in miles, data
   age, link status, local clock — and the driver sees the partner move.

End-to-end latency is ≈ the LoRa airtime (~0.5 s) — negligible against the
30–60 s broadcast cadence, which is why **data age, not delivery confirmation,
is the reliability metric shown to the driver**: a newer position always
supersedes an older one, so a lost packet costs 30 s of freshness, never
correctness.
