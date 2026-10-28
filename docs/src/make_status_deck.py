# Status deck for 28 October 2026, nine sheets, written to be presented by a teammate without the author.
# One idea per sheet, short text, and a spoken script in every sheet's notes. Run from docs/src.
src = open("make_combined_deck.py", encoding="utf-8").read()
exec(src[:src.index("# ============ 1 TITLE")])
DATE = "2026-10-28"; REV = "STATUS"; TOTAL = 9

# 1 title
s = slide(); gridpaper(s); frame(s, "status update")
txt(s, 0.7, 1.0, 11.9, 0.9, "STATUS, 28 OCTOBER", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "THE ROOF-TOP ANTENNA DRIVE, THE WEATHER, AND WHAT WE DID INSTEAD", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.5, "We went to New Mexico to measure the radios' maximum range with the antenna on the roof of the car. A flash flood warning stopped the drive. The weekend went into the radios instead: the settings-loss problem was traced to its cause, and a fix is now on both radios.", 14, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\n28 October 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "SAY: This is a short status update. Three things: the range test we planned in New Mexico, why it did not run, and what the team did with the weekend instead. About five minutes.")

# 2 the plan
s = slide(); frame(s, "status update")
head(s, "The plan: a roof-top antenna range drive", "The one range number we still do not have")
pic(s, "g_onset4.png", 0.55, 1.4, 6.6)
card(s, 7.4, 1.4, 5.4, 2.45, "The idea", ["Put the radio's antenna on the roof of the car instead of inside it", "Drive two cars apart on open road with no hills in between", "Record the distance where the display says LINK LOST"], INK, 14, 13)
card(s, 7.4, 4.05, 5.4, 2.45, "Why it matters", ["Every range we have so far was limited by terrain or buildings: 0.5 mi in town, 3.75 mi on a farm road, 4.7 mi from a canyon rim", "Open country with a roof antenna gives the true maximum of the hardware"], ACC, 14, 13)
notes(s, "SAY: The chart shows the range we have measured so far, in four kinds of terrain. All of them were limited by what was in the way: buildings, hills, canyon walls. The plan for New Mexico was to remove those limits: antenna on the roof, open flat country, drive apart until the link drops. That gives the true maximum of the radios, which we still do not have.")

# 3 on site
s = slide(); frame(s, "status update")
head(s, "On site, 25 October: cancelled by weather", "Below the Capitan Mountains, north of Capitan, New Mexico")
pic(s, "g_nm_cancel.png", 0.55, 1.35, 8.4)
pic(s, "g_nm_alert.jpg", 9.15, 1.55, 3.65)
txt(s, 9.15, 2.95, 3.65, 1.4, "NATIONAL WEATHER SERVICE: FLASH FLOOD WARNING FOR THE AREA UNTIL 9:15 PM MDT. \"DO NOT ATTEMPT TO TRAVEL.\"", 10, True, RED, PP_ALIGN.LEFT, MONO)
card(s, 0.55, 4.65, 12.25, 1.95, "What happened", ["The team was on site with both radios checked and ready (both screens read 912.875 MHz)", "Low cloud sat on the peaks and rain was moving in", "A National Weather Service flash flood warning covered the area: a travel ban, not a judgment call. The drive was not started"], RED, 14, 13)
notes(s, "SAY: We were there. The map shows where, just below the Capitan Mountains. The photos show the cloud on the peaks and the road we were on. Then the phone alert on the right: a flash flood warning, do not attempt to travel. That is a travel ban, so the drive was not started. The test is rescheduled, not dropped. Next sheet.")

# 4 reschedule
s = slide(); frame(s, "status update")
head(s, "Rescheduled: same test, next clear weekend")
steps = [("1", "Pick a clear day", "Check the forecast the day before; no warnings, no rain"),
         ("2", "Pre-flight", "Both radio screens must read 912.875 MHz; both displays show the link"),
         ("3", "Antennas on the roofs", "One radio per car, antenna mounted on the roof, display on the dash"),
         ("4", "Drive apart", "Open road, no hills between the cars, until the display says LINK LOST"),
         ("5", "Record", "Note the distance of the last packet and the distance where the link came back")]
