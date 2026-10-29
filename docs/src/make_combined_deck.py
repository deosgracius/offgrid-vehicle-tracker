# Group 9 combined presentation, REV E (4 November 2026): the REV D structure with the on-sheet text cut to
# what a listener can read while someone talks. The deep explanation lives in the notes and in the slide guide
# (docs/presentations/Group9_Presentation_SlideGuide.pdf). Run from docs/src.
# Presenters: Deo 6 sheets (the technical core), Victor, Josiah and Cannon 5 each.
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
DATE = "2026-11-04"; REV = "REV E"; A = "deck_assets/"

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
TOTAL = 21; sheet_no = [0]

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
    txt(s, 9.7, 6.94, 3.3, 0.32, "SHEET %02d/%02d  %s  %s" % (sheet_no[0], TOTAL, REV, DATE), 9, False, MUT, PP_ALIGN.RIGHT, MONO)
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
        p2 = tf.add_paragraph(); p2.space_before = Pt(5)
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
def table(s, x, y, w, rows, colw, hdr=True, fs=11, rh=0.42, firstbold=False):
    tb = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(rh*len(rows))).table
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tb.cell(i, j); c.text = ""
            p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = val
            r.font.size = Pt(fs); r.font.name = BF
            r.font.bold = (hdr and i == 0) or (firstbold and j == 0); r.font.color.rgb = PAPER if (hdr and i == 0) else BODY
            c.fill.solid(); c.fill.fore_color.rgb = INK if (hdr and i == 0) else (CARD if i % 2 else PAPER)
            c.margin_left = c.margin_right = Inches(0.08); c.margin_top = c.margin_bottom = Inches(0.03)
    for j, cw in enumerate(colw): tb.columns[j].width = Inches(cw)
    return tb
def pic(s, name, x, y, w): return s.shapes.add_picture(A + name, Inches(x), Inches(y), width=Inches(w))
def fail_sheet(owner, title, sub, rows, fig, caption, note):
    s = slide(); frame(s, "part i - the failures", owner)
    head(s, title, sub)
    table(s, 0.55, 1.35, 12.2, rows, [1.7, 3.1, 2.3, 2.5, 2.6], fs=11, rh=0.78, firstbold=True)
    pic(s, fig, 0.55, 4.7, 8.75)                       # 8.75 x 1.91
    card(s, 9.5, 4.7, 3.3, 1.91, "The figure", caption, INK, 12, 11)
    notes(s, note)

# ============ 1 TITLE ============
s = slide(); gridpaper(s); frame(s, "tests, failures, root cause", "CANNON")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHAT BROKE, AND WHAT IT TAUGHT US", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "THE TEST AND FAILURE RECORD, AND THE ONE FAILURE WE CHASED TO THE SILICON", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.3, "Part I: ten failures, each with the rule it left behind. Part II: the one that kept returning, traced to the flash cells, repaired, and fixed.", 14, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\n4 November 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Two parts, one arc: the record of what broke, then the deepest dive we made into the failure that kept returning. Introduce the team and hand to Josiah.")

# ============ 2 WHY FAILURES + THE CATALOG ============
s = slide(); frame(s, "part i - the failures", "JOSIAH")
head(s, "Why the failures are the deliverable")
pts = [("A failure is only useful once it has a signature", "Symptom as a stranger sees it, root cause, recovery."),
       ("Each failure produced a rule or a feature", "Pre-flight checks, the course-up compass, the config snapshot, LINK LOST."),
       ("Field equipment fails between outings", "Three failures hit the night before a test. All three cleared in time.")]
y = 1.35
for t1, t2 in pts:
    card(s, 0.55, y, 5.9, 1.55, t1, t2, INK, 13, 12.5); y += 1.7
txt(s, 6.7, 1.35, 6.1, 0.3, "ONE CATALOG ENTRY, TECHNICAL MANUAL SECTION 16", 11, True, ACC, PP_ALIGN.LEFT, MONO)
rows = [["Field", "Entry 1"],
        ["Symptom", "Total silence; configs read back identical; 0 % channel use"],
        ["Root cause", "Frequency slot mismatch: one channel write silently reverted"],
        ["Recovery", "Both OLEDs must read 912.875; re-apply channel, verify, power-cycle"],
        ["Rule", "Pre-flight: both OLEDs read 912.875 before any drive"]]
