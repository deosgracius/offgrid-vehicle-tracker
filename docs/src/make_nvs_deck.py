# Configuration-loss root-cause deck: drawing-set chrome, Cambria body.
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
    txt(s, 9.7, 6.94, 3.3, 0.32, "SHEET %02d/%02d  REV A  %s" % (sheet_no[0], TOTAL, DATE), 9, False, MUT, PP_ALIGN.RIGHT, MONO)
    if owner:
        rect(s, 10.55, 0.38, 2.35, 0.46, PAPER, M[owner], 1.5)
        txt(s, 10.55, 0.44, 2.35, 0.34, "OWNER: " + owner, 11, True, M[owner], PP_ALIGN.CENTER, MONO)
def head(s, t): txt(s, 0.5, 0.36, 9.9, 0.62, t.upper(), 23, True, INK, PP_ALIGN.LEFT, HF, spc=200)
def card(s, x, y, w, h, title, body, accent=INK, ts=14, bs=12.5):
    rect(s, x, y, w, h, CARD, accent, 1.25)
    tb = s.shapes.add_textbox(Inches(x+0.18), Inches(y+0.13), Inches(w-0.36), Inches(h-0.26))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; r = p.add_run(); r.text = title.upper()
    r.font.size = Pt(ts); r.font.bold = True; r.font.color.rgb = accent; r.font.name = HF; set_spc(r, 100)
    p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = body
    r2.font.size = Pt(bs); r2.font.color.rgb = BODY; r2.font.name = BF
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

# ============ 1 TITLE ============
s = slide(); gridpaper(s); frame(s, "root cause investigation")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHY THE RADIOS FORGET", 40, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "CONFIGURATION LOSS AFTER BATTERY DEATH: EVIDENCE, MECHANISM, AND FIX", 17, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.3, 1.5, "Four times this semester a Meshtastic radio came back from a flat battery with factory settings. A reviewer asked whether the memory itself is at fault. This deck answers that question with measurements taken on the affected radio, the firmware's own source, and the parts' datasheets, and it ends with a fix plan that can be tested.", 13, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\nOctober 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Frame: one failure mode, investigated to the physical layer. Everything quantitative on these sheets was measured on the SF radio today or read from the vendor's source and datasheets; the sources are named on the sheets.")

# ============ 2 THE QUESTION ============
s = slide(); frame(s, "part i - the question")
head(s, "The question and what counts as an answer")
card(s, 0.55, 1.35, 6.0, 2.35, "The hypothesis we were handed", "\"It might be the memory itself.\" Taken seriously, this means one of three things: the flash chip is worn out (program/erase endurance exhausted), it has defective or marginal cells, or its contents are being corrupted by something outside the chip (a write performed under bad conditions). Each leaves a different fingerprint, and each has a different fix.", INK, 13.5, 12)
card(s, 6.75, 1.35, 6.0, 2.35, "How we decided to test it", "Not by opinion. We read the settings partition straight off the flash chip with the firmware stopped, several times in one session, and asked whether the chip returns the same bytes. We read the firmware's save and load code at the exact tag we run (2.7.26). We read the flash datasheet's supply limits and the brownout threshold the firmware is built with. Then we lined the four incidents up against all of it.", GREEN, 13.5, 12)
rows = [["If the cause is...", "The fingerprint would be...", "The fix would be..."],
        ["Flash wear", "Failures spread across many sectors; write volume near 100k cycles per sector", "Replace the part; reduce write rate"],
        ["Defective / marginal cells", "The SAME sectors misread on every pass, with the chip otherwise healthy", "Avoid or re-form those sectors; or replace the radio"],
        ["Torn write (power loss mid-program)", "Failures only after power events; cells left half-programmed read unstably until re-erased", "Stop writing when the supply is low; make the fallback harmless"],
        ["Firmware policy", "Any read failure becomes a permanent factory reset; no backup consulted", "Change the defaults, add a backup, retry before resetting"]]
