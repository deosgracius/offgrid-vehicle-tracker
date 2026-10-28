# Configuration-loss root-cause deck, edition B: figure-led, short text, detail in notes.
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

INK = RGBColor(0x16,0x21,0x3D); PAPER = RGBColor(0xFF,0xFF,0xFF)
ACC = RGBColor(0xE5,0x8E,0x1A); MUT = RGBColor(0x5E,0x6B,0x85)
RULE = RGBColor(0x9A,0xA7,0xBE); CARD = RGBColor(0xF2,0xF5,0xFA)
CODEBG = RGBColor(0x1B,0x24,0x40); ICE = RGBColor(0xC9,0xD8,0xF0)
GRID = RGBColor(0xE8,0xED,0xF5); GREEN = RGBColor(0x1F,0x9D,0x68)
RED = RGBColor(0xC4,0x3A,0x4B); BODY = RGBColor(0x22,0x2A,0x3F)
PINK = RGBColor(0xFF,0x9A,0xA8)
M = {"DEO": RGBColor(0x11,0x99,0xBD), "JOSIAH": RGBColor(0x6D,0x4B,0xDB),
     "VICTOR": RGBColor(0xE5,0x8E,0x1A), "CANNON": RGBColor(0xD9,0x48,0x8C)}
HF, BF, MONO = "Cambria", "Cambria", "Courier New"
DATE = "2026-10-27"

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
TOTAL = 18; sheet_no = [0]

def set_spc(r, v): r._r.get_or_add_rPr().set('spc', str(v))
def txt(s, x, y, w, h, text, size, bold=False, color=BODY, align=PP_ALIGN.LEFT, font=BF, spc=0, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    if spc: set_spc(r, spc)
    return tb
def rect(s, x, y, w, h, fill=None, line=None, lw=1.0):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: sh.fill.background()
    else: sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb = line; sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    return sh
def frame(s, part, owner=None):
    sheet_no[0] += 1
    rect(s, 0.18, 0.16, 12.97, 7.18, None, INK, 1.75)
    ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.18), Inches(6.86), Inches(12.97), Pt(1))
    ln.fill.solid(); ln.fill.fore_color.rgb = INK; ln.line.fill.background(); ln.shadow.inherit = False
    txt(s, 0.35, 6.94, 4.6, 0.32, "GROUP 9  |  OFF-GRID VEHICLE TRACKER", 9, False, MUT, PP_ALIGN.LEFT, MONO)
    txt(s, 5.0, 6.94, 4.6, 0.32, part.upper(), 9, False, MUT, PP_ALIGN.CENTER, MONO)
    txt(s, 9.7, 6.94, 3.3, 0.32, "SHEET %02d/%02d  REV B  %s" % (sheet_no[0], TOTAL, DATE), 9, False, MUT, PP_ALIGN.RIGHT, MONO)
    if owner:
        rect(s, 10.55, 0.38, 2.35, 0.46, PAPER, M[owner], 1.5)
        txt(s, 10.55, 0.44, 2.35, 0.34, "OWNER: " + owner, 11, True, M[owner], PP_ALIGN.CENTER, MONO)
