# Tests & Failures deck -- drawing-set chrome, Cambria body, failures first.
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
M = {"DEO": RGBColor(0x11,0x99,0xBD), "JOSIAH": RGBColor(0x6D,0x4B,0xDB),
     "VICTOR": RGBColor(0xE5,0x8E,0x1A), "CANNON": RGBColor(0xD9,0x48,0x8C)}
HF, BF, MONO = "Cambria", "Cambria", "Courier New"

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]; W, H = 13.333, 7.5
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
    txt(s, 9.7, 6.94, 3.3, 0.32, "SHEET %02d/%02d  REV A  2026-10-24" % (sheet_no[0], TOTAL), 9, False, MUT, PP_ALIGN.RIGHT, MONO)
    if owner:
        rect(s, 10.55, 0.38, 2.35, 0.46, PAPER, M[owner], 1.5)
        txt(s, 10.55, 0.44, 2.35, 0.34, "OWNER: " + owner, 11, True, M[owner], PP_ALIGN.CENTER, MONO)
def head(s, t): txt(s, 0.5, 0.36, 9.9, 0.62, t.upper(), 23, True, INK, PP_ALIGN.LEFT, HF, spc=200)
def card(s, x, y, w, h, title, body, accent=INK, ts=14, bs=13):
    rect(s, x, y, w, h, CARD, accent, 1.25)
    tb = s.shapes.add_textbox(Inches(x+0.18), Inches(y+0.13), Inches(w-0.36), Inches(h-0.26))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; r = p.add_run(); r.text = title.upper()
    r.font.size = Pt(ts); r.font.bold = True; r.font.color.rgb = accent; r.font.name = HF; set_spc(r, 100)
    p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = body
    r2.font.size = Pt(bs); r2.font.color.rgb = BODY; r2.font.name = BF
def codebox(s, x, y, w, h, label, lines):
    rect(s, x, y, w, h, CODEBG)
    txt(s, x+0.18, y+0.1, w-0.36, 0.3, label, 10, True, ACC, PP_ALIGN.LEFT, MONO)
    tb = s.shapes.add_textbox(Inches(x+0.18), Inches(y+0.42), Inches(w-0.36), Inches(h-0.5))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, (t, c) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = t; r.font.size = Pt(11.5); r.font.name = MONO; r.font.color.rgb = c
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
def table(s, x, y, w, rows, colw, hdr=True, fs=11.5, rh=0.42):
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

# ============ 1 TITLE ============
s = slide(); gridpaper(s); frame(s, "tests and failures")
txt(s, 0.7, 1.0, 11.9, 0.9, "WHAT BROKE, AND WHAT IT TAUGHT US", 34, True, INK, PP_ALIGN.LEFT, HF, spc=300)
txt(s, 0.72, 1.92, 11.9, 0.45, "THE TEST AND FAILURE RECORD, AUGUST TO OCTOBER 2026", 17, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.72, 2.55, 8.0, 1.3, "Ten root-caused failures, four field campaigns, and the rules each one left behind. Every entry here happened on this hardware and was reproduced or root-caused before it was written down. The New Mexico drive test will be added when it is complete.", 13, False, BODY)
txt(s, 8.3, 4.0, 4.3, 2.6, "Deo Grace Mwala\nJosiah Horn\nVictor Okwonna\nCannon Thomas\n\nSponsor: Dr. Richard Gale\nOctober 2026", 13, False, BODY, PP_ALIGN.LEFT, MONO)
notes(s, "Open with the thesis: a system is only as deployable as its failures are diagnosable. This deck is the evidence that ours are.")

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

# ============ 8 BATTERY DEATH ============
s = slide(); frame(s, "part i - the failures", "DEO")
head(s, "Failures 8-10: battery death reverts config")
rows = [["Date", "Radio", "What reverted", "How it was found"],
        ["Sep 30", "Both", "RG: channels. SF: everything (channel, role, Bluetooth, telemetry, owner)", "Healthy screens, total silence; peer missing from node tables"],
        ["Oct 17", "SF (EA:D4)", "Bluetooth mode, channel (906.875), owner name", "Display looping: encrypted=1 bonded=0, write rc=261, disconnect 534"],
        ["Oct 24", "SF (EA:D4)", "Channel + key, precision, Bluetooth, cadence, owner, canned messages, node DB", "Routine diagnostic before the New Mexico test; role survived"]]
