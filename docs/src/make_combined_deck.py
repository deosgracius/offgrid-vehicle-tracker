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
TOTAL = 31; sheet_no = [0]

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
    txt(s, 9.7, 6.94, 3.3, 0.32, "SHEET %02d/%02d  REV C  %s" % (sheet_no[0], TOTAL, DATE), 9, False, MUT, PP_ALIGN.RIGHT, MONO)
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
s = slide(); gridpaper(s); frame(s, "tests, failures, root cause")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHAT BROKE, AND WHAT IT TAUGHT US", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "THE TEST AND FAILURE RECORD, AND THE ONE FAILURE WE CHASED TO THE SILICON", 16, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.3, "Part I: eleven root-caused failures and seven test campaigns, each with the rule it left behind. Part II: the battery-death configuration loss, investigated to the flash cells with measurements on both radios, repaired, and fixed at the root.", 13, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\nOctober 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Two parts, one arc: the record of what broke, then the deepest dive we made into the failure that kept returning.")

# ============ 2 WHY FAILURES ============
s = slide(); frame(s, "part i - the failures")
head(s, "Why the failures are the deliverable")
pts = [("A failure is only useful once it has a signature", "Every entry in our catalog records the symptom, the root cause, and the recovery, so the next person recognizes it in minutes, not days. A failure that was merely survived is a failure that will happen again; one with a written signature is a test case."),
       ("Each failure produced a rule or a feature", "Pre-flight checks, cadence-aware alarms, the course-up compass, the config snapshot, the LINK LOST alarm: none were in the original plan. All came from something breaking on a bench, on a road, or on a canyon rim, and all are now in the manuals."),
       ("Field equipment fails between outings", "The question is never whether; it is whether the team can diagnose it on a canyon rim with a phone. Three of ten failures struck the night before a test, and every one was cleared in time because the signature had already been written down.")]
y = 1.35
for t1, t2 in pts:
    card(s, 0.55, y, 12.2, 1.55, t1, t2, INK, 14, 13); y += 1.72
notes(s, "Set expectations: this is not a list of embarrassments, it is the verification record of a system that is honest about itself. Ten failures, ten rules.")

# ============ 3 TIMELINE ============
s = slide(); frame(s, "part i - the failures")
head(s, "The semester on one line")
s.shapes.add_picture("deck/g_failtimeline.png", Inches(0.55), Inches(1.3), width=Inches(12.2))
txt(s, 0.55, 6.45, 12.2, 0.35, "RED: FAILURES, ROOT-CAUSED.  GREEN: TESTS.  THE HOLLOW TRIANGLE IS NEW MEXICO, PENDING.", 10.5, True, MUT, PP_ALIGN.CENTER, MONO)
notes(s, "Walk it left to right. Note how failures cluster right before tests - and how the same villain, battery death, returns three times.")

# ============ 4 BRING-UP ============
s = slide(); frame(s, "part i - the failures", "DEO")
head(s, "Failures 1-3: bring-up, August 30-31")
cards = [("1. The display boot-looped silently", "The official espressif32 platform (Arduino core 2.x) boot-loops this panel's chip revision. Fix: the pioarduino platform, dio_opi memory, dio flash mode. One full day to find.", RED),
         ("2. A bonded radio goes invisible", "Store a BLE bond and the Meshtastic radio stops advertising to everyone, including its own peer. Fix: pair Just-Works on every connect, never store a bond, never deleteAllBonds() at boot.", RED),
         ("3. PIN pairing rejected us", "Default RANDOM_PIN mode fails our keypad-less display (SM confirm mismatch, rc=1284). Fix: radios run NO_PIN. This same setting is what reverts in failures 8 and 10.", RED)]
x = 0.55
for t1, t2, c in cards:
    card(s, x, 1.35, 4.0, 2.45, t1, t2, c, 13.5, 12.5); x += 4.18
