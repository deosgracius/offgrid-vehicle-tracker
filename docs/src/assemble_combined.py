# Assemble one coherent deck from the two generators: Part I (tests and failures,
# with the battery-death sheet rewritten as a bridge) + Part II (root cause) + one close.
d2 = open("make_nvs_deck2.py", encoding="utf-8").read()
tf = open("make_failures_deck.py", encoding="utf-8").read()

helpers = d2[: d2.index("# ============ 1 TITLE ============")]
helpers = helpers.replace("TOTAL = 18; sheet_no = [0]", "TOTAL = 29; sheet_no = [0]").replace("REV B", "REV C")

def block(src, start, end):
    a = src.index(start); b = src.index(end)
    return src[a:b]

TITLE = '''# ============ 1 TITLE ============
s = slide(); gridpaper(s); frame(s, "tests, failures, root cause")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHAT BROKE, AND WHAT IT TAUGHT US", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "THE TEST AND FAILURE RECORD, AND THE ONE FAILURE WE CHASED TO THE SILICON", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.3, "Part I: eleven root-caused failures and seven test campaigns, each with the rule it left behind. Part II: the battery-death configuration loss, investigated to the flash cells with measurements on both radios, repaired, and fixed at the root.", 13, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\\nJosiah Horn\\nVictor Okwonna\\nCannon Thomas\\n\\nSponsor: Dr. Richard Gale\\nOctober 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Two parts, one arc: the record of what broke, then the deepest dive we made into the failure that kept returning.")

'''

BRIDGE = '''# ============ BRIDGE: BATTERY DEATH ============
s = slide(); frame(s, "part i - the failures", "DEO")
head(s, "Failures 8-10: battery death reverts config", "The failure that kept coming back, and the one chased to the silicon in Part II.")
rows = [["Date", "Radio", "What reverted", "How it was found"],
        ["Sep 30", "Both", "RG: channels. SF: everything (channel, role, Bluetooth, telemetry, owner)", "Healthy screens, total silence"],
        ["Oct 17", "SF", "Bluetooth mode, channel (906.875), owner name", "Display looping: write rc=261, disconnect 534"],
        ["Oct 24", "SF", "Channel + key, precision, Bluetooth, cadence, owner, presets, node DB", "Routine diagnostic before a drive"]]
table(s, 0.55, 1.5, 12.2, rows, [1.1, 1.0, 5.9, 4.2], fs=11, rh=0.6)
card(s, 0.55, 4.1, 6.0, 2.4, "Mitigated in October", ["Pre-flight: both OLEDs read 912.875 (2 s)", "Config snapshot per radio, restored with --configure (90 s)", "Phone-app QR path when no laptop is at hand", "Never store a radio flat"], GREEN, 13.5, 12.5)
card(s, 6.75, 4.1, 6.0, 2.4, "Then the question that opened Part II", ["A reviewer asked: is it the memory itself?", "Three of four losses follow a flat battery; SF three times, RG once; losses partial and different each time", "Answered on 27 October with measurements on both radios"], ACC, 13.5, 12.5)
notes(s, "This sheet is the hinge of the deck. Part I shows the pattern; Part II takes it apart. Do not pre-empt the answer here.")

'''

TESTS = '''# ============ TESTS SO FAR ============
s = slide(); frame(s, "part i - the tests", "CANNON")
head(s, "The test campaigns")
rows = [["Date", "Campaign", "Environment", "Key result"],
        ["Aug 31", "Bench, end-to-end", "Desk", "Live GPS decoded radio-to-display"],
        ["Sep 1", "First drive", "Town", "Pipeline works at speed; five faults found"],
        ["Sep 25", "Two-radio link", "Desk", "Round-trip traceroute 6.75 / 5.75 dB"],
        ["Oct 4", "Night convoy drive", "Town", "Stale onset ~0.5 mi; course-up and cadence-aware cue born"],
        ["Oct 5", "Open-road range", "Flat farm road", "Full tracking to 3.26 mi; stale edge 3.75 mi"],
        ["Oct 18", "Canyon range", "Ceta Canyon", "Stale from 1.29 mi; packet at 4.28; 7-min outage healed; rim antenna 4.7 mi"],
        ["Oct 25", "New Mexico maximum range", "Open highway", "Cancelled by weather; the radios were diagnosed instead (Part II)"]]
table(s, 0.55, 1.3, 5.9, rows, [0.75, 1.55, 1.2, 2.4], fs=9.5, rh=0.52)
s.shapes.add_picture("deck/g_onset4.png", Inches(6.6), Inches(1.3), width=Inches(6.2))
txt(s, 6.6, 5.0, 6.2, 0.8, "Same radios, four geometries: 0.5 to 4.7 mi. Terrain and antenna height set the range, not the hardware.", 12, False, BODY)
notes(s, "Seven campaigns; each found what the previous one could not. The New Mexico drive was rained out, which is why the last weekend went into the radios instead.")

'''