def head(s, t, sub=None):
    txt(s, 0.5, 0.36, 9.9, 0.62, t.upper(), 23, True, INK, PP_ALIGN.LEFT, HF, spc=200)
    if sub: txt(s, 0.52, 0.95, 9.9, 0.35, sub, 12.5, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
def card(s, x, y, w, h, title, items, accent=INK, ts=13.5, bs=12.5):
    rect(s, x, y, w, h, CARD, accent, 1.25)
    tb = s.shapes.add_textbox(Inches(x+0.18), Inches(y+0.13), Inches(w-0.36), Inches(h-0.26))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; r = p.add_run(); r.text = title.upper()
    r.font.size = Pt(ts); r.font.bold = True; r.font.color.rgb = accent; r.font.name = HF; set_spc(r, 100)
    if isinstance(items, str): items = [items]
    for it in items:
        p2 = tf.add_paragraph(); p2.space_before = Pt(4)
        r2 = p2.add_run(); r2.text = ("•  " + it) if len(items) > 1 else it
        r2.font.size = Pt(bs); r2.font.color.rgb = BODY; r2.font.name = BF
def stat(s, x, y, w, h, big, small, col=ACC, bigsize=30):
    rect(s, x, y, w, h, CARD, RULE, 1.0)
    txt(s, x, y+0.12, w, bigsize/36, big, bigsize, True, col, PP_ALIGN.CENTER, HF)
    txt(s, x+0.15, y+0.22+bigsize/36, w-0.3, h-0.3-bigsize/36, small, 11, False, BODY, PP_ALIGN.CENTER)
def codebox(s, x, y, w, h, label, lines, fs=11):
    rect(s, x, y, w, h, CODEBG)
    txt(s, x+0.18, y+0.1, w-0.36, 0.3, label, 10, True, ACC, PP_ALIGN.LEFT, MONO)
    tb = s.shapes.add_textbox(Inches(x+0.18), Inches(y+0.42), Inches(w-0.36), Inches(h-0.5))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, (t, c) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = t; r.font.size = Pt(fs); r.font.name = MONO; r.font.color.rgb = c
def notes(s, t): s.notes_slide.notes_text_frame.text = t
def slide(): return prs.slides.add_slide(blank)
def gridpaper(s):
    x = 0.18
    while x < 13.15:
        ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(0.16), Pt(0.5), Inches(6.7))
        ln.fill.solid(); ln.fill.fore_color.rgb = GRID; ln.line.fill.background(); ln.shadow.inherit = False
        x += 0.72
    y = 0.16
    while y < 6.86:
        ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.18), Inches(y), Inches(12.97), Pt(0.5))
        ln.fill.solid(); ln.fill.fore_color.rgb = GRID; ln.line.fill.background(); ln.shadow.inherit = False
        y += 0.72
def table(s, x, y, w, rows, colw, hdr=True, fs=11, rh=0.42):
    tb = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(rh*len(rows))).table
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tb.cell(i, j); c.text = ""
            p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = val
            r.font.size = Pt(fs); r.font.name = BF
            r.font.bold = (hdr and i == 0); r.font.color.rgb = PAPER if (hdr and i == 0) else BODY
            c.fill.solid(); c.fill.fore_color.rgb = INK if (hdr and i == 0) else (CARD if i % 2 else PAPER)
            c.margin_left = c.margin_right = Inches(0.08); c.margin_top = c.margin_bottom = Inches(0.03)
    for j, cw in enumerate(colw): tb.columns[j].width = Inches(cw)
    return tb
def chip(s, x, y, text, col):
    rect(s, x, y, 1.15, 0.3, col)
    txt(s, x, y+0.04, 1.15, 0.25, text, 9.5, True, PAPER, PP_ALIGN.CENTER, MONO)

# ============ 1 TITLE ============
s = slide(); gridpaper(s); frame(s, "root cause investigation")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHY THE RADIOS FORGET", 40, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "CONFIGURATION LOSS AFTER BATTERY DEATH: EVIDENCE, MECHANISM, REPAIR", 17, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.6, 8.0, 1.2, "Four losses in one semester. One question from a reviewer: is it the memory itself? One answer, measured on the hardware and traced through the firmware and the datasheets.", 13.5, False, BODY)
stat(s, 0.72, 4.0, 2.6, 1.5, "4", "configuration losses, Sep 3 to Oct 24")
stat(s, 3.52, 4.0, 2.6, 1.5, "21 -> 0", "unstable flash sectors on SF, before and after repair")
stat(s, 6.32, 4.0, 2.6, 1.5, "260 mV", "window in which the CPU writes to a flash that is out of spec")
txt(s, 9.4, 4.0, 3.4, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\nOctober 2026", 12.5, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Open with the three numbers. Everything on these sheets was measured on SF or RG on 27 October, read from the Meshtastic v2.7.26 source at the exact tag we run, or taken from the Heltec, Boya and Espressif documents named on the sheets. The one-line answer: the memory bore the scar, the power rail made it, the firmware made it permanent, and all three are fixable.")

