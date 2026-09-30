# Radio & hardware — Victor

## Radio #2 provisioning (REQUIRED — do this when flashing the second radio)

Radio #1 runs on a **private encrypted channel** ("Group9", random PSK) — the
default public channel clamps position broadcasts to 1 hour, and the team needs
its own encryption anyway. Radio #2 MUST join the same channel or the radios
cannot decrypt each other. After flashing radio #2 + setting `lora.region US`:

```
python -m meshtastic --port COMx --seturl "https://meshtastic.org/e/#Ci4SIC0URMiOXgfkbAVS687btSBj1NwlgUQFVPeHuTw59xsGGgZHcm91cDk6AgggEhQIARj6ASALOAFAA0gBUB5oAdAGAQ"
python -m meshtastic --port COMx --set position.position_broadcast_secs 60
python -m meshtastic --port COMx --set position.broadcast_smart_minimum_interval_secs 10
python -m meshtastic --port COMx --set position.broadcast_smart_minimum_distance 20
python -m meshtastic --port COMx --set position.gps_update_interval 10
python -m meshtastic --port COMx --set bluetooth.mode NO_PIN   # only if a display pairs to it
python -m meshtastic --port COMx --set telemetry.device_update_interval 300   # 5-min heartbeat keeps online counters honest on the bench
python -m meshtastic --port COMx --set device.role CLIENT_MUTE   # 2-node system: relaying each other's packets is pure airtime waste (halves ChUtil). REVERT to CLIENT if a 3rd node/relay is ever added
python -m meshtastic --port COMx --set canned_message.enabled true
python -m meshtastic --port COMx --set-canned-message "OK|Yes|No|Hi|How are you?|All good|Need help|Are you injured?|Send position|Position updated|On my way|Wait there|Arrived|Low battery|Heading home"
```

(Canned messages: on-screen preset texts selectable with the user button —
quick replies first, then status/safety/position/movement. Both radios carry
the identical set (applied + `--get-canned-message`-verified 2026-09-25) so
every prompt has its short answer available on the other end.)

**Config-write trap (cost us an afternoon):** settings that trigger a reboot
(`lora.region`, `bluetooth.mode`) may silently revert when set via
`meshtastic --set ...` — the CLI's serial-port close toggles DTR/RTS, which
hard-resets the ESP32 *before* it finishes saving. Always `--get` to verify;
if a value keeps reverting, set it via the Python API and hold the port open
~20 s (see `git log` for the recovery session), or use the phone app.

**Channel-change truth-teller (solved the 2026-09-25 "0 online" mystery):** after
ANY `--seturl`, check the OLED **LoRa screen frequency**. The frequency slot is
`djb2(channelName) % 104` — **Group9 = slot 43 = 912.875 MHz**. The default
public channel is slot 19 = 906.875 MHz. If a radio "on Group9" shows 906.875,
the channel write silently reverted (see config-write trap) and the radios are
on different frequencies — same key, mutual deafness, both show "0 online".
`--info` can read back the intended config while the radio still radiates on the
old slot until a clean reboot, so trust the screen, not just the CLI. Link was
verified 2026-09-25: round-trip traceroute ead4↔bb5c on Group9, ~6 dB SNR both
directions at 30 dBm desk range ("1 online" on both OLEDs).

**"0 online" with a perfect link (bench-only illusion):** a node with **no live
GPS fix rebroadcasts its stored position with the OLD fix timestamp** — peers
book it as "last heard" months ago, so the OLED online counter stays 0 (or
counts stale ghosts as online after a clock-less reboot: we saw "17 online"
from a July node list) even while texts and traceroutes work perfectly. Fix:
give the node a real fix (window/outside); the first live position broadcast
heals the counter on both ends (verified 2026-09-25: fresh fix → "16 secs ago"
→ 1 online) — but only until the fix is lost again: the stored stale fix
resumes broadcasting and drags last-heard back (ours read "72d ago" mid-chat).
Permanent cure: `meshtastic --port COMx --remove-position` (clears the stored
position; no-fix periods then go quiet instead of lying) + `--set-time` to
sync the clock. Impossible in a vehicle with sky view — bench artifact only.
Related: `--reset-nodedb` can silently no-op (same DTR port-close race as
config writes) — re-run and verify the node count actually dropped.
Also: every serial connection hard-resets the radio (DTR), and fw 2.7.26
saves its node DB to flash only on its own schedule — so a stale flash
record can outlive wipes and commanded reboots on the bench. It heals by
itself once real traffic flows; don't chase it. Leave bench radios OFF
USB when observing the online counters.

**Stale-pubkey trap (2026-09-27):** broadcasts work but DIRECT packets
(position requests, DMs) silently time out in ONE direction = the requester
holds an outdated public key for the peer (keys regenerate on factory
re-flash). Direct traffic is encrypted to the STORED key; the peer drops what
it cannot decrypt, with no NAK. Fix: `--reset-nodedb` on the requester, wait
~1 min for NodeInfo relearn, retry — verified: request then returned the
peer's live fix. Also: a stale node-DB position entry poisons the distance
screen (ours showed ~11 km between radios on the same desk) until any fresh
position packet overwrites it.

