# Group 9 combined presentation, REV D (2026-10-28): Part I tests and failures (three table sheets),
# Part II root cause explained in plain words, one fix sheet, references and attribution, one close.
# Run from docs/src:  python make_combined_deck.py   -> ../presentations/Group9_Presentation.pptx
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
DATE = "2026-11-04"; REV = "REV D"; A = "deck_assets/"

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
    table(s, 0.55, 1.35, 12.2, rows, [1.55, 3.25, 2.3, 2.5, 2.6], fs=10, rh=0.8, firstbold=True)
    pic(s, fig, 0.55, 4.75, 8.75)                       # 8.75 x 1.91
    card(s, 9.5, 4.75, 3.3, 1.91, "Reading the figure", caption, INK, 12, 10.5)
    notes(s, note)

# ============ 1 TITLE ============
s = slide(); gridpaper(s); frame(s, "tests, failures, root cause")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHAT BROKE, AND WHAT IT TAUGHT US", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "THE TEST AND FAILURE RECORD, AND THE ONE FAILURE WE CHASED TO THE SILICON", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.3, "Part I: ten root-caused failures and seven test campaigns, each with the rule or feature it left behind. Part II: the battery-death configuration loss, investigated to the flash cells with measurements on both radios, repaired, and fixed at the root.", 13, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\n4 November 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Two parts, one arc: the record of what broke, then the deepest dive we made into the failure that kept returning.")

# ============ 2 WHY FAILURES + THE CATALOG ============
s = slide(); frame(s, "part i - the failures", "JOSIAH")
head(s, "Why the failures are the deliverable")
pts = [("A failure is only useful once it has a signature", "Each catalog entry records the symptom exactly as it appears, the root cause, and the recovery, so the next person recognizes it in minutes, not days."),
       ("Each failure produced a rule or a feature", "Pre-flight checks, cadence-aware alarms, the course-up compass, the config snapshot, the LINK LOST alarm: none were in the plan. All came from something breaking."),
       ("Field equipment fails between outings", "Three of ten failures struck the night before a test. Every one was cleared in time because its signature had already been written down.")]
y = 1.35
for t1, t2 in pts:
    card(s, 0.55, y, 5.9, 1.62, t1, t2, INK, 13, 12); y += 1.75
txt(s, 6.7, 1.35, 6.1, 0.3, "WHAT ONE CATALOG ENTRY LOOKS LIKE", 11, True, ACC, PP_ALIGN.LEFT, MONO)
rows = [["Field", "Entry 1, Technical Manual Section 16"],
        ["Symptom", "Total mutual silence; configs read back identical; 0 percent channel utilization"],
        ["Root cause", "Frequency-slot mismatch: a channel write silently reverted, leaving the radios on different slots with the same key"],
        ["Recovery", "Check both OLED LoRa screens: Group9 must read 912.875. Re-apply the channel URL, verify, power-cycle, verify again"],
        ["Rule it left", "Pre-flight: both OLEDs read 912.875 before any drive"]]
table(s, 6.7, 1.7, 6.1, rows, [1.25, 4.85], fs=10.5, rh=0.78, firstbold=True)
txt(s, 6.7, 5.75, 6.1, 0.8, "Eleven entries in this form. Every one happened on this hardware and was reproduced or root-caused before being written down. The catalog is the part of the project a stranger could use tomorrow.", 11, False, MUT, PP_ALIGN.LEFT, BF, italic=True)
notes(s, "Set expectations: this is not a list of embarrassments, it is the verification record of a system that is honest about itself. Show the entry on the right: symptom as a stranger would see it, root cause, recovery, and the rule. Ten failures in this deck, each in that form.")

# ============ 3 TIMELINE ============
s = slide(); frame(s, "part i - the failures", "CANNON")
head(s, "The semester on one line")
pic(s, "g_failtimeline.png", 0.55, 1.3, 12.2)
txt(s, 0.55, 6.45, 12.2, 0.35, "RED: FAILURES, ROOT-CAUSED.  GREEN: TESTS.  THE HOLLOW TRIANGLE IS NEW MEXICO: ON SITE, STOPPED BY A FLASH FLOOD WARNING; THE WEEKEND WENT INTO THE RADIOS.", 10.5, True, MUT, PP_ALIGN.CENTER, MONO)
notes(s, "Walk it left to right. Failures cluster right before tests, and the same villain, battery death, returns three times. The last weekend's drive was rained out, which is why Part II exists.")