card(s, 0.55, 4.05, 12.2, 1.6, "What they bought", "The BLE link state machine with exactly one recovery path (any failure tears down to SCANNING), the ignition-on product flow, and the first entries of the scar catalog. The display has never wedged since.", GREEN, 13.5, 12)
notes(s, "Day one. None of these were in any datasheet. The boot-loop alone cost a day and taught us to trust the vendor's ESP-IDF config over its Arduino screenshot.")

# ============ 5 FIRST DRIVE ============
s = slide(); frame(s, "part i - the failures", "JOSIAH")
head(s, "Failure 4: the first drive test, September 1")
rows = [["Symptom on the road", "Root cause", "Fix"],
        ["Partner position frozen on a 6 km grid", "Channel default position_precision = 13 truncates every broadcast", "Precision 32 (full) on the channel"],
        ["~4 minutes of apparent latency", "gps_update_interval default 120 s: fresh fixes only every two minutes", "GPS interval 10 s, broadcast 10 s moving"],
        ["Speeds wildly wrong", "Position.ground_speed is km/h on the wire, not m/s", "Decoder converts; display shows mph"],
        ["Parked car shows 1-3 mph", "GPS jitter reported as speed", "4.5 km/h deadband in the node table"],
        ["Clock an hour off", "West Texas is Central time; the CT/MT line is not at -97.5", "Timezone bands carried to the TX/NM border"]]
table(s, 0.55, 1.35, 12.2, rows, [3.6, 5.0, 3.6], fs=11.5, rh=0.6)
txt(s, 0.55, 5.4, 12.2, 1.0, "The lesson that outlived the fixes: windowsill tests cannot find any of these. Smart broadcast, GPS refresh, precision quantization and speed units only show while actually driving. Every later feature was validated on the road.", 12.5, False, BODY)
notes(s, "Five faults, one drive. Every one invisible on the bench. This is why we drove six more times.")

# ============ 6 WRONG FIRMWARE + CLI ============
s = slide(); frame(s, "part i - the failures", "DEO")
head(s, "Failures 5-6: wrong flash, lying CLI (Sep 3)")
card(s, 0.55, 1.35, 6.0, 2.3, "5. Display firmware flashed onto a radio", "Both boards share USB ID 303A:1001; an auto-picked COM port put our firmware on the Heltec and erased Meshtastic. Seeing display logs proved nothing about WHICH board was flashed. Recovery: esptool erase, factory image, full re-provision. The node number survives (MAC-derived), so the display reconnected unchanged.", RED, 13.5, 11.5)
card(s, 6.75, 1.35, 6.0, 2.3, "6. A config write that silently reverted", "The CLI's port-close toggles DTR/RTS, hard-resetting the ESP32 mid-save. The write 'succeeds'; the next read shows the old value. Reboot-triggering settings (region, Bluetooth mode) are the usual victims, and nothing on the radio's screen changes.", RED, 13.5, 11.5)
card(s, 0.55, 3.9, 12.2, 1.8, "Rules that came out of it", "Identify every board by its MAC (SER=) before touching it - never let a tool pick the port. Verify every config write by read-back AND on the radio's own screen. For stubborn values, use the Python API holding the port open. Both rules are now steps in the manual's flashing procedure.", GREEN, 13.5, 12)
notes(s, "The identity rule and the verification rule. Both sound obvious; both were learned by losing a radio for an afternoon.")

# ============ 7 SILENT FREQUENCY REVERT ============
s = slide(); frame(s, "part i - the failures", "VICTOR")
head(s, "Failure 7: \"0 online\", same configs (Sep 25)")
card(s, 0.55, 1.35, 6.0, 2.5, "The symptom", "Two radios, same key, every config read-back identical, zero channel utilization, traceroute MAX_RETRANSMIT - total mutual silence. Every instrument said RF failure, and both radios' screens looked perfectly healthy.", RED, 13.5, 12)
card(s, 6.75, 1.35, 6.0, 2.5, "The root cause", "Meshtastic derives the frequency from a hash of the channel name: slot = djb2(name) mod 104. One channel write had silently reverted, so one radio sat on the public slot (906.875 MHz) and the other on Group9's slot 43 (912.875). Same key, different frequencies: nothing couples.", RED, 13.5, 12)
codebox(s, 0.55, 4.1, 12.2, 1.6, "THE TWO-SECOND PRE-FLIGHT THAT CAME OUT OF IT", [
    ("Both OLED LoRa screens must read  912.875 MHz  before any test or drive.", ICE),
    ("The screen is ground truth. The CLI can read back the intended config while the radio still radiates on the old slot.", MUT)])
