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
python -m meshtastic --port COMx --set position.gps_update_interval 30
python -m meshtastic --port COMx --set bluetooth.mode NO_PIN   # only if a display pairs to it
```

(The URL embeds the channel key — fine in this team repo, don't post publicly.
It also carries `position_precision 32` — full-resolution positions. The
channel default of 13 truncates every broadcast to a ~6 km grid, which froze
the displayed location during the 2026-08-31 drive test; if positions ever
look quantized/stuck, check `positionPrecision` in `--info` first.)
Radio #1 config summary: region US · channel Group9 (private PSK, precision 32) ·
broadcast 60 s / smart 10 s + 20 m · gps_update_interval 30 · bluetooth NO_PIN.
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
