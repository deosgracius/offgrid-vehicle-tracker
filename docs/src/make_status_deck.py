# Short status deck for 28 October 2026: New Mexico rained out; what the weekend went into instead.
# Reuses the drawing helpers of make_combined_deck.py. Run from docs/src.
src = open("make_combined_deck.py", encoding="utf-8").read()
exec(src[:src.index("# ============ 1 TITLE")])
DATE = "2026-10-28"; REV = "STATUS"; TOTAL = 6

# 1 title
s = slide(); gridpaper(s); frame(s, "status update")
txt(s, 0.7, 1.0, 11.9, 0.9, "STATUS, 28 OCTOBER", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "NEW MEXICO RAINED OUT; THE WEEKEND WENT INTO THE RADIOS INSTEAD", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.3, "The maximum-range drive was cancelled by weather. In its place: the battery-death configuration loss was traced to the flash cells and measured on both radios, SF was repaired, and a firmware build that makes the failure harmless is now on both radios. Full root-cause presentation on 4 November.", 13, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\n28 October 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Five minutes. One cancelled test, one investigation, one fix, one plan.")

# 2 NM cancelled
s = slide(); frame(s, "status update", "CANNON")
head(s, "The New Mexico test: cancelled by weather", "Planned for 25 October: maximum range on open highway, the one geometry we have not measured")
pic(s, "g_onset4.png", 0.55, 1.4, 6.6)
card(s, 7.4, 1.4, 5.4, 2.1, "What it would have measured", ["Flat open road with no terrain: the true maximum of the radios", "Range so far: 0.5 mi in town, 3.26 to 3.75 mi on a farm road, 1.29 to 4.7 mi at the canyon", "Expectation from the two-ray model: beyond 4.7 mi with both antennas on the roof"], INK, 13, 11.5)
card(s, 7.4, 3.7, 5.4, 1.6, "Why it did not happen", "Rain and low visibility on the 25th; a range drive needs a clear day and two cars for about two hours. Pre-flight was done (both OLEDs 912.875) before the call to cancel.", RED, 13, 11.5)
card(s, 0.55, 5.0, 12.25, 1.5, "Reschedule", "Next clear weekend, same plan: two cars, one radio each on the roof, drive apart on US-84 or US-62 until the display shows LINK LOST, log the last packet distance, drive back. Both radios now carry the fix described on sheet 4, so a flat battery on the way cannot cost the test.", GREEN, 13, 11.5)
notes(s, "Say plainly that the test is rescheduled, not dropped, and that the radios are in better shape for it than they were on the 25th.")

# 3 what the weekend went into
s = slide(); frame(s, "status update", "DEO")
head(s, "The weekend instead: why the radios forget", "A Qualcomm engineer asked whether the memory itself was at fault. We measured it.")
pic(s, "g_maps_compare.png", 0.55, 1.4, 8.6)
card(s, 9.35, 1.4, 3.45, 2.5, "The measurement", ["Settings area of the flash read three times with the firmware stopped, on both radios", "SF: 21 sectors gave different bytes on every pass", "RG: zero", "Program code, read the same way: zero differences"], ACC, 12.5, 10.5)
card(s, 9.35, 4.05, 3.45, 2.45, "The answer", ["The cells are healthy: erased and rewritten on a good supply they held every pattern", "They were left half-written when the firmware wrote to flash while the battery sagged below the chip's 2.7 V minimum", "The firmware then overwrites any unreadable file with factory settings"], GREEN, 12.5, 10.5)
txt(s, 0.55, 4.05, 8.6, 0.9, "Each square is one 4 KB sector. Red: read differently every time with nothing running. Green: the live settings files. SF was repaired the same day (21 to 0 unstable sectors). The full chain of evidence, the firmware source, the datasheets and the upstream reports are the 4 November presentation.", 11.5, False, BODY)
stat(s, 0.55, 5.1, 2.7, 1.35, "21 -> 0", "unstable sectors on SF, before and after repair", RED, 22)
stat(s, 3.5, 5.1, 2.7, 1.35, "0", "unstable sectors on RG", GREEN, 22)
stat(s, 6.45, 5.1, 2.7, 1.35, "260 mV", "gap between CPU reset (2.44 V) and flash minimum (2.70 V)", ACC, 22)
notes(s, "Keep this to the headline. The hypothesis came from a Qualcomm engineer; the experiment design and scripts were drafted with an AI assistant; every measurement was run by us on our radios, with the records in the repository. Details next week.")

# 4 fix 1 deployed
s = slide(); frame(s, "status update", "DEO")
head(s, "Fix 1 is on both radios", "Built 27 October, flashed and accepted 28 October")
card(s, 0.55, 1.4, 6.0, 2.6, "What it is", "Meshtastic rebuilt from source so that its factory settings are our settings: Group9 at 912.875 MHz, No PIN, CLIENT_MUTE, named SF or RG, our GPS cadence. When the firmware falls back to defaults after a bad write, the defaults are now right. The key is compiled into a binary that never leaves the private repository.", GREEN, 13.5, 12)
card(s, 6.75, 1.4, 6.05, 2.6, "Acceptance test, both radios", ["Flash, then send a factory reset, then read back with zero provisioning", "SF came back as SF and RG as RG: Group9 with the 32-byte key, precision 32, No PIN, CLIENT_MUTE, US LONG_FAST", "The snapshot then restored the 21 presets, the smart-broadcast minimums and the original key pair", "Both OLEDs read 912.875 before they were unplugged"], INK, 13.5, 11.5)
stat(s, 0.55, 4.25, 3.95, 1.3, "2 / 2", "radios flashed and accepted", GREEN, 26)
stat(s, 4.675, 4.25, 3.95, 1.3, "0", "commands needed after a future revert", GREEN, 26)
stat(s, 8.8, 4.25, 3.95, 1.3, "90 s", "to restore presets and minimums from the snapshot", ACC, 26)
card(s, 0.55, 5.75, 12.25, 0.8, "Also in force", "Pre-flight: both OLEDs read 912.875. Config snapshot per radio. Phone-app QR recovery when no laptop is at hand (User Guide 12). Never store a radio flat.", MUT, 12.5, 11.5)
notes(s, "This is the deliverable of the week: a configuration loss is now invisible to the driver.")

# 5 other deliverables
s = slide(); frame(s, "status update", "JOSIAH")
head(s, "Since the canyon: display and documents")
cards = [("Display firmware", ["Headings as clock positions (12, 3, 6, 9), partner arrow kept", "Heading held while stopped; 'holding' when both cars are parked", "LINK LOST alarm when the radio drops", "Flashed to both displays; 13 of 13 native tests pass"], M["JOSIAH"]),
         ("Bench observations", ["Two radios on one desk showed 0.21 mi apart: indoor GPS scatter of 100 to 400 m, not a link fault", "Both displays paired in under 8 s with every config write accepted", "Rule: judge a bench distance only with sky view"], ACC),
         ("Documents", ["User Guide 12: restoring a radio that forgot its settings, phone and laptop paths", "Technical Manual 15 and 16: verification record and failure catalog updated through 28 October", "Presentation for 4 November: 20 sheets, built and in the repository"], INK)]
x = 0.55
for t, items, c in cards:
    card(s, x, 1.4, 4.0, 3.0, t, items, c, 13.5, 11.5); x += 4.1
txt(s, 0.55, 4.65, 12.2, 0.9, "Everything above is committed and pushed. The private repository holds the channel key, the config snapshots and the fix-1 firmware images; nothing with the key is public.", 12, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
notes(s, "One sheet for the rest of the team's output. The display changes were validated on the bench; the next drive validates them on the road.")

# 6 next
s = slide(); frame(s, "status update")
head(s, "Next")
rows = [["When", "What", "Pass criterion", "Owner"],
        ["Next clear weekend", "New Mexico maximum-range drive, rescheduled", "Last packet distance logged; LINK LOST behaviour on the road", "Cannon, Victor"],
        ["This week", "Flat-battery campaign: five full discharges per radio, config and flash map read after each", "0 of 10 cycles lose configuration; no new unstable sectors", "Deo"],
        ["This week", "Oscilloscope on the 3V3 pin during a transmit burst at a 3.4 V cell", "Minimum rail voltage recorded", "Victor"],
        ["4 November", "Full presentation: tests, failures, root cause", "20 sheets, 25 minutes", "All"]]
table(s, 0.55, 1.4, 12.2, rows, [1.8, 5.0, 3.6, 1.8], fs=11.5, rh=0.7)
card(s, 0.55, 5.1, 12.2, 1.4, "The ask", "Approve the flat-battery campaign before the next field test. It reproduces the exact conditions of all three battery incidents, with the flash read after every cycle, and it is the test that proves the fix rather than hoping for it.", GREEN, 13.5, 12.5)
notes(s, "End on the ask.")

assert sheet_no[0] == TOTAL
prs.save("../presentations/Group9_Status_2026-10-28.pptx")
print("status deck saved")