notes(s, "Idea 2 of the project - the name IS the frequency - was learned here. The debug ladder: config diff, matched-power tests, traceroute, regression on the default channel, then the hash math exposed the slot mismatch.")

# ============ BRIDGE: BATTERY DEATH ============
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

# ============ 9 NIGHT DRIVE ============
s = slide(); frame(s, "part i - the failures", "JOSIAH")
head(s, "Failure 9: the hand-rotated compass (Oct 4)")
card(s, 0.55, 1.35, 6.0, 2.2, "The symptom", "North-up ring at night: to read the arrow against the road the driver physically turned the unit - at which point nothing on it could be read. And the staleness cue alarmed at 59 s of perfectly normal silence from a parked partner.", RED, 13.5, 11.5)
card(s, 6.75, 1.35, 6.0, 2.2, "The fix, shipped the next day", "Course-up compass: the top of the ring is always straight ahead, cardinals rotate with the car, a nose mark at 12 o'clock, directions in clock positions. Cadence-aware staleness: 30 s for a moving partner, 90 s for a parked one.", GREEN, 13.5, 11.5)
card(s, 0.55, 3.8, 12.2, 1.9, "Why it belongs in a failure deck", "Neither change was a bug fix; both were design errors that only a real drive at night could expose. They were validated on the road the next day (dart at 12 o'clock at 37 mph) and have carried every test since. The honest-display philosophy was tested here first: a cue that cries wolf is as dishonest as one that stays silent.", INK, 13.5, 12)
notes(s, "The user-experience failures. Thirty seconds of night footage redesigned the main screen.")

# ============ 10 NIGHT BEFORE CANYON ============
s = slide(); frame(s, "part i - the failures", "DEO")
head(s, "Failure 10: the night before the canyon (Oct 17)")
cards = [("Display 1 \"dead\"", "Actually fine. Power banks shut off under the display's milliwatt draw, and a reflective screen in a dim room reads as off. Flashlight test first.", MUT),
         ("Display 2 half-dead USB-C", "Powers in ONE plug orientation - damaged pins on one side. A coin-flip failure on every plug-in. Marked the working orientation; a repair item.", ACC),
         ("Radio EA:D4 reverted", "A week idle, battery flat: Bluetooth mode, channel and name gone. The display's serial log named it in one line: write status 261, insufficient authentication.", RED)]
x = 0.55
for t1, t2, c in cards:
    card(s, x, 1.35, 4.0, 2.2, t1, t2, c, 13.5, 12.5); x += 4.18
codebox(s, 0.55, 3.8, 12.2, 1.85, "DISPLAY SERIAL LOG - THE SIGNATURE", [
    ("[ble] auth complete: encrypted=1 bonded=0", ICE),
    ("Write complete; status=261            <- insufficient authentication: radio not in NO_PIN", RGBColor(0xFF,0x9A,0xA8)),
    ("[ble] want_config write failed", ICE),
    ("[ble] disconnected (reason 534)       <- our side hung up, by design, to retry", ICE)])
notes(s, "Three independent faults in one evening, diagnosed in forty minutes because every one had a written signature. The test ran the next morning.")

