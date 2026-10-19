# High-Ground Repeater Recipe

The canyon range test (2026-10-18, `RANGE_TEST_RESULTS.md`) measured the case
for this: one antenna with elevation out-ranged two car-height antennas, and
behind rock the car-to-car link is intermittent at any distance. A third
Meshtastic node parked on high ground sees down both arms of a canyon and
relays between vehicles that cannot see each other. Each hop gets the full
161 dB link budget of the technical manual's Section 4.

## What you need

Any Meshtastic-capable LoRa node (a third Heltec V4 is ideal; any SX126x
board on 915 MHz works), a battery, and a high parking spot: canyon rim,
ridge line, or simply a hill between the two arms of the route.

## Provisioning (one USB session, ~5 minutes)

Flash stock Meshtastic firmware if the node is new, then:

```
python -m meshtastic --port COMx --set lora.region US
python -m meshtastic --port COMx --seturl "<Group9 channel URL - hardware/README.md, line 11>"
python -m meshtastic --port COMx --set device.role ROUTER
python -m meshtastic --port COMx --set-owner "RPT" --set-owner-short "RPT"
python -m meshtastic --port COMx --set position.position_broadcast_secs 900
```

Then verify, in this order (the scar catalog's rules apply to repeaters too):

1. Read back every setting with `--get` (reboot-triggering writes can
   silently revert; see Technical Manual Section 12, entry 6).
2. **The OLED LoRa screen must read 912.875 MHz.** The screen is the ground
   truth, not the CLI.
3. Power-cycle the node and read back again (entry 2: NVS reverts).

## Why these settings

- **ROUTER role**: the node rebroadcasts every packet it hears, once. The
  vehicles' radios stay in CLIENT_MUTE exactly as provisioned today; nothing
  about the cars changes. Vehicle A's broadcast reaches the repeater, the
  repeater rebroadcasts, vehicle B hears it one hop later.
- **900 s position broadcast**: a parked repeater's position is not
  navigation data; this keeps its own airtime near zero.
- **Airtime cost**: every relayed packet is transmitted twice on the shared
  channel, so channel utilization roughly doubles. Measured idle utilization
  in CLIENT_MUTE is 5-6 percent (Appendix C of the report), so the relayed
  figure stays far below the 25 percent throttle. Two vehicles and one
  repeater is a comfortable fit; this is the arithmetic of the manual's
  Section 4.2 applied to three nodes.
- **Hop limit 3** (already the channel default) is plenty: vehicle, repeater,
  vehicle is one hop of relay.

## Deployment notes

- Height beats everything else. The 2026-10-18 measurement: ~1,100 m Ceta Canyon rim
  elevation held line-of-sight stretches to ~4.7 mi while flat car-to-car
  died by 3.75 mi. Park the repeater where it can see the road you will
  drive, not where it is convenient to park.
- The repeater is invisible to the displays by design: they track the
  partner vehicle's node only. Drivers simply see fewer DATA STALE banners.
- Battery: a Heltec V4 idles for days on its cell (manual Section 3.1 power
  notes), but do not run it to empty; a flat battery is the NVS-revert
  failure mode (scar catalog entries 2 and 10). Recover the node at the end
  of the day.
- Antenna height on the cars (recommendation 2 of the range analysis) stacks
  with this: a roof-mounted whip roughly doubles open-road range and shrinks
  every canyon shadow. No configuration changes needed; it is purely an
  antenna swap.