table(s, 0.55, 1.35, 12.2, rows, [1.2, 1.4, 5.4, 4.2], fs=11, rh=0.62)
card(s, 0.55, 4.05, 6.0, 2.45, "Mechanism - mitigated, not fixed", "A brownout mid-write corrupts the config records in flash; at the next boot the firmware substitutes compiled-in defaults and saves them. This happens inside stock Meshtastic, which we do not fork, so we cannot prevent it. What we did is make it cheap: detectable in seconds and recoverable in a minute, without a laptop reflash.", ACC, 13.5, 12)
card(s, 6.75, 4.05, 6.0, 2.45, "The mitigation stack", "Detect in 2 s: the OLED pre-flight. Recover in 90 s: a full config snapshot per radio (--export-config / --configure) replaces the four-command recipe; the phone app's channel QR is the no-laptop path. Rule: re-run the WHOLE block, reverts come in batches. Never store a radio flat.", GREEN, 13.5, 12)
notes(s, "Be precise on stage: this is mitigated, not fixed. The corruption lives in the vendor firmware. Our contribution is that it went from a lost test morning to a non-event.")

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

# ============ 11 FAILURE -> RULE MAP ============
s = slide(); frame(s, "part i - the failures")
head(s, "Every failure became a rule")
rows = [["Failure", "Rule or feature it produced", "Where it lives now"],
        ["Boot-loop", "pioarduino + dio_opi; vendor IDF config is ground truth", "platformio.ini, manual 14"],
        ["Bonded radio invisible", "Just-Works pairing, no stored bond, one teardown path", "ble_link.cpp, manual 8"],
        ["First-drive faults", "Precision 32, 10 s GPS, km/h decode, deadband; validate on the road", "Provisioning recipe, node_table.cpp"],
        ["Wrong flash", "Identify by MAC before any upload; never auto-pick a port", "Manual 14.2 fleet table"],
        ["Lying CLI", "Read back every write; the OLED outranks the CLI", "Manual 16, entry 6"],
        ["Silent frequency revert", "Pre-flight: both OLEDs read 912.875", "User guide 3, manual 7"],
        ["Battery death reverts", "Config snapshots; re-run the whole block; never store flat", "hardware/*-config.yaml"],
        ["Hand-rotated compass", "Course-up compass; cadence-aware staleness", "ui_render.cpp, manual 9"],
        ["Night before the canyon", "Flashlight test, plug orientation, the 261 signature", "Manual 16, entries 9-10"]]
table(s, 0.55, 1.3, 12.2, rows, [3.0, 5.6, 3.6], fs=11, rh=0.52)
notes(s, "The point of the deck in one table: ten failures, ten rules, every rule with an address in the codebase or the manual.")

# ============ 12 TESTS SO FAR ============
s = slide(); frame(s, "part ii - the tests", "CANNON")
head(s, "The test campaigns so far")
rows = [["Date", "Campaign", "Environment", "Key result"],
        ["Aug 31", "Bench, end-to-end", "Desk", "Live GPS decoded radio-to-display; link held across the room"],
        ["Sep 1", "First drive", "Town", "Pipeline works at speed; five faults found (sheet 5)"],
        ["Sep 25", "Two-radio link", "Desk", "Round-trip traceroute 6.75 / 5.75 dB after the slot fix"],
        ["Oct 4", "Night convoy drive", "Town", "Stale onset ~0.5 mi; course-up and cadence-aware cue born"],
        ["Oct 5", "Open-road range", "Flat farm road", "Full tracking to 3.26 mi; stale edge 3.75 mi; auto-reacquisition"],
        ["Oct 18", "Canyon range", "Ceta Canyon", "Stale from 1.29 mi; packet at 4.28; 7-min outage healed; rim antenna 4.7 mi"],
        ["pending", "New Mexico maximum", "Open highway", "Prediction: beats 3.75 mi - to be added"]]
table(s, 0.55, 1.3, 12.2, rows, [1.1, 2.4, 2.1, 6.6], fs=11, rh=0.6)
notes(s, "Seven campaigns. Each one found something the previous one could not. The last row is reserved.")