# ============ 4 FAILURES 1-3 ============
fail_sheet("DEO", "Failures 1-3: bring-up, August 30-31", "Causation, impact, fix, and what each one became",
    [["Failure", "Cause", "Impact", "Fix", "Became"],
     ["1  Display boot-looped silently", "The official espressif32 platform (Arduino core 2.x) cannot start this panel's chip revision", "No display at all; one full day lost finding it", "pioarduino platform, dio_opi memory, dio flash mode", "Rule: the vendor's ESP-IDF config is ground truth (platformio.ini, manual 14)"],
     ["2  Bonded radio goes invisible", "A stored BLE bond makes the Meshtastic radio stop advertising, even to its own peer", "Display cannot find the radio; factory reset was the only cure", "Pair Just-Works on every connect; never store a bond; never deleteAllBonds() at boot", "Feature: one-path BLE state machine, any failure tears down to SCANNING (ble_link.cpp, manual 8)"],
     ["3  PIN pairing refused (rc=1284)", "Radio default RANDOM_PIN needs a keypad to type the PIN; the display has none, so the pairing confirm values never match", "Encrypted link never forms: no config, no GPS", "Radios provisioned with bluetooth.mode NO_PIN", "Signature: NO_PIN reverting is how failures 8 and 10 announce themselves (status 261)"]],
    "g_bringup.png", "The display's start-up path. Each red dot is where day one stopped; the green line under it is the fix. rc=1284 is the Bluetooth stack's 'confirm value failed' code: the two sides computed different pairing confirms because one had a PIN and the other could not enter it.",
    "Day one. None of these were in any datasheet. The boot-loop alone cost a day and taught us to trust the vendor's ESP-IDF config over its Arduino screenshot. Failure 3 matters later: NO_PIN is a provisioned setting, so when the radio's configuration reverts, the display's log shows 'status 261, insufficient authentication' and that line is the signature of failures 8 and 10.")

# ============ 5 FAILURES 4-6 ============
fail_sheet("JOSIAH", "Failures 4-6: first drive, wrong flash, lying CLI", "September 1 to 3: five faults on one drive, then two tooling failures on the bench",
    [["Failure", "Cause", "Impact", "Fix", "Became"],
     ["4  First drive: five faults", "Channel precision 13 snaps every position to a 5.8 km cell; GPS refresh 120 s; speed sent in km/h; GPS jitter read as speed; wrong time-zone line", "Partner frozen on a grid, 4 min late, wrong speed, parked car 'moving', clock an hour off", "Precision 32; GPS 10 s; km/h decode; 4.5 km/h deadband; time-zone bands to the NM border", "Rule: validate every feature on the road, never on a windowsill (provisioning recipe, node_table.cpp)"],
     ["5  Display firmware flashed onto a radio", "Radios and displays share USB ID 303A:1001; a tool auto-picked the port", "Meshtastic erased; radio out for an afternoon; full re-provision", "esptool erase, factory image, re-provision (node number survives: MAC-derived)", "Rule: identify every board by its MAC before any upload; never let a tool pick the port (manual 14.2)"],
     ["6  Config write silently reverted", "Closing the CLI's serial port toggles DTR/RTS and resets the ESP32 mid-save", "Write 'succeeds'; the next read shows the old value; nothing on screen changes", "Hold the port open (Python API); re-run the whole block", "Rule: read back every write; the OLED outranks the CLI (manual 16, entry 6)"]],
    "g_precision.png", "Meshtastic sends latitude and longitude as 32-bit numbers and the channel's precision setting says how many of those bits to keep. The default keeps 13: every broadcast lands on the centre of a 5.8 km cell, so a moving partner looks frozen. We keep all 32.",
    "Five faults, one drive, every one invisible on the bench: that is why we drove six more times. The figure answers 'why 6 km': 2 to the power (32-13) times 1e-7 degrees is 0.052 degrees, 5.8 km of latitude. GPS jitter: a parked receiver's fix wanders a few metres between fixes, and the receiver reports that wander as 1 to 3 mph; the deadband ignores anything under 4.5 km/h. Failures 5 and 6 are tooling: identity and verification.")

# ============ 6 FAILURES 7-9 ============
fail_sheet("VICTOR", "Failures 7-9: silence, battery death, the compass", "September 25 to October 24: the name sets the frequency, the flash holds the configuration, the compass sits in the driver's hands",
    [["Failure", "Cause", "Impact", "Fix", "Became"],
     ["7  '0 online', same configs", "The frequency is a hash of the channel name. One channel write reverted, so one radio sat on the public slot (906.875 MHz), the other on Group9's (912.875)", "Total mutual silence with healthy screens and identical config read-backs; a day of RF debugging", "Re-apply the channel, verify on the OLED, power-cycle, verify again", "Rule: pre-flight, both OLEDs read 912.875 before any drive (guide 3, manual 7)"],
     ["8  Battery death reverts config  (Sep 30 both; Oct 17 SF; Oct 24 SF)", "Flat battery, then boot-time flash writes on a sagging rail; the firmware installs factory defaults when a settings file will not read", "Channel, key, role, Bluetooth, owner, cadence lost in varying combinations; three times on SF, once on RG", "Snapshot per radio restored with --configure (90 s); phone-app QR path when no laptop is at hand", "Rule: never store a radio flat. Root cause, repair and fix: Part II"],
     ["9  Hand-rotated compass (Oct 4)", "North-up ring: the driver turned the unit to read it; the staleness cue alarmed after 59 s of a parked partner's normal silence", "Unreadable at night; a cue that cried wolf", "Course-up compass, nose at 12 o'clock, clock positions; staleness 30 s moving, 90 s parked", "Feature: the honest display. A cue that cries wolf is as wrong as one that stays silent (ui_render.cpp, manual 9)"]],
    "g_slots.png", "The US band is cut into 104 slots and Meshtastic picks the slot from a hash of the channel name. A radio that reverts to the default name moves to 906.875 MHz while its partner stays on 912.875: same key, no contact. The OLED shows the real slot; the CLI only shows the intended one.",
    "Failure 7 is the project's idea 2: the name IS the frequency. The debug ladder was config diff, matched-power tests, traceroute, regression on the default channel, then the hash math. Failure 8 is the hinge of the deck: state the pattern (three of four losses after a flat battery, SF three times, partial and different each time) and the mitigation, but do not pre-empt Part II. Failure 9 came from thirty seconds of night footage.")