table(s, 0.55, 3.95, 12.2, rows, [2.6, 5.4, 4.2], fs=11, rh=0.52)
notes(s, "The point of the sheet: the recruiter's suggestion is testable, and the four candidate causes are distinguishable by evidence we can actually collect with a USB cable.")

# ============ 3 THE RECORD ============
s = slide(); frame(s, "part i - the question", "DEO")
head(s, "The record: four losses, one pattern")
rows = [["Date", "Radio", "Preceded by", "What came back as factory default", "What survived"],
        ["Sep 3", "SF", "CLI port-close reset mid-save (not a battery event)", "Reboot-triggering settings: region, Bluetooth mode", "Everything else"],
        ["Sep 30", "RG and SF", "Both batteries ran flat overnight", "RG: channels only. SF: channel + key, role, Bluetooth, telemetry, owner name", "RG: all but channels"],
        ["Oct 17", "SF", "About a week idle, battery flat", "Bluetooth mode, channel (back to 906.875 MHz), owner name", "Position cadence, role"],
        ["Oct 24", "SF", "Battery flat in transit", "Channel + key, position precision, Bluetooth, cadence, owner, canned messages, node database", "Role (as read back)"]]
table(s, 0.55, 1.3, 12.2, rows, [0.9, 1.2, 3.1, 4.6, 2.4], fs=10.5, rh=0.62)
card(s, 0.55, 4.6, 6.0, 1.95, "What the pattern says", "Three of four follow a flat battery; the fourth is a known reset-during-write race. SF accounts for three of four. The losses are partial and vary from event to event, which is what you expect if individual files, not the whole store, are being damaged.", INK, 13, 12)
card(s, 6.75, 4.6, 6.0, 1.95, "What it rules out already", "Not a single bad setting and not operator error: the same provisioning block was applied and read back each time. Not the display firmware: the displays only read from the radio over Bluetooth. Whatever this is lives between the radio's power rail and its flash.", GREEN, 13, 12)
notes(s, "Each row is in the scar catalog with its log evidence. Emphasise partial and varying: that detail matters for the mechanism.")

# ============ 4 STORAGE ============
s = slide(); frame(s, "part ii - how the radio remembers", "DEO")
head(s, "How the radio stores its settings")
s.shapes.add_picture("deck/g_storage.png", Inches(0.55), Inches(1.25), width=Inches(12.2))
txt(s, 0.55, 6.25, 12.2, 0.5, "Partition table and file sizes read from the SF radio on 2026-10-27; save/load behaviour from meshtastic/firmware tag v2.7.26 (NodeDB.cpp, SafeFile.cpp, PowerHAL.cpp, PowerFSM.cpp, sleep.cpp).", 10.5, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "Two stores: a tiny NVS and a 3.4 MB LittleFS partition holding six protobuf files. Red boxes are the policy weaknesses: no power gate on ESP32, one non-atomic file, ignored close result, and defaults installed and saved on any load failure.")

# ============ 5 FIRMWARE FACTS ============
s = slide(); frame(s, "part ii - how the radio remembers")
head(s, "What the firmware does, verified at tag v2.7.26")
rows = [["Behaviour", "Source", "Consequence for us"],
        ["Every save is gated by powerHAL_isPowerLevelSafe()", "PowerHAL.cpp: weak default `return true;` no ESP32 override exists", "On our radios a save is never refused for low voltage"],
        ["Atomic save: write .tmp, re-read, 1-byte XOR check, rename", "SafeFile.cpp", "Protects against a torn write of the NEW copy, if the check runs"],
        ["nodes.proto saved with fullAtomic=false", "NodeDB.cpp saveNodeDatabaseToDisk", "Original deleted before the write: a reset mid-save leaves no node database (seen Oct 24)"],
        ["saveProto ignores the close() result", "NodeDB.cpp: logs 'Can't write prefs!' then returns okay", "A failed save is invisible to the caller"],
        ["device.proto is re-saved at every boot", "Our boot log: 'Opening /prefs/device.proto, fullAtomic=1 / Save'", "Every reboot of a dying battery is a flash write"],
        ["Load failure -> installDefault*() and save", "NodeDB.cpp loadFromDisk; no backup consulted", "One unreadable file becomes a permanent factory reset"],
        ["Low-battery path: deep sleep with skipSaveNodeDb=true", "PowerFSM.cpp lowBattSDSEnter -> sleep.cpp", "The clean shutdown does NOT write: the firmware already knows this is dangerous"],
        ["Brownout reset threshold", "Arduino-ESP32 core sdkconfig: CONFIG_ESP_BROWNOUT_DET_LVL=7 (2.44 V)", "CPU keeps running 260 mV below the flash's minimum supply"]]