# ============ 13 RANGE GRAPH ============
s = slide(); frame(s, "part ii - the tests")
head(s, "What the range tests measured")
s.shapes.add_picture("deck/g_onset4.png", Inches(1.7), Inches(1.4), width=Inches(9.9))
txt(s, 0.55, 6.4, 12.2, 0.4, "SAME RADIOS, FOUR GEOMETRIES: 0.5 MI TO 4.7 MI. TERRAIN AND ANTENNA HEIGHT SET THE RANGE, NOT THE HARDWARE.", 10.5, True, MUT, PP_ALIGN.CENTER, MONO)
notes(s, "The measured envelope. Every bar is a different day, same two radios, same settings - verified by post-test audit.")

# ============ 14 CANYON ============
s = slide(); frame(s, "part ii - the tests")
head(s, "The hardest test: Ceta Canyon, October 18")
s.shapes.add_picture("deck/g_timeline.png", Inches(0.55), Inches(1.3), width=Inches(8.0))
card(s, 8.8, 1.3, 4.0, 3.6, "What it proved", "Behind rock the link is intermittent at any distance: stale from 1.29 mi, yet a packet landed at 4.28 mi through a gap. The longest silence ran seven minutes and was healed by one packet with no operator action. Both radios audited clean afterward: terrain, not hardware. The rim antenna held 4.7 mi - the quantitative case for the repeater.", INK, 13.5, 11.5)
notes(s, "Red stale, green live. The 7:30 age reset is the finding: intermittent, not binary.")

# ============ 15 PRE-DRIVE DIAGNOSTIC: DISPLAYS ============
s = slide(); frame(s, "part ii - the tests", "DEO")
head(s, "Pre-drive diagnostic, Oct 24: the displays")
s.shapes.add_picture("deck/g_lcddiag.png", Inches(0.55), Inches(1.25), width=Inches(8.3))
card(s, 9.05, 1.25, 3.75, 3.1, "What the serial logs proved", "Both displays booted clean, paired in under 8 s (encrypted=1 bonded=0, every config write status 0), completed the config dump, built the correct node table (SF/RG), and held the link at heartbeat state 3 with zero rescans. Display 1 again needed a USB-C plug flip before it enumerated.", GREEN, 13, 11)
card(s, 0.55, 4.55, 12.25, 1.75, "The observation: 0.21 mi between two radios on one desk", "The displays were right and the GPS fixes were wrong. Indoors, SF's fix scattered 100 to 400 m between packets with 1.4 m/s of phantom speed; RG later reported a coherent 50 mph eastbound drive for a minute before snapping home. A marginal fix produces fake velocity, not just jitter, and dead reckoning faithfully projects it. Fixes shipped the same hour: the closing/apart line reads \"holding\" when both cars are parked; the distance stays honest. Rule: judge a bench distance only with sky view.", RED, 13, 11.5)
notes(s, "This is the display track's own verification record: the links and the firmware were fine; the data they rendered was bad because the radios' GPS receivers were indoors. The graph is parsed straight from the archived serial logs.")

# ============ 16 PRE-DRIVE DIAGNOSTIC: RADIOS ============
s = slide(); frame(s, "part ii - the tests", "DEO")
head(s, "Pre-drive diagnostic, Oct 24: the radios")
rows = [["Check", "SF (EA:D4)", "RG (BB:5C)"],
        ["Channel 0", "Group9, 32-byte key, precision 32", "Group9, 32-byte key, precision 32"],
        ["Role / Bluetooth", "CLIENT_MUTE / No PIN", "CLIENT_MUTE / No PIN"],
        ["Position cadence", "60 s, smart 10 s / 20 m, GPS 10 s", "60 s, smart 10 s / 20 m, GPS 10 s"],
        ["Telemetry heartbeat", "was OFF (leftover of the morning revert): set to 300 s", "300 s"],
        ["Owner", "SF / SF", "was \"Meshtastic bb5c\": set to RG / RG"],
        ["Battery", "96 % (4.15 V)", "69 % (3.88 V): charge before the drive"],
        ["Own GPS, indoors", "fix at 14:27, alt 1398 m", "no fix: the radio that showed the phantom drive"],
        ["Heard the partner", "RG 1.1 min ago, 6.25 dB", "SF 0.6 min ago, 6.5 dB"],
        ["OLED LoRa screen", "912.875 MHz", "912.875 MHz"]]