**Battery-death CONFIG LOSS (2026-09-30 — affects BOTH radios):** letting a
radio's battery run dead can silently revert configuration on the next boot —
observed twice in one night: RG lost its channels (back to the public slot),
SF lost EVERYTHING (factory channel, role, bluetooth, telemetry, owner name).
Symptom is always the same: healthy screens, total mutual silence. PRE-FLIGHT
RULE before any test or drive: check both OLED LoRa screens read 912.875 MHz —
two seconds, catches every variant of this. OPERATING RULE: don't run the
radios to empty; power off or charge before the battery dies. Recovery: this
section's recipe top to bottom, then verify a power-cycle keeps 912.875.

**Flat-battery wedge (2026-09-27):** a radio whose battery ran flat can come
back half-alive when charged: OLED renders and shows a GPS fix, but the LoRa
TX and USB serial are both frozen (nothing heard from it for 18 h; CLI could
not connect on a working COM port). A screen that looks fine proves nothing —
check its LAST-HEARD age on the OTHER radio. Cure: full power-cycle (off 5 s,
on); it announces itself within a minute of a clean boot.

**Flashing trap:** `pio run -t upload` auto-picks the only COM port — with two
identical ESP32-S3 boards, ALWAYS pass `--upload-port` and verify which board
is on which port first (unplug one and watch which port disappears). We once
overwrote the radio's Meshtastic with display firmware this way. Full radio
recovery = flash `firmware-heltec-v4-*.factory.bin` at 0x0 with esptool, then
re-apply this section top to bottom (node number survives — it derives from
the MAC).

**After ANY factory re-flash, re-run this whole section and `--get`-verify every
line.** Radio #1 was found on 2026-09-25 with factory position settings (3600 s
broadcast / 120 s GPS) and RANDOM_PIN bluetooth — silently reset by the Sep 3
recovery re-flash. A drive test in that state shows hour-stale positions and
the display cannot pair. Re-applied and verified 2026-09-25; both radios now
match this recipe.

(The URL embeds the channel key — fine in this team repo, don't post publicly.
It also carries `position_precision 32` — full-resolution positions. The
channel default of 13 truncates every broadcast to a ~6 km grid, which froze
the displayed location during the 2026-08-31 drive test; if positions ever
look quantized/stuck, check `positionPrecision` in `--info` first.)
Radio #1 config summary: region US · channel Group9 (private PSK, precision 32) ·
broadcast 60 s / smart 10 s + 20 m · gps_update_interval 10 · bluetooth NO_PIN.
(gps_update_interval must be <= the smart interval, or the radio re-broadcasts
stale fixes: at 30 s GPS / 10 s smart, updates still only changed every 30 s.)
(10 s ≈ 5% channel airtime per moving node at SF11 — do not go faster; Meshtastic
throttles position broadcasts above ~25% utilization, and 1 Hz is physically
impossible at this range setting: each broadcast costs ~0.5 s of airtime.)

Heltec WiFi LoRa 32 V4 setup, radio configuration, antennas, and range testing.

Put here:
- Meshtastic config exports (channel/preset/interval settings used on both nodes)
- GNSS module notes (which module, wiring, fix quality)
- Antenna selection notes + mount photos
- `range-tests/` — one dated log per test: locations, terrain, preset, antenna, result

First tasks (W2–W3): flash stock Meshtastic via https://flasher.meshtastic.org, attach the
GNSS modules, confirm both nodes see each other's position in the Meshtastic phone app.
**Week 1 blocker check: do the kits include the GNSS modules?** (V4 has a connector, not onboard GPS.)

## Radio #2 — provisioned state (2026-09-25)

Fully on team spec and link-verified against radio #1: Group9 primary
(912.875 MHz, precision 32) · position broadcast 60 s / smart 10 s + 20 m ·
gps_update_interval 10 · tx_power 30. The first provisioning attempt had left
the position settings at factory defaults (3600 s broadcast / 300 s smart) —
the channel URL only carries channel + LoRa config, so the `position.*` lines
of the recipe must be applied and `--get`-verified separately.

## Radio #2 — as-received record (2026-09-24)

Arrived as "Meshtastic bb5c (RG)", node 0x49B5DBDC-family, fw 2.7.26, region
US, default public primary channel plus a secondary "Alaska" channel. To
restore Dr. Gale's original configuration if the radio is ever returned:

```
python -m meshtastic --port COMx --seturl "https://meshtastic.org/e/#CgcSAQE6AgggCi4SIGeI9YYn01Lhr8NNDAcoqCpLhQJ2JHpMnBz0Hw0h4qk9GgZBbGFza2E6AgggEhQIARj6ASALOAFAA0gBUB5oAdAGAQ"
```