table(s, 0.55, 1.3, 12.2, rows, [3.6, 4.6, 4.0], fs=10.5, rh=0.56)
notes(s, "This is the vendor's code, not ours. The important asymmetry: the firmware refuses to write during its own low-battery shutdown, but has no voltage check on the ordinary save path that runs at every boot.")

# ============ 6 PHYSICS ============
s = slide(); frame(s, "part ii - how the radio remembers", "VICTOR")
head(s, "The physics: a 260 mV window")
s.shapes.add_picture("deck/g_voltage.png", Inches(0.55), Inches(1.25), width=Inches(12.2))
txt(s, 0.55, 6.1, 12.2, 0.6, "Flash: Boya BY25Q128AS (JEDEC 68 40 18, read from the chip), VCC 2.7 to 3.6 V, page program 0.6 ms typ, sector erase 50 ms typ, 100k cycles, 20-year retention. Board: Heltec V4 datasheet tables 3.2 and 3.4. Brownout level: ESP-IDF Kconfig for ESP32-S3.", 10.5, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "A sector erase takes 50 ms. A 750 mA transmit pulse on a nearly flat cell can drop the rail through 2.7 V and back inside that window without ever reaching the 2.44 V reset. The datasheet forbids exactly this.")

# ============ 7 UPSTREAM ============
s = slide(); frame(s, "part ii - how the radio remembers")
head(s, "Upstream already knows this failure")
rows = [["Reference", "Boards / version", "What it reports", "Status"],
        ["meshtastic/firmware #4555", "Heltec HT-CT62, V3, V4; 2.4 to 2.7.15", "Power loss during early boot resets configuration after 2-3 attempts; later only owner names (device.proto written at boot)", "Closed 'not planned' Oct 2025; still reported 2026"],
        ["#4622", "Heltec V3, 2.4.3", "Resets when the battery is empty", "Closed as duplicate of #4555"],
        ["#2936, #3260", "RAK4631, Heltec V2; 2.2.x", "Defaults (region UNSET) after the battery dies; prefs files missing at boot", "Older platform, same symptom"],
        ["#5259", "ESP32 boards, 2.5.x", "Low-voltage cutoff (3.10 V) is below what most LDOs need; asks for 3.42 or 3.53 V", "Open discussion"],
        ["PR #11872 (nRF52 only)", "nRF52", "Retry failed saves, check the power rail before retrying, stop formatting on a low rail", "Merged for nRF52; no ESP32 equivalent"]]
table(s, 0.55, 1.3, 12.2, rows, [2.3, 2.6, 4.9, 2.4], fs=10.5, rh=0.62)
codebox(s, 0.55, 5.2, 12.2, 1.35, "MAINTAINER'S OWN DIAGNOSIS IN #4555", [
    ("\"If the brownout circuit worked, it should hold the CPU in reset when voltage is too low for flash.\"", ICE),
    ("Workarounds users adopted: hard-code the configuration in userPrefs.jsonc so the 'defaults' are the intended settings.", MUT)], 10.5)
notes(s, "We are not the first. The maintainers' own reading matches ours. The nRF52 branch got a fix this year; the ESP32 branch, which we run, did not.")