# ============ 15 PRE-DRIVE DIAGNOSTIC: DISPLAYS ============
s = slide(); frame(s, "part i - the failures", "DEO")
head(s, "Failure 11: the 0.21 mi that was not there")
s.shapes.add_picture("deck/g_lcddiag.png", Inches(0.55), Inches(1.25), width=Inches(8.3))
card(s, 9.05, 1.25, 3.75, 3.1, "What the serial logs proved", "Both displays booted clean, paired in under 8 s (encrypted=1 bonded=0, every config write status 0), completed the config dump, built the correct node table (SF/RG), and held the link at heartbeat state 3 with zero rescans. Display 1 again needed a USB-C plug flip before it enumerated.", GREEN, 13, 11)
card(s, 0.55, 4.55, 12.25, 1.75, "The observation: 0.21 mi between two radios on one desk", "The displays were right and the GPS fixes were wrong. Indoors, SF's fix scattered 100 to 400 m between packets with 1.4 m/s of phantom speed; RG later reported a coherent 50 mph eastbound drive for a minute before snapping home. A marginal fix produces fake velocity, not just jitter, and dead reckoning faithfully projects it. Fixes shipped the same hour: the closing/apart line reads \"holding\" when both cars are parked; the distance stays honest. Rule: judge a bench distance only with sky view.", RED, 13, 11.5)
notes(s, "This is the display track's own verification record: the links and the firmware were fine; the data they rendered was bad because the radios' GPS receivers were indoors. The graph is parsed straight from the archived serial logs.")

# ============ TESTS SO FAR ============
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

# ============ 14 CANYON ============
s = slide(); frame(s, "part i - the tests")
head(s, "The hardest test: Ceta Canyon, October 18")
s.shapes.add_picture("deck/g_timeline.png", Inches(0.55), Inches(1.3), width=Inches(8.0))
card(s, 8.8, 1.3, 4.0, 3.6, "What it proved", "Behind rock the link is intermittent at any distance: stale from 1.29 mi, yet a packet landed at 4.28 mi through a gap. The longest silence ran seven minutes and was healed by one packet with no operator action. Both radios audited clean afterward: terrain, not hardware. The rim antenna held 4.7 mi - the quantitative case for the repeater.", INK, 13.5, 11.5)
notes(s, "Red stale, green live. The 7:30 age reset is the finding: intermittent, not binary.")

# ============ 11 FAILURE -> RULE MAP ============
s = slide(); frame(s, "part i - the failures")
head(s, "Every failure became a rule", "The close of Part I; the battery-death row is where Part II begins.")
rows = [["Failure", "Rule or feature it produced", "Where it lives now"],
        ["Boot-loop", "pioarduino + dio_opi; vendor IDF config is ground truth", "platformio.ini, manual 14"],
        ["Bonded radio invisible", "Just-Works pairing, no stored bond, one teardown path", "ble_link.cpp, manual 8"],
        ["First-drive faults", "Precision 32, 10 s GPS, km/h decode, deadband; validate on the road", "Provisioning recipe, node_table.cpp"],
        ["Wrong flash", "Identify by MAC before any upload; never auto-pick a port", "Manual 14.2 fleet table"],
        ["Lying CLI", "Read back every write; the OLED outranks the CLI", "Manual 16, entry 6"],
        ["Silent frequency revert", "Pre-flight: both OLEDs read 912.875", "User guide 3, manual 7"],
        ["Battery death reverts", "Snapshots and pre-flight in October; root cause and repair on Oct 27: Part II", "Part II"],
        ["Hand-rotated compass", "Course-up compass; cadence-aware staleness", "ui_render.cpp, manual 9"],
        ["Night before the canyon", "Flashlight test, plug orientation, the 261 signature", "Manual 16, entries 9-10"],
        ["Phantom 0.21 mi", "Judge distances only with sky view; holding when both parked", "Manual 16, entry 11; Guide 11"]]
table(s, 0.55, 1.3, 12.2, rows, [3.0, 5.6, 3.6], fs=10.5, rh=0.48)
notes(s, "The point of the deck in one table: ten failures, ten rules, every rule with an address in the codebase or the manual.")

