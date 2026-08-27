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