# ============ 2 THE QUESTION ============
s = slide(); frame(s, "part i - the question")
head(s, "One question, three possible meanings", "\"It might be the memory itself.\" Each meaning leaves a different fingerprint and needs a different fix.")
cards = [("Worn out", ["Endurance exhausted by write volume", "Fingerprint: diffuse failures, many sectors", "Fix: replace the part"], RED),
         ("Defective or marginal cells", ["Specific cells that will not hold a value", "Fingerprint: the same sectors misread, every pass", "Fix: avoid or re-form those sectors"], ACC),
         ("Corrupted by the conditions of a write", ["Healthy cells written while the supply was out of spec", "Fingerprint: follows power events; heals when rewritten", "Fix: never write under low voltage"], GREEN)]
x = 0.55
for t, items, c in cards:
    card(s, x, 1.55, 4.0, 2.6, t, items, c, 13.5, 12); x += 4.1
card(s, 0.55, 4.45, 12.2, 2.1, "How we told them apart", ["Read the settings partition straight off the chip, firmware halted, three times in one session", "Read the firmware's save and load code at tag v2.7.26", "Read the flash and board datasheets and the brownout level the firmware is built with", "Line the four incidents up against all of it"], INK, 13.5, 12.5)
notes(s, "The recruiter's suggestion is a testable hypothesis, not an opinion to argue with. State the three readings of 'the memory itself', what each would look like in data, and what each would require as a fix. The rest of the deck collects exactly that data.")

# ============ 3 THE RECORD ============
s = slide(); frame(s, "part i - the question", "DEO")
head(s, "The record")
s.shapes.add_picture("deck/g_events.png", Inches(0.55), Inches(1.25), width=Inches(12.2))
stat(s, 0.55, 4.35, 3.95, 2.15, "3 of 4", "losses followed a battery run flat; the fourth is a reset-during-write race")
stat(s, 4.675, 4.35, 3.95, 2.15, "3 : 1", "SF to RG; the carried, bench-tested unit that is run flat most often")
stat(s, 8.8, 4.35, 3.95, 2.15, "partial", "and different each time: single files damaged, not the whole store")
notes(s, "Each incident is in the scar catalog with its log evidence: Sep 3 CLI port-close reset (region, Bluetooth); Sep 30 both radios after flat batteries (RG channels only, SF everything); Oct 17 SF after a week idle (Bluetooth, channel back to 906.875, owner name); Oct 24 SF flat in transit (channel and key, precision, Bluetooth, cadence, owner, canned messages, node DB). Partial and varying is the detail that matters: files, not the store.")

# ============ 4 STORAGE ============
s = slide(); frame(s, "part ii - how the radio remembers", "DEO")
head(s, "How the radio stores its settings", "Partition table and file sizes read from SF; save and load behaviour from meshtastic/firmware v2.7.26.")
s.shapes.add_picture("deck/g_storage.png", Inches(0.55), Inches(1.4), width=Inches(12.2))
notes(s, "Six protobuf files on a 3.4 MB LittleFS partition. Red boxes are the policy weaknesses in the vendor's code: the power gate that always returns true on ESP32, the one non-atomic file, the ignored close() result, and the load-failure path that installs factory defaults and saves them with no backup consulted. The green line is the one protection that exists: the low-battery deep sleep skips the write. Sources: NodeDB.cpp, SafeFile.cpp, PowerHAL.cpp, PowerFSM.cpp, sleep.cpp at the tag.")