# ============ PART II DIVIDER ============
s = slide(); gridpaper(s); frame(s, "part ii - root cause")
txt(s, 0.7, 1.6, 11.9, 0.9, "PART II", 20, True, ACC, PP_ALIGN.LEFT, HF, spc=400)
txt(s, 0.7, 2.2, 11.9, 1.2, "WHY THE RADIOS FORGET", 40, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 3.2, 11.0, 0.9, "The battery-death failure, chased from the symptom to the flash cells and back to a fix. Measurements on both radios, 27 October 2026.", 14, False, BODY)
stat(s, 0.72, 4.4, 2.8, 1.5, "21 -> 0", "unstable flash sectors on SF, before and after repair")
stat(s, 3.72, 4.4, 2.8, 1.5, "260 mV", "window in which the CPU writes to an out-of-spec flash")
stat(s, 6.72, 4.4, 2.8, 1.5, "true", "what the firmware's power-safety check always returns")
notes(s, "Part II answers one question: is it the memory itself? It ends with the fix that makes the failure harmless.")

# ============ 2 THE QUESTION ============
s = slide(); frame(s, "part ii - root cause")
head(s, "One question, three possible meanings", "\"It might be the memory itself.\" Each meaning leaves a different fingerprint and needs a different fix.")
cards = [("Worn out", ["Endurance exhausted by write volume", "Fingerprint: diffuse failures, many sectors", "Fix: replace the part"], RED),
         ("Defective or marginal cells", ["Specific cells that will not hold a value", "Fingerprint: the same sectors misread, every pass", "Fix: avoid or re-form those sectors"], ACC),
         ("Corrupted by the conditions of a write", ["Healthy cells written while the supply was out of spec", "Fingerprint: follows power events; heals when rewritten", "Fix: never write under low voltage"], GREEN)]
x = 0.55
for t, items, c in cards:
    card(s, x, 1.55, 4.0, 2.6, t, items, c, 13.5, 12); x += 4.1
card(s, 0.55, 4.45, 12.2, 2.1, "How we told them apart", ["Read the settings partition straight off the chip, firmware halted, three times in one session", "Read the firmware's save and load code at tag v2.7.26", "Read the flash and board datasheets and the brownout level the firmware is built with", "Line the four incidents up against all of it"], INK, 13.5, 12.5)
notes(s, "The recruiter's suggestion is a testable hypothesis, not an opinion to argue with. State the three readings of 'the memory itself', what each would look like in data, and what each would require as a fix. The rest of the deck collects exactly that data.")

# ============ 4 STORAGE ============
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "How the radio stores its settings", "Partition table and file sizes read from SF; save and load behaviour from meshtastic/firmware v2.7.26.")
s.shapes.add_picture("deck/g_storage.png", Inches(0.55), Inches(1.4), width=Inches(12.2))
notes(s, "Six protobuf files on a 3.4 MB LittleFS partition. Red boxes are the policy weaknesses in the vendor's code: the power gate that always returns true on ESP32, the one non-atomic file, the ignored close() result, and the load-failure path that installs factory defaults and saves them with no backup consulted. The green line is the one protection that exists: the low-battery deep sleep skips the write. Sources: NodeDB.cpp, SafeFile.cpp, PowerHAL.cpp, PowerFSM.cpp, sleep.cpp at the tag.")

# ============ 5 FIRMWARE FACTS ============
s = slide(); frame(s, "part ii - root cause")
head(s, "What the firmware does and does not do", "Verified in source at tag v2.7.26; every line has a file name.")
card(s, 0.55, 1.5, 6.0, 3.3, "Does", ["Write .tmp, re-read it, 1-byte XOR check, then rename (SafeFile.cpp)", "Re-save device.proto on every boot (our boot log)", "Install factory defaults when a file is missing or will not decode, then save them (NodeDB.cpp)", "Skip the flash write on its own low-battery deep sleep (PowerFSM.cpp, sleep.cpp)", "Reset the CPU only below 2.44 V (core sdkconfig, level 7)"], INK, 13.5, 12.5)
card(s, 6.75, 1.5, 6.0, 3.3, "Does not", ["Check the supply before any save: powerHAL_isPowerLevelSafe() is a stub returning true on ESP32", "Keep nodes.proto atomic: the original is deleted before the new copy is written", "Act on a failed save: close() result discarded, 'Can't write prefs!' then return okay", "Consult the backup copy at boot: restorePreferences() runs only on operator command", "Retry before resetting: one unreadable file is a permanent factory reset"], RED, 13.5, 12.5)
codebox(s, 0.55, 5.0, 12.2, 1.5, "src/power/PowerHAL.cpp, tag v2.7.26: THE GATE EVERY SAVE PASSES THROUGH ON OUR RADIOS", [("__attribute__((weak, noinline)) bool powerHAL_isPowerLevelSafe()", ICE), ("{", ICE), ("    return true;        // no ESP32 override exists in src/platform/esp32", PINK), ("}", ICE)], 11)
notes(s, "The asymmetry to point out: the firmware refuses to write during its own low-battery shutdown, which proves the authors knew the danger, but it has no voltage check on the ordinary save path, and that path runs on every boot. On ESP32 the gate function is a weak default; no platform override exists in src/platform/esp32.")