# ============ 8 HYPOTHESIS MATRIX ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "Hypotheses before the measurement")
rows = [["#", "Hypothesis", "Predicts", "Prior evidence"],
        ["H1", "Flash wear-out", "Random sectors fail; write counts near endurance", "Against: 20 sectors per boot spread by wear-levelling over 864; 100k cycles = millions of boots"],
        ["H2", "Defective or marginal cells in the settings partition", "Same sectors misread on every pass while code partition reads clean", "Neutral: would explain why SF fails more than RG"],
        ["H3", "Torn write under low supply", "Losses follow power events; files, not the whole store, affected", "For: 3 of 4 events follow a flat battery; partial, varying losses"],
        ["H4", "Filesystem (LittleFS) bug", "Corrupted directory pairs, mount failures", "Against: LittleFS mounts cleanly; upstream reports the same loss on three filesystems"],
        ["H5", "Firmware policy turns any failure into a reset", "Loss is permanent and silent", "For: verified in source (sheet 5)"]]
table(s, 0.55, 1.3, 12.2, rows, [0.5, 3.0, 4.0, 4.7], fs=10.5, rh=0.62)
card(s, 0.55, 5.15, 12.2, 1.4, "The discriminating experiment", "Read the settings partition from the chip, with the firmware halted, three times inside one open connection, at two serial speeds; read a megabyte of the program partition, the NVS partition and the bootloader the same way as controls. Identical reads everywhere: H2 falls. Repeating differences in fixed sectors: H2 or the residue of H3. Random differences everywhere: the test rig, not the chip.", GREEN, 13, 12)
notes(s, "State the predictions before showing the data. That is what makes the result credible.")