table(s, 0.55, 1.3, 12.2, rows, [2.6, 4.8, 4.8], fs=11, rh=0.46)
card(s, 0.55, 6.0, 12.2, 0.72, "Result", "Both radios fully provisioned and in agreement; link at the September figure (~6.5 dB); config snapshots re-exported. Both displays showed the link on the first power-cycle after unplugging.", GREEN, 12, 11)
notes(s, "Same diagnostic as the morning's, run on both radios at 14:27 before the New Mexico drive. Two leftovers corrected and read back.")

# ============ 17 NEW MEXICO PLACEHOLDER ============
s = slide(); frame(s, "part ii - the tests", "VICTOR")
head(s, "New Mexico maximum-range test - results pending")
rect(s, 0.55, 1.35, 12.2, 5.1, CARD, RULE, 1.25)
txt(s, 0.8, 1.55, 11.7, 0.5, "EXPERIMENT A - TO BE COMPLETED", 15, True, ACC, PP_ALIGN.LEFT, HF, spc=100)
txt(s, 0.8, 2.1, 11.7, 0.9, "Flat highway, clear Fresnel zone, drive until the catches stop. Prediction written before the test: beats the 3.75 mi flat-ground edge; with any elevation on one end, approaches the 4.7 mi rim figure or better.", 12.5, False, BODY)
rows = [["Measurement", "Open road (10-05)", "Canyon (10-18)", "New Mexico"],
        ["Full-health range", "3.26 mi", "4.7 mi (rim LOS)", "____"],
        ["First staleness", "3.75 mi", "1.29 mi", "____"],
        ["Longest silence", "~2 min", "7 min", "____"],
        ["Reacquired by (inbound)", "0.85 mi", "2.90 mi", "____"],
        ["Pre-test audit", "clean", "clean", "SF re-provisioned 10-24 after revert"]]
table(s, 0.8, 3.15, 11.7, rows, [3.2, 2.6, 2.6, 3.3], fs=11.5, rh=0.5)
notes(s, "Reserved sheet. Fill the right-hand column from the screen footage when the drive is done; the pre-test audit row is already true.")

# ============ 16 CLOSE ============
s = slide(); frame(s, "part ii - the tests")
head(s, "What the failures bought")
stats = [("10", "root-caused failures, each with a written signature and recovery"),
         ("10", "rules or features that exist only because something broke"),
         ("0", "reflashes needed for any configuration failure - all are re-provisioning"),
         ("90 s", "to recover a fully reverted radio today, versus a lost morning in September"),
         ("2 s", "pre-flight check that would have caught every field-day failure so far"),
         ("4.7 mi", "measured reach, with the honest envelope 0.5-4.7 mi by terrain")]
pos = [(0.55, 1.35), (4.85, 1.35), (9.15, 1.35), (0.55, 3.95), (4.85, 3.95), (9.15, 3.95)]
for (big, small), (x, y) in zip(stats, pos):
    rect(s, x, y, 3.65, 2.35, CARD, RULE, 1.0)
    txt(s, x, y+0.2, 3.65, 0.95, big, 36, True, ACC, PP_ALIGN.CENTER, HF)
    txt(s, x+0.25, y+1.12, 3.15, 1.15, small, 11.5, False, BODY, PP_ALIGN.CENTER)
rect(s, 0.55, 6.4, 12.2, 0.4, INK)
txt(s, 0.8, 6.46, 11.7, 0.3, "EVERY FAILURE BECAME A RULE; EVERY RULE BECAME A TEST.", 12, True, PAPER, PP_ALIGN.CENTER, HF)
notes(s, "Close on the numbers. The system is not one that never fails; it is one whose failures name themselves.")

prs.save("Group9_TestsAndFailures.pptx")
import os
print("saved", os.path.getsize("Group9_TestsAndFailures.pptx")//1024, "KB, slides:", len(prs.slides._sldIdLst))