DIVIDER = '''# ============ PART II DIVIDER ============
s = slide(); gridpaper(s); frame(s, "part ii - root cause")
txt(s, 0.7, 1.6, 11.9, 0.9, "PART II", 20, True, ACC, PP_ALIGN.LEFT, HF, spc=400)
txt(s, 0.7, 2.2, 11.9, 1.2, "WHY THE RADIOS FORGET", 40, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 3.2, 11.0, 0.9, "The battery-death failure, chased from the symptom to the flash cells and back to a fix. Measurements on both radios, 27 October 2026.", 14, False, BODY)
stat(s, 0.72, 4.4, 2.8, 1.5, "21 -> 0", "unstable flash sectors on SF, before and after repair")
stat(s, 3.72, 4.4, 2.8, 1.5, "260 mV", "window in which the CPU writes to an out-of-spec flash")
stat(s, 6.72, 4.4, 2.8, 1.5, "true", "what the firmware's power-safety check always returns")
notes(s, "Part II answers one question: is it the memory itself? It ends with the fix that makes the failure harmless.")

'''

CLOSE = '''# ============ CLOSE ============
s = slide(); frame(s, "close")
head(s, "The answer, and what the failures bought")
card(s, 0.55, 1.45, 12.2, 1.55, "Is it the memory itself?", "Partly, and measurably, but not as the question implies. SF's settings flash carried 21 sectors that would not hold a value; rewritten under a healthy supply they became perfect. The cells had been left half-written below the flash's 2.7 V minimum but above the 2.44 V reset point, a window the firmware never checks and then punishes with factory defaults.", INK, 15, 13)
stats = [("11", "root-caused failures, each with a written signature and recovery"), ("21 -> 0", "unstable flash sectors on SF; RG clean at 0"),
         ("0", "reflashes ever needed for a configuration failure"), ("90 s", "to recover a reverted radio; 2 s to detect one"),
         ("4.7 mi", "measured reach; honest envelope 0.5 to 4.7 mi by terrain"), ("1 build", "makes a future revert restore OUR configuration")]
pos = [(0.55, 3.25), (4.65, 3.25), (8.75, 3.25), (0.55, 4.75), (4.65, 4.75), (8.75, 4.75)]
for (big, small), (x, y) in zip(stats, pos):
    stat(s, x, y, 4.0, 1.35, big, small, ACC, 24)
rect(s, 0.55, 6.25, 12.2, 0.42, INK)
txt(s, 0.8, 6.31, 11.7, 0.3, "EVERY FAILURE BECAME A RULE; THE WORST ONE BECAME A MEASUREMENT, A REPAIR, AND A FIX.", 11.5, True, PAPER, PP_ALIGN.CENTER, HF)
notes(s, "Close on the bar. Then the ask: fix 1 is built; approve the flat-battery campaign that proves it before the next field test.")

'''