# ============ 9 METHOD ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "Method: reading the chip, firmware stopped")
codebox(s, 0.55, 1.3, 7.4, 3.1, "ESPTOOL STUB, ONE CONNECTION, NO RESET BETWEEN READS", [
    ("esp = detect_chip('COM4'); esp = esp.run_stub()", ICE),
    ("A = esp.read_flash(0xC90000, 0x360000)   # settings partition, 3.4 MB", ICE),
    ("B = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("C = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("app = esp.read_flash(0x10000, 0x100000) x2   # control: program code", MUT),
    ("nvs = esp.read_flash(0x9000, 0x5000) x2      # control: NVS", MUT),
    ("A == B ?   B == C ?   app1 == app2 ?", ACC),
    ("", ICE),
    ("# every chunk is MD5-checked by the stub against what it read,", MUT),
    ("# so a transfer error raises; a changed byte means the chip returned it", MUT)], 10.5)
card(s, 8.15, 1.3, 4.6, 3.1, "Why the first two attempts were thrown away", "This board resets whenever the USB serial port closes, so two 'back-to-back' reads made with separate esptool commands had a boot, and a boot-time flash write, hidden between them. Only reads inside one open connection count. The pitfall is itself a finding: this radio writes to flash every time it starts.", ACC, 13, 11.5)
card(s, 0.55, 4.6, 12.2, 1.95, "What else was captured", "The serial boot log (file names, sizes, 'Loaded ... successfully' for every file, 'Save /prefs/device.proto' at boot). The partition table and the flash JEDEC ID. The LittleFS image mounted on the laptop with littlefs-python and every settings file decoded with the Meshtastic protobufs, which also proved the configuration in flash today is correct: Group9, 32-byte key, precision 32, CLIENT_MUTE, No PIN, 60 / 10 / 20 / 10 s.", INK, 13, 12)
notes(s, "Reproducible by anyone with the repo: the scripts are archived under docs/src. Note the controls.")

# ============ 10 RESULT: SECTOR MAP ============
s = slide(); frame(s, "part iii - the measurement")
head(s, "Result: the same sectors misread on every pass")
s.shapes.add_picture("deck/g_sectormap.png", Inches(0.55), Inches(1.25), width=Inches(12.2))
txt(s, 0.55, 6.25, 12.2, 0.5, "SF RADIO, 2026-10-27. GREEN: WHERE THE LIVE CONFIG FILES SIT TODAY. RED: SECTORS WHOSE BYTES CHANGED BETWEEN CONSECUTIVE READS WITH NO FIRMWARE RUNNING.", 10.5, True, MUT, PP_ALIGN.CENTER, MONO)
notes(s, "A cluster of about a dozen unstable sectors low in the partition, plus a few singles. The live files happen not to be on them today.")

# ============ 11 RESULT: NUMBERS ============
s = slide(); frame(s, "part iii - the measurement")
head(s, "Result: the numbers")
s.shapes.add_picture("deck/g_unstable.png", Inches(0.55), Inches(1.25), width=Inches(8.0))
rows = [["Measurement", "Value"],
        ["Settings partition, read 1 vs 2 / 2 vs 3", "117 / 107 differing bytes"],
        ["Bits flipped (1 vs 2)", "118, in BOTH directions (0x02 to 0x00, 0x00 to 0x10)"],
        ["Differing bytes inside erased (0xFF) areas", "none: all in programmed data"],
        ["Same at 115200 and 921600 baud", "yes (16 KB window, 4 reads each)"],
        ["Program partition, 1 MB, two reads", "identical"],
        ["NVS partition and bootloader, two reads", "identical"],
        ["LittleFS mount and all six files decoded", "clean, configuration correct"],
        ["Unstable sectors vs live-file sectors", "no overlap today (25, 26, 470 are clean)"]]
table(s, 8.75, 1.3, 4.05, rows, [2.2, 1.85], fs=9.5, rh=0.5)
card(s, 0.55, 4.0, 8.0, 2.55, "Reading the result", "Bit flips confined to fixed sectors, in both directions, independent of transfer speed, with the code partition perfectly stable, is the signature of cells whose stored charge sits near the read threshold: marginal cells. It is not a serial artifact (the stub verifies each chunk), not wear (the pattern would be diffuse), and not a filesystem bug (the image mounts and decodes). The recruiter's intuition is confirmed in this narrow sense: today, part of SF's settings memory does not hold a definite value.", RED, 13.5, 12)
notes(s, "Be exact about what is and is not claimed. Marginal cells exist in SF's settings partition today. Why they exist is the next sheet.")

# ============ 12 INTERPRETATION ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "Interpretation: marginal cells and the losses")
card(s, 0.55, 1.35, 6.0, 2.55, "Why the live files are safe today and not tomorrow", "LittleFS is copy-on-write with wear-levelling: every save lands on a new sector, and the allocator walks forward through all 864. The unstable sectors are stale copies now, but each boot's device.proto write and each node-table save moves the live data on. When a live file, or the directory metadata that points to it, lands on a marginal sector, the next boot reads garbage, the protobuf decode fails, and the firmware installs and saves factory defaults. Which file is hit decides what is lost: that is the partial, varying pattern in the record.", INK, 13, 11.5)
card(s, 6.75, 1.35, 6.0, 2.55, "Why SF and not RG: now measured", "Marginal cells are specific to one chip and one history. RG, measured the same way the same day, shows a clean map: 0 differing bytes across three reads of its settings partition, 112 sectors holding data, program partition stable, LittleFS mounting and decoding correctly. SF is the carried, bench-tested unit run flat most often and reverted three times; RG reverted once and shows no residue today. The scar follows the history, not the design.", ACC, 13, 11.5)
card(s, 0.55, 4.1, 12.2, 2.45, "Where the marginal cells most likely came from", "NOR cells are programmed and erased by moving charge with internal high-voltage pumps that need VCC within 2.7 to 3.6 V. If the rail sags into the 2.44 to 2.7 V window mid-operation (a transmit pulse on a flat cell, or a reboot loop while charging a flat pack), the operation completes with cells left between the two charge states. Those cells read differently from one access to the next until the sector is erased and programmed again under good voltage. That is hypothesis H3 leaving the fingerprint predicted for H2. Alternatively the cells are permanently weak. One short experiment separates the two.", GREEN, 13, 11.5)
notes(s, "The honest framing: the measurement proves marginal cells; the physics plus the incident timing make torn writes the most probable origin; one more test decides it.")

# ============ 13 DECISIVE TEST ============
s = slide(); frame(s, "part iii - the measurement", "DEO")
head(s, "The decisive test: disturbed, not damaged")
rows = [["Sector", "As found (3 reads)", "After erase", "Programmed 0x00", "Programmed A5/5A", "Programmed random", "Erased again"],
        ["57 (worst)", "unstable: 27 bytes disagree", "5/5 clean", "5/5 clean", "5/5 clean", "5/5 clean", "5/5 clean"],
        ["31", "unstable: 20 bytes disagree", "5/5 clean", "5/5 clean", "5/5 clean", "5/5 clean", "5/5 clean"],
        ["200 (control, free)", "stable: 0", "5/5 clean", "5/5 clean", "5/5 clean", "5/5 clean", "5/5 clean"]]
table(s, 0.55, 1.3, 12.2, rows, [1.7, 2.6, 1.5, 1.6, 1.6, 1.7, 1.5], fs=10.5, rh=0.5)
card(s, 0.55, 3.5, 6.0, 3.05, "What was done (SF, 2026-10-27, authorised)", "Each sector: read three times as found; erase; program all-zeros and read five times; erase; program 0xA5/0x5A and read five times; erase; program a fixed random page and read five times; erase and leave free. Sector 200, which had never been written, served as the control. The sectors were free in LittleFS (its live data is in sectors 0, 1, 25, 26 and 470), so the configuration was untouched; the radio booted normally afterwards. Record: docs/src/flash_forensics/decisive_test_2026-10-27.json.", INK, 13, 11.5)
card(s, 6.75, 3.5, 6.0, 3.05, "What it means", "Outcome A. The cells program, erase and hold every pattern perfectly once written under a healthy supply: there is nothing wrong with the silicon. The instability we measured was the physical residue of earlier writes completed while the supply was outside the flash's operating range, exactly the mechanism the datasheet forbids and the firmware does not guard against. This closes the hardware question: not a defective or worn part, but a part that was written to under conditions in which no flash is specified to work. The repair was then carried out the same day: one clean erase of the settings partition under USB power, LittleFS re-formatted by the firmware, snapshot re-applied; the partition now reads with zero differing bytes across three passes.", GREEN, 13, 11.5)
notes(s, "This is the sheet that settles the recruiter's question. Healthy cells, damaged by the conditions of the write. Say that the control sector behaved identically, which validates the method.")

# ============ 14 CHAIN ============
s = slide(); frame(s, "part iv - the fix")
head(s, "The chain of causation")
s.shapes.add_picture("deck/g_chain.png", Inches(0.55), Inches(1.3), width=Inches(12.2))
rows = [["Link", "Evidence that it is real", "Confidence"],
        ["Battery flat, reboot churn on recovery", "Three of four incidents; #4555 reproduces by cutting power in early boot", "High"],
        ["Flash write on every boot, no voltage gate", "Boot log; PowerHAL.cpp weak stub; sheet 5", "Verified"],
        ["Rail can sit between 2.44 and 2.7 V", "Datasheets and sdkconfig; 750 mA TX pulses", "High (not oscilloscoped yet)"],
        ["Cells left marginal", "Measured on SF today: fixed unstable sectors", "Measured"],
        ["Decode fails -> defaults installed and saved", "NodeDB.cpp; the losses themselves", "Verified"]]
table(s, 0.55, 4.0, 12.2, rows, [3.6, 6.2, 2.4], fs=10.5, rh=0.42)
notes(s, "Every link is tagged with its evidence class: verified in source, measured on hardware, or inferred from datasheets. The one unmeasured link is the rail voltage during the event; a scope capture during a deliberate flat-battery test would close it.")

# ============ 15 FIX PLAN ============
s = slide(); frame(s, "part iv - the fix", "DEO")
head(s, "Fix plan, ranked by leverage")
rows = [["#", "Fix", "What it does", "Effort", "Owner"],
        ["1", "Make the defaults OUR configuration", "Build Meshtastic from source with userPrefs.jsonc: channel Group9 name + key + precision 32, region US, owner names, role CLIENT_MUTE; one-line patch for Bluetooth No PIN. A revert then restores the intended state instead of the factory one. The key lives only in the private build.", "1 day", "Deo"],
        ["2", "Refuse to write under low voltage", "Implement powerHAL_isPowerLevelSafe() for ESP32: return false below 3.5 V on battery with no USB; drop the boot-time device.proto rewrite (metala's proposal in #4555). Offer upstream.", "1 day + test", "Deo"],
        ["3", "Clear the marginal sectors: DONE on SF 2026-10-27", "Settings partition (0xC90000, 3.4 MB) erased on USB power; firmware re-formatted LittleFS; snapshot re-applied with --configure (two passes: the region write reboots the radio mid-transaction, so the second pass is mandatory); read-back correct and persistent; node key pair preserved. Re-measured: 0 unstable sectors. Repeat on RG after its baseline map.", "done (30 min)", "Deo"],
        ["4", "Raise the brownout threshold", "Rebuild the core with CONFIG_ESP_BROWNOUT_DET_LVL at 2.67 or 2.84 V so the CPU resets before the flash leaves spec. Needs the pioarduino libs rebuilt; validate it does not trip on TX pulses.", "2 days", "Victor"],
        ["5", "Operations, already in force", "Never store a radio flat; OLED pre-flight (912.875); config snapshots with --configure; phone-QR recovery (User Guide 12).", "done", "all"]]
table(s, 0.55, 1.3, 12.2, rows, [0.4, 2.6, 6.6, 1.2, 1.4], fs=10, rh=0.78)
notes(s, "Fix 1 alone makes the failure invisible to the driver. Fix 2 attacks the cause. Fix 3 cleans up the damage already done. Fix 4 is the hardware-correct answer and the most work.")

# ============ 16 FIX 1 DETAIL ============
s = slide(); frame(s, "part iv - the fix", "DEO")
head(s, "Fix 1: a revert that restores OUR settings")
codebox(s, 0.55, 1.3, 7.2, 3.3, "userPrefs.jsonc (private repo only; values illustrative, key redacted)", [
    ('"USERPREFS_CHANNELS_TO_WRITE": 1,', ICE),
    ('"USERPREFS_CHANNEL_0_NAME": "Group9",', ICE),
    ('"USERPREFS_CHANNEL_0_PRECISION": 32,', ICE),
    ('"USERPREFS_CHANNEL_0_PSK": "{ 0x.., 0x.., ... 32 bytes }",', PINK),
    ('"USERPREFS_CONFIG_LORA_REGION": "meshtastic_Config_LoRaConfig_RegionCode_US",', ICE),
    ('"USERPREFS_CONFIG_OWNER_LONG_NAME": "SF",   "USERPREFS_CONFIG_OWNER_SHORT_NAME": "SF",', ICE),
    ('"USERPREFS_CONFIG_DEVICE_ROLE": "meshtastic_Config_DeviceConfig_Role_CLIENT_MUTE",', ICE),
    ('"USERPREFS_CONFIG_GPS_UPDATE_INTERVAL": 10,  "USERPREFS_CONFIG_POSITION_BROADCAST_INTERVAL": 60,', ICE),
    ('// NodeDB.cpp installDefaultConfig(): bluetooth.mode = NO_PIN   (one-line patch)', ACC)], 10)
card(s, 7.95, 1.3, 4.8, 3.3, "Why this is the highest-leverage change", "Every mechanism on sheets 4 to 7 ends the same way: installDefault*(). Today that means the public frequency, a random PIN and a nameless radio. With the defaults set to our configuration, the same code path puts the radio back on 912.875 MHz with the right key, name and role. The failure still happens; nobody notices. Each radio gets its own build (SF / RG names), flashed once with the fleet procedure in the manual.", GREEN, 13, 11.5)
card(s, 0.55, 4.85, 12.2, 1.7, "Acceptance test", "Flash the build, provision nothing, power on: the radio must come up on Group9 at 912.875 MHz, CLIENT_MUTE, No PIN, named SF, and link to a display with no commands issued. Then delete /prefs over the CLI (meshtastic --factory-reset) and confirm it comes back identical. That is the proof that a future revert is harmless.", INK, 13, 12)
notes(s, "This is the workaround the upstream community converged on. The security consideration is that the key is compiled into a binary that must stay in the private repository and never be published.")

# ============ 17 VERIFICATION ============
s = slide(); frame(s, "part iv - the fix", "CANNON")
head(s, "How we will prove the fix")
rows = [["Step", "Procedure", "Pass criterion"],
        ["1", "Baseline flash map on both radios: done 2026-10-27", "RG: 0 unstable sectors (clean). SF: 21 before repair, 0 after"],
        ["2", "Decisive sector test on SF, then clean erase + re-provision: done 2026-10-27", "Outcome A; after the clean erase the partition reads with 0 differing bytes across 3 reads"],
        ["3", "Flash fix 1 (+2) builds; acceptance test on each radio", "Correct configuration with zero provisioning commands"],
        ["4", "Deliberate flat-battery campaign: run each radio to shutdown 5 times, recharge, boot, read config and flash map each cycle", "0 of 10 cycles lose configuration; no new unstable sectors"],
        ["5", "Rail capture: oscilloscope on the 3V3 pin during a TX burst at 3.4 V cell voltage", "Minimum rail voltage recorded; confirms or refutes the 2.7 V excursion"],
        ["6", "Documents: manual section 16 entry 2 rewritten with the mechanism; User Guide 12 kept as the operator recovery", "Both rebuilt and pushed"]]
table(s, 0.55, 1.3, 12.2, rows, [0.6, 7.2, 4.4], fs=10.5, rh=0.56)
card(s, 0.55, 5.5, 12.2, 1.05, "What this costs", "About a week of Deo's time for the firmware builds and the campaign, one afternoon of Victor's for the rail capture, and no new hardware. The result is a radio whose worst case after a dead battery is the configuration we wanted anyway.", INK, 13, 12)
notes(s, "A fix without a test is a hope. Step 4 is the one that would have caught this in September.")

# ============ 18 CLOSE ============
s = slide(); frame(s, "part iv - the fix")
head(s, "The answer")
card(s, 0.55, 1.35, 12.2, 2.3, "Is it the memory itself?", "Partly, and measurably, but not in the way the question implies. SF's settings partition held 21 sectors (12 heavily) whose cells did not return a definite value, while the program partition, NVS and bootloader were perfectly stable. Erasing and reprogramming those sectors under a healthy supply made them perfect again: the silicon is sound and not worn. The cells had been left half-written by operations completed while the supply was below the flash's 2.7 V minimum but above the 2.44 V reset point, a window the firmware never checks before writing and then punishes by installing factory defaults.", INK, 15, 13)
stats = [("21 -> 0", "unstable sectors in SF's settings flash before and after the clean erase (measured, 2026-10-27)"), ("2.44 V", "reset threshold the firmware is built with, against a 2.7 V flash minimum"),
         ("true", "what the firmware's 'is power safe to write?' check returns on ESP32, always"), ("1 build", "makes a revert restore OUR configuration instead of the factory's")]
pos = [(0.55, 3.9), (3.6, 3.9), (6.65, 3.9), (9.7, 3.9)]
for (big, small), (x, y) in zip(stats, pos):
    rect(s, x, y, 3.05, 2.1, CARD, RULE, 1.0)
    txt(s, x, y+0.15, 3.05, 0.8, big, 30, True, ACC, PP_ALIGN.CENTER, HF)
    txt(s, x+0.2, y+0.95, 2.65, 1.1, small, 11, False, BODY, PP_ALIGN.CENTER)
rect(s, 0.55, 6.2, 12.2, 0.42, INK)
txt(s, 0.8, 6.27, 11.7, 0.3, "THE MEMORY BORE THE SCAR AND HEALS WHEN REWRITTEN; THE POWER RAIL MADE IT; THE FIRMWARE MADE IT PERMANENT. ALL THREE ARE FIXABLE.", 11.5, True, PAPER, PP_ALIGN.CENTER, HF)
notes(s, "One sentence for the reviewer: the memory shows the scar, the power rail made it, the firmware made it permanent, and all three are fixable, in that order of effort.")

prs.save("Group9_ConfigLoss_RootCause.pptx")
import os
print("saved", os.path.getsize("Group9_ConfigLoss_RootCause.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))