# ============ 6 PHYSICS ============
s = slide(); frame(s, "part ii - root cause", "VICTOR")
head(s, "The physics: a 260 mV window")
s.shapes.add_picture("deck/g_voltage.png", Inches(0.55), Inches(1.25), width=Inches(12.2))
txt(s, 0.55, 6.15, 12.2, 0.5, "Boya BY25Q128AS (JEDEC 68 40 18, read from the chip): VCC 2.7 to 3.6 V, page program 0.6 ms, sector erase 50 ms, 100k cycles. Heltec V4 datasheet tables 3.2 and 3.4. ESP-IDF Kconfig for ESP32-S3.", 10.5, False, MUT, PP_ALIGN.LEFT, MONO)
notes(s, "A sector erase takes 50 ms. A 750 mA transmit pulse on a nearly flat cell can pull the rail through 2.7 V and back inside that window without ever reaching the 2.44 V reset. The datasheet states that VCC must be held within range during all operations. Between 2.44 and 2.7 V the CPU is alive, the write proceeds, and the result is undefined.")

# ============ 7 UPSTREAM ============
s = slide(); frame(s, "part ii - root cause")
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
s = slide(); frame(s, "part ii - root cause", "DEO")
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
s = slide(); frame(s, "part ii - root cause", "DEO")
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
s = slide(); frame(s, "part ii - root cause")
head(s, "Result: the same sectors misread, every pass", "SF against RG, same day, same method")
s.shapes.add_picture("deck/g_maps_compare.png", Inches(0.55), Inches(1.4), width=Inches(12.2))
txt(s, 0.55, 5.0, 12.2, 0.6, "Red sectors changed between consecutive reads with no firmware running: the same sectors on every pass, at both serial speeds, while the program partition read identically.", 12.5, False, BODY)
stat(s, 0.55, 5.6, 3.95, 1.1, "21", "unstable sectors on SF, 12 heavily", RED, 22)
stat(s, 4.675, 5.6, 3.95, 1.1, "0", "unstable sectors on RG", GREEN, 22)
stat(s, 8.8, 5.6, 3.95, 1.1, "0", "differences in program code, NVS, bootloader", GREEN, 22)
notes(s, "SF: 117 and 107 differing bytes between consecutive reads, 118 bits flipped in both directions, none inside erased areas, confined to 21 sectors with 12 carrying almost all of it. RG: zero. The live files on SF sat in clean sectors 25, 26 and 470 that day, which is why the radio was working; LittleFS wear-levelling would have moved them onto the bad ones eventually.")

# ============ 11 RESULT NUMBERS ============
s = slide(); frame(s, "part ii - root cause")
head(s, "Result: the numbers")
s.shapes.add_picture("deck/g_unstable.png", Inches(0.55), Inches(1.3), width=Inches(7.9))
stat(s, 8.75, 1.3, 1.95, 1.45, "117 / 107", "differing bytes, reads 1v2 and 2v3", ACC, 20)
stat(s, 10.85, 1.3, 1.95, 1.45, "118", "bits flipped, both directions", ACC, 20)
stat(s, 8.75, 2.9, 1.95, 1.45, "0", "differences in 1 MB of program code", GREEN, 20)
stat(s, 10.85, 2.9, 1.95, 1.45, "0", "differences in NVS and bootloader", GREEN, 20)
card(s, 0.55, 4.6, 12.2, 1.9, "Reading it", ["Fixed sectors, both bit directions, speed-independent, code partition stable: cells whose stored charge sits at the read threshold", "Not a serial artifact (chunks are verified), not wear (the pattern would be diffuse), not a filesystem bug (the image mounts and decodes)"], RED, 13.5, 12.5)
notes(s, "Be exact: the measurement establishes marginal cells in SF's settings partition on that day. Why they were marginal is the next two sheets.")