# ============ 7 FAILURE 10 ============
s = slide(); frame(s, "part i - the failures", "JOSIAH")
head(s, "Failure 10: the night before the canyon (Oct 17)")
cards = [("Display 1 \"dead\"", "Actually fine. Power banks shut off under the display's milliwatt draw, and a reflective screen in a dim room reads as off. Flashlight test first.", MUT),
         ("Display 2 half-dead USB-C", "Powers in ONE plug orientation - damaged pins on one side. A coin-flip failure on every plug-in. Marked the working orientation; a repair item.", ACC),
         ("Radio EA:D4 reverted", "A week idle, battery flat: Bluetooth mode, channel and name gone. The display's serial log named it in one line: write status 261, insufficient authentication.", RED)]
x = 0.55
for t1, t2, c in cards:
    card(s, x, 1.35, 4.0, 2.2, t1, t2, c, 13.5, 12.5); x += 4.18
codebox(s, 0.55, 3.8, 12.2, 1.85, "DISPLAY SERIAL LOG - THE SIGNATURE", [
    ("[ble] auth complete: encrypted=1 bonded=0", ICE),
    ("Write complete; status=261            <- insufficient authentication: radio not in NO_PIN", PINK),
    ("[ble] want_config write failed", ICE),
    ("[ble] disconnected (reason 534)       <- our side hung up, by design, to retry", ICE)])
notes(s, "Three independent faults in one evening, diagnosed in forty minutes because every one had a written signature. The test ran the next morning.")

# ============ 8 TESTS ============
s = slide(); frame(s, "part i - the tests", "CANNON")
head(s, "The test campaigns")
rows = [["Date", "Campaign", "Environment", "Key result"],
        ["Aug 31", "Bench, end-to-end", "Desk", "Live GPS decoded radio-to-display"],
        ["Sep 1", "First drive", "Town", "Pipeline works at speed; five faults found"],
        ["Sep 25", "Two-radio link", "Desk", "Round-trip traceroute 6.75 / 5.75 dB"],
        ["Oct 4", "Night convoy drive", "Town", "Stale onset ~0.5 mi; course-up and cadence-aware cue born"],
        ["Oct 5", "Open-road range", "Flat farm road", "Full tracking to 3.26 mi; stale edge 3.75 mi"],
        ["Oct 18", "Canyon range", "Ceta Canyon", "Stale from 1.29 mi; packet at 4.28; 7-min outage healed; rim antenna 4.7 mi"],
        ["Oct 25", "New Mexico maximum range", "Capitan Mountains, NM", "On site; flash flood warning, cancelled; the radios were diagnosed instead (Part II)"]]
table(s, 0.55, 1.3, 5.9, rows, [0.75, 1.55, 1.2, 2.4], fs=9.5, rh=0.52)
pic(s, "g_onset4.png", 6.6, 1.3, 6.2)
txt(s, 6.6, 5.0, 6.2, 0.8, "Same radios, four geometries: 0.5 to 4.7 mi. Terrain and antenna height set the range, not the hardware.", 12, False, BODY)
notes(s, "Seven campaigns; each found what the previous one could not. Ceta Canyon: behind rock the link is intermittent at any distance; the seven-minute outage healed with one packet and no operator action; the rim antenna held 4.7 mi, the quantitative case for a repeater.")

# ============ 9 PART II: THE QUESTION ============
s = slide(); gridpaper(s); frame(s, "part ii - root cause", "VICTOR")
txt(s, 0.7, 0.5, 11.9, 0.5, "PART II", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=400)
txt(s, 0.7, 0.95, 11.9, 0.9, "WHY THE RADIOS FORGET", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.85, 11.9, 0.95, "In October a Qualcomm engineer asked us: is it the memory itself? 'The memory' is a 16 MB flash chip beside the CPU, and the settings live in a 3.4 MB corner of it. The question can mean three different things. Each leaves a different fingerprint in the data and needs a different fix, so we treated it as a hypothesis to test, not an opinion to argue with.", 12.5, False, BODY)
cards = [("Worn out", ["Cells exhausted by write volume (100k cycles)", "Fingerprint: scattered failures over many sectors", "Fix: replace the part"], RED),
         ("Defective or marginal cells", ["Specific cells that cannot hold a value", "Fingerprint: the same sectors misread, and fail again after being rewritten", "Fix: avoid those sectors"], ACC),
         ("Corrupted by the conditions of a write", ["Healthy cells written while the supply was out of spec", "Fingerprint: follows power events; heals once rewritten", "Fix: never write under low voltage"], GREEN)]