# ============ 5 FIRMWARE FACTS ============
s = slide(); frame(s, "part ii - how the radio remembers")
head(s, "What the firmware does and does not do", "Verified in source at tag v2.7.26; every line has a file name.")
card(s, 0.55, 1.5, 6.0, 3.3, "Does", ["Write .tmp, re-read it, 1-byte XOR check, then rename (SafeFile.cpp)", "Re-save device.proto on every boot (our boot log)", "Install factory defaults when a file is missing or will not decode, then save them (NodeDB.cpp)", "Skip the flash write on its own low-battery deep sleep (PowerFSM.cpp, sleep.cpp)", "Reset the CPU only below 2.44 V (core sdkconfig, level 7)"], INK, 13.5, 12.5)
card(s, 6.75, 1.5, 6.0, 3.3, "Does not", ["Check the supply before any save: powerHAL_isPowerLevelSafe() is a stub returning true on ESP32", "Keep nodes.proto atomic: the original is deleted before the new copy is written", "Act on a failed save: close() result discarded, 'Can't write prefs!' then return okay", "Consult the backup copy at boot: restorePreferences() runs only on operator command", "Retry before resetting: one unreadable file is a permanent factory reset"], RED, 13.5, 12.5)
codebox(s, 0.55, 5.0, 12.2, 1.5, "src/power/PowerHAL.cpp, tag v2.7.26: THE GATE EVERY SAVE PASSES THROUGH ON OUR RADIOS", [("__attribute__((weak, noinline)) bool powerHAL_isPowerLevelSafe()", ICE), ("{", ICE), ("    return true;        // no ESP32 override exists in src/platform/esp32", PINK), ("}", ICE)], 11)
notes(s, "The asymmetry to point out: the firmware refuses to write during its own low-battery shutdown, which proves the authors knew the danger, but it has no voltage check on the ordinary save path, and that path runs on every boot. On ESP32 the gate function is a weak default; no platform override exists in src/platform/esp32.")

# ============ 6 PHYSICS ============
s = slide(); frame(s, "part ii - how the radio remembers", "VICTOR")
head(s, "The physics: a 260 mV window")
s.shapes.add_picture("deck/g_voltage.png", Inches(0.55), Inches(1.25), width=Inches(12.2))
txt(s, 0.55, 6.15, 12.2, 0.5, "Boya BY25Q128AS (JEDEC 68 40 18, read from the chip): VCC 2.7 to 3.6 V, page program 0.6 ms, sector erase 50 ms, 100k cycles. Heltec V4 datasheet tables 3.2 and 3.4. ESP-IDF Kconfig for ESP32-S3.", 10.5, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "A sector erase takes 50 ms. A 750 mA transmit pulse on a nearly flat cell can pull the rail through 2.7 V and back inside that window without ever reaching the 2.44 V reset. The datasheet states that VCC must be held within range during all operations. Between 2.44 and 2.7 V the CPU is alive, the write proceeds, and the result is undefined.")

# ============ 7 UPSTREAM ============
s = slide(); frame(s, "part ii - how the radio remembers")
head(s, "Upstream already knows", "meshtastic/firmware issue tracker")
rows = [["Reference", "Boards", "Report", "Status"],
        ["#4555", "Heltec HT-CT62, V3, V4", "Power loss in early boot resets configuration after 2 to 3 attempts", "Closed 'not planned' Oct 2025"],
        ["#4622", "Heltec V3", "Resets when the battery is empty", "Duplicate of #4555"],
        ["#2936, #3260", "RAK4631, Heltec V2", "Defaults after the battery dies; prefs files missing", "Older platform, same symptom"],
        ["#5259", "ESP32 boards", "3.10 V low-battery cutoff is below what the LDOs need", "Open"],
        ["PR #11872", "nRF52 only", "Retry saves, check the rail first, stop formatting on a low rail", "Merged; no ESP32 equivalent"]]
table(s, 0.55, 1.5, 12.2, rows, [1.7, 2.5, 5.2, 2.8], fs=11, rh=0.52)
codebox(s, 0.55, 4.8, 12.2, 1.6, "MAINTAINER, IN #4555", [
    ("\"If the brownout circuit worked, it should hold the CPU in reset when voltage is too low for flash.\"", ICE),
    ("Community workaround: hard-code the configuration in userPrefs.jsonc so the defaults ARE the intended settings.", MUT)], 11)
notes(s, "We are not the first. The maintainers' reading matches ours. The nRF52 branch received a fix in 2026; the ESP32 branch we run did not. The community workaround on the last line becomes our fix 1.")

# ============ 8 HYPOTHESES ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "Hypotheses, predictions, verdicts", "Predictions written before the measurement; verdicts after.")
rows = [["#", "Hypothesis", "Would show", "Verdict"],
        ["H1", "Flash wear-out", "Diffuse failures; write counts near 100k per sector", "Rejected: 20 sectors per boot over 864 is millions of boots"],
        ["H2", "Defective cells", "Same sectors misread every pass; cells fail again after a rewrite", "Rejected: unstable sectors became perfect once rewritten"],
        ["H3", "Torn writes under low supply", "Follows power events; fixed sectors unstable until erased and reprogrammed", "Confirmed: measured on SF, repaired by a rewrite"],
        ["H4", "LittleFS bug", "Mount failures, corrupted directory pairs", "Rejected: mounts and decodes cleanly on both radios"],
        ["H5", "Firmware turns any failure into a reset", "Loss is permanent and silent", "Confirmed in source"]]
