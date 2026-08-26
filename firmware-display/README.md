# Display firmware (Waveshare ESP32-S3-RLCD-4.2)

The only custom firmware in the system. Two modules, two owners:

- `protocol/` — **Deo.** Meshtastic BLE client: NimBLE central, pairing, `FromRadio`
  protobuf decode (nanopb), node tracking. Publishes `TrackerState` (DESIGN.md §7).
- `ui/` + `nav/` — **Josiah.** RLCD rendering, arrow/distance/staleness UI, and the
  distance/bearing/heading math. Consumes `TrackerState` — develop against fake data
  until integration (week 7).

The `TrackerState` struct is the contract between the two halves — change it only by agreement, in one commit that updates both sides.

Starting points:
- Waveshare demo code: https://github.com/waveshareteam/ESP32-S3-RLCD-4.2
- Meshtastic Client API: https://meshtastic.org/docs/development/device/client-api/
- Meshtastic protobufs: https://github.com/meshtastic/protobufs (+ nanopb)
- Prior art for ESP32-as-BLE-client-of-Meshtastic: https://github.com/0io/ESPHome-Meshtastic-MQTT