# ============ 12 DECISIVE TEST ============
s = slide(); frame(s, "part ii - root cause", "DEO")
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
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "The repair, same day", "Clean erase of the settings partition on USB power, then the snapshot.")
stat(s, 0.55, 1.5, 3.95, 2.1, "21 -> 0", "unstable sectors on SF, measured before and after", GREEN, 36)
stat(s, 4.675, 1.5, 3.95, 2.1, "2 passes", "of --configure: the region write reboots the radio mid-transaction", ACC, 36)
stat(s, 8.8, 1.5, 3.95, 2.1, "same key", "node key pair preserved; RG's node table stays valid", INK, 36)
card(s, 0.55, 3.9, 6.0, 2.6, "Steps", ["esptool erase_region 0xC90000 0x360000 (USB powered)", "First boot: 'Failed to initialize LittleFS', format, factory defaults", "meshtastic --configure sf-config.yaml, twice, 20 s apart", "Read back, reset, read back again: identical", "Three reads of the partition: 0 differing bytes"], INK, 13.5, 12)
card(s, 6.75, 3.9, 6.0, 2.6, "What the first pass taught", ["Pass 1 restored Bluetooth, region and the presets; owner, role, channel and cadence were lost in the reboot the region write triggers", "Now a rule in User Guide 12.2: run the command twice", "RG needs no repair today; its baseline is clean"], ACC, 13.5, 12)
notes(s, "Thirty minutes end to end. The two-pass behaviour is the same reset-during-write race as the Sep 3 incident, seen from the other side.")

# ============ 14 CHAIN ============
s = slide(); frame(s, "part ii - root cause")
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
s = slide(); frame(s, "part ii - root cause", "DEO")
head(s, "Fix plan, ranked by leverage")
rows = [["#", "Fix", "Effect", "Effort", "Status"],
        ["1", "Build with our configuration as the defaults (userPrefs.jsonc + NO_PIN patch)", "A revert restores the intended state; the failure becomes invisible", "1 day", "built Oct 27"],
        ["2", "ESP32 power gate: refuse saves below 3.5 V on battery; drop the boot-time device.proto rewrite", "Removes the write that happens at the worst moment", "1 day + test", "next"],
        ["3", "Clean erase and re-provision of scarred partitions", "Removes residue already present", "30 min / radio", "done: SF"],
        ["4", "Raise the brownout reset to 2.67 or 2.84 V (core rebuild)", "CPU resets before the flash leaves spec", "2 days", "planned"],
        ["5", "Operations: never store flat, OLED pre-flight, config snapshots, phone-QR recovery", "Detection in 2 s, recovery in 90 s", "in force", "done"]]
tb = table(s, 0.55, 1.4, 12.2, rows, [0.4, 5.0, 4.1, 1.3, 1.4], fs=11, rh=0.72)
card(s, 0.55, 5.85, 12.2, 0.7, "Order of value", "Fix 1 hides the failure from the driver; fix 2 removes its cause; fix 3 cleans up the past; fix 4 is the hardware-correct answer and the most work.", INK, 12.5, 12)
notes(s, "Fix 1 is the community's own answer to #4555 and costs one build per radio. The key is compiled into a binary that lives only in the private repository. Fix 2 is a ten-line patch we would offer upstream.")

# ============ 16 FIX 1 ============
s = slide(); frame(s, "part ii - root cause", "DEO")
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
s = slide(); frame(s, "part ii - root cause", "CANNON")
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

# ============ CLOSE ============
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

prs.save("Group9_Presentation.pptx")
import os
print("saved", os.path.getsize("Group9_Presentation.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))
