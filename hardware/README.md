# Radio & hardware — Victor

## Radio #2 provisioning (REQUIRED — do this when flashing the second radio)

Radio #1 runs on a **private encrypted channel** ("Group9", random PSK) — the
default public channel clamps position broadcasts to 1 hour, and the team needs
its own encryption anyway. Radio #2 MUST join the same channel or the radios
cannot decrypt each other. After flashing radio #2 + setting `lora.region US`:

```
python -m meshtastic --port COMx --seturl "https://meshtastic.org/e/#Ci4SIC0URMiOXgfkbAVS687btSBj1NwlgUQFVPeHuTw59xsGGgZHcm91cDk6AggNEhQIARj6ASALOAFAA0gBUB5oAdAGAQ"
python -m meshtastic --port COMx --set position.position_broadcast_secs 60
python -m meshtastic --port COMx --set bluetooth.mode NO_PIN   # only if a display pairs to it
```

(The URL embeds the channel key — fine in this team repo, don't post publicly.)
Radio #1 config summary: region US · channel Group9 (private PSK) ·
position_broadcast_secs 60 · bluetooth NO_PIN.

Heltec WiFi LoRa 32 V4 setup, radio configuration, antennas, and range testing.

Put here:
- Meshtastic config exports (channel/preset/interval settings used on both nodes)
- GNSS module notes (which module, wiring, fix quality)
- Antenna selection notes + mount photos
- `range-tests/` — one dated log per test: locations, terrain, preset, antenna, result

First tasks (W2–W3): flash stock Meshtastic via https://flasher.meshtastic.org, attach the
GNSS modules, confirm both nodes see each other's position in the Meshtastic phone app.
**Week 1 blocker check: do the kits include the GNSS modules?** (V4 has a connector, not onboard GPS.)