x = 0.55
for t, items, c in cards:
    card(s, x, 2.95, 4.0, 2.3, t, items, c, 13, 11.5); x += 4.1
card(s, 0.55, 5.45, 12.2, 1.15, "How we told them apart", "Read the settings area straight off the chip three times with the firmware halted; read the firmware's save and load code at the exact version we run; read the flash and board datasheets and the brownout level the firmware is built with; line up the four incidents (Sep 3, Sep 30, Oct 17, Oct 24) against all of it.", INK, 12.5, 11.5)
notes(s, "Plain words for the room: the radio's settings are files on a flash chip. Three things could be wrong with that chip. Worn out would look like random damage everywhere. Defective would look like fixed bad spots that stay bad. Written under bad power would look like fixed bad spots that heal when rewritten. The rest of Part II collects exactly the data that separates those three.")

# ============ 10 STORAGE (+ what the firmware checks) ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "How the radio stores its settings", "Partition table and file sizes read from SF; save and load behaviour from meshtastic/firmware v2.7.26")
pic(s, "g_storage.png", 0.55, 1.35, 8.9)                                  # 8.9 x 3.59
card(s, 9.65, 1.35, 3.15, 3.59, "In plain words", ["Six small files hold everything: channel, config, device, modules, node list, presets", "LittleFS is the tiny file system that keeps them; it survives power loss only if the chip itself writes correctly", "Every boot the firmware rewrites one file (device.proto) without checking the supply voltage", "If a file will not read, the firmware does not retry or ask: it writes factory settings over it"], ACC, 12.5, 10.5)
card(s, 0.55, 5.1, 6.0, 1.55, "What it checks", ["Writes a temp file, reads it back, then renames it (SafeFile.cpp)", "Skips the write during its own low-battery shutdown; the authors knew the danger", "The CPU resets below 2.44 V"], GREEN, 12.5, 11)
card(s, 6.75, 5.1, 6.05, 1.55, "What it never checks", ["The supply before an ordinary save: powerHAL_isPowerLevelSafe() returns true on ESP32, always", "Whether a save actually failed: the result is discarded", "The backup copy at boot: it is only used on operator command"], RED, 12.5, 11)
notes(s, "Red boxes in the figure are the policy weaknesses in the vendor's code: the power gate that always returns true on ESP32, the one non-atomic file, the ignored close() result, and the load-failure path that installs factory defaults and saves them. The green line is the one protection that exists: the low-battery deep sleep skips the write. Sources at tag v2.7.26: NodeDB.cpp, SafeFile.cpp, PowerHAL.cpp, PowerFSM.cpp, sleep.cpp. The asymmetry to say out loud: the firmware refuses to write during its own low-battery shutdown, which proves the authors knew the danger, but it has no voltage check on the ordinary save path, and that path runs on every boot.")

# ============ 11 PHYSICS ============
s = slide(); frame(s, "part ii - root cause", "VICTOR")
head(s, "The physics: a 260 mV window", "Why a healthy chip can still be left holding half-written cells")
pic(s, "g_voltage.png", 0.55, 1.35, 8.6)                                   # 8.6 x 3.33
card(s, 9.35, 1.35, 3.45, 3.33, "In plain words", ["The CPU keeps running down to 2.44 V, its brownout reset", "The flash chip is only guaranteed to store data above 2.70 V", "Between the two, 260 mV, the CPU is alive and can order a write, but the chip may not finish it", "A 750 mA transmit pulse on a nearly flat cell can drag the rail through that window and back"], ACC, 12.5, 10.5)
card(s, 0.55, 4.85, 12.25, 1.2, "What a half-written cell does", "A flash cell stores a small charge; reading it compares that charge with a threshold. A write cut short by low voltage leaves the charge near the threshold, so the same cell reads 1 on one pass and 0 on the next. That is the fingerprint the measurement on sheet 15 looks for, and it is what the firmware then punishes with factory defaults.", INK, 12.5, 11.5)
txt(s, 0.55, 6.2, 12.2, 0.45, "Boya BY25Q128AS (JEDEC 68 40 18, read from the chip): VCC 2.7 to 3.6 V, page program 0.6 ms, sector erase 50 ms, 100k cycles. Heltec V4 datasheet V4.2.0, tables 3.2 and 3.4. ESP-IDF Kconfig for ESP32-S3.", 10, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "What this sheet achieves: it is the mechanism. The memory can be perfectly good and still end up holding garbage, because the chip that orders the write (the CPU) stays awake 260 mV below the point where the chip that stores the data (the flash) is guaranteed to work. A sector erase takes 50 ms; a transmit pulse on a nearly flat battery can pull the rail through 2.7 V and back inside that time without ever reaching the 2.44 V reset. The datasheet says VCC must be held in range during all operations; between 2.44 and 2.7 V the write proceeds and the result is undefined.")