y = 1.4
for n, t, d in steps:
    rect(s, 0.55, y, 0.7, 0.85, INK); txt(s, 0.55, y+0.18, 0.7, 0.5, n, 22, True, PAPER, PP_ALIGN.CENTER, HF)
    rect(s, 1.25, y, 11.5, 0.85, CARD, RULE, 1.0)
    txt(s, 1.45, y+0.1, 3.2, 0.4, t.upper(), 13, True, INK, PP_ALIGN.LEFT, HF, spc=100)
    txt(s, 4.7, y+0.22, 7.9, 0.5, d, 13, False, BODY)
    y += 1.0
txt(s, 0.55, 6.45, 12.2, 0.4, "Both radios now carry the fix on sheet 6, so a flat battery on the drive out cannot cost the test.", 12, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
notes(s, "SAY: Same site, same plan, five steps. Nothing new has to be built for it. The one change since the 25th is that both radios now have a firmware fix, which I will get to, so even a dead battery on the way cannot lose the radio settings and cost us the day.")

# 5 the problem
s = slide(); frame(s, "status update")
head(s, "Meanwhile: why the radios forget", "A Qualcomm engineer asked whether the memory itself was at fault. We measured it.")
pic(s, "g_maps_compare.png", 0.55, 1.4, 8.6)
card(s, 9.35, 1.4, 3.45, 4.95, "In plain words", ["Three times this semester a radio came back from a flat battery with its settings gone", "We read the settings area of the memory chip three times in a row, with nothing running", "SF: 21 spots gave different answers each time (red). RG: none", "Rewriting those spots on a good power supply made them perfect. The chip is healthy", "The cause: the radio writes to memory while the battery is sagging below what the chip needs"], ACC, 14, 12.5)
txt(s, 0.55, 4.15, 8.6, 1.1, "Each square is a 4 KB block of the settings area. Red blocks read differently on every pass. Green blocks held the live settings that day. SF was repaired the same day: 21 red blocks to 0. The full evidence is a separate 20-sheet presentation, ready in the repository.", 12.5, False, BODY)
stat(s, 0.55, 5.55, 4.15, 1.05, "21 -> 0", "bad blocks on SF, before and after the repair", RED, 20)
stat(s, 5.0, 5.55, 4.15, 1.05, "0", "bad blocks on RG", GREEN, 20)
notes(s, "SAY: While the weather stopped the drive, the weekend went into a problem that has hit us three times: a radio runs its battery flat and comes back with its settings gone. An engineer at Qualcomm suggested the memory chip itself might be bad, so we measured it. Left picture is radio SF: the red blocks gave a different answer every time we read them. Right is radio RG: clean. Rewriting the red blocks fixed them, so the chip is fine; it was written while the battery was too low. That is the cause. The full evidence is a separate presentation.")

# 6 the fix
s = slide(); frame(s, "status update")
head(s, "The fix is on both radios", "Built 27 October, flashed and tested 28 October")
card(s, 0.55, 1.4, 6.0, 2.7, "What it is", "The radio firmware was rebuilt so that its factory settings ARE our settings: our channel, our frequency, no PIN, our names. If the radio ever loses its settings again, it falls back to the right ones by itself.", GREEN, 14, 13.5)
card(s, 6.75, 1.4, 6.05, 2.7, "How it was tested", ["Flash the radio, then order a factory reset", "The radio came back on Group9 at 912.875 MHz with the right name and no PIN, with nobody touching it", "Done on both SF and RG; both screens read 912.875 before they were unplugged"], INK, 14, 13)
stat(s, 0.55, 4.35, 3.95, 1.35, "2 / 2", "radios flashed and tested", GREEN, 28)
stat(s, 4.675, 4.35, 3.95, 1.35, "0", "commands needed if a radio forgets again", GREEN, 28)
stat(s, 8.8, 4.35, 3.95, 1.35, "912.875", "MHz on both screens, the pre-flight check", ACC, 28)
txt(s, 0.55, 5.95, 12.2, 0.6, "Still in force: check both screens read 912.875 before any drive; never store a radio with a flat battery.", 12, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
notes(s, "SAY: The fix is simple to explain. The radio software was rebuilt so that its factory settings are our settings. If it ever forgets again, it forgets back to the right values. We tested it by forcing a factory reset on both radios: each came back on our channel with the right name, with nobody touching it.")

# 7 display
s = slide(); frame(s, "status update")
head(s, "The display: what changed since the canyon")
cards = [("Clock-face headings", "Directions are given as clock positions: 12 is straight ahead, 3 is to the right, 6 behind, 9 to the left. The partner arrow stays.", M["JOSIAH"]),
         ("Holding", "When the car stops, the heading is held instead of spinning. When both cars are parked the screen says 'holding' instead of inventing a distance.", ACC),
         ("LINK LOST", "If the display loses the radio, it says so in large letters. No silent failure.", RED)]
x = 0.55
for t, d, c in cards:
    card(s, x, 1.4, 4.0, 2.2, t, d, c, 14, 13); x += 4.1
card(s, 0.55, 3.85, 12.25, 1.5, "Bench finding", "Two radios on one desk once showed 0.21 miles apart. The displays were right; the GPS fixes were wrong, because indoors the receivers scatter by 100 to 400 m. Rule for anyone testing: judge a distance only with a clear view of the sky.", INK, 14, 13)
txt(s, 0.55, 5.6, 12.2, 0.6, "Both displays were flashed on 24 October; 13 of 13 firmware tests pass. The bench record behind the 0.21 mi observation is in the Technical Manual, Section 15.", 12, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
notes(s, "SAY: Three changes on the display, all from the night drive and the canyon. Directions are clock positions, the screen says holding when both cars are parked, and it says LINK LOST if the radio drops. One bench lesson: indoors the GPS can be hundreds of metres off, so only trust distances outside.")

# 8 documents
s = slide(); frame(s, "status update")
head(s, "Documents and repository")
rows = [["Document", "What is new", "Where"],
        ["Device User Guide", "Section 12: restoring a radio that forgot its settings, with a phone and with a laptop", "docs/manuals/DEVICE_USER_GUIDE.pdf, 16 pages"],
        ["Technical Manual", "Sections 15 and 16: the verification record and the failure catalog, updated through 28 October", "docs/manuals/TECHNICAL_MANUAL.pdf, 62 pages"],
        ["Root-cause presentation", "Tests, failures and the memory investigation, 20 sheets", "docs/presentations/Group9_Presentation.pptx"],
        ["Measurement records", "Every flash read and test from 27 October, reproducible", "docs/src/flash_forensics"]]
table(s, 0.55, 1.4, 12.2, rows, [2.3, 5.5, 4.4], fs=12.5, rh=0.8)
card(s, 0.55, 5.6, 12.2, 0.95, "Private", "The channel key, the radio configuration snapshots and the fixed firmware images stay in the private repository only.", MUT, 13, 12.5)
notes(s, "SAY: Everything is written down and in the repository: how to recover a radio with a phone or a laptop, the full failure catalog, the measurement records, and the long presentation. The channel key never leaves the private repo.")

# 9 next
s = slide(); frame(s, "status update")
head(s, "Next")
rows = [["When", "What", "Done when", "Owner"],
        ["Next clear weekend", "Roof-top antenna range drive, rescheduled (sheet 4)", "Last-packet distance recorded", "Cannon, Victor"],
        ["This week", "Flat-battery test: run each radio flat five times, check settings and memory after each", "0 of 10 runs lose settings", "Deo"],
        ["Next week", "Enclosure for the Waveshare LCD display", "Waterproof", "Josiah"],
        ["This week", "Oscilloscope on the radio's 3.3 V supply during a transmit burst on a low battery", "Lowest voltage recorded", "Victor"]]
table(s, 0.55, 1.4, 12.2, rows, [1.9, 5.5, 2.8, 2.0], fs=12.5, rh=0.8)
card(s, 0.55, 5.6, 12.2, 1.0, "The ask", "Approve the flat-battery test before the next field drive. It repeats the exact conditions of all three failures and proves the fix instead of hoping for it.", GREEN, 13.5, 12.5)
notes(s, "SAY: Four items. The range drive, rescheduled for the next clear weekend. The flat-battery test that proves the fix. Josiah's waterproof enclosure for the display, due next week. And a scope measurement on the radio's supply. The ask is to approve the flat-battery test before the next drive.")

assert sheet_no[0] == TOTAL
prs.save("../presentations/Group9_Status_2026-10-28.pptx")
print("status deck saved")
