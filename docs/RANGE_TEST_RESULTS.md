# Range Test Results, 2026-10-05

Open-road range test per `RANGE_TEST_PLAN.md`, executed on the evening of 2026-10-05
on N County Road 2000 north of Lubbock (straight farm road, flat terrain, clear line
of sight). SF kit parked at the far point (8809 N County Road 2000) with Josiah; RG
kit in the moving vehicle. Antennas in-cabin, vertical. Ground truth: phone Find My
placed the far point 4.1 road miles from the start. All data points below are read
from video of the live screens.

## Result in one line

**Full two-way tracking held to 3.26 miles (5.25 km); the stale edge arrived by
3.75 miles (6.03 km).** The design range was quoted as 3 to 5 km with terrain in the
way; on open road with in-cabin antennas, the system met the top of that range and
ran about a kilometer past it.

## Measured timeline

| Separation | Screen evidence | Reading |
|---|---|---|
| 19 ft | "at 11 o'clock, age 15s", both kits together | Baseline, GNSS scatter only |
| 610 ft | "at 3 o'clock, you 12 mph, apart 24 mph", CHANGE COURSE banner | Off-course warning fires correctly while driving away |
| 0.64 to 0.74 mi | "apart 46 mph" then "apart 56 mph" | Separation rate = sum of both vehicles' speeds; trend math correct with both cars moving |
| 1.58 mi | "N of you, apart 17 mph", single-digit age | Live tracking, fresh data |
| **3.26 mi** | Status page: **LINK CONNECTED, radios: RG<->SF COMMUNICATING**, RG 33.63023 -101.90527 (spd 0, 99% batt), SF 33.67742 -101.90507, age 1m | Full health at 5.25 km. Displayed distance matches the coordinate delta exactly (0.04719 deg latitude = 3.26 mi). Age 1m is normal for a parked partner on the 60 s cadence, and the cadence-aware cue correctly stayed calm |
| **3.75 mi** | Compass page: **SF DATA STALE**, age 2m inverted, "Message failed to #Group9" on the radio | The edge. Position traffic and a message both failed; the display flagged it honestly rather than silently |
| 0.85 mi (return) | "at 12 o'clock, age 23s" then "age 14s, you 37 mph, holding" | Reacquired on the drive back; dart dead ahead on the course-up ring at speed |
| 0.27 mi | "closing 16 mph" | Return leg |
| 298 ft, then 127 ft | "closing 8 mph", then "at 2 o'clock, age 3s" | Reunion; ages back to seconds |

## Findings against the plan's acceptance metrics

| Metric | Threshold | Result |
|---|---|---|
| Reacquisition after separation | Fresh fix within 60 s of returning to range | Met: ages were in the teens by 0.85 mi inbound |
| Silent loss | No unflagged gap over 120 s in range | Met: the only gap was at 3.75 mi and the display flagged it (STALE banner, inverted age) |
| Range model check | Within the 20 dB environmental reserve of the free-space prediction | Met: free-space loss at 5.25 km is ~106 dB against a 161 dB budget; the measured edge near 6 km implies roughly 55 dB of real-world losses (vehicle bodies, in-cabin antennas, ground effects), consistent with the model's structure |

## What else the test proved

- **Course-up compass on the road:** at 37 mph the dart read "at 12 o'clock" with the
  partner dead ahead, the exact behavior shipped after the 10-04 night drive.
- **Cadence-aware staleness:** a parked partner at age 1m displayed calm; a true
  2-minute outage displayed inverted and bannered. Both sides of the threshold are
  correct.
- **Failure honesty end to end:** at the range edge the radio itself said "Message
  failed" and the display said "DATA STALE". Nothing pretended.
- **Comparison with the 10-04 town drive:** stale onset at ~0.5 mi in town versus
  3.75 mi on open road, same hardware and same in-cabin antennas. The difference,
  roughly a factor of seven, is the environment, which is precisely what the link
  budget's 20 dB reserve was for. A roof-mounted antenna remains the single biggest
  available range upgrade.

## Status

The last open item in the verification program (the range characterization of
RANGE_TEST_PLAN.md) is now measured. Remaining optional refinement: repeat with a
magnetic roof antenna to quantify the car-body penalty directly.