table(s, 0.55, 1.5, 12.2, rows, [0.5, 2.6, 4.4, 4.7], fs=11, rh=0.6)
card(s, 0.55, 5.3, 12.2, 1.25, "The discriminating experiment", "Three reads of the settings partition in one open connection with the firmware halted, at two serial speeds; a megabyte of program code, the NVS partition and the bootloader read the same way as controls.", GREEN, 13.5, 12.5)
notes(s, "Say the predictions first, then the data. H2 and H3 both predict fixed unstable sectors; only the erase-and-reprogram test separates them, and it did.")

# ============ 9 METHOD ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "Method: reading the chip, firmware stopped")
codebox(s, 0.55, 1.4, 7.4, 2.9, "ESPTOOL STUB, ONE CONNECTION, NO RESET BETWEEN READS", [
    ("esp = detect_chip('COM4'); esp = esp.run_stub()", ICE),
    ("A = esp.read_flash(0xC90000, 0x360000)   # settings, 3.4 MB", ICE),
    ("B = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("C = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("app = esp.read_flash(0x10000, 0x100000) x2   # control", MUT),
    ("A == B ?   B == C ?   app1 == app2 ?", ACC),
    ("# each chunk is MD5-checked by the stub: a transfer error raises,", MUT),
    ("# a changed byte is what the chip returned", MUT)], 10.5)
card(s, 8.15, 1.4, 4.6, 2.9, "Controls", ["Program partition, 1 MB, twice", "NVS partition and bootloader, twice", "16 KB window, four reads, at 115200 and at 921600 baud", "LittleFS image mounted and every file decoded on the laptop"], GREEN, 13.5, 12)
card(s, 0.55, 4.55, 12.2, 1.95, "The pitfall that cost two attempts", ["This board resets whenever the USB serial port closes: separate esptool commands hide a boot, and a boot-time flash write, between 'back-to-back' reads", "Only reads inside one open connection count; the pitfall is itself evidence that the radio writes flash every time it starts"], ACC, 13.5, 12.5)
notes(s, "Reproducible by anyone with the repository: scripts under docs/src, records under docs/src/flash_forensics. The LittleFS image also proved the configuration in flash on measurement day was correct: Group9, 32-byte key, precision 32, CLIENT_MUTE, No PIN, 60/10/20/10 s.")

# ============ 10 RESULT MAPS ============
s = slide(); frame(s, "part iii - the measurement")
head(s, "Result: the same sectors misread, every pass", "SF against RG, same day, same method")
s.shapes.add_picture("deck/g_maps_compare.png", Inches(0.55), Inches(1.4), width=Inches(12.2))
txt(s, 0.55, 5.0, 12.2, 0.6, "Red sectors changed between consecutive reads with no firmware running: the same sectors on every pass, at both serial speeds, while the program partition read identically.", 12.5, False, BODY)
stat(s, 0.55, 5.6, 3.95, 1.1, "21", "unstable sectors on SF, 12 heavily", RED, 22)
stat(s, 4.675, 5.6, 3.95, 1.1, "0", "unstable sectors on RG", GREEN, 22)
stat(s, 8.8, 5.6, 3.95, 1.1, "0", "differences in program code, NVS, bootloader", GREEN, 22)
notes(s, "SF: 117 and 107 differing bytes between consecutive reads, 118 bits flipped in both directions, none inside erased areas, confined to 21 sectors with 12 carrying almost all of it. RG: zero. The live files on SF sat in clean sectors 25, 26 and 470 that day, which is why the radio was working; LittleFS wear-levelling would have moved them onto the bad ones eventually.")

# ============ 11 RESULT NUMBERS ============
s = slide(); frame(s, "part iii - the measurement")
head(s, "Result: the numbers")
s.shapes.add_picture("deck/g_unstable.png", Inches(0.55), Inches(1.3), width=Inches(7.9))
stat(s, 8.75, 1.3, 1.95, 1.45, "117 / 107", "differing bytes, reads 1v2 and 2v3", ACC, 20)
stat(s, 10.85, 1.3, 1.95, 1.45, "118", "bits flipped, both directions", ACC, 20)
stat(s, 8.75, 2.9, 1.95, 1.45, "0", "differences in 1 MB of program code", GREEN, 20)
stat(s, 10.85, 2.9, 1.95, 1.45, "0", "differences in NVS and bootloader", GREEN, 20)
card(s, 0.55, 4.6, 12.2, 1.9, "Reading it", ["Fixed sectors, both bit directions, speed-independent, code partition stable: cells whose stored charge sits at the read threshold", "Not a serial artifact (chunks are verified), not wear (the pattern would be diffuse), not a filesystem bug (the image mounts and decodes)"], RED, 13.5, 12.5)
notes(s, "Be exact: the measurement establishes marginal cells in SF's settings partition on that day. Why they were marginal is the next two sheets.")

# ============ 12 DECISIVE TEST ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "The decisive test: disturbed, not damaged", "Erase, program three patterns, read five times each. Free sectors only; configuration untouched.")
rows = [["Sector", "As found", "0x00 x5", "A5/5A x5", "random x5", "Erased x5"],
        ["57 (worst)", "27 bytes disagree", "clean", "clean", "clean", "clean"],
        ["31", "20 bytes disagree", "clean", "clean", "clean", "clean"],
        ["200 (control)", "stable", "clean", "clean", "clean", "clean"]]
table(s, 0.55, 1.6, 12.2, rows, [2.2, 2.6, 1.85, 1.85, 1.85, 1.85], fs=12, rh=0.5)
stat(s, 0.55, 3.9, 3.95, 2.2, "0", "mismatches in 45 reads of three patterns across two scarred sectors", GREEN, 40)
card(s, 4.7, 3.9, 8.05, 2.2, "Verdict", ["The silicon is sound: it programs, erases and holds every pattern once written under a healthy supply", "The instability was the residue of earlier writes completed with the supply outside the flash's range", "H2 falls; H3 stands. The hardware question is closed"], GREEN, 13.5, 12.5)
notes(s, "Run on 27 October with authorisation. Sectors 57 and 31 were free in LittleFS (live data in 0, 1, 25, 26, 470), so nothing was lost; the radio booted normally afterwards. Record: docs/src/flash_forensics/decisive_test_2026-10-27.json. The control sector behaving identically validates the method.")

# ============ 13 REPAIR ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "The repair, same day", "Clean erase of the settings partition on USB power, then the snapshot.")
stat(s, 0.55, 1.5, 3.95, 2.1, "21 -> 0", "unstable sectors on SF, measured before and after", GREEN, 36)
stat(s, 4.675, 1.5, 3.95, 2.1, "2 passes", "of --configure: the region write reboots the radio mid-transaction", ACC, 36)
stat(s, 8.8, 1.5, 3.95, 2.1, "same key", "node key pair preserved; RG's node table stays valid", INK, 36)
card(s, 0.55, 3.9, 6.0, 2.6, "Steps", ["esptool erase_region 0xC90000 0x360000 (USB powered)", "First boot: 'Failed to initialize LittleFS', format, factory defaults", "meshtastic --configure sf-config.yaml, twice, 20 s apart", "Read back, reset, read back again: identical", "Three reads of the partition: 0 differing bytes"], INK, 13.5, 12)
card(s, 6.75, 3.9, 6.0, 2.6, "What the first pass taught", ["Pass 1 restored Bluetooth, region and the presets; owner, role, channel and cadence were lost in the reboot the region write triggers", "Now a rule in User Guide 12.2: run the command twice", "RG needs no repair today; its baseline is clean"], ACC, 13.5, 12)
notes(s, "Thirty minutes end to end. The two-pass behaviour is the same reset-during-write race as the Sep 3 incident, seen from the other side.")

# ============ 14 CHAIN ============
s = slide(); frame(s, "part iv - the fix")
head(s, "The chain of causation", "Every link tagged with its class of evidence.")
s.shapes.add_picture("deck/g_chain.png", Inches(0.55), Inches(1.4), width=Inches(12.2))
rows = [["Link", "Evidence", "Class"],
        ["Flat battery, reboot churn on recovery", "3 of 4 incidents; #4555 reproduces it", "Observed"],
        ["Flash write on every boot, no voltage gate", "Boot log; PowerHAL.cpp stub", "Verified in source"],
        ["Rail between 2.44 and 2.7 V during a write", "Datasheets, sdkconfig, 750 mA TX pulses", "Inferred (scope capture pending)"],
        ["Cells left half-programmed", "SF sector map; healed by rewrite", "Measured"],
        ["Decode fails, defaults installed and saved", "NodeDB.cpp; the losses themselves", "Verified in source"]]
table(s, 0.55, 4.1, 12.2, rows, [4.0, 5.2, 3.0], fs=11, rh=0.42)
notes(s, "One link is inferred rather than measured: the rail voltage during the event. An oscilloscope on the 3V3 pin during a transmit burst at 3.4 V cell voltage closes it; it is step 5 of the proof plan.")

# ============ 15 FIX PLAN ============
s = slide(); frame(s, "part iv - the fix", "DEO")
head(s, "Fix plan, ranked by leverage")
rows = [["#", "Fix", "Effect", "Effort", "Status"],
        ["1", "Build with our configuration as the defaults (userPrefs.jsonc + NO_PIN patch)", "A revert restores the intended state; the failure becomes invisible", "1 day", "next"],
        ["2", "ESP32 power gate: refuse saves below 3.5 V on battery; drop the boot-time device.proto rewrite", "Removes the write that happens at the worst moment", "1 day + test", "next"],
        ["3", "Clean erase and re-provision of scarred partitions", "Removes residue already present", "30 min / radio", "done: SF"],
        ["4", "Raise the brownout reset to 2.67 or 2.84 V (core rebuild)", "CPU resets before the flash leaves spec", "2 days", "planned"],
        ["5", "Operations: never store flat, OLED pre-flight, config snapshots, phone-QR recovery", "Detection in 2 s, recovery in 90 s", "in force", "done"]]
tb = table(s, 0.55, 1.4, 12.2, rows, [0.4, 5.0, 4.1, 1.3, 1.4], fs=11, rh=0.72)
card(s, 0.55, 5.85, 12.2, 0.7, "Order of value", "Fix 1 hides the failure from the driver; fix 2 removes its cause; fix 3 cleans up the past; fix 4 is the hardware-correct answer and the most work.", INK, 12.5, 12)
notes(s, "Fix 1 is the community's own answer to #4555 and costs one build per radio. The key is compiled into a binary that lives only in the private repository. Fix 2 is a ten-line patch we would offer upstream.")

# ============ 16 FIX 1 ============
s = slide(); frame(s, "part iv - the fix", "DEO")
head(s, "Fix 1: a revert that restores OUR settings")
codebox(s, 0.55, 1.4, 7.2, 2.75, "userPrefs.jsonc (private repo; key redacted)", [
    ('"USERPREFS_CHANNELS_TO_WRITE": 1,', ICE),
    ('"USERPREFS_CHANNEL_0_NAME": "Group9",', ICE),
    ('"USERPREFS_CHANNEL_0_PRECISION": 32,', ICE),
    ('"USERPREFS_CHANNEL_0_PSK": "{ 0x.., ... 32 bytes }",', PINK),
    ('"USERPREFS_CONFIG_LORA_REGION": "..._RegionCode_US",', ICE),
    ('"USERPREFS_CONFIG_OWNER_LONG_NAME": "SF", "..._SHORT_NAME": "SF",', ICE),
    ('"USERPREFS_CONFIG_DEVICE_ROLE": "..._Role_CLIENT_MUTE",', ICE),
    ('"USERPREFS_CONFIG_GPS_UPDATE_INTERVAL": 10, "..._POSITION_BROADCAST_INTERVAL": 60,', ICE),
    ('// NodeDB.cpp installDefaultConfig(): bluetooth.mode = NO_PIN   (one line)', ACC)], 10)
card(s, 7.95, 1.4, 4.8, 2.75, "Why it is first", ["Every failure path ends in installDefault*()", "Today that means 906.875 MHz, a random PIN, a nameless radio", "With these defaults it means Group9 at 912.875, No PIN, SF or RG", "One build per radio, flashed with the fleet procedure"], GREEN, 13.5, 12)
card(s, 0.55, 4.4, 12.2, 1.6, "Acceptance test", ["Flash, provision nothing, power on: Group9 at 912.875 MHz, CLIENT_MUTE, No PIN, named, linked to a display with zero commands", "meshtastic --factory-reset, power-cycle: comes back identical. That is the proof a future revert is harmless"], INK, 13.5, 12.5)
notes(s, "The only security consideration: the channel key is compiled into the firmware image, which must stay in the private repository and never be published.")

# ============ 17 PROOF ============
s = slide(); frame(s, "part iv - the fix", "CANNON")
head(s, "How we prove it")
rows = [["Step", "Procedure", "Pass criterion", "Status"],
        ["1", "Baseline flash map on both radios", "Recorded", "done: SF 21, RG 0"],
        ["2", "Decisive sector test; clean erase and re-provision", "Outcome recorded; 0 unstable after", "done: SF"],
        ["3", "Fix 1 (+2) builds; acceptance test on each radio", "Correct configuration with zero provisioning", "next"],
        ["4", "Flat-battery campaign: 5 full discharges per radio, read config and flash map each cycle", "0 of 10 cycles lose configuration; no new unstable sectors", "planned"],
        ["5", "Oscilloscope on the 3V3 pin during a TX burst at 3.4 V cell", "Minimum rail recorded; confirms or refutes the 2.7 V excursion", "planned"],
        ["6", "Documents: manual 16, User Guide 12", "Rebuilt and pushed", "done"]]
table(s, 0.55, 1.4, 12.2, rows, [0.6, 5.6, 4.0, 2.0], fs=11, rh=0.58)
card(s, 0.55, 5.6, 12.2, 0.9, "Cost", "About a week of firmware work and one afternoon with a scope; no new hardware. Step 4 is the test that would have caught this in September.", INK, 12.5, 12)
notes(s, "A fix without a test is a hope. The flat-battery campaign is deliberately brutal: it reproduces the exact conditions of all three battery incidents, with the flash map read after every cycle.")

# ============ 18 ANSWER ============
s = slide(); frame(s, "part iv - the fix")
head(s, "The answer")
card(s, 0.55, 1.45, 12.2, 1.6, "Is it the memory itself?", "Partly, and measurably, but not in the way the question implies. SF's settings flash carried 21 sectors that would not hold a value; the same sectors became perfect once rewritten under a healthy supply. The chip is sound and not worn. The cells had been left half-written by operations completed below the flash's 2.7 V minimum but above the 2.44 V reset point, a window the firmware never checks and then punishes with factory defaults.", INK, 15, 13)
stat(s, 0.55, 3.45, 2.95, 2.3, "21 -> 0", "unstable sectors on SF, before and after one clean rewrite")
stat(s, 3.63, 3.45, 2.95, 2.3, "0", "unstable sectors on RG, the radio that reverted once")
stat(s, 6.71, 3.45, 2.95, 2.3, "true", "what the firmware's 'is power safe to write?' returns on ESP32, always")
stat(s, 9.79, 3.45, 2.95, 2.3, "1 build", "makes a future revert restore our configuration, not the factory's")
rect(s, 0.55, 6.0, 12.2, 0.5, INK)
txt(s, 0.8, 6.09, 11.7, 0.35, "THE MEMORY BORE THE SCAR; THE POWER RAIL MADE IT; THE FIRMWARE MADE IT PERMANENT; A REWRITE HEALS IT. ALL THREE ARE FIXABLE.", 11.5, True, PAPER, PP_ALIGN.CENTER, HF)
notes(s, "Close on the sentence in the bar. Then the ask: approval to build fix 1 and fix 2 and to run the flat-battery campaign before the next field test.")

prs.save("Group9_ConfigLoss_RootCause.pptx")
import os
print("saved", os.path.getsize("Group9_ConfigLoss_RootCause.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))