p1 = ""
p1 += block(tf, "# ============ 2 WHY FAILURES ============", "# ============ 3 TIMELINE ============")
p1 += block(tf, "# ============ 3 TIMELINE ============", "# ============ 4 BRING-UP ============")
p1 += block(tf, "# ============ 4 BRING-UP ============", "# ============ 5 FIRST DRIVE ============")
p1 += block(tf, "# ============ 5 FIRST DRIVE ============", "# ============ 6 WRONG FIRMWARE + CLI ============")
p1 += block(tf, "# ============ 6 WRONG FIRMWARE + CLI ============", "# ============ 7 SILENT FREQUENCY REVERT ============")
p1 += block(tf, "# ============ 7 SILENT FREQUENCY REVERT ============", "# ============ 8 BATTERY DEATH ============")
p1 += BRIDGE
p1 += block(tf, "# ============ 9 NIGHT DRIVE ============", "# ============ 10 NIGHT BEFORE CANYON ============")
p1 += block(tf, "# ============ 10 NIGHT BEFORE CANYON ============", "# ============ 11 FAILURE -> RULE MAP ============")
disp = block(tf, "# ============ 15 PRE-DRIVE DIAGNOSTIC: DISPLAYS ============", "# ============ 16 PRE-DRIVE DIAGNOSTIC: RADIOS ============")
disp = disp.replace('head(s, "Pre-drive diagnostic, Oct 24: the displays")', 'head(s, "Failure 11: the 0.21 mi that was not there")').replace('frame(s, "part ii - the tests", "DEO")', 'frame(s, "part i - the failures", "DEO")')
p1 += disp
p1 += TESTS
canyon = block(tf, "# ============ 14 CANYON ============", "# ============ 15 PRE-DRIVE DIAGNOSTIC: DISPLAYS ============").replace('frame(s, "part ii - the tests")', 'frame(s, "part i - the tests")')
p1 += canyon
rules = block(tf, "# ============ 11 FAILURE -> RULE MAP ============", "# ============ 12 TESTS SO FAR ============")
rules = rules.replace('head(s, "Every failure became a rule")', 'head(s, "Every failure became a rule", "The close of Part I; the battery-death row is where Part II begins.")')
rules = rules.replace('["Battery death reverts", "Config snapshots; re-run the whole block; never store flat", "hardware/*-config.yaml"]',
                      '["Battery death reverts", "Snapshots and pre-flight in October; root cause and repair on Oct 27: Part II", "Part II"]')
rules = rules.replace('["Night before the canyon", "Flashlight test, plug orientation, the 261 signature", "Manual 16, entries 9-10"]]',
                      '["Night before the canyon", "Flashlight test, plug orientation, the 261 signature", "Manual 16, entries 9-10"],\n        ["Phantom 0.21 mi", "Judge distances only with sky view; holding when both parked", "Manual 16, entry 11; Guide 11"]]')
rules = rules.replace("fs=11, rh=0.52)", "fs=10.5, rh=0.48)")
p1 += rules

p2 = DIVIDER
for start, end in [("# ============ 2 THE QUESTION ============", "# ============ 3 THE RECORD ============"),
                   ("# ============ 4 STORAGE ============", "# ============ 5 FIRMWARE FACTS ============"),
                   ("# ============ 5 FIRMWARE FACTS ============", "# ============ 6 PHYSICS ============"),
                   ("# ============ 6 PHYSICS ============", "# ============ 7 UPSTREAM ============"),
                   ("# ============ 7 UPSTREAM ============", "# ============ 8 HYPOTHESES ============"),
                   ("# ============ 8 HYPOTHESES ============", "# ============ 9 METHOD ============"),
                   ("# ============ 9 METHOD ============", "# ============ 10 RESULT MAPS ============"),
                   ("# ============ 10 RESULT MAPS ============", "# ============ 11 RESULT NUMBERS ============"),
                   ("# ============ 11 RESULT NUMBERS ============", "# ============ 12 DECISIVE TEST ============"),
                   ("# ============ 12 DECISIVE TEST ============", "# ============ 13 REPAIR ============"),
                   ("# ============ 13 REPAIR ============", "# ============ 14 CHAIN ============"),
                   ("# ============ 14 CHAIN ============", "# ============ 15 FIX PLAN ============"),
                   ("# ============ 15 FIX PLAN ============", "# ============ 16 FIX 1 ============"),
                   ("# ============ 16 FIX 1 ============", "# ============ 17 PROOF ============"),
                   ("# ============ 17 PROOF ============", "# ============ 18 ANSWER ============")]:
    p2 += block(d2, start, end)
for old in ['frame(s, "part i - the question")', 'frame(s, "part ii - how the radio remembers"', 'frame(s, "part iii - the measurement"', 'frame(s, "part iv - the fix"']:
    p2 = p2.replace(old, 'frame(s, "part ii - root cause"' + (")" if old.endswith(")") else ""))
# fix-plan status: fix 1 now built
p2 = p2.replace('"A revert restores the intended state; the failure becomes invisible", "1 day", "next"]', '"A revert restores the intended state; the failure becomes invisible", "1 day", "built Oct 27"]')

out = helpers + TITLE + p1 + p2 + CLOSE + 'prs.save("Group9_Presentation.pptx")\nimport os\nprint("saved", os.path.getsize("Group9_Presentation.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))\n'
n = out.count("s = slide()")
out = out.replace("TOTAL = 29; sheet_no = [0]", f"TOTAL = {n}; sheet_no = [0]")
open("make_combined_deck.py", "w", encoding="utf-8").write(out)
print("combined generator written; sheets:", n)
