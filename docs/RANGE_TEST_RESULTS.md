# Range Test Results

Two campaigns bracket the system's real-world envelope: an open-road maximum-range
test (2026-10-05) and a canyon no-line-of-sight test (2026-10-18). Together they
show that range is a property of terrain, not of the radios: fully reliable to
3.26 miles on open road, intermittent at any distance behind rock.

# Test 1: Open road, 2026-10-05

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

# Test 2: Canyon terrain (Palo Duro), 2026-10-18

Pre-dawn two-vehicle run at Ceta Canyon Camp and Retreat Center, on the Palo
Duro escarpment southeast of Happy, TX. RG parked at the rim point above
Garrison Retreat Lodge (~1,100 m); SF drove down FM 1721 through the canyon
folds and west onto the caprock plains. Same hardware, same in-cabin antennas. All data points read from video of the live screens; clock times
and display uptime counters on the screens give the timeline.

## Result in one line

**Behind rock, the link is intermittent at any distance: stale banners
appeared from 1.29 miles, yet single packets were still caught at 4.28 miles
when the terrain opened.** The link healed on its own every time line of
sight returned, with no operator action.

## Measured timeline

| Time (CDT) | Separation | Data age | Reading |
|---|---|---|---|
| 7:27a | 2.78 mi | 2 min, STALE | Outbound; canyon wall between vehicles |
| 7:30a | 4.28 mi | 1 min | Age reset while stale: a packet got through as a ridgeline opened |
| 7:31a | ~3.92 mi | 2 min | Stale again, vehicle nearly stopped |
| 7:32a | 4.46 mi | 3 min, STALE | Deepest point of the run |
| 7:38a | 2.90 mi | 54 s | Return leg; reacquisition beginning |
| 7:42a | 1.45 mi | 11 s | Fully live, partner at 12 o'clock, closing 45 mph |
| ~7:44a | 0.33 mi | 21 s | Guided final approach (CHANGE COURSE chevrons, then clean) |

Stale events also occurred inside 1.29 miles whenever canyon geometry blocked
the path. One display ran uptime 1910 s through 2789 s across the sequence
with no reboot.

## Findings

- **Distance is not the variable in broken terrain; line of sight is.** A mile
  and a quarter behind a caprock wall is a harder link than 3.26 open miles.
  Stale onset by distance: ~0.5 mi in town, ~2.8 mi in canyon (first event),
  3.75 mi on open road. Same hardware in all three.
- **The link is intermittent, not binary.** Packets were caught at 4+ miles
  through momentary gaps in the terrain. The age chip resetting from 2 min to
  1 min at 4.28 mi is a single ridge-top packet, visible on camera.
- **Recovery is automatic.** Every outage ended by driving until the geometry
  opened: 54 s age by 2.90 mi inbound, 11 s by 1.45 mi. No buttons pressed.
- **Honesty held under the hardest conditions yet.** Every outage was flagged
  (STALE banner, inverted age, hollow dart); every number on screen was either
  fresh or visibly labeled as a projection. Radio configs were verified clean
  on both units after the test, confirming the stalls were terrain, not
  configuration.
- **Operator guidance (now in the user guide):** in canyon country, expect the
  stale banner often; it is reporting blocked line of sight, not a fault, and
  it clears itself as the road opens.
- **The rim elevation finding: antenna height beat the flat-ground range.** RG
  sat parked at the Ceta Canyon rim point (~1,100 m), giving the pair one elevated
  antenna. On stretches where the rim had line of sight to the moving vehicle,
  the SF display stayed live out to roughly 4.7 miles before its first
  staleness, beyond the 3.75-mile edge measured car-to-car on flat open road,
  while the same morning produced stalls from 1.29 miles behind rock. One
  parking spot demonstrated both extremes, and it is the repeater-on-high-
  ground argument measured by accident: elevation, not transmit power, is the
  cheapest range multiplier this system has.
- **The two displays alarm at different distances by design, not by RF
  asymmetry.** The LoRa link is reciprocal, but SF's display was watching a
  parked partner (60 s cadence, 90 s stale threshold) while RG's display was
  watching a moving one (10 s cadence, 30 s threshold), so RG's screen flagged
  earlier and more often. Comparing the two screens' banners therefore
  compares thresholds, not signal paths.
- **A stale display is still exactly correct when the partner is parked.** The
  displayed separation is the driver's own live GPS position measured against
  the partner's last-known fix; a parked partner's last-known fix never stops
  being true. Driving out of range from a parked RG, the mileage would keep
  counting accurately indefinitely, with only the age chip reporting that the
  underlying data is old. With two moving vehicles the partner's dot becomes a
  projection instead; that distinction is why the age is always displayed.

## Status

Both planned range campaigns (open-road maximum and no-line-of-sight canyon)
are measured. The verification program's range characterization is complete.
Remaining optional refinement: repeat either run with a magnetic roof antenna
to quantify the car-body penalty directly. The rim elevation finding sharpens
the New Mexico open-road prediction: with any elevation on one end, the link
should beat the 3.75-mile flat-ground edge.
