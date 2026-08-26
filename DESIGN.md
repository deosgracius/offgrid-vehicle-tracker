# Off-Grid Vehicle Tracking — Design Document

Project sponsor: Dr. Richard Gale
Goal: fully off-grid system showing the **direction and distance** to a partner vehicle on a driver-visible screen, over moderate distances with no cell/WiFi (Alaska use case).

---

## 1. Hardware (verified specs)

### Radio/GPS unit — Heltec WiFi LoRa 32 V4
- ESP32-S3 + Semtech SX1262 LoRa (915 MHz US band), up to **28 dBm TX** (high-power version), −137 dBm sensitivity
- WiFi b/g/n + BLE, 0.96" OLED, USB-C, solar-charge input (4.7–6 V)
- **Important:** GPS is *not* on the main board. The V4 has a 1.25mm 8-pin **GNSS connector**; the GPS receiver is a separate small module that plugs into it.
  → **Action item: confirm the Meshnology Amazon kit ships with the GNSS module.** If not, order Heltec's GNSS module (or a UC6580/L76K module wired to the connector).
- Officially supported by Meshtastic firmware.

### Display unit — Waveshare ESP32-S3-RLCD-4.2
- 4.2" reflective LCD, 300×400, black & white — sunlight-readable (reflective, like e-paper but with fast refresh), ideal for a dashboard in daylight
- ESP32-S3, 16 MB flash / 8 MB PSRAM, WiFi + BLE
- USB-C, optional 18650 battery, microSD, RTC
- Supported in Arduino IDE and ESP-IDF; Waveshare publishes demo code on GitHub (`waveshareteam/ESP32-S3-RLCD-4.2`)
- Note: reflective = great in daylight, **invisible at night without a light**. For night driving, plan a small LED edge-light or accept dome-light use.

### Quantities (2-vehicle system)
| Item | Qty | Notes |
|---|---|---|
| Heltec V4 + GNSS module | 2 | one per vehicle |
| Waveshare RLCD-4.2 | 1–2 | 2 if both drivers want a display |
| External 915 MHz antenna + roof mount | 2 | biggest single range improvement; stock whip antennas inside a metal vehicle will cripple range |
| USB power (12 V → 5 V) | 2–4 | vehicle power; no batteries to manage |

---

## 2. Architecture decision

### Recommended: stock Meshtastic firmware on the Heltecs + custom firmware on the display

**No Meshtastic hacking required.** Meshtastic exposes a documented **Client API** — a stream of `FromRadio`/`ToRadio` protobuf messages over BLE, USB serial, or TCP. It's the same API the Meshtastic phone apps use. The device firmware already:
- reads GPS and broadcasts position over LoRa on a configurable interval
- maintains a node database (last known position of every node it has heard)
- pushes `NodeInfo` / `Position` packets to any connected API client
- handles encryption (AES), channel management, and mesh relaying for free

So the system is:

```
Vehicle A                                Vehicle B
┌─────────────────┐                     ┌─────────────────┐
│ Heltec V4        │◄══ LoRa 915 MHz ══►│ Heltec V4        │
│ (stock Meshtastic│    position         │ (stock Meshtastic│
│  + GPS module)   │    broadcasts       │  + GPS module)   │
└───────┬─────────┘                     └───────┬─────────┘
        │ BLE (Meshtastic Client API,           │ BLE
        │ protobufs)                            │
┌───────▼─────────┐                     ┌───────▼─────────┐
│ Waveshare RLCD   │                     │ Waveshare RLCD   │
│ custom firmware: │                     │ (optional 2nd    │
│ arrow + distance │                     │  display)        │
└─────────────────┘                     └─────────────────┘
```

The only firmware **we** write runs on the Waveshare board:
1. BLE central: scan for the Heltec, connect, subscribe to the Meshtastic GATT service (`6ba1b218-...` service; `fromRadio`/`toRadio`/`fromNum` characteristics)
2. Decode protobufs with **nanopb** (Meshtastic publishes its `.proto` files; the `meshtastic/protobufs` repo + nanopb generates the C decoders)
3. Track two positions: **own node** (local GPS) and **partner node** (from mesh `Position` packets)
4. Compute distance + bearing, render big on the RLCD

Prior art proving the BLE-client approach works from an ESP32: the ESPHome-Meshtastic-MQTT gateway project does exactly this GATT client + protobuf decode.

**Why not ESP-NOW for the wireless link?** ESP-NOW requires custom firmware on *both* ends — stock Meshtastic doesn't speak it. BLE costs nothing because Meshtastic already serves its API over BLE. ESP-NOW only makes sense in the fallback plan below.

### Fallback: fully custom firmware (if Meshtastic BLE proves painful)
Both Heltecs run custom RadioLib-based firmware: read GPS over UART, broadcast `{id, lat, lon, course, ts}` every N seconds over raw LoRa; forward to the display via ESP-NOW or BLE. Simpler data path, total control, but we lose mesh relay, encryption, store-of-last-position, the phone app for debugging, and range-tested radio settings. Keep as plan B.

---

## 3. Direction & distance math

- **Distance:** haversine between own fix and partner's last fix.
- **Bearing to partner:** standard initial-bearing formula (true north referenced).
- **Direction the driver sees** must be relative to the *vehicle's heading*, not north. Use **GPS course-over-ground** from the own-node position packets — in a moving vehicle this is accurate above ~5 mph. Show absolute compass bearing (N/E/S/W arrow) when stationary/slow, or hold last heading.
  - No magnetometer needed (and inside a vehicle a magnetometer is unreliable anyway).
