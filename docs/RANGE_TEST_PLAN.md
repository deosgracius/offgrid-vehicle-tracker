# Range Test Plan

Goal: turn the link-budget prediction (technical report, Section 5) into a measured
curve, and find the real distance where DATA STALE begins on open road versus in town.
The 2026-10-04 night drive showed stale onset near 0.5 mi **in a built-up area with
in-cabin antennas** — that is an environment number, not a range number. This test
produces the range number.

## Prediction being tested

- Budget: +30 dBm TX, -131 dBm sensitivity at SF11/250 kHz → 161 dB absorbable loss.
- Free space at 913 MHz: 91.7 dB at 1 km, 105.7 dB at 5 km → huge margin in open air.
- Design claim: 3–5 km with 20 dB reserved for terrain/clutter/fading.
- Measured baseline: ~6 dB SNR at desk range; decode floor is -17.5 dB SNR, so the
  link holds until SNR drops ~23.5 dB → every 6 dB drop ≈ double distance.

## Setup (both vehicles)

1. Pre-flight: both OLED LoRa screens read **912.875** (two seconds, catches everything).
2. Batteries charged or on USB power; displays paired ("link OK").
3. Antennas **vertical and near glass** (dashboard against windshield). Note placement
   on the log sheet — it is part of the result.
4. One driver + one operator per vehicle, or park the far vehicle and drive the other.

## Procedure (open road, e.g. a straight farm road out of town)

Vehicle A parks at the start point. Vehicle B drives away along the route, stopping at
each distance step. At **each stop**:

1. Record straight-line distance (the display's own distance number is fine — it is
   GPS-to-GPS).
2. On each radio's OLED, open the node list and record the **SNR and RSSI** of the
   last packet from the partner (gives both directions).
3. Send one canned message each way; record delivered / not delivered.
4. Note the display state: age behavior, hollow dart, STALE banner yes/no.
5. Note terrain between vehicles (open / trees / buildings / crest).

Distance steps: 0.25, 0.5, 1, 2, 3, 4, 5 km — continue past 5 km until two consecutive
steps show no delivery in either direction. The last two-way step is the measured range.

Then repeat the **town route** from the drive test once, same log sheet, so the report
can show open-road vs in-town side by side.

## Log sheet columns

| time | dist | SNR A→B | RSSI A→B | SNR B→A | RSSI B→A | msg OK? | display state | terrain |

## Acceptance metrics (report, Table 3)

- 95th-percentile displayed age ≤ 15 s while both vehicles move (convoy leg).
- Reacquisition ≤ 60 s after returning to range.
- No silent gap > 120 s while within the measured range.
- SNR-vs-distance points fall within the 20 dB environmental reserve of the
  free-space model (plot both on one chart for the report).

## What the numbers mean afterward

- SNR falls ~6 dB per doubling of distance in open air. Plotting measured SNR against
  log(distance) should give a line; where it crosses -17.5 dB is the physics limit.
- If stale onset comes far earlier than that line predicts, the loss is environmental
  (antenna placement, car body, terrain) — the first fix is roof/glass antenna
  placement, not more transmit power (already at the legal ceiling).
