# Display firmware (Waveshare ESP32-S3-RLCD-4.2)

The only custom firmware in the system. PlatformIO project — install the PlatformIO
extension in VS Code (or `pip install platformio`), then:

```
pio run -e display              # build firmware
pio run -e display -t upload    # flash the Waveshare board (USB-C)
pio device monitor              # watch the serial output
pio test -e native              # run nav-math unit tests on your LAPTOP (no hardware)
```

`SIM_MODE=1` (the default, set in [platformio.ini](platformio.ini)) feeds the UI from the
simulator — the whole pipeline runs with zero radios. Set `-DSIM_MODE=0` once the BLE link
is implemented.

## Layout & ownership

```
include/tracker_state.h    THE CONTRACT (Deo + Josiah co-own; change = 1 agreed commit)
src/protocol/  (Deo)       tracker_store (mutex'd state) · ble_link (NimBLE central, stub)
src/nav/       (Josiah)    distance/bearing/arrow math — DONE, unit-tested
src/ui/        (Josiah)    ui_render — serial stub; TODO: RLCD driver from Waveshare demo
src/sim/       (shared)    5 fake-data scenarios (approaching, crossing, stationary,
                           stale, link-lost) — drives the UI on the bench
test/test_nav/             nav unit tests (pio test -e native)
```

Data flow (one direction, one writer/one reader):
`ble_link | sim_feed` → `tracker_store_set()` → `tracker_store_get()` → `nav_compute()` → `ui_render`

## Status (Aug 31, 2026 — protocol track functionally complete)

**Entire pipeline verified with live data**: connect → pair → subscribe →
want_config → FromRadio drain → nanopb decode → config dump → **real GPS
position decoded end-to-end** (`[node] pos 0x49b5ead4: 33.633..., -101.895...`
from a 7-sat fix), with the BLE link surviving a walk across the room.
Heltec config: `bluetooth.mode NO_PIN`. See commits `1598376`..`f73b96f`.

**Known Meshtastic behavior (fw 2.7.26), design consequence:** the radio
advertises only from boot until its first BLE disconnect — after that, no new
connection is possible until the radio reboots (regardless of bond/PIN mode).
Validated product flow: **power both units together** ("ignition-on"); the
display fires direct-connect attempts continuously and reliably catches the
radio's boot window, then the link holds. Mid-drive link loss requires a radio
power-cycle — document as a limitation; candidate fixes: newer Meshtastic
firmware, or an upstream look at NimbleBluetooth advertising-restart logic.

Remaining protocol work (small): persist the radio's BLE address in NVS
(currently hardcoded for the bench unit), partner-node selection UI hook, and
long-run soak testing. The arrow will light up the moment a second radio
(Victor's) broadcasts positions into the mesh — no new decode work needed.

## Product requirement — location-aware clock (Deo, Aug 31)

If the driver display shows a clock, local time must follow the vehicle's
location automatically (Texas -> Alaska crosses 3 zones). We have everything
needed on-device: GPS supplies UTC (`Position.time`) and position; derive the
zone from a small longitude/latitude band table (US + Alaska political zones
+ DST rules) — no user setting, no network. Note: the Heltec's own OLED can't
do this (stock Meshtastic supports only a static `tzdef` string — currently
set to CST6CDT for the bench); that screen is not driver-facing, so cosmetic.
Implementation slot: a `nav/local_time` helper feeding Josiah's UI.

## Replacement-display bring-up checklist (run top to bottom when the new panel arrives)

Precondition: both radios provisioned per `hardware/README.md` (Group9 @ 912.875,
verified on the OLED LoRa screen) and radio 1 set to `bluetooth.mode NO_PIN`.

1. [ ] Assemble the 3D-printed case FIRST (armor on before first power-up;
       M2.5×6 screws max — see the case notes in `hardware/README.md`).
2. [ ] `pio run -e display -t upload` (SIM_MODE) — RLCD shows the sim scenarios;
       BOOT cycles them. Proves panel + flash + UI with zero radios.
3. [ ] `pio run -e display-ble -t upload`, then power display and radio 1
       TOGETHER ("ignition-on" flow) — serial shows connect → pair → subscribe →
       config dump; screen shows RADIO LINK connected.
4. [ ] Own position appears (radio 1 near a window / outside, needs a GPS fix).
5. [ ] Partner appears: radio 2 on and with a fix — arrow, distance, bearing
       populate from its broadcasts. Ages tick honestly.
6. [ ] **Position-request button (commit `01b9373`; radio-level exchange
       pre-proven 2026-09-27: CLI `--request-position` returned the partner's
       live fix at full precision — only the button→BLE write is untested)**: let radio 2 sit
       PARKED with a fix so its cadence drops to 60 s. Wait until the partner
       age on the display reads ≥ 30 s, then press BOOT on the display.
       Expect: serial logs `position request sent to 0x...`, and the partner
       age snaps to ~2 s within a couple of seconds — that reply came from the
       want-response request, not the schedule. If it does not: check serial
       for `no partner known yet` (node DB still empty) or `no radio link`.
7. [ ] BLE RSSI sanity with the case on: within ~2 dB of the bare-panel value
       (case acceptance criterion).

## Next steps

- **Deo** — implement `ble_link.cpp` per the milestones in its header comment. Before
  writing any of it, prove the API from a laptop: `pip install meshtastic`, then
  `meshtastic --ble-scan` and `meshtastic --ble <name> --nodes`. Then add nanopb +
  the Meshtastic protobufs (`proto_decode`).
- **Josiah** — `pio test -e native` should pass on your machine today. Then replace the
  serial stub in `ui_render.cpp` with the RLCD driver from the
  [Waveshare demo](https://github.com/waveshareteam/ESP32-S3-RLCD-4.2); build against
  `SIM_PARTNER_APPROACHING` first, then the other four scenarios.
- Board settings note: `platformio.ini` uses the generic ESP32-S3 devkit board with
  16 MB flash / octal PSRAM flags. If flashing or PSRAM misbehaves, compare against the
  settings in Waveshare's demo project and adjust `board_build.*`.

Starting points: [Meshtastic Client API](https://meshtastic.org/docs/development/device/client-api/) ·
[Meshtastic protobufs](https://github.com/meshtastic/protobufs) ·
[prior art: ESP32 BLE client of Meshtastic](https://github.com/0io/ESPHome-Meshtastic-MQTT)