- Display: large rotating arrow + distance in mi/km + data age ("2 min old") + link status. Data age matters: with 30–60 s position intervals and possible dropouts, the driver must know how stale the fix is.

## 4. Radio/range reality check (set expectations with Dr. Gale)

- Vehicle-to-vehicle at ground level, 915 MHz: typically **2–8 km in open/rolling terrain**, much more with line of sight (ridge to ridge), much less in deep valleys/dense forest. Terrain blocking is the dominant factor in Alaska, not TX power.
- Mitigations: roof-mounted external antennas (largest win), Meshtastic `LONG_FAST`→`LONG_SLOW` presets trade update rate for link margin, and any other Meshtastic node in the area (or a cheap third node left on a high point) relays automatically — a mesh benefit the custom-firmware fallback wouldn't have.
- Position broadcast interval: 30–60 s is a good balance of freshness vs. airtime/legal duty cycle.

## 5. Build plan (phased)

1. **Bench bring-up** — flash stock Meshtastic on both Heltecs via web flasher, attach GPS, verify position exchange using the Meshtastic phone app. (Zero code; validates all hardware.)
2. **Display hello-world** — run Waveshare's demo, get LVGL or plain framebuffer text/arrow rendering on the RLCD.
3. **BLE client** — Waveshare connects to Heltec, receives `FromRadio` stream, decodes `Position`/`NodeInfo` with nanopb. (This is the hard/risky milestone — do it early.)
4. **Nav math + UI** — bearing/distance/heading, arrow UI, staleness indicator.
5. **Vehicle test** — two cars, external antennas, real-world range logging.
6. **Polish** — enclosures, 12 V power, night lighting, config (pairing, units).

## 6. Open questions / risks

- Does the Meshnology kit include the GNSS module? (Blocker for everything — verify on arrival.)
- Meshtastic BLE bonding/pairing from a custom ESP32 central: the API requires a PIN pairing step; need to confirm the ESP32 NimBLE stack handles Meshtastic's bonding flow (prior art suggests yes). Fallback if BLE fights us: Meshtastic also serves the same API over **WiFi/TCP** (port 4403) — Heltec joins a WiFi network; the Waveshare could host a softAP. Still wireless, same protobufs.
- Night readability of the reflective LCD (see hardware note).
- V4 is a new board (late 2025) — confirm current Meshtastic firmware release fully supports the V4 + its GNSS module out of the box.

---

## 7. Team roles (Group 9 — Deo, Josiah, Victor, Cannon)

The system has natural seams, so the four tracks can run mostly in parallel after week 2:

**Victor — Radio & hardware lead (Heltec/Meshtastic side)**
Flash and configure Meshtastic on both Heltecs, integrate the GNSS modules, verify position exchange with the phone app, choose radio preset (LONG_FAST vs LONG_SLOW) and broadcast interval, select/mount external antennas, run structured range tests and log results. Owns the "does the link work in the real world" question — the part Dr. Gale will ask about first.

**Deo — Protocol firmware (the risky one)**
The Meshtastic BLE client on the Waveshare board: NimBLE central, bonding/PIN pairing, subscribing to the GATT service, decoding `FromRadio` protobufs with nanopb, maintaining own-position and partner-position state. Deliverable is a clean data interface the UI consumes:
```c
struct TrackerState {
  Fix   self;        // lat, lon, course, speed, fix_ok
  Fix   partner;     // lat, lon, age_seconds, valid
  bool  ble_connected;
};
```
This is the highest-uncertainty work — start it the day the boards arrive. If BLE bonding fights back for more than ~2 weeks, switch to the WiFi/TCP (port 4403) fallback — same protobufs, simpler transport.

**Josiah — Display & navigation firmware**
RLCD driver bring-up from Waveshare's demo code, rendering (big rotating arrow, distance, staleness, link status), haversine + bearing math, heading from course-over-ground with the stationary/slow-speed fallback. Can develop against *fake* `TrackerState` data from day one — no dependency on Deo's track until integration.

**Cannon — Systems integration & test lead**
Vehicle power (12 V→USB), mounting/enclosures, night-lighting solution for the RLCD, integration testing when B+C merge, drive tests with Role A, plus project management: parts ordering/tracking, the shared repo, weekly status, and the final report/demo for Dr. Gale. In weeks 1–5 (before there's much to integrate), Cannon pairs with Victor on bench bring-up and range testing.

Shared rules: one git repo from day one; B and C agree on the `TrackerState` interface in week 1 and treat it as a contract; everyone flashes their own boards (no single "person with the hardware").

## 8. Schedule (14-week semester, part-time)

| Weeks | Milestone |
|---|---|
| 1–2 | Parts ordered & arrived; Meshtastic flashed; positions visible in phone app (Victor/Cannon). Waveshare demo running (Josiah). Repo + interface contract set (all). |
| 3–5 | **BLE client receives and decodes Position packets (Deo)** — the make-or-break milestone. Arrow UI working on fake data (Josiah). First antenna range test (Victor/Cannon). |
| 6–7 | Integration: live partner position on the RLCD on the bench. |
| 8–9 | Two-vehicle drive tests; fix heading/staleness/reconnect issues found on the road. |
| 10–11 | Mounting, 12 V power, enclosures, night lighting; second display unit if building two. |
| 12–13 | Buffer (something in weeks 3–9 will slip — most likely BLE pairing or V4 GNSS support). Final range characterization. |
| 14 | Demo + report for Dr. Gale. |

Estimate: **one semester at a few hours/person/week**, with working bench demo around week 7 and road-tested system by week 11. The long pole is the protocol firmware (Deo); the most common schedule killer is parts delay — order everything in week 1, including the GNSS modules and external antennas.