# ============ 12 UPSTREAM ============
s = slide(); frame(s, "part ii - root cause", "CANNON")
head(s, "Upstream already knows", "meshtastic/firmware issue tracker on GitHub")
rows = [["Reference", "Boards", "Report", "Status"],
        ["#4555", "Heltec HT-CT62, V3, V4", "Power loss in early boot resets configuration after 2 to 3 attempts", "Closed 'not planned' Oct 2025"],
        ["#4622", "Heltec V3", "Resets when the battery is empty", "Duplicate of #4555"],
        ["#2936, #3260", "RAK4631, Heltec V2", "Defaults after the battery dies; prefs files missing", "Older platform, same symptom"],
        ["#5259", "ESP32 boards", "3.10 V low-battery cutoff is below what the LDOs need", "Open"],
        ["PR #11872", "nRF52 only", "Retry saves, check the rail first, stop formatting on a low rail", "Merged; no ESP32 equivalent"]]
table(s, 0.55, 1.5, 12.2, rows, [1.7, 2.5, 5.2, 2.8], fs=11, rh=0.52)
codebox(s, 0.55, 4.75, 12.2, 1.45, "MAINTAINER, IN #4555", [
    ("\"If the brownout circuit worked, it should hold the CPU in reset when voltage is too low for flash.\"", ICE),
    ("Community workaround: hard-code the configuration in userPrefs.jsonc so the defaults ARE the intended settings.", MUT)], 11)
txt(s, 0.55, 6.3, 12.2, 0.4, "#4555 is issue number 4555 at github.com/meshtastic/firmware/issues. A PR (pull request) is a proposed code change; #11872 is the one that fixed the nRF52 boards.", 10, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "We are not the first. The maintainers' reading matches ours. The nRF52 branch received a fix in 2026; the ESP32 branch we run did not. The community workaround on the last line becomes our fix 1.")

# ============ 13 HYPOTHESES ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Hypotheses, predictions, verdicts", "Predictions written before the measurement; verdicts after")
rows = [["#", "Hypothesis", "Would show", "Verdict"],
        ["H1", "Flash wear-out", "Diffuse failures; write counts near 100k per sector", "Rejected: 20 sectors per boot over 864 is millions of boots"],
        ["H2", "Defective cells", "Same sectors misread every pass; cells fail again after a rewrite", "Rejected: unstable sectors became perfect once rewritten"],
        ["H3", "Torn writes under low supply", "Follows power events; fixed sectors unstable until erased and reprogrammed", "Confirmed: measured on SF, repaired by a rewrite"],
        ["H4", "LittleFS bug", "Mount failures, corrupted directory pairs", "Rejected: mounts and decodes cleanly on both radios"],
        ["H5", "Firmware turns any failure into a reset", "Loss is permanent and silent", "Confirmed in source"]]
table(s, 0.55, 1.5, 12.2, rows, [0.5, 2.6, 4.4, 4.7], fs=11, rh=0.6)
card(s, 0.55, 5.3, 12.2, 1.25, "The discriminating experiment", "Three reads of the settings partition in one open connection with the firmware halted, at two serial speeds; a megabyte of program code, the NVS partition and the bootloader read the same way as controls.", GREEN, 13.5, 12.5)
notes(s, "Say the predictions first, then the data. H2 and H3 both predict fixed unstable sectors; only the erase-and-reprogram test separates them, and it did.")

