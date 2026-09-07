// Week 3 deck, rev C — engineering drawing-set style.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

const INK = "16213D", PAPER = "FFFFFF", ACC = "E58E1A", MUT = "5E6B85";
const RULE = "9AA7BE", CARD = "F2F5FA", CODEBG = "1B2440", ICE = "C9D8F0";
const M = { DEO: "1199BD", JOSIAH: "6D4BDB", VICTOR: "E58E1A", CANNON: "D9488C" };
const HFONT = "Arial", BFONT = "Arial", MONO = "Courier New";
const D3 = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/scratchpad/deck3/";
const MPNG = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/scratchpad/mermaid_png/";
const SYS = "C:/Users/deogr/Documents/Fall Project/Off-Grid Vehicle dection project/docs/system-diagram.png";

const TOTAL = 14;
let sheetNo = 0;

// Drawing frame + title-block footer on every sheet.
function frame(s, owner, sheetTitle) {
  sheetNo++;
  s.background = { color: PAPER };
  s.addShape("rect", { x: 0.18, y: 0.16, w: 12.97, h: 7.18, fill: { type: "none" }, line: { color: INK, width: 1.75 } });
  s.addShape("line", { x: 0.18, y: 6.86, w: 12.97, h: 0, line: { color: INK, width: 1 } });
  // footer title block
  s.addText("GROUP 9  |  OFF-GRID VEHICLE TRACKER", { x: 0.35, y: 6.94, w: 4.6, h: 0.32, fontSize: 9,
    fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addText(sheetTitle.toUpperCase(), { x: 5.0, y: 6.94, w: 4.6, h: 0.32, align: "center", fontSize: 9,
    fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addText("SHEET " + String(sheetNo).padStart(2, "0") + "/" + TOTAL + "  REV C  2026-09-07",
    { x: 9.7, y: 6.94, w: 3.3, h: 0.32, align: "right", fontSize: 9, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  if (owner) {
    s.addShape("rect", { x: 10.55, y: 0.38, w: 2.35, h: 0.46, fill: { color: PAPER }, line: { color: M[owner], width: 1.5 } });
    s.addText("OWNER: " + owner, { x: 10.55, y: 0.44, w: 2.35, h: 0.34, align: "center", fontSize: 11, bold: true,
      color: M[owner], fontFace: MONO, isTextBox: true, margin: 0 });
  }
}
function title(s, txt) {
  s.addText(txt.toUpperCase(), { x: 0.5, y: 0.36, w: 9.9, h: 0.62, fontSize: 23, bold: true, charSpacing: 2,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
}
function codebox(s, x, y, w, h, label, code, labelColor) {
  s.addShape("rect", { x, y, w, h, fill: { color: CODEBG } });
  s.addText(label, { x: x + 0.15, y: y + 0.07, w: w - 0.3, h: 0.26, fontSize: 10, bold: true,
    color: labelColor || ACC, fontFace: MONO, isTextBox: true, margin: 0 });
  s.addText(code, { x: x + 0.15, y: y + 0.35, w: w - 0.3, h: h - 0.45, fontSize: 10,
    fontFace: MONO, color: ICE, isTextBox: true, margin: 0, valign: "top" });
}
function harrow(s, x, y, w, color) {
  s.addShape("line", { x, y, w, h: 0, line: { color: color || INK, width: 2.25, endArrowType: "triangle" } });
}
function varrow(s, x, y, h, color) {
  s.addShape("line", { x, y, w: 0, h, line: { color: color || INK, width: 2.25, endArrowType: "triangle" } });
}
function pic(s, path, x, y, w, h, cap) {
  s.addImage({ path, x, y, w, h });
  s.addShape("rect", { x, y, w, h, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  if (cap) s.addText(cap, { x, y: y + h + 0.03, w, h: 0.3, fontSize: 9.5, color: MUT,
    align: "center", fontFace: MONO, isTextBox: true, margin: 0 });
}
const B = (text, last) => ({ text, options: { bullet: { code: "25AA" }, breakLine: !last, paraSpaceAfter: last ? 0 : 6, indentLevel: 0 } });

// ============================================================ SHEET 01 · COVER
{
  const s = pres.addSlide();
  frame(s, null, "design review, week 3");
  // graph-paper grid
  for (let gx = 0.68; gx < 13.0; gx += 0.5)
    s.addShape("line", { x: gx, y: 0.16, w: 0, h: 6.7, line: { color: "E8EDF5", width: 0.5 } });
  for (let gy = 0.66; gy < 6.86; gy += 0.5)
    s.addShape("line", { x: 0.18, y: gy, w: 12.97, h: 0, line: { color: "E8EDF5", width: 0.5 } });
  s.addText("OFF-GRID VEHICLE TRACKER", { x: 0.7, y: 1.15, w: 11.9, h: 0.9, fontSize: 44, bold: true,
    charSpacing: 3, fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText("WEEK 3 DESIGN REVIEW: A WORKING TRACKER, END TO END", { x: 0.72, y: 2.05, w: 11.9, h: 0.45,
    fontSize: 17, bold: true, charSpacing: 1, fontFace: HFONT, color: ACC, isTextBox: true, margin: 0 });
  s.addText("The display now shows a live vehicle: real packets, real navigation math, a screen that moves every second. Each section: architecture first, then the working hardware and its code.",
    { x: 0.72, y: 2.65, w: 8.3, h: 1.15, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  // responsibility table (revision-table style)
  const rows = [
    ["OWNER", "SUBSYSTEM", "SCOPE THIS WEEK"],
    ["DEO", "Backend, protocol/", "system diagram, BLE link, decode, TrackerState"],
    ["JOSIAH", "Frontend, ui/ and nav/", "arrow math, two-page UI, dead reckoning"],
    ["VICTOR", "Radio and PHY", "link physics: real time versus 10 seconds"],
    ["CANNON", "Integration and test", "the constraints ledger, test sequence"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 10 : 11.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 0 ? MONO : BFONT,
      color: i === 0 ? PAPER : (j === 0 ? (M[r[0]] || INK) : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.72, y: 4.0, w: 8.3, colW: [1.35, 2.75, 4.2], rowH: 0.42,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  // title block, drawing style, bottom right
  const blk = [["PROJECT", "Off-Grid Vehicle Tracker"], ["SPONSOR", "Dr. Richard Gale"],
    ["COURSE", "Capstone Project Lab"], ["STATUS", "29% vs 19% target, ahead"],
    ["HOURS", "60 of 768 logged"], ["DATE", "2026-09-07"]];
  s.addShape("rect", { x: 9.55, y: 2.65, w: 3.3, h: 3.55, fill: { color: PAPER }, line: { color: INK, width: 1.25 } });
  blk.forEach((r, i) => {
    const y = 2.72 + i * 0.575;
    if (i) s.addShape("line", { x: 9.55, y: y - 0.035, w: 3.3, h: 0, line: { color: RULE, width: 0.75 } });
    s.addText(r[0], { x: 9.7, y, w: 1.25, h: 0.28, fontSize: 9, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
    s.addText(r[1], { x: 9.7, y: y + 0.24, w: 3.05, h: 0.3, fontSize: 10.5, fontFace: BFONT, color: INK, isTextBox: true, margin: 0 });
  });
}

// ============================================================ SHEET 02 · DEO, complete system
{
  const s = pres.addSlide();
  frame(s, "DEO", "complete system diagram");
  title(s, "The Complete System on One Sheet");
  s.addImage({ path: SYS, x: 0.5, y: 1.1, w: 5.62, h: 5.65 });
  s.addShape("rect", { x: 0.5, y: 1.1, w: 5.62, h: 5.65, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText("READING ORDER", { x: 6.5, y: 1.2, w: 5.0, h: 0.32, fontSize: 13, bold: true, charSpacing: 2,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    B("Left: one vehicle's hardware. GNSS feeds the radio; the radio drives the roof antenna."),
    B("Right: the display firmware. Protocol writes TrackerState; navigation reads it. One writer, one reader."),
    B("Bottom: the telecom view. A 40 byte payload on a PHY that decodes 15 dB below the noise."),
    B("Vehicle B is an identical copy. No server, no master, no single point of failure.", true),
  ], { x: 6.5, y: 1.6, w: 6.1, h: 3.1, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 6.5, y: 5.0, w: 6.1, h: 1.6, fill: { color: INK } });
  s.addText([
    { text: "WHY THIS SHAPE", options: { bold: true, fontSize: 12, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Everything hard about long-range radio ships pre-tested in Meshtastic. The chains on the right are the only custom code, and they meet at one struct.", options: { color: PAPER, fontFace: BFONT } },
  ], { x: 6.75, y: 5.15, w: 5.6, h: 1.35, fontSize: 12.5, isTextBox: true, margin: 0 });
  s.addNotes("Open with the whole system so every later sheet has a home. Walk left region (hardware per vehicle), right region (firmware split with TrackerState as the single interface), bottom strip (telecom layers). Close on symmetry: vehicle B is identical, nothing is a server.");
}

// ============================================================ SHEET 03 · DEO, inside the transceiver
{
  const s = pres.addSlide();
  frame(s, "DEO", "inside the sx1262");
  title(s, "Inside the Transceiver (Datasheet Rev 2.2)");
  s.addImage({ path: D3 + "fig_block.png", x: 0.5, y: 1.15, w: 7.35, h: 3.5 });
  s.addShape("rect", { x: 0.5, y: 1.15, w: 7.35, h: 3.5, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText("SX1262 BLOCK DIAGRAM, DS FIG 4-1 p.23. TWO MODEMS SHARE ONE FRONT END; WE USE ONLY THE LoRa ONE.",
    { x: 0.5, y: 4.7, w: 7.35, h: 0.24, fontSize: 8, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addImage({ path: D3 + "fig_modes.png", x: 8.3, y: 1.15, w: 3.5, h: 3.5 });
  s.addShape("rect", { x: 8.3, y: 1.15, w: 3.5, h: 3.5, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText("OPERATING MODES, DS FIG 9-1 p.64", { x: 8.3, y: 4.7, w: 3.5, h: 0.24, fontSize: 8,
    fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  // one broadcast traced over the state machine
  const steps = [["RX", "always listening"], ["CAD", "channel clear? 6.1.5 p.41"], ["FS", "PLL locks channel"],
    ["TX", "chirps, ~0.5 s"], ["TxDone", "IRQ on DIO1"], ["RX", "back to listening"]];
  steps.forEach((st, i) => {
    const x = 0.5 + i * 2.1;
    s.addShape("rect", { x, y: 5.1, w: 1.85, h: 0.68, fill: { color: CARD }, line: { color: ACC, width: 1.25 } });
    s.addText([{ text: st[0], options: { bold: true, fontFace: MONO, breakLine: true } },
      { text: st[1], options: { fontSize: 8, color: MUT } }],
      { x: x + 0.06, y: 5.13, w: 1.73, h: 0.62, fontSize: 10.5, fontFace: BFONT, color: INK,
        isTextBox: true, margin: 0, align: "center" });
    if (i < 5) harrow(s, x + 1.85, 5.44, 0.25, ACC);
  });
  s.addText("ONE POSITION BROADCAST TRACED ON THE STATE MACHINE. CAD IS THE PHYSICAL LISTEN-BEFORE-TALK: BELOW THE NOISE FLOOR RSSI IS USELESS, SO THE CHIP CORRELATES FOR LoRa SYMBOLS INSTEAD.",
    { x: 0.5, y: 5.85, w: 12.35, h: 0.24, fontSize: 8, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  codebox(s, 0.5, 6.15, 8.1, 0.62, "meshtastic RadioInterface.cpp  how region US becomes a frequency",
`RDEF(US, 902.0f, 928.0f, ...);  freq = start + bw/2000 + hash(name)*(bw/1000);`, ACC);
  s.addText("Both radios hash the same channel name, so they meet on the same frequency with no coordination message. Full walkthrough: docs/RADIO_PHY_DEEP_DIVE.pdf",
    { x: 8.75, y: 6.15, w: 4.1, h: 0.62, fontSize: 8.5, fontFace: BFONT, color: MUT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Presented by Deo as the descent from the system map into the machine my protocol rides on. This sheet is the silicon-level story, all from the Semtech datasheet in our repo of references. Left: the block diagram - antenna, matching, LNA, mixer, ADC, then everything is digital: the LoRa modem correlates chirps (that is the processing gain), the protocol engine handles preamble, header, FEC and CRC, and a 256-byte buffer meets the ESP32 over SPI. Note the FSK modem sitting beside the LoRa modem: present, powered, and unused - FSK needs positive SNR, LoRa decodes at minus 17.5 dB. Right: the operating-mode state machine, and below it one of our broadcasts traced across it: park in RX, CAD to check the channel (the physical CSMA - below the noise floor RSSI is meaningless so the chip listens for LoRa symbols), FS while the PLL locks, half a second of TX, TxDone interrupt, back to RX. Bottom code: the region line that sets 902 to 928 MHz and the hash that picks the channel - both radios compute the same hash from the channel name, so the shared URL is simultaneously the encryption domain and the frequency agreement. Close by handing the physics forward: Victor will quantify what this silicon buys and what it costs.");
}

// ============================================================ SHEET 04 · DEO, backend architecture
{
  const s = pres.addSlide();
  frame(s, "DEO", "backend architecture");
  title(s, "Backend: the Data Spine");
  s.addImage({ path: MPNG + "diag5.png", x: 0.65, y: 1.15, w: 11.9, h: 3.36 });
  s.addShape("rect", { x: 0.65, y: 1.15, w: 11.9, h: 3.36, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText([
    B("ble_link connects by remembered address, encrypts, subscribes, drains. proto_decode names the bytes. node_table keeps honest fixes and publishes TrackerState v2."),
    B("Road-tested: the link reconnects itself, and stale re-broadcasts can no longer pose as fresh data.", true),
  ], { x: 0.65, y: 4.85, w: 12.0, h: 1.6, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addNotes("Zoom from sheet 02 into the firmware. Emphasize the single mutex-protected interface and that the whole left chain is proven on the road, not the bench: automatic reconnection, duplicate re-broadcast detection for honest ages, and the GPS clock guard.");
}

// ============================================================ SHEET 04 · DEO, code path
{
  const s = pres.addSlide();
  frame(s, "DEO", "backend code path");
  title(s, "How the Pieces Connect in Code");
  codebox(s, 0.5, 1.15, 6.05, 1.5, "ble_link.cpp  drain the radio's GATT queue",
`for (;;) {
  NimBLEAttValue v = s_fromRadio->readValue();
  if (v.size() == 0) break;      // queue empty
  proto_decode_from_radio(v.data(), v.size());
}`, M.DEO);
  codebox(s, 6.95, 1.15, 5.9, 1.5, "proto_decode.cpp  bytes to named fields",
`if (pb_decode(&is, meshtastic_Position_fields, &pos))
  node_table_position(pkt->from,
      pos->latitude_i, pos->longitude_i,
      pos->ground_speed, pos->time);`, M.DEO);
  varrow(s, 3.5, 2.65, 0.38, M.DEO);
  varrow(s, 9.9, 2.65, 0.38, M.DEO);
  codebox(s, 0.5, 3.03, 6.05, 1.55, "node_table.cpp  publish the contract, 1 Hz",
`TrackerState st;
st.self = s_self.fix;   st.partner = s_partner.fix;
st.ble_connected = connected;
st.utc_epoch = s_utc_epoch;      // GPS wall clock
tracker_store_set(&st);          // the ONE writer`, M.DEO);
  codebox(s, 6.95, 3.03, 5.9, 1.55, "ui_render.cpp  frontend picks it up, 2 Hz",
`tracker_store_get(&st);          // the ONE reader
dr_apply(&st);   // dead-reckon fixes forward
NavOutput nav = nav_compute(&st);
// arrow angle, distance, ages, clock`, M.JOSIAH);
  harrow(s, 6.58, 3.8, 0.34, INK);
  s.addText("MUTEX BOUNDARY", { x: 5.55, y: 4.02, w: 2.4, h: 0.24, fontSize: 8.5, bold: true, color: MUT,
    align: "center", fontFace: MONO, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 4.95, w: 12.35, h: 1.7, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  s.addText([
    { text: "Four files, one direction of flow, one struct. The halves meet only at the store functions; the mutex cannot be bypassed.", options: { fontFace: BFONT, breakLine: true, paraSpaceAfter: 7 } },
    { text: "Road hardening: km/h converted at the door, jitter deadband, duplicate detection, a clock that cannot run backwards.", options: { fontFace: BFONT } },
  ], { x: 0.8, y: 5.18, w: 11.75, h: 1.3, fontSize: 13, color: "222A3F", isTextBox: true, margin: 0 });
  s.addNotes("Read the arrows aloud: the GATT loop reads until the radio reports empty; nanopb decodes with code generated from Meshtastic's own schema; node_table publishes once per second; the UI copies its own snapshot at 2 Hz, projects it forward, and computes the arrow. Every hardening item in the bottom card came out of an actual drive test.");
}

// ============================================================ SHEET 06 · JOSIAH, frontend architecture
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "frontend architecture");
  title(s, "Frontend: From Struct to Arrow");
  function fbox(x, y, w, h, main, sub, line) {
    s.addShape("rect", { x, y, w, h, fill: { color: PAPER }, line: { color: line || M.JOSIAH, width: 1.5 } });
    s.addText([{ text: main, options: { bold: true, breakLine: true } },
      { text: sub, options: { fontSize: 9.5, color: MUT } }],
      { x: x + 0.08, y, w: w - 0.16, h, fontSize: 11.5, fontFace: BFONT, color: INK,
        isTextBox: true, margin: 0, align: "center", valign: "middle" });
  }
  fbox(0.5, 1.25, 2.3, 0.95, "TrackerState v2", "snapshot copy under mutex", INK);
  harrow(s, 2.8, 1.72, 0.5, M.JOSIAH);
  fbox(3.3, 1.25, 2.4, 0.95, "dr_apply()", "project both fixes forward");
  harrow(s, 5.7, 1.72, 0.5, M.JOSIAH);
  fbox(6.2, 1.25, 2.4, 0.95, "nav_compute()", "distance, bearing, arrow");
  harrow(s, 8.6, 1.72, 0.5, M.JOSIAH);
  fbox(9.1, 1.25, 3.6, 0.95, "render at 2 Hz", "compass page and status page, KEY toggles, hold resets");
  codebox(s, 0.5, 2.55, 6.05, 1.35, "nav.c  the arrow in three lines",
`d       = haversine(self, partner);       // meters
bearing = initial_bearing(self, partner);  // deg
arrow   = wrap180(bearing - self.course);  // 0 = ahead`, M.JOSIAH);
  codebox(s, 6.95, 2.55, 5.9, 1.35, "dead_reckon.c  1 Hz motion between fixes",
`d = speed * min(age, 120);    // meters traveled
lat += d*cos(course)/111320;
lon += d*sin(course)/(111320*cos(lat));`, M.JOSIAH);
  s.addText([
    B("Heading from GPS course over ground: no magnetometer in a steel cab. Below 5 mph, north-up rose."),
    B("Every element is a state machine on the struct: CHANGE COURSE, chevrons, STALE past 120 s, position-derived clock."),
    B("Pure C, no hardware dependencies: 12 of 12 native tests pass on a laptop.", true),
  ], { x: 0.5, y: 4.2, w: 12.35, h: 1.45, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.85, w: 12.35, h: 0.85, fill: { color: INK } });
  s.addText("Measurements every 10 s. The display projects both vehicles every second, and each real fix snaps it back to truth.",
    { x: 0.8, y: 5.97, w: 11.75, h: 0.65, fontSize: 13, color: PAPER, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Sector flow left to right, then the two fragments that do all the work. Testability is the design win: nav.c and dead_reckon.c run on the laptop with zero hardware, which is how the whole UI was built before the radio link existed.");
}

// ============================================================ SHEET 07 · JOSIAH, photos
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "the ui on real packets");
  title(s, "The UI, Running on Real Packets");
  pic(s, D3 + "p_compass.jpg", 0.5, 1.2, 4.35, 3.59, "Driving view. Partner 2.41 mi, CHANGE COURSE with turn chevron, age 15 s");
  pic(s, D3 + "p_close.jpg", 0.85, 5.35, 1.72, 1.25, "Close range, 0.2 mi");
  pic(s, D3 + "p_stopped.jpg", 5.15, 1.2, 4.3, 2.81, "Stopped: automatic north-up rose fallback");
  pic(s, D3 + "p_status.jpg", 5.15, 4.42, 3.15, 2.12, "Status page: live ME and PTR coordinates");
  s.addShape("rect", { x: 9.75, y: 1.2, w: 3.1, h: 5.5, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  s.addText("WHY THESE SHOTS MATTER", { x: 9.95, y: 1.35, w: 2.7, h: 0.55, fontSize: 12, bold: true, charSpacing: 1,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    B("No simulator: every value arrived by radio."),
    B("Reflective panel: sharper in sunlight, built for a dash."),
    B("The age readout is the honesty metric."),
    B("Banner, chevron, rose: state machines on live data.", true),
  ], { x: 9.95, y: 1.95, w: 2.7, h: 4.6, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addNotes("All four photos show the real display on decoded radio packets. Point at the state machine working: banner and chevron in the driving view, rose fallback when stopped, and the diagnostic page with raw coordinates that we use for debugging.");
}

// ============================================================ SHEET 08 · VICTOR, radio
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "radio and phy");
  title(s, "Radio and PHY: the Long-Range Link");
  s.addText("RADIO NODE, HELTEC V4 RUNNING STOCK MESHTASTIC", { x: 0.5, y: 1.08, w: 8.0, h: 0.3, fontSize: 11, bold: true,
    charSpacing: 1, fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addImage({ path: MPNG + "diag2.png", x: 0.5, y: 1.42, w: 7.6, h: 1.55 });
  s.addShape("rect", { x: 0.5, y: 1.42, w: 7.6, h: 1.55, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  pic(s, D3 + "p_rig.jpg", 8.4, 1.08, 1.95, 2.6, "The rig with 915 MHz antenna");
  pic(s, D3 + "p_oled.jpg", 10.55, 1.08, 2.25, 1.18, "OLED: 9 satellites, ChUtil 0%");
  s.addText([
    B("LONG_FAST: SF11 over 250 kHz, FEC 4/5, 915 MHz ISM, private AES-256 channel, full precision."),
    B("Smart broadcast 10 s / 20 m moving, 60 s parked. GPS refresh 10 s: every broadcast carries a new fix."),
    B("The OLED is the free field debugger: satellites, nodes, utilization, last RSSI.", true),
  ], { x: 0.5, y: 3.25, w: 7.7, h: 1.9, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.3, w: 12.35, h: 1.4, fill: { color: "FDF3E3" }, line: { color: ACC, width: 1.25 } });
  s.addText([
    { text: "PROVISIONING DISCIPLINE (hardware/README.md)", options: { bold: true, fontSize: 11, color: "B06207", fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Radio 2 joins with the exact channel URL (it carries the AES key). Verify every CLI write; always name the upload port.", options: { fontFace: BFONT } },
  ], { x: 0.8, y: 5.44, w: 11.75, h: 1.15, fontSize: 12.5, color: "222A3F", isTextBox: true, margin: 0 });
  s.addNotes("Hardware diagram first, then the configuration that three road tests produced: 10 second smart broadcast matched by 10 second GPS refresh on a full-precision private channel. The amber card is the recipe that makes radio two a fifteen-minute job instead of a rediscovery project.");
}

// ============================================================ SHEET 09 · VICTOR, physics
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "link physics");
  title(s, "Real Time versus 10 Seconds: the Physics");
  function eq(y, label, cite, img, iw, ih) {
    s.addText(label, { x: 0.5, y, w: 2.7, h: 0.32, fontSize: 11, bold: true, color: INK,
      fontFace: MONO, isTextBox: true, margin: 0 });
    s.addText(cite, { x: 0.5, y: y + 0.3, w: 2.7, h: 0.24, fontSize: 8, color: MUT,
      fontFace: MONO, isTextBox: true, margin: 0 });
    s.addImage({ path: D3 + img, x: 3.35, y: y + 0.02, w: iw, h: ih });
  }
  eq(1.2, "EQ 1  AIRTIME", "DS 6.1.1 p.39 + AN1200.22", "eq_airtime.png", 8.9, 0.47);
  eq(2.0, "EQ 2  UTILIZATION", "Meshtastic docs, ~25% cap", "eq_util.png", 9.3, 0.43);
  eq(2.8, "EQ 3  SENSITIVITY", "DS Table 6-1 p.39, 3.5.3 p.20", "eq_sens.png", 9.3, 0.32);
  eq(3.55, "EQ 4  LATENCY", "DS 6.1.4 p.41 (airtime term)", "eq_latency.png", 9.3, 0.34);
  eq(4.3, "EQ 5  DEAD RECKONING", "dead_reckon.c, 12/12 tests", "eq_dr.png", 6.9, 0.4);
  s.addShape("rect", { x: 0.5, y: 5.2, w: 12.35, h: 1.5, fill: { color: INK } });
  s.addText([
    { text: "THE VERDICT", options: { bold: true, fontSize: 12, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Delivery is real time: about one second. Sampling is 10 s, because airtime is the currency and we bought range with it. Dead reckoning fills the gap at 1 Hz.", options: { color: PAPER, fontFace: BFONT } },
  ], { x: 0.8, y: 5.32, w: 11.75, h: 1.3, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("This sheet answers the question everyone asks: why not every second. Equation 1: at spreading factor 11 each symbol is 2048 chips, so one position costs about half a second of air. Equation 2: two vehicles at one hertz would occupy 100 percent of the channel; at ten seconds they occupy ten percent. Equation 3: the same slowness buys sensitivity of minus 131 dBm, fifteen decibels below thermal noise, which is the entire range budget. Equation 4: actual information latency is about one second. Equation 5: the display projects both vehicles forward every second between fixes. Marine AIS beacons every 2 to 30 seconds and every chartplotter animates between reports; we are in good company.");
}

// ============================================================ SHEET 10 · VICTOR, graphs + references
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "link behavior, graphed");
  title(s, "The Same Physics, Graphed");
  s.addImage({ path: D3 + "g_utilization.png", x: 0.5, y: 1.12, w: 5.9, h: 4.09 });
  s.addShape("rect", { x: 0.5, y: 1.12, w: 5.9, h: 4.09, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addImage({ path: D3 + "g_deadreckon.png", x: 6.9, y: 1.12, w: 5.9, h: 4.09 });
  s.addShape("rect", { x: 6.9, y: 1.12, w: 5.9, h: 4.09, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText("The update-rate wall: 1 s would take 100% of the channel. Our point: 10 s, 10%, under the enforced 25% ceiling.",
    { x: 0.5, y: 5.32, w: 5.9, h: 1.05, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addText("Raw fix: up to 200 m behind at 45 mph. Dead reckoning: bounded near 25 m, snapped to zero by each real fix.",
    { x: 6.9, y: 5.32, w: 5.9, h: 1.05, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("line", { x: 0.5, y: 6.42, w: 12.35, h: 0, line: { color: RULE, width: 0.75 } });
  s.addText("SOURCES  [1] Semtech SX1276 datasheet, SNR limit per spreading factor   [2] Semtech AN1200.22, LoRa modulation and airtime   [3] Meshtastic docs, LoRa config and duty limit   [4] ITU-R M.1371, AIS reporting intervals   (full citations in the notes)",
    { x: 0.5, y: 6.5, w: 12.35, h: 0.3, fontSize: 8.5, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addNotes("Two pictures replace ten minutes of argument. Left graph: utilization is inversely proportional to the interval; the 1 s point is literally impossible and the dashed line is Meshtastic's own 25 percent duty limit; we sit at 10 percent. Right graph: the sawtooth is the display error over time at 45 mph; orange is what holding the raw fix would show, up to 200 meters stale; navy is dead reckoning with a worst-case maneuver assumption of 0.5 m/s^2, bounded near 25 meters and typically a few meters in steady driving. Sources are on this sheet's reference list in the notes: the SNR-per-spreading-factor table and airtime equations are from Semtech's datasheet and AN1200.22, the duty limit and configuration from the Meshtastic documentation, and the AIS precedent from ITU-R M.1371.");
}

// ============================================================ SHEET 10 · CANNON, integration proven
{
  const s = pres.addSlide();
  frame(s, "CANNON", "integration, one device");
  title(s, "Integration: the Halves Are Joined");
  // integration stack, each layer with a status stamp
  const layers = [
    ["GPS to radio", "satellites acquired, fixes flowing over UART", "PROVEN", "own GPS: locked"],
    ["Radio to display", "BLE GATT link, automatic reconnect", "PROVEN", "radio link: connected"],
    ["Decode to TrackerState", "protobuf frames become live coordinates", "PROVEN", "ME 33.60719 -101.89643"],
    ["Navigation and UI", "state-driven pages, honest ages, local clock", "PROVEN", "6:59a CDT, age 55 s"],
    ["Partner over LoRa", "second radio joins the encrypted channel", "NEXT", "PTR no partner heard yet"]];
  layers.forEach((L, i) => {
    const y = 1.2 + i * 1.06, pending = L[2] === "NEXT";
    s.addShape("rect", { x: 0.5, y, w: 5.6, h: 0.88, fill: { color: pending ? PAPER : CARD },
      line: { color: pending ? ACC : M.CANNON, width: 1.25, ...(pending ? { dashType: "dash" } : {}) } });
    s.addText([{ text: L[0], options: { bold: true, breakLine: true } },
      { text: L[1], options: { fontSize: 9, color: MUT } }],
      { x: 0.65, y: y + 0.06, w: 3.6, h: 0.78, fontSize: 11, fontFace: BFONT, color: INK, isTextBox: true, margin: 0 });
    s.addText(L[2], { x: 4.35, y: y + 0.08, w: 0.85, h: 0.3, align: "center", fontSize: 9, bold: true,
      fontFace: MONO, color: pending ? "B06207" : "1F9D68", isTextBox: true, margin: 0 });
    s.addText('"' + L[3] + '"', { x: 4.32, y: y + 0.4, w: 1.72, h: 0.42, fontSize: 7.5,
      fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
    if (i < 4) varrow(s, 1.1, y + 0.88, 0.18, M.CANNON);
  });
  pic(s, D3 + "p_search.jpg", 6.4, 1.2, 1.95, 1.53, "Boot: link + GPS proven");
  pic(s, D3 + "p_overall.jpg", 8.5, 1.2, 2.1, 1.51, "ME 33.60719 -101.89643");
  s.addShape("rect", { x: 10.75, y: 1.2, w: 2.1, h: 2.0, fill: { color: CARD }, line: { color: "1F9D68", width: 1.25 } });
  s.addText("POSITION CROSS-CHECK", { x: 10.87, y: 1.3, w: 1.9, h: 0.5, fontSize: 10, bold: true,
    charSpacing: 1, fontFace: HFONT, color: "1F9D68", isTextBox: true, margin: 0 });
  s.addText("Same fix, same radio, two programs sharing no code. Agreement is the accuracy check.",
    { x: 10.87, y: 1.78, w: 1.88, h: 1.38, fontSize: 9.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addText("INDEPENDENT CLIENT: MESHTASTIC WEB APP, SAME RADIO, NODE ead4 CONNECTED",
    { x: 6.4, y: 3.28, w: 6.45, h: 0.24, fontSize: 8.5, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addImage({ path: D3 + "p_map_zoom.png", x: 6.4, y: 3.56, w: 4.35, h: 3.21 });
  s.addShape("rect", { x: 6.4, y: 3.56, w: 4.35, h: 3.21, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText("One device proves four of five layers. The dashed one waits only for radio two.",
    { x: 10.95, y: 3.56, w: 1.9, h: 3.21, fontSize: 10, fontFace: BFONT, color: MUT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("This sheet is the integration story: the two halves of the firmware are joined and running on real hardware. Walk the stack top to bottom, and point at the photo text that proves each layer: own GPS locked proves layer one, radio link connected proves layer two, the live coordinates prove decoding, and the clock reading Central time proves the navigation layer is deriving timezone from position. The dashed layer is the honest gap, and the display itself says it: no partner heard yet. The strategy: one device tracking itself exercises everything except the LoRa hop, so integration bugs get found cheaply before the two-vehicle test. Radio two closes the loop without changing a line of display code.");
}

// ============================================================ SHEET 11 · CANNON, constraints
{
  const s = pres.addSlide();
  frame(s, "CANNON", "integration constraints");
  title(s, "Integration Constraints: the Ledger");
  s.addImage({ path: MPNG + "diag1.png", x: 0.5, y: 1.1, w: 6.2, h: 2.12 });
  s.addShape("rect", { x: 0.5, y: 1.1, w: 6.2, h: 2.12, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText("Every constraint below was discovered on the bench or on the road, and each one shaped the design. None are theoretical.",
    { x: 7.0, y: 1.2, w: 5.75, h: 0.85, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addText("TEST SEQUENCE: provision radio 2, bench two-radio decode, two-vehicle drive test, range characterization.",
    { x: 7.0, y: 2.15, w: 5.75, h: 0.95, fontSize: 12, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
  const cons = [
    ["RADIO / PHY", "0.5 s airtime caps cadence at 10 s. Utilization under ~25%. No region, no transmit. Roof antenna is the biggest range factor."],
    ["GPS", "Needs sky view; cold start takes minutes. Indoor multipath fakes phantom speed (deadbanded). Fix rate must match broadcast rate."],
    ["BLE LINK", "The radio advertises only at boot: power both units together. One client at a time; a phone or USB session steals the link."],
    ["DISPLAY", "One-bit reflective panel: no grayscale, needs ambient light at night (edge light planned). 2 Hz redraw budget."],
    ["POWER", "Cheap 12 V USB adapters cut off on low draw: validate every adapter."],
    ["PROVISIONING", "Channel URL (the AES key) must match on every radio. Node IDs survive reflashes. Read back every write."]];
  cons.forEach((c, i) => {
    const x = 0.5 + (i % 3) * 4.2, y = 3.45 + Math.floor(i / 3) * 1.68;
    s.addShape("rect", { x, y, w: 4.0, h: 1.56, fill: { color: CARD }, line: { color: M.CANNON, width: 1.25 } });
    s.addText(c[0], { x: x + 0.14, y: y + 0.07, w: 3.7, h: 0.26, fontSize: 10.5, bold: true, color: M.CANNON,
      fontFace: MONO, isTextBox: true, margin: 0 });
    s.addText(c[1], { x: x + 0.14, y: y + 0.36, w: 3.74, h: 1.16, fontSize: 9.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  });
  s.addNotes("Each card becomes a line item in the test protocol. The strength of this slide is provenance: phantom speed, the advertise-once trap, the charger cutoff, and the configuration revert were all found by us, on our hardware, and every one is documented in the repository with its fix.");
}

// ============================================================ SHEET 11 · scoreboard
{
  const s = pres.addSlide();
  frame(s, null, "status and next steps");
  title(s, "Week 3 Status and What Comes Next");
  const stats = [["29%", "complete against a 19% week-three target"], ["60 h", "logged, eight hours per member this week"],
    ["12/12", "native unit tests passing"], ["10 s / 1 s", "measurement cadence / on-screen motion"]];
  stats.forEach((st, i) => {
    const x = 0.5 + i * 3.14;
    s.addShape("rect", { x, y: 1.2, w: 2.94, h: 1.5, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
    s.addText(st[0], { x: x + 0.2, y: 1.32, w: 2.6, h: 0.6, fontSize: 27, bold: true, color: INK,
      fontFace: HFONT, isTextBox: true, margin: 0 });
    s.addText(st[1], { x: x + 0.2, y: 1.95, w: 2.6, h: 0.65, fontSize: 10.5, color: MUT,
      fontFace: BFONT, isTextBox: true, margin: 0 });
  });
  s.addText("PROVEN END TO END THIS WEEK", { x: 0.5, y: 3.05, w: 6.0, h: 0.35, fontSize: 13, bold: true, charSpacing: 1,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    B("GPS fix to arrow, end to end, at 10 s cadence with 1 Hz projected motion."),
    B("Position-derived clock, honest ages, ghost re-broadcasts detected."),
    B("The link reconnected itself after every drop, four drive tests running."),
    B("Full radio recovery drill: flash, provision, verify, in minutes.", true),
  ], { x: 0.5, y: 3.45, w: 6.3, h: 2.3, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addText("NEXT, WEEKS 4 AND 5", { x: 7.15, y: 3.05, w: 5.0, h: 0.35, fontSize: 13, bold: true, charSpacing: 1,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    B("Victor: provision radio two from the recipe; first two-radio bench decode."),
    B("Cannon: constraints ledger becomes the drive-test protocol and logging harness."),
    B("Deo and Josiah: partner selection in NVS; night readability."),
    B("Then the milestone: the first two-vehicle drive test.", true),
  ], { x: 7.15, y: 3.45, w: 5.6, h: 2.3, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.95, w: 12.35, h: 0.75, fill: { color: INK } });
  s.addText("One radio still talks to itself. But every layer between a GPS fix and the driver's arrow is now real, tested code. Radio number two turns this into a tracker.",
    { x: 0.8, y: 6.05, w: 11.75, h: 0.55, fontSize: 12.5, color: PAPER, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
}

// ============================================================ SHEET 13 · references
{
  const s = pres.addSlide();
  frame(s, null, "references");
  title(s, "References");
  const refs = [
    ["[1]", "Semtech Corp., SX1276/77/78/79 LoRa Transceiver Datasheet. Demodulator SNR limit per spreading factor (SF11 = -17.5 dB), used on sheet 09.", "semtech.com/products/wireless-rf/lora-connect/sx1276", "https://www.semtech.com/products/wireless-rf/lora-connect/sx1276"],
    ["[2]", "Semtech Corp., AN1200.22, LoRa Modulation Basics. Symbol duration T_sym = 2^SF / BW, packet airtime, and processing gain.", "info.semtech.com/find-documentation (search AN1200.22)", "https://info.semtech.com/find-documentation"],
    ["[3]", "Semtech Corp., SX1261/2 Transceiver Datasheet. The radio IC on the Heltec V4; sensitivity and transmit specifications.", "semtech.com/products/wireless-rf/lora-connect/sx1262", "https://www.semtech.com/products/wireless-rf/lora-connect/sx1262"],
    ["[4]", "Meshtastic Project Documentation, LoRa and Position Configuration. Presets, smart broadcast, position precision, the ~25% utilization limit.", "meshtastic.org/docs/configuration/radio/lora", "https://meshtastic.org/docs/configuration/radio/lora/"],
    ["[5]", "Meshtastic Protobufs Repository. The published message schema our decoder is generated from, including Position field units.", "github.com/meshtastic/protobufs", "https://github.com/meshtastic/protobufs"],
    ["[6]", "FCC Rules, 47 CFR 15.247. Operation in the 902 to 928 MHz ISM band.", "law.cornell.edu/cfr/text/47/15.247", "https://www.law.cornell.edu/cfr/text/47/15.247"],
    ["[7]", "ITU-R Recommendation M.1371, Automatic Identification System (AIS). Reporting intervals of 2 s to 3 min; the beacon-then-animate precedent.", "itu.int/rec/R-REC-M.1371/en", "https://www.itu.int/rec/R-REC-M.1371/en"],
    ["[8]", "R. W. Sinnott, Virtues of the Haversine, Sky & Telescope, vol. 68, no. 2, p. 159, 1984. The distance formula used in nav.c.", "movable-type.co.uk/scripts/latlong.html (implementation ref)", "https://www.movable-type.co.uk/scripts/latlong.html"],
    ["[9]", "Bluetooth SIG, Bluetooth Core Specification (GATT). The service and characteristic model behind the Meshtastic Client API.", "bluetooth.com/specifications/specs/core-specification", "https://www.bluetooth.com/specifications/specs/core-specification/"],
    ["[10]", "Group 9 repository: TELECOM_ANALYSIS, ARCHITECTURE, BLE_LINK_WALKTHROUGH, RADIO_PHY_DEEP_DIVE, hardware/README. Our link budget, architecture, silicon walkthrough, and recipes.", "github.com/deosgracius/offgrid-vehicle-tracker", "https://github.com/deosgracius/offgrid-vehicle-tracker"]];
  refs.forEach((r, i) => {
    const col = i < 5 ? 0 : 1, row = i % 5;
    const x = 0.5 + col * 6.35, y = 1.22 + row * 1.06;
    s.addText(r[0], { x, y, w: 0.5, h: 0.3, fontSize: 10, bold: true, fontFace: MONO, color: ACC, isTextBox: true, margin: 0 });
    s.addText(r[1], { x: x + 0.55, y, w: 5.55, h: 0.72, fontSize: 9.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
    s.addText([{ text: r[2], options: { hyperlink: { url: r[3], tooltip: r[3] } } }],
      { x: x + 0.55, y: y + 0.72, w: 5.55, h: 0.24, fontSize: 8, fontFace: MONO, color: "1199BD", isTextBox: true, margin: 0 });
  });
  s.addShape("line", { x: 0.5, y: 6.55, w: 12.35, h: 0, line: { color: RULE, width: 0.75 } });
  s.addText("All firmware, documentation, logs, and this deck's generator are version controlled at github.com/deosgracius/offgrid-vehicle-tracker",
    { x: 0.5, y: 6.6, w: 12.35, h: 0.26, fontSize: 8.5, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addNotes("Leave this up during questions. If a number is challenged, the sources are: equations from Semtech [1][2], configuration behavior from Meshtastic docs [4], wire units from the protobuf schema itself [5], and the AIS precedent [7].");
}

pres.writeFile({ fileName: D3 + "Group9_Presentation3_Week3.pptx" }).then(() => console.log("written"));