table(s, 6.7, 1.7, 6.1, rows, [1.25, 4.85], fs=11, rh=0.72, firstbold=True)
txt(s, 6.7, 5.5, 6.1, 0.8, "Eleven entries in this form, every one reproduced on this hardware.", 11.5, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
notes(s, "Set expectations: this is a verification record, not a list of embarrassments. Show the entry: symptom as a stranger would see it, root cause, recovery, rule. Three failures struck the night before a test and all three were cleared in time because the signature was already written down.")

# ============ 3 TIMELINE ============
s = slide(); frame(s, "part i - the failures", "CANNON")
head(s, "The semester on one line")
pic(s, "g_failtimeline.png", 0.55, 1.3, 12.2)
txt(s, 0.55, 6.45, 12.2, 0.35, "RED: FAILURES.  GREEN: TESTS.  HOLLOW TRIANGLE: NEW MEXICO, STOPPED BY A FLASH FLOOD WARNING.", 10.5, True, MUT, PP_ALIGN.CENTER, MONO)
notes(s, "Walk it left to right. Failures cluster right before tests, and the same villain, battery death, returns three times. The New Mexico weekend went into the radios instead, which is why Part II exists.")

# ============ 4 FAILURES 1-3 ============
fail_sheet("JOSIAH", "Failures 1-3: bring-up, August 30-31", "Cause, impact, fix, and what each one became",
    [["Failure", "Cause", "Impact", "Fix", "Became"],
     ["1  Display boot-loop", "Official platform cannot start this chip revision", "No display; a day lost", "pioarduino, dio_opi memory", "Rule: vendor IDF config is ground truth"],
     ["2  Bonded radio invisible", "A stored BLE bond stops the radio advertising", "Display cannot find the radio", "Just-Works pairing, no stored bond", "Feature: one-path BLE state machine"],
     ["3  PIN pairing refused (rc=1284)", "Radio wants a PIN typed; the display has no keypad", "No encrypted link, no GPS", "Radios run NO_PIN", "Signature: status 261 when a radio reverts"]],
    "g_bringup.png", "The display's start-up path and the three places it stopped on day one. rc=1284 is the Bluetooth stack's 'confirm value failed'.",
    "Day one, none of it in a datasheet. Failure 1: the espressif32 platform with Arduino core 2.x boot-loops this panel; pioarduino with dio_opi fixed it. Failure 2: a stored bond makes the Meshtastic radio stop advertising to everyone; we pair Just-Works on every connect and never store a bond. Failure 3: RANDOM_PIN mode needs a keypad; rc=1284 is NimBLE 0x500+4, confirm value failed on our side. NO_PIN is a stored setting, so when a radio reverts, the display log shows status 261, the signature of failures 8 and 10.")

# ============ 5 FAILURES 4-6 ============
fail_sheet("JOSIAH", "Failures 4-6: first drive, wrong flash, lying CLI", "September 1 to 3",
    [["Failure", "Cause", "Impact", "Fix", "Became"],
     ["4  First drive: five faults", "Precision 13 snaps positions to a 5.8 km cell; 120 s GPS; km/h on the wire; jitter; time zone", "Partner frozen, 4 min late, wrong speed, clock off", "Precision 32; 10 s GPS; km/h decode; deadband", "Rule: validate on the road, never on a desk"],
     ["5  Wrong board flashed", "Radios and displays share one USB ID; a tool picked the port", "Radio erased for an afternoon", "Erase, factory image, re-provision", "Rule: identify every board by MAC first"],
     ["6  Config write reverted", "Closing the CLI port resets the radio mid-save", "Write 'succeeds'; old value comes back", "Hold the port open; re-run the block", "Rule: read back every write; the OLED outranks the CLI"]],
    "g_precision.png", "How many of the 32 position bits the channel keeps. Default 13: a 5.8 km cell. Ours 32: the exact fix.",
    "Five faults, one drive, none visible on a desk. Why 6 km: 2 to the power (32-13) times 1e-7 degrees is 0.052 degrees, 5.8 km of latitude; the default exists for privacy on public meshes. GPS jitter: a parked receiver's fix wanders a few metres and is reported as 1 to 3 mph; the deadband ignores anything under 4.5 km/h. Failures 5 and 6 are tooling: identity and verification.")

# ============ 6 FAILURES 7-9 ============
fail_sheet("VICTOR", "Failures 7-9: silence, battery death, the compass", "September 25 to October 24",
    [["Failure", "Cause", "Impact", "Fix", "Became"],
     ["7  '0 online', same configs", "Frequency comes from the channel name; one write reverted, one radio moved slot", "Total silence with healthy screens", "Re-apply the channel; verify on the OLED", "Rule: both OLEDs read 912.875 before any drive"],
     ["8  Battery death reverts config  (Sep 30, Oct 17, Oct 24)", "Flat battery; the firmware overwrites unreadable settings with defaults", "Channel, key, role, PIN mode, name lost; SF three times", "Snapshot restored in 90 s; phone QR path", "Rule: never store a radio flat. Part II"],
     ["9  Hand-rotated compass", "North-up ring; staleness cue cried wolf", "Unreadable at night", "Course-up, clock positions; 30 s / 90 s staleness", "Feature: the honest display"]],
    "g_slots.png", "104 slots in the US band; the channel name picks the slot. A reverted radio moves to 906.875 while its partner stays on 912.875.",
    "Failure 7: slot = djb2(name) mod 104 = 43 for Group9, 902.125 + 43 x 0.25 = 912.875 MHz; the CLI reports what was written, the OLED what is radiating. Failure 8 is the hinge: three of four losses after a flat battery, partial and different each time; mitigations in October, root cause in Part II, do not pre-empt it. Failure 9 came from thirty seconds of night footage.")

# ============ 7 FAILURE 10 ============
s = slide(); frame(s, "part i - the failures", "JOSIAH")
head(s, "Failure 10: the night before the canyon (Oct 17)")
cards = [("Display 1 \"dead\"", "Power bank shut off; reflective screen in a dim room. Flashlight test first.", MUT),
         ("Display 2 half-dead USB-C", "Powers in one plug orientation only. Marked; a repair item.", ACC),
         ("Radio EA:D4 reverted", "A week idle, battery flat: PIN mode, channel and name gone. One log line named it.", RED)]
x = 0.55
for t1, t2, c in cards:
    card(s, x, 1.35, 4.0, 2.0, t1, t2, c, 13.5, 12.5); x += 4.18
codebox(s, 0.55, 3.6, 12.2, 1.85, "DISPLAY SERIAL LOG - THE SIGNATURE", [
    ("[ble] auth complete: encrypted=1 bonded=0", ICE),
    ("Write complete; status=261            <- insufficient authentication: radio not in NO_PIN", PINK),
    ("[ble] want_config write failed", ICE),
    ("[ble] disconnected (reason 534)       <- our side hung up, by design, to retry", ICE)])
txt(s, 0.55, 5.7, 12.2, 0.6, "Three faults, forty minutes, because each had a signature. The test ran the next morning.", 13, False, BODY)
notes(s, "Three independent faults in one evening. Display 1: power banks shut off under a milliwatt load. Display 2: damaged USB-C pins on one side. The radio: third battery revert, named by status 261 in one line. Diagnosed in forty minutes because every one had a written signature.")

# ============ 8 TESTS ============
s = slide(); frame(s, "part i - the tests", "CANNON")
head(s, "The test campaigns")
rows = [["Date", "Campaign", "Where", "Result"],
        ["Aug 31", "Bench, end-to-end", "Desk", "Live GPS radio to display"],
        ["Sep 1", "First drive", "Town", "Works at speed; five faults"],
        ["Sep 25", "Two-radio link", "Desk", "Traceroute 6.75 / 5.75 dB"],
        ["Oct 4", "Night convoy", "Town", "Stale at ~0.5 mi; course-up born"],
        ["Oct 5", "Open road", "Farm road", "Tracking to 3.26 mi; stale 3.75"],
        ["Oct 18", "Canyon", "Ceta Canyon", "Stale 1.29 mi; packet at 4.28; rim 4.7"],
        ["Oct 25", "Roof-top antenna, max range", "Capitan, NM", "On site; flash flood warning; rescheduled"]]
table(s, 0.55, 1.3, 5.9, rows, [0.75, 1.9, 1.15, 2.1], fs=10, rh=0.52)
pic(s, "g_onset4.png", 6.6, 1.3, 6.2)
txt(s, 6.6, 5.0, 6.2, 0.8, "Same radios, four terrains: 0.5 to 4.7 mi. Terrain and antenna height set the range.", 12.5, False, BODY)
notes(s, "Seven campaigns; each found what the previous one could not. Canyon: behind rock the link is intermittent at any distance; a seven-minute outage healed with one packet; the rim antenna held 4.7 mi. New Mexico: on site below the Capitan Mountains on the 25th, a National Weather Service flash flood warning stopped the roof-top antenna drive; rescheduled for the next clear weekend.")

# ============ 9 PART II: THE QUESTION ============
s = slide(); gridpaper(s); frame(s, "part ii - root cause", "VICTOR")
txt(s, 0.7, 0.5, 11.9, 0.5, "PART II", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=400)
txt(s, 0.7, 0.95, 11.9, 0.9, "WHY THE RADIOS FORGET", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.9, 11.9, 0.8, "A Qualcomm engineer asked: is it the memory itself? That can mean three things, each with its own fingerprint and its own fix. So we measured.", 14, False, BODY)
cards = [("Worn out", ["Cells exhausted by writes", "Looks like: scattered damage", "Fix: new part"], RED),
         ("Defective cells", ["Spots that cannot hold a value", "Looks like: fixed bad spots, stay bad", "Fix: avoid them"], ACC),
         ("Written under bad power", ["Healthy cells, supply sagged mid-write", "Looks like: fixed bad spots, heal when rewritten", "Fix: never write under low voltage"], GREEN)]
x = 0.55
for t, items, c in cards:
    card(s, x, 2.95, 4.0, 2.3, t, items, c, 13.5, 12.5); x += 4.1
card(s, 0.55, 5.45, 12.2, 1.1, "How we told them apart", "Read the chip with the firmware halted. Read the firmware source. Read the datasheets. Line up the four incidents.", INK, 12.5, 12.5)
notes(s, "Plain words: the settings are files on a 16 MB flash chip, in a 3.4 MB corner of it. Worn out would look like random damage everywhere. Defective would look like fixed bad spots that stay bad. Written under bad power would look like fixed bad spots that heal when rewritten. The rest of Part II collects exactly the data that separates those three.")

# ============ 10 STORAGE ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "How the radio stores its settings", "Read from SF and from the firmware source at v2.7.26")
pic(s, "g_storage.png", 0.55, 1.35, 8.9)
card(s, 9.65, 1.35, 3.15, 3.59, "In plain words", ["Six small files in LittleFS, a tiny file system for microcontrollers", "Every boot rewrites one file, with no voltage check", "A file that will not read is overwritten with factory settings"], ACC, 13, 11.5)
card(s, 0.55, 5.1, 6.0, 1.5, "What it checks", ["Temp file, read back, rename", "No write during its own low-battery shutdown"], GREEN, 13, 12)
card(s, 6.75, 5.1, 6.05, 1.5, "What it never checks", ["The supply before a save: the gate always returns true on ESP32", "Whether the save failed; the backup copy"], RED, 13, 12)
notes(s, "Red boxes in the figure are the policy weaknesses: the power gate that always returns true on ESP32 (weak default in PowerHAL.cpp, no override in src/platform/esp32), the one non-atomic file (nodes.proto), the ignored close() result, and the load-failure path in NodeDB.cpp that installs factory defaults and saves them with no retry and no backup consulted. The boot log shows device.proto re-saved on every boot. The one protection: the low-battery deep sleep skips the write, which proves the authors knew the danger. The damage happens in the reboot churn around a flat battery, not in the shutdown itself.")

# ============ 11 PHYSICS ============
s = slide(); frame(s, "part ii - root cause", "VICTOR")
head(s, "The physics: a 260 mV window", "Why a healthy chip can be left holding half-written cells")
pic(s, "g_voltage.png", 0.55, 1.35, 8.6)
card(s, 9.35, 1.35, 3.45, 3.33, "In plain words", ["The CPU runs down to 2.44 V", "The flash is only guaranteed above 2.70 V", "In between, the CPU writes and the flash promises nothing", "A transmit pulse on a flat cell puts the rail there"], ACC, 13, 11.5)
card(s, 0.55, 4.85, 12.25, 1.1, "A half-written cell", "Its charge sits at the read threshold: it reads 1 one time and 0 the next. Not damaged, never finished.", INK, 13, 12.5)
txt(s, 0.55, 6.15, 12.2, 0.45, "Boya BY25Q128AS (JEDEC 68 40 18): VCC 2.7 to 3.6 V, page 0.6 ms, erase 50 ms. Heltec V4 datasheet 3.2, 3.4. ESP-IDF brownout level 7.", 10, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "This sheet is the mechanism. Two chips share one supply line. The CPU keeps running down to 2.44 V, its brownout reset as the Arduino core is built. The flash is specified above 2.70 V and its datasheet says VCC must be held in range during all operations. A 27 dBm transmit draws about 750 mA; on a nearly flat cell the regulator cannot hold the rail through the pulse. A page program takes 0.6 ms, a sector erase 50 ms, and the firmware writes on every boot, so a write eventually lands in the dip. The 3.10 V deep-sleep trigger protects a slow discharge, not these fast dips. The rail excursion itself is the one link not yet measured; the scope capture closes it.")

# ============ 12 UPSTREAM ============
s = slide(); frame(s, "part ii - root cause", "CANNON")
head(s, "Upstream already knows", "meshtastic/firmware issue tracker on GitHub")
rows = [["Reference", "Boards", "Report", "Status"],
        ["#4555", "Heltec V3, V4", "Power loss in early boot resets configuration", "Closed 'not planned', Oct 2025"],
        ["#4622", "Heltec V3", "Resets when the battery is empty", "Duplicate of #4555"],
        ["#2936, #3260", "RAK4631, Heltec V2", "Defaults after the battery dies", "Older boards, same symptom"],
        ["#5259", "ESP32 boards", "3.10 V cutoff is below what the regulators need", "Open"],
        ["PR #11872", "nRF52 only", "Check the rail, retry saves, never format on a low rail", "Merged; no ESP32 version"]]
table(s, 0.55, 1.5, 12.2, rows, [1.7, 2.3, 5.2, 3.0], fs=11.5, rh=0.52)
codebox(s, 0.55, 4.75, 12.2, 1.45, "MAINTAINER, IN #4555", [
    ("\"If the brownout circuit worked, it should hold the CPU in reset when voltage is too low for flash.\"", ICE),
    ("Community workaround: compile the configuration in as the defaults. That is our fix 1.", MUT)], 11)
txt(s, 0.55, 6.3, 12.2, 0.4, "#4555 = issue 4555 at github.com/meshtastic/firmware/issues.  PR = pull request, a proposed code change.", 10, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "We are not the first. The same loss has been reported on these boards since 2023 and the maintainers' reading matches ours. The nRF52 boards received a fix in 2026; the ESP32 boards we run did not. The community workaround on the last line is what became our fix 1.")

# ============ 13 HYPOTHESES ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Hypotheses, predictions, verdicts", "Predictions written before the measurement")
rows = [["#", "Hypothesis", "Would show", "Verdict"],
        ["H1", "Worn out", "Scattered failures, write counts near 100k", "Rejected: millions of boots needed"],
        ["H2", "Defective cells", "Same sectors, fail again after a rewrite", "Rejected: rewritten sectors became perfect"],
        ["H3", "Written under low supply", "Same sectors, heal when rewritten", "Confirmed: measured, then repaired"],
        ["H4", "File-system bug", "Mount failures, broken directories", "Rejected: mounts and decodes cleanly"],
        ["H5", "Firmware turns a bad read into a reset", "Loss permanent and silent", "Confirmed in source"]]
table(s, 0.55, 1.5, 12.2, rows, [0.5, 2.8, 4.4, 4.5], fs=11.5, rh=0.6)
card(s, 0.55, 5.3, 12.2, 1.1, "The discriminating experiment", "H2 and H3 look identical until you erase and rewrite the sectors. That one test decided it.", GREEN, 13, 12.5)
notes(s, "Say the predictions first, then the data. H1: the firmware touches about 20 of 864 sectors per boot; reaching 100k cycles would take millions of boots. H2 and H3 both predict fixed unstable sectors; only the erase-and-reprogram test separates them. H4: the LittleFS image mounts and every file decodes on both radios. H5: verified in NodeDB.cpp.")

# ============ 14 METHOD ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Method: reading the chip, firmware stopped")
codebox(s, 0.55, 1.35, 7.4, 2.3, "ESPTOOL STUB, ONE CONNECTION, NO RESET BETWEEN READS", [
    ("esp = detect_chip('COM4'); esp = esp.run_stub()", ICE),
    ("A = esp.read_flash(0xC90000, 0x360000)   # settings, 3.4 MB", ICE),
    ("B = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("C = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("app = esp.read_flash(0x10000, 0x100000) x2   # control", MUT),
    ("A == B ?   B == C ?   app1 == app2 ?", ACC)], 11)
card(s, 8.15, 1.35, 4.65, 2.3, "Controls", ["1 MB of program code, twice", "NVS and bootloader, twice", "Two serial speeds", "Image mounted, every file decoded"], GREEN, 13, 12)
card(s, 0.55, 3.85, 12.25, 1.1, "In plain words", "Read the settings area three times through one connection and compare. A healthy chip returns the same bytes every time. If the control changed too, the method would be at fault.", ACC, 13, 12.5)
card(s, 0.55, 5.15, 7.4, 1.45, "The pitfall", ["This board resets when the USB port closes", "Separate commands hide a boot, and a boot-time write, between reads"], MUT, 12.5, 11.5)
card(s, 8.15, 5.15, 4.65, 1.45, "How this was done", "Hypothesis: a Qualcomm engineer. Design, scripts, analysis: drafted with Claude as an AI assistant. Every measurement: run and checked by us. Records: sheet 20.", INK, 12.5, 11)
notes(s, "esptool loads a stub into RAM and takes over; the firmware is not running. Every chunk is MD5-checked, so a transfer error raises and a changed byte is what the chip returned. The pitfall cost two attempts and is itself evidence that the radio writes flash every time it starts. The LittleFS image also proved the configuration in flash on measurement day was correct. Attribution if asked: the recruiter supplied the hypothesis, the AI the experimental design and the code, the team the hardware, the authorisation of each destructive step and the checking; scripts and records are in the repository and the measurement repeats in four minutes without the AI.")

# ============ 15 RESULT MAPS ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Result: the same sectors misread, every pass", "SF against RG, same day, same method")
pic(s, "g_maps_compare.png", 0.55, 1.35, 12.2)
txt(s, 0.55, 4.95, 12.2, 0.6, "Each square is one 4 KB sector. Red: different bytes on every read, with nothing running. Green: the live settings files.", 12.5, False, BODY)
stat(s, 0.55, 5.65, 3.95, 1.0, "21", "unstable sectors on SF, 12 heavily", RED, 20)
stat(s, 4.675, 5.65, 3.95, 1.0, "0", "unstable sectors on RG", GREEN, 20)
stat(s, 8.8, 5.65, 3.95, 1.0, "0", "differences in program code, NVS, bootloader", GREEN, 20)
notes(s, "SF: 117 and 107 differing bytes between consecutive reads, 118 bits flipped in both directions, none inside erased areas, confined to 21 sectors with 12 carrying almost all of it. RG: zero. The live files on SF sat in clean sectors 25, 26 and 470 that day, which is why the radio was working; wear-levelling would have moved them onto the bad ones eventually. Plain words: the chip was asked the same question three times and gave different answers in the same 21 places; the control gave the same answer every time.")

# ============ 16 NUMBERS, DECISIVE TEST, REPAIR ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "The decisive test, and the repair", "SF, 27 October")
stat(s, 0.55, 1.35, 2.9, 1.15, "117 / 107", "differing bytes between reads", ACC, 20)
stat(s, 3.65, 1.35, 2.9, 1.15, "118", "bits flipped, both directions", ACC, 20)
stat(s, 6.75, 1.35, 2.9, 1.15, "0", "differences in the controls", GREEN, 20)
stat(s, 9.85, 1.35, 2.95, 1.15, "21 -> 0", "unstable sectors after the repair", GREEN, 20)
txt(s, 0.55, 2.7, 7.4, 0.3, "ERASE, PROGRAM THREE PATTERNS, READ FIVE TIMES EACH (FREE SECTORS ONLY)", 9.5, True, ACC, PP_ALIGN.LEFT, MONO)
rows = [["Sector", "As found", "0x00 x5", "A5/5A x5", "random x5", "Erased x5"],
        ["57 (worst)", "27 bytes disagree", "clean", "clean", "clean", "clean"],
        ["31", "20 bytes disagree", "clean", "clean", "clean", "clean"],
        ["200 (control)", "stable", "clean", "clean", "clean", "clean"]]
table(s, 0.55, 3.0, 7.4, rows, [1.4, 1.6, 1.1, 1.1, 1.1, 1.1], fs=11, rh=0.42)
card(s, 8.15, 2.7, 4.65, 2.0, "Verdict: disturbed, not damaged", "0 mismatches in 45 reads. The cells are sound; they were written at the wrong moment.", GREEN, 13, 12)
card(s, 0.55, 4.9, 7.4, 1.7, "The repair, same day", ["Erase the settings area on USB power", "Snapshot applied twice (the region write reboots the radio)", "Three reads after: 0 differing bytes"], INK, 13, 12)
card(s, 8.15, 4.9, 4.65, 1.7, "In plain words", "Rewriting the bad spots on good power made them perfect. Worn or defective memory would have failed again.", ACC, 13, 12)
notes(s, "Numbers: fixed sectors, both bit directions, speed-independent, code partition stable: cells whose stored charge sits at the read threshold. Decisive test on sectors 57 and 31, free in LittleFS, so nothing was lost; sector 200 was the control. Zero mismatches in 45 reads: H2 falls, H3 stands. Repair: erase 0xC90000 to 0xFF0000 on USB, the first boot formats and installs defaults, --configure twice because the region write reboots mid-transaction (now User Guide 12.2), read back, reset, read back, three reads: 0 differing bytes; node key pair preserved. Thirty minutes end to end.")

# ============ 17 NOW ============
s = slide(); frame(s, "part ii - root cause", "VICTOR")
head(s, "Now: two days later, both radios clean", "Measured again on 29 October, after SF sat two days at 0 % battery")
pic(s, "g_now.png", 0.55, 1.35, 12.2)
card(s, 0.55, 4.85, 6.0, 1.75, "Checked on 29 October", ["All settings intact on both radios, zero provisioning", "Flash: 0 differing bytes, 0 unstable sectors, both radios"], GREEN, 13, 12)
card(s, 6.75, 4.85, 6.05, 1.75, "Read it honestly", ["The condition that wiped SF three times; this time nothing lost", "One cycle is evidence, not proof: stored flat, not running flat"], ACC, 13, 12)
notes(s, "This is the state today. The red bar is SF as found on the 27th; everything after it is zero, including SF after two days at zero percent battery on the new firmware; it reconnected at 18 percent and 3.40 V. Be honest: the radio was stored flat, not transmitting while it died, so the dangerous write may not have happened this time. Fix 1 makes a revert harmless; it does not remove the cause. The five running-flat cycles per radio, flash map read after each, are what prove it.")

# ============ 18 CHAIN ============
s = slide(); frame(s, "part ii - root cause", "VICTOR")
head(s, "The chain of causation", "Every link tagged with its class of evidence")
pic(s, "g_chain.png", 0.55, 1.4, 12.2)
rows = [["Link", "Evidence", "Class"],
        ["Flat battery, reboot churn on recovery", "3 of 4 incidents; issue 4555", "Observed"],
        ["Flash write on every boot, no voltage gate", "Boot log; PowerHAL.cpp", "Verified in source"],
        ["Rail between 2.44 and 2.7 V during a write", "Datasheets; 750 mA transmit pulses", "Inferred: scope pending"],
        ["Cells left half-written", "SF sector map; healed by rewrite", "Measured"],
        ["Bad read becomes factory defaults", "NodeDB.cpp; the losses themselves", "Verified in source"]]
table(s, 0.55, 4.1, 12.2, rows, [4.3, 4.6, 3.3], fs=11.5, rh=0.42)
notes(s, "Read the chain left to right: the battery goes flat; on recovery the radio boots and reboots; every boot writes a settings file with no check of the supply; the supply is sagging where the CPU runs but the flash is not guaranteed; cells are left half-written; next boot a file will not decode and the firmware installs factory defaults. One link is inferred rather than measured, the rail voltage during the event; an oscilloscope on the 3V3 pin during a transmit burst at 3.4 V cell voltage closes it, and we say so.")

# ============ 19 THE FIX ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "The fix: plan and proof", "Ranked by leverage")
rows = [["#", "Fix", "Effect", "Status"],
        ["1", "Our configuration compiled in as the factory defaults", "A revert restores OUR settings", "Both radios, Oct 28; SF clean after 2 days flat"],
        ["2", "Power gate: no saves below 3.5 V on battery; no boot-time write", "Removes the dangerous write", "Next; to offer upstream"],
        ["3", "Clean erase of a scarred settings area", "Removes residue", "Done on SF; RG clean"],
        ["4", "Raise the brownout reset to 2.67 or 2.84 V", "CPU resets before the flash leaves spec", "Planned"],
        ["5", "Never store flat; OLED pre-flight; snapshots; phone QR", "Detect in 2 s, recover in 90 s", "In force"]]
table(s, 0.55, 1.35, 12.2, rows, [0.4, 5.0, 3.5, 3.3], fs=11.5, rh=0.52)
card(s, 0.55, 4.6, 6.0, 2.0, "Fix 1 in plain words", "The radio's factory settings are now OUR settings: Group9 at 912.875, No PIN, SF or RG. When the firmware falls back to defaults, the defaults are right.", GREEN, 13, 12.5)
card(s, 6.75, 4.6, 6.05, 2.0, "Proven", ["Factory reset on each radio: came back fully configured, nobody touching it", "Next: five running-flat cycles per radio; scope on the 3V3 rail"], INK, 13, 12.5)
notes(s, "Fix 1 is the community's own answer to issue 4555: Meshtastic rebuilt from source with a userPrefs.jsonc naming channel, key, precision, region, preset, owner names, role and cadence, plus a one-line patch for default No PIN. The key is compiled into a binary that never leaves the private repository. Acceptance on 28 October: flash, --factory-reset, read back with zero provisioning; SF came back as SF and RG as RG on Group9 with the key. The snapshot restores the smart-broadcast minimums, the 21 presets and the original key pair. Fix 2 removes the cause, fix 3 cleans the past, fix 4 is the hardware-correct answer. The ask: approve the flat-battery campaign before the next drive.")

# ============ 20 REFERENCES AND ATTRIBUTION ============
s = slide(); frame(s, "part ii - root cause", "CANNON")
head(s, "References, records and attribution")
rows = [["Source", "Used for"],
        ["Heltec WiFi LoRa 32 V4 datasheet V4.2.0  (resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf)", "Rails, battery path, transmit current"],
        ["Boya BY25Q128AS datasheet, the flash on the V4", "2.7 to 3.6 V, timing, endurance"],
        ["ESP-IDF Kconfig; Arduino-ESP32 sdkconfig", "Brownout level 7 = 2.44 V"],
        ["meshtastic/firmware v2.7.26: NodeDB, SafeFile, PowerHAL, PowerFSM, sleep", "Save and load behaviour"],
        ["github.com/meshtastic/firmware issues 4555, 4622, 2936, 3260, 5259; PR 11872", "Prior reports; the nRF52 fix"],
        ["esptool 4.11; python-pptx; matplotlib", "Reading flash; this deck"],
        ["This repository: docs/src/flash_forensics, docs/src/*.py, Manual 15-16, Guide 12", "Every number here, reproducible"]]
table(s, 0.55, 1.35, 7.9, rows, [5.4, 2.5], fs=10, rh=0.6)
card(s, 8.65, 1.35, 4.15, 4.8, "How this work was done", ["Hypothesis: a Qualcomm engineer, October 2026", "Experiment design, scripts and analysis: drafted with Claude (Anthropic) as an AI assistant", "Every measurement run, authorised and checked by the team on our radios", "Scripts and records in the repository: repeatable without the AI"], INK, 13, 12)
notes(s, "Attribution policy: say exactly who supplied what. Hypothesis: the recruiter. Experimental design, code and analysis: the AI assistant, under the team's direction. Hardware, authorisation and checking: the team. Reproducibility: the repository; the sector map re-runs on either radio in four minutes.")

# ============ 21 CLOSE ============
s = slide(); frame(s, "close", "JOSIAH")
head(s, "The answer, and what the failures bought")
card(s, 0.55, 1.45, 12.2, 1.45, "Is it the memory itself?", "Measurably, on one radio, and not as the question implies: the chip is healthy, it was written at the wrong moment. The firmware never checks for that, and then punishes it with factory defaults.", INK, 15, 13.5)
stats = [("10", "root-caused failures, each with a signature and a recovery"), ("21 -> 0", "unstable flash sectors on SF; RG clean"),
         ("0", "reflashes ever needed for a configuration failure"), ("90 s", "to recover a reverted radio; 2 s to detect one"),
         ("4.7 mi", "measured reach; 0.5 to 4.7 mi by terrain"), ("1 build", "makes a future revert restore OUR settings; proven on both radios")]
pos = [(0.55, 3.15), (4.65, 3.15), (8.75, 3.15), (0.55, 4.65), (4.65, 4.65), (8.75, 4.65)]
for (big, small), (x, y) in zip(stats, pos):
    stat(s, x, y, 4.0, 1.35, big, small, ACC, 24)
rect(s, 0.55, 6.2, 12.2, 0.42, INK)
txt(s, 0.8, 6.26, 11.7, 0.3, "EVERY FAILURE BECAME A RULE; THE WORST ONE BECAME A MEASUREMENT, A REPAIR, AND A FIX.", 11.5, True, PAPER, PP_ALIGN.CENTER, HF)
notes(s, "Close on the bar. Then the ask: fix 1 is proven on both radios; approve the flat-battery campaign before the next field test.")

assert sheet_no[0] == TOTAL, sheet_no[0]
prs.save("../presentations/Group9_Presentation.pptx")
import os
print("saved", os.path.getsize("../presentations/Group9_Presentation.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))