# ============ 14 METHOD ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Method: reading the chip, firmware stopped")
codebox(s, 0.55, 1.35, 7.4, 2.45, "ESPTOOL STUB, ONE CONNECTION, NO RESET BETWEEN READS", [
    ("esp = detect_chip('COM4'); esp = esp.run_stub()", ICE),
    ("A = esp.read_flash(0xC90000, 0x360000)   # settings, 3.4 MB", ICE),
    ("B = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("C = esp.read_flash(0xC90000, 0x360000)", ICE),
    ("app = esp.read_flash(0x10000, 0x100000) x2   # control", MUT),
    ("A == B ?   B == C ?   app1 == app2 ?", ACC),
    ("# every chunk is MD5-checked: a transfer error raises; a changed byte is what the chip returned", MUT)], 10.5)
card(s, 8.15, 1.35, 4.65, 2.45, "Controls", ["Program partition, 1 MB, twice", "NVS partition and bootloader, twice", "16 KB window, four reads, at 115200 and at 921600 baud", "LittleFS image mounted and every file decoded on the laptop"], GREEN, 13, 11.5)
card(s, 0.55, 3.95, 12.25, 1.15, "In plain words", "Stop the firmware, read the whole settings area three times in a row through one open USB connection, and compare. A healthy chip returns the same bytes every time. Reading a megabyte of program code the same way is the control: if that had changed too, the method, not the chip, would be at fault.", ACC, 12.5, 11.5)
card(s, 0.55, 5.25, 7.4, 1.4, "The pitfall that cost two attempts", ["This board resets whenever the USB serial port closes, so separate esptool commands hide a boot, and a boot-time flash write, between 'back-to-back' reads", "Only reads inside one open connection count; the pitfall is itself evidence that the radio writes flash every time it starts"], MUT, 12, 10.5)
card(s, 8.15, 5.25, 4.65, 1.4, "How this was done", "Hypothesis: a Qualcomm engineer, October 2026. Experiment design, scripts and analysis drafted with Claude (Anthropic) as an AI assistant; every measurement run by Deo on the team's radios, each step authorised and checked against the raw records (sheet 20).", INK, 12, 10.5)
notes(s, "Reproducible by anyone with the repository: scripts under docs/src, records under docs/src/flash_forensics. The LittleFS image also proved the configuration in flash on measurement day was correct: Group9, 32-byte key, precision 32, CLIENT_MUTE, No PIN, 60/10/20/10 s. If asked about the AI: the recruiter supplied the hypothesis, the AI supplied the experimental design and the code, the team supplied the hardware, the authorisation of each destructive step, and the checking; the records are in the repo and the measurements can be repeated without the AI.")

# ============ 15 RESULT MAPS ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Result: the same sectors misread, every pass", "SF against RG, same day, same method")
pic(s, "g_maps_compare.png", 0.55, 1.35, 12.2)                              # 12.2 x 3.55
txt(s, 0.55, 4.95, 12.2, 0.65, "Each small square is one 4 KB sector of the settings area, 864 per radio. Red: the bytes came back different on consecutive reads with nothing running, the same sectors every time and at both serial speeds. Green: the sectors holding the live settings files that day. The program code read identically.", 11.5, False, BODY)
stat(s, 0.55, 5.65, 3.95, 1.0, "21", "unstable sectors on SF, 12 heavily", RED, 20)
stat(s, 4.675, 5.65, 3.95, 1.0, "0", "unstable sectors on RG", GREEN, 20)
stat(s, 8.8, 5.65, 3.95, 1.0, "0", "differences in program code, NVS, bootloader", GREEN, 20)
notes(s, "SF: 117 and 107 differing bytes between consecutive reads, 118 bits flipped in both directions, none inside erased areas, confined to 21 sectors with 12 carrying almost all of it. RG: zero. The live files on SF sat in clean sectors 25, 26 and 470 that day, which is why the radio was working; LittleFS wear-levelling would have moved them onto the bad ones eventually. Plain words: the chip was asked the same question three times and gave different answers in the same 21 places; the control (program code) gave the same answer every time.")

# ============ 16 NUMBERS, DECISIVE TEST, REPAIR ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "The numbers, the decisive test, the repair", "All on SF, 27 October; RG read the same way as the healthy control")
stat(s, 0.55, 1.35, 2.9, 1.15, "117 / 107", "differing bytes, reads 1v2 and 2v3", ACC, 20)
stat(s, 3.65, 1.35, 2.9, 1.15, "118", "bits flipped, in both directions", ACC, 20)
stat(s, 6.75, 1.35, 2.9, 1.15, "0", "differences in 1 MB of code, NVS, bootloader", GREEN, 20)
stat(s, 9.85, 1.35, 2.95, 1.15, "21 -> 0", "unstable sectors after the repair", GREEN, 20)
txt(s, 0.55, 2.7, 7.4, 0.3, "THE DECISIVE TEST: ERASE, PROGRAM THREE PATTERNS, READ FIVE TIMES EACH (FREE SECTORS ONLY)", 9.5, True, ACC, PP_ALIGN.LEFT, MONO)
rows = [["Sector", "As found", "0x00 x5", "A5/5A x5", "random x5", "Erased x5"],
        ["57 (worst)", "27 bytes disagree", "clean", "clean", "clean", "clean"],
        ["31", "20 bytes disagree", "clean", "clean", "clean", "clean"],
        ["200 (control)", "stable", "clean", "clean", "clean", "clean"]]
table(s, 0.55, 3.0, 7.4, rows, [1.4, 1.6, 1.1, 1.1, 1.1, 1.1], fs=10.5, rh=0.42)
card(s, 8.15, 2.7, 4.65, 2.0, "Verdict: disturbed, not damaged", "0 mismatches in 45 reads. The scarred sectors hold every pattern once written on a healthy supply, so the cells are sound; the instability was the residue of earlier writes under a sagging rail. The hardware question is closed.", GREEN, 12.5, 11)
card(s, 0.55, 4.9, 7.4, 1.75, "The repair, same day", ["Erase the settings area on USB power; the first boot formats it and installs defaults", "meshtastic --configure sf-config.yaml, twice: the region write reboots the radio mid-transaction (now a rule in User Guide 12.2)", "Three reads afterwards: 0 differing bytes; node key pair preserved, so RG's node table stays valid"], INK, 12.5, 10.5)
card(s, 8.15, 4.9, 4.65, 1.75, "In plain words", "Rewriting the bad spots on a good supply made them perfect. Worn-out or defective memory would have failed again. The memory was disturbed by how it was written, not broken.", ACC, 12.5, 11)
notes(s, "Numbers: fixed sectors, both bit directions, speed-independent, code partition stable: cells whose stored charge sits at the read threshold. Not a serial artifact (chunks are verified), not wear (the pattern would be diffuse), not a filesystem bug (the image mounts and decodes). Decisive test run on 27 October with authorisation on sectors 57 and 31, free in LittleFS (live data in 0, 1, 25, 26, 470), so nothing was lost. Record: docs/src/flash_forensics/decisive_test_2026-10-27.json. Repair: thirty minutes end to end; the two-pass --configure behaviour is the Sep 3 reset-during-write race seen from the other side. RG needs no repair; its baseline is clean.")

# ============ 17 NOW ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Now: two days later, both radios clean", "Measured again on 29 October, after SF sat two days at 0 percent battery")
pic(s, "g_now.png", 0.55, 1.35, 12.2)                                       # 12.2 x 3.35
card(s, 0.55, 4.85, 6.0, 1.8, "What was checked on 29 October", ["Configuration read back with zero provisioning on both radios: name, role, No PIN, Group9 with key, precision 32, cadence, presets: all intact", "Flash settings area read three times each: 0 differing bytes, 0 unstable sectors on SF and on RG"], GREEN, 12.5, 11)
card(s, 6.75, 4.85, 6.05, 1.8, "Read it honestly", ["SF's flat-battery episode is the exact condition that wiped it three times before; this time nothing was lost and the flash stayed clean", "One cycle is evidence, not proof: the radio was stored flat, not transmitting while it died. The campaign of five running-flat cycles per radio is what closes it"], ACC, 12.5, 11)
notes(s, "SAY: This is the state today. The red bar is SF as we found it on the 27th; everything after it is zero, including SF after two days at zero percent battery on the new firmware. Be honest about what one cycle proves: the radio was stored flat, not transmitting while it died, so the dangerous write may simply not have happened this time. The five-cycle campaign is what proves the fix.")

# ============ 17 CHAIN ============
s = slide(); frame(s, "part ii - root cause", "VICTOR")
head(s, "The chain of causation", "Every link tagged with its class of evidence")
pic(s, "g_chain.png", 0.55, 1.4, 12.2)
rows = [["Link", "Evidence", "Class"],
        ["Flat battery, reboot churn on recovery", "3 of 4 incidents; #4555 reproduces it", "Observed"],
        ["Flash write on every boot, no voltage gate", "Boot log; PowerHAL.cpp stub", "Verified in source"],
        ["Rail between 2.44 and 2.7 V during a write", "Datasheets, sdkconfig, 750 mA TX pulses", "Inferred (scope capture pending)"],
        ["Cells left half-programmed", "SF sector map; healed by rewrite", "Measured"],
        ["Decode fails, defaults installed and saved", "NodeDB.cpp; the losses themselves", "Verified in source"]]
table(s, 0.55, 4.1, 12.2, rows, [4.0, 5.2, 3.0], fs=11, rh=0.42)
notes(s, "Read the chain left to right in plain words: the battery goes flat; on recovery the radio boots and reboots; every boot writes a settings file with no check of the supply; the supply is sagging in the window where the CPU runs but the flash is not guaranteed; cells are left half-written; next boot a file will not decode and the firmware installs factory defaults and saves them. One link is inferred rather than measured: the rail voltage during the event. An oscilloscope on the 3V3 pin during a transmit burst at 3.4 V cell voltage closes it.")

# ============ 18 THE FIX ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "The fix: plan and proof", "Ranked by leverage; fix 1 is built, flashed and proven on both radios")
rows = [["#", "Fix", "Effect", "Status"],
        ["1", "Rebuild Meshtastic with our configuration compiled in as its factory defaults (userPrefs.jsonc + one-line NO_PIN patch)", "A revert now restores OUR settings; the failure becomes invisible to the driver", "Both radios flashed and accepted Oct 28; SF clean after 2 days at 0 percent, Oct 29"],
        ["2", "ESP32 power gate: refuse saves below 3.5 V on battery; drop the boot-time rewrite", "Removes the write that happens at the worst moment", "Next: ten-line patch, to offer upstream"],
        ["3", "Clean erase and re-provision of a scarred settings area", "Removes residue already present", "Done on SF; RG clean"],
        ["4", "Raise the brownout reset to 2.67 or 2.84 V (core rebuild)", "The CPU resets before the flash leaves spec", "Planned"],
        ["5", "Operations: never store flat; OLED pre-flight; snapshots; phone-QR recovery", "Detection in 2 s, recovery in 90 s", "In force"]]
table(s, 0.55, 1.35, 12.2, rows, [0.4, 5.5, 3.9, 2.4], fs=10.5, rh=0.52)
card(s, 0.55, 4.6, 6.0, 2.05, "Fix 1 in plain words", "Meshtastic ships with factory settings: public channel, random PIN, no name. We rebuilt it from source so that ITS factory settings are OUR settings: Group9 at 912.875 MHz, No PIN, CLIENT_MUTE, named SF or RG, our GPS cadence. The firmware's failure path still 'resets to defaults', but the defaults are now right. The key is compiled into a binary that never leaves the private repository.", GREEN, 12.5, 11)
card(s, 6.75, 4.6, 6.05, 2.05, "Proven on both radios, 28 October", ["Flashed each radio's fix-1 image, sent meshtastic --factory-reset: SF came back as SF and RG as RG, Group9 with the 32-byte key, precision 32, No PIN, CLIENT_MUTE, US LONG_FAST, with zero provisioning", "Only the smart-broadcast minimums and the 21 canned presets need the snapshot, which also restores the node key pair", "Next proof: five flat-battery cycles per radio with the flash map read after each; a scope on the 3V3 rail during a transmit burst"], INK, 12.5, 10.5)
notes(s, "Fix 1 is the community's own answer to #4555 and costs one build per radio: build Meshtastic from source with a userPrefs.jsonc that names our channel, key, region, role, owner names, cadence, plus a one-line patch so the default Bluetooth mode is No PIN. Acceptance on SF and RG, 28 October: after a factory reset each radio was already configured; the snapshot then restored the smart-broadcast minimums (10 s / 20 m), the 21 presets and the original key pair. The ask: approve the flat-battery campaign before the next field test. Fix 2 removes the cause; fix 3 cleans up the past; fix 4 is the hardware-correct answer and the most work.")

# ============ 19 REFERENCES AND ATTRIBUTION ============
s = slide(); frame(s, "part ii - root cause", "CANNON")
head(s, "References, records and attribution")
rows = [["Source", "Used for"],
        ["Heltec WiFi LoRa 32 V4 datasheet V4.2.0: resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf", "Supply rails, battery path, transmit current (tables 3.2, 3.4)"],
        ["Boya Microelectronics BY25Q128AS datasheet (the 16 MB flash on the V4, JEDEC 68 40 18)", "VCC 2.7 to 3.6 V, program and erase times, 100k-cycle endurance"],
        ["Espressif ESP32-S3: ESP-IDF Kconfig; Arduino-ESP32 core sdkconfig", "Brownout detector level 7 = 2.44 V"],
        ["meshtastic/firmware, tag v2.7.26.54e0d8d: NodeDB.cpp, SafeFile.cpp, PowerHAL.cpp, PowerFSM.cpp, sleep.cpp", "Save and load behaviour, the power gate stub"],
        ["github.com/meshtastic/firmware issues #4555, #4622, #2936, #3260, #5259; pull request #11872", "Prior reports of the same loss; the nRF52 fix"],
        ["Espressif esptool 4.11; python-pptx; matplotlib", "Reading flash with the firmware halted; this deck and its figures"],
        ["This repository: docs/src/flash_forensics (records), docs/src/*.py (scripts), Technical Manual 15-16, Device User Guide 12", "Every number in Part II, reproducible"]]
table(s, 0.55, 1.35, 7.9, rows, [5.3, 2.6], fs=9.5, rh=0.62, firstbold=False)
card(s, 8.65, 1.35, 4.15, 4.95, "How this work was done", ["The hypothesis that the memory itself might be at fault came from a Qualcomm engineer during a recruiting conversation in October 2026.", "The investigation (sheets 13 to 18) was designed and run by the team with Claude (Anthropic) as an AI assistant: the AI drafted the experiment design, the flash-reading scripts and the analysis.", "Deo Grace Mwala ran every measurement on the team's radios, authorised each erase or write, and checked each result against the raw records.", "Every script and record is in the repository, so the measurements can be repeated without the AI."], INK, 12.5, 10.5)
notes(s, "Attribution policy: say exactly who supplied what. Hypothesis: the recruiter. Experimental design, code and analysis: the AI assistant, under the team's direction. Hardware, authorisation and checking: the team. Reproducibility: the repository. If the audience wants proof, open docs/src/flash_forensics and re-run the sector map on either radio; it takes four minutes.")

# ============ 20 CLOSE ============
s = slide(); frame(s, "close", "DEO")
head(s, "The answer, and what the failures bought")
card(s, 0.55, 1.45, 12.2, 1.55, "Is it the memory itself?", "Partly, and measurably, but not as the question implies. SF's settings flash carried 21 sectors that would not hold a value; rewritten under a healthy supply they became perfect. The cells had been left half-written below the flash's 2.7 V minimum but above the 2.44 V reset point, a window the firmware never checks and then punishes with factory defaults.", INK, 15, 13)
stats = [("10", "root-caused failures, each with a written signature and recovery"), ("21 -> 0", "unstable flash sectors on SF; RG clean at 0"),
         ("0", "reflashes ever needed for a configuration failure"), ("90 s", "to recover a reverted radio; 2 s to detect one"),
         ("4.7 mi", "measured reach; honest envelope 0.5 to 4.7 mi by terrain"), ("1 build", "makes a future revert restore OUR configuration: proven on both radios")]
pos = [(0.55, 3.25), (4.65, 3.25), (8.75, 3.25), (0.55, 4.75), (4.65, 4.75), (8.75, 4.75)]
for (big, small), (x, y) in zip(stats, pos):
    stat(s, x, y, 4.0, 1.35, big, small, ACC, 24)
rect(s, 0.55, 6.25, 12.2, 0.42, INK)
txt(s, 0.8, 6.31, 11.7, 0.3, "EVERY FAILURE BECAME A RULE; THE WORST ONE BECAME A MEASUREMENT, A REPAIR, AND A FIX.", 11.5, True, PAPER, PP_ALIGN.CENTER, HF)
notes(s, "Close on the bar. Then the ask: fix 1 is proven on both radios; approve the flat-battery campaign before the next field test.")

assert sheet_no[0] == TOTAL, sheet_no[0]
prs.save("../presentations/Group9_Presentation.pptx")
import os
print("saved", os.path.getsize("../presentations/Group9_Presentation.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))
