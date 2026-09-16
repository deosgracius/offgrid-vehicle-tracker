// Week 4 deck, rev D — "Closing the Loop": method before measurement.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

const INK = "16213D", PAPER = "FFFFFF", ACC = "E58E1A", MUT = "5E6B85";
const RULE = "9AA7BE", CARD = "F2F5FA", CODEBG = "1B2440", ICE = "C9D8F0";
const M = { DEO: "1199BD", JOSIAH: "6D4BDB", VICTOR: "E58E1A", CANNON: "D9488C" };
const HFONT = "Arial", BFONT = "Arial", MONO = "Courier New";
const D3 = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/scratchpad/deck3/";

const TOTAL = 11;
let sheetNo = 0;

function frame(s, owner, sheetTitle) {
  sheetNo++;
  s.background = { color: PAPER };
  s.addShape("rect", { x: 0.18, y: 0.16, w: 12.97, h: 7.18, fill: { type: "none" }, line: { color: INK, width: 1.75 } });
  s.addShape("line", { x: 0.18, y: 6.86, w: 12.97, h: 0, line: { color: INK, width: 1 } });
  s.addText("GROUP 9  |  OFF-GRID VEHICLE TRACKER", { x: 0.35, y: 6.94, w: 4.6, h: 0.32, fontSize: 9,
    fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addText(sheetTitle.toUpperCase(), { x: 5.0, y: 6.94, w: 4.6, h: 0.32, align: "center", fontSize: 9,
    fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addText("SHEET " + String(sheetNo).padStart(2, "0") + "/" + TOTAL + "  REV D  2026-09-16",
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
const B = (text, last) => ({ text, options: { bullet: { code: "25AA" }, breakLine: !last, paraSpaceAfter: last ? 0 : 6 } });

// ============================================================ SHEET 01 · cover
{
  const s = pres.addSlide();
  frame(s, null, "design review, week 4");
  for (let gx = 0.68; gx < 13.0; gx += 0.5)
    s.addShape("line", { x: gx, y: 0.16, w: 0, h: 6.7, line: { color: "E8EDF5", width: 0.5 } });
  for (let gy = 0.66; gy < 6.86; gy += 0.5)
    s.addShape("line", { x: 0.18, y: gy, w: 12.97, h: 0, line: { color: "E8EDF5", width: 0.5 } });
  s.addText("CLOSING THE LOOP", { x: 0.7, y: 1.15, w: 11.9, h: 0.9, fontSize: 44, bold: true,
    charSpacing: 3, fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText("WEEK 4 DESIGN REVIEW: METHOD BEFORE MEASUREMENT", { x: 0.72, y: 2.05, w: 11.9, h: 0.45,
    fontSize: 17, bold: true, charSpacing: 1, fontFace: HFONT, color: ACC, isTextBox: true, margin: 0 });
  s.addText("This week's drive test closed the cadence question: position and speed measured fresh every ten seconds on the road, with one-second motion in between. The rest of this review publishes, in advance, everything the fifth layer will be judged by: procedure, design, predicted curve, protocol, and metrics.",
    { x: 0.72, y: 2.65, w: 8.3, h: 1.35, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  const rows = [
    ["OWNER", "SUBSYSTEM", "THIS WEEK"],
    ["DEO", "Backend, protocol/", "drive test: the ten-second cadence, proven"],
    ["JOSIAH", "Frontend, ui/ and nav/", "what changes on screen when the partner appears"],
    ["VICTOR", "Radio and PHY", "radio two procedure, predicted link curve"],
    ["CANNON", "Integration and test", "drive-test protocol, metrics declared in advance"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 10 : 11.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 0 ? MONO : BFONT,
      color: i === 0 ? PAPER : (j === 0 ? (M[r[0]] || INK) : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.72, y: 4.2, w: 8.3, colW: [1.35, 2.75, 4.2], rowH: 0.42,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  const blk = [["PROJECT", "Off-Grid Vehicle Tracker"], ["SPONSOR", "Dr. Richard Gale"],
    ["COURSE", "Capstone Project Lab"], ["STATUS", "48% vs 25% target, ahead"],
    ["HOURS", "122 of 768 logged"], ["DATE", "2026-09-16"]];
  s.addShape("rect", { x: 9.55, y: 2.65, w: 3.3, h: 3.55, fill: { color: PAPER }, line: { color: INK, width: 1.25 } });
  blk.forEach((r, i) => {
    const y = 2.72 + i * 0.575;
    if (i) s.addShape("line", { x: 9.55, y: y - 0.035, w: 3.3, h: 0, line: { color: RULE, width: 0.75 } });
    s.addText(r[0], { x: 9.7, y, w: 1.25, h: 0.28, fontSize: 9, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
    s.addText(r[1], { x: 9.7, y: y + 0.24, w: 3.05, h: 0.3, fontSize: 10.5, fontFace: BFONT, color: INK, isTextBox: true, margin: 0 });
  });
  s.addNotes("Opening line: last week ended on our own cliffhanger - one radio still talks to itself; radio two turns this into a tracker. This week we do the disciplined thing: publish the procedure, the design, the predicted curve, and the metrics BEFORE the measurement. Next review reports against exactly this sheet set, so nothing can be quietly redefined after the fact.");
}

// ============================================================ SHEET 02 · DEO, where we left off
{
  const s = pres.addSlide();
  frame(s, "DEO", "the open layer");
  title(s, "Where We Left Off: One Layer Open");
  const layers = [
    ["GPS to radio", "PROVEN"], ["Radio to display", "PROVEN"],
    ["Decode to TrackerState", "PROVEN"], ["Navigation and UI", "PROVEN"],
    ["Partner over LoRa", "THIS WEEK"]];
  layers.forEach((L, i) => {
    const y = 1.3 + i * 0.92, pending = L[1] !== "PROVEN";
    s.addShape("rect", { x: 0.6, y, w: 5.2, h: 0.74, fill: { color: pending ? PAPER : CARD },
      line: { color: pending ? ACC : M.DEO, width: 1.25, ...(pending ? { dashType: "dash" } : {}) } });
    s.addText(L[0], { x: 0.78, y: y + 0.05, w: 3.4, h: 0.64, fontSize: 12.5, bold: true,
      fontFace: BFONT, color: INK, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(L[1], { x: 4.15, y, w: 1.5, h: 0.74, align: "center", fontSize: 10, bold: true,
      fontFace: MONO, color: pending ? "B06207" : "1F9D68", isTextBox: true, margin: 0, valign: "middle" });
    if (i < 4) varrow(s, 1.15, y + 0.74, 0.18, M.DEO);
  });
  pic(s, D3 + "p_search.jpg", 6.3, 1.3, 2.55, 2.0, "The display says it plainly");
  s.addShape("rect", { x: 9.15, y: 1.3, w: 3.65, h: 2.0, fill: { color: INK } });
  s.addText([
    { text: "THE CLIFFHANGER", options: { bold: true, fontSize: 11.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "\u201cOne radio still talks to itself. Radio number two turns this into a tracker.\u201d That sentence is this week's work order.", options: { color: PAPER, fontFace: BFONT } },
  ], { x: 9.35, y: 1.45, w: 3.25, h: 1.75, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addText([
    B("Everything below the dashed layer runs today: decoding, navigation, dead reckoning, honest ages."),
    B("The partner path is the same decode code with a different node number. Nothing new is written; something existing gets its second speaker.", true),
  ], { x: 6.3, y: 3.85, w: 6.5, h: 1.6, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.6, y: 6.0, w: 12.2, h: 0.7, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  s.addText("This review publishes the plan the fifth layer will be judged by: procedure, design, predicted curve, protocol, metrics.",
    { x: 0.85, y: 6.08, w: 11.75, h: 0.55, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Thirty seconds of recap, no re-teaching: four layers proven with one device, the dashed fifth is this week. Key claim to land: the partner path is the identical decode path with a different node number - the code that will handle the partner has been running for weeks on our own packets.");
}

// ============================================================ SHEET 03 · DEO, drive-test result
{
  const s = pres.addSlide();
  frame(s, "DEO", "drive test result");
  title(s, "Result: Every Ten Seconds, on the Road");
  // the cadence pipeline, each stage with its verified rate
  const chain = [
    ["GPS fix", "every 10 s", "gps_update_interval 10"],
    ["Smart broadcast", "10 s / 20 m moving", "min interval + distance"],
    ["BLE delivery", "milliseconds", "notify, then drain"],
    ["Screen motion", "every second", "dead reckoning"]];
  chain.forEach((c, i) => {
    const x = 0.5 + i * 3.18;
    s.addShape("rect", { x, y: 1.3, w: 2.85, h: 1.15, fill: { color: CARD }, line: { color: M.DEO, width: 1.5 } });
    s.addText([{ text: c[0], options: { bold: true, breakLine: true } },
      { text: c[1], options: { fontSize: 12, bold: true, color: "1F9D68", breakLine: true } },
      { text: c[2], options: { fontSize: 8.5, color: MUT, fontFace: MONO } }],
      { x: x + 0.1, y: 1.38, w: 2.65, h: 1.0, fontSize: 12, fontFace: BFONT, color: INK,
        isTextBox: true, margin: 0, align: "center" });
    if (i < 3) harrow(s, x + 2.85, 1.87, 0.33, M.DEO);
  });
  s.addText("VERIFIED IN MOTION, 2026-09-16 DRIVE TEST", { x: 0.5, y: 2.65, w: 12.35, h: 0.28, fontSize: 10, bold: true,
    charSpacing: 1, fontFace: MONO, color: "1F9D68", isTextBox: true, margin: 0 });
  s.addText([
    B("Observed while driving: coordinates and speed refreshed roughly every ten seconds, matching the configured cadence for the first time on the road."),
    B("This closes the chain of cadence fixes from weeks three and four: the coarse-grid freeze, the stale GPS refresh, and the re-broadcast ghost each hid this behavior until removed."),
    B("The cadence question is now settled for one vehicle. Radio two inherits this configuration through the channel recipe, so the partner arrives at the same ten seconds.", true),
  ], { x: 0.5, y: 3.1, w: 12.35, h: 1.9, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.15, w: 12.35, h: 1.5, fill: { color: INK } });
  s.addText([
    { text: "WHY THIS MATTERS FOR THE EXAM", options: { bold: true, fontSize: 11, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Two of the five declared metrics depend on this cadence: packet delivery ratio counts against the ten-second schedule, and the age target of 25 seconds assumes fixes arrive on it. This drive test pinned down the denominator before the two-radio test supplies the numerator.", options: { color: PAPER, fontFace: BFONT } },
  ], { x: 0.8, y: 5.3, w: 11.75, h: 1.25, fontSize: 12.5, isTextBox: true, margin: 0 });
  s.addNotes("The week's one hard result: on the road, position and speed updated every ten seconds as configured - the first drive where observed cadence matched designed cadence. Tell the archaeology briefly: three earlier defects (position precision grid, 30-second GPS refresh, ghost re-broadcasts) each masked this until fixed, so this drive is the validation that the whole chain is clean. The navy card ties it forward: PDR and the age metric on sheet 09 are only measurable because the schedule is now known-good.");
}

// ============================================================ SHEET 04 · DEO, partner selection
{
  const s = pres.addSlide();
  frame(s, "DEO", "partner selection");
  title(s, "Partner Selection: From Rule to Configuration");
  codebox(s, 0.5, 1.2, 6.05, 1.7, "node_table.cpp  today: the bring-up rule",
`// first non-self node heard becomes the partner
if (s_partner_num == 0) {
    s_partner_num = from_num;
    Serial.printf("[node] partner: 0x%08lx", from_num);
}`, M.DEO);
  codebox(s, 6.95, 1.2, 5.9, 1.7, "design: partner as configuration",
`// NVS-persisted choice, selectable from the UI
prefs.putUInt("partner", chosen_node);
// node_table accepts only the chosen node;
// KEY-hold cycles candidates when several heard`, M.DEO);
  harrow(s, 6.55, 2.05, 0.35, M.DEO);
  s.addText([
    B("The bring-up rule was correct for one radio: with a single voice on the channel, first-heard is unambiguous."),
    B("With a mesh it becomes a race. The fix is the same pattern as the radio's own address: the choice lives in NVS flash, survives power cycles, and is set from the display, not the code."),
    B("Same firmware in every vehicle. Pairing is configuration, not code.", true),
  ], { x: 0.5, y: 3.2, w: 12.35, h: 1.8, fontSize: 13, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.15, w: 12.35, h: 1.5, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  s.addText([
    { text: "WHY THIS ORDER OF WORK", options: { bold: true, fontSize: 11, color: INK, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Selection ships before the two-radio bench test on purpose: the first time two real nodes speak, the display must already know how to choose between them. Designing the chooser after the ambiguity exists would mean debugging both at once.", options: { fontFace: BFONT } },
  ], { x: 0.8, y: 5.3, w: 11.75, h: 1.25, fontSize: 12.5, color: "222A3F", isTextBox: true, margin: 0 });
  s.addNotes("Left box is the code running today, verbatim from the repository, including its own TODO comment. Right box is the design being implemented this week. The argument: the pattern is proven - the radio's BLE address already lives in NVS the same way. And the sequencing point matters to a reviewer: build the chooser before the ambiguity arrives, not after.");
}

// ============================================================ SHEET 04 · VICTOR, provisioning procedure
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "radio two procedure");
  title(s, "Radio Two: a Fifteen-Minute Procedure");
  codebox(s, 0.5, 1.2, 8.0, 2.5, "hardware/README.md  the recipe, one command per line",
`meshtastic --port COMx --seturl "https://meshtastic.org/e/#Ci4S..."
   # channel URL: carries the AES key AND the frequency agreement
meshtastic --port COMx --set position.position_broadcast_secs 60
meshtastic --port COMx --set position.broadcast_smart_minimum_interval_secs 10
meshtastic --port COMx --set position.broadcast_smart_minimum_distance 20
meshtastic --port COMx --set position.gps_update_interval 10
meshtastic --port COMx --get lora.region     # VERIFY every write`, ACC);
  s.addShape("rect", { x: 8.85, y: 1.2, w: 4.0, h: 2.5, fill: { color: "FDF3E3" }, line: { color: ACC, width: 1.25 } });
  s.addText([
    { text: "TWO DOCUMENTED TRAPS", options: { bold: true, fontSize: 11, color: "B06207", fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Reboot-triggering writes can silently revert (the port close resets the chip mid-save): read back every setting. And identical boards demand a named upload port: we have paid for that lesson once.", options: { fontFace: BFONT, fontSize: 11 } },
  ], { x: 9.0, y: 1.35, w: 3.7, h: 2.25, fontSize: 11, color: "222A3F", isTextBox: true, margin: 0 });
  const accept = [
    ["1", "Radio two's OLED shows the Group9 channel and US region"],
    ["2", "Both OLEDs read \u201c1 online\u201d: each radio hears the other"],
    ["3", "The display's PTR row fills with radio two's live position"],
    ["4", "ChUtil stays in single digits with both radios broadcasting"]];
  s.addText("ACCEPTANCE CRITERIA, WRITTEN BEFORE THE ATTEMPT", { x: 0.5, y: 4.0, w: 8.0, h: 0.32, fontSize: 12, bold: true,
    charSpacing: 1, fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  accept.forEach((a, i) => {
    const y = 4.45 + i * 0.56;
    s.addShape("rect", { x: 0.5, y, w: 0.5, h: 0.44, fill: { color: INK } });
    s.addText(a[0], { x: 0.5, y: y + 0.03, w: 0.5, h: 0.38, align: "center", fontSize: 12, bold: true,
      color: ACC, fontFace: MONO, isTextBox: true, margin: 0 });
    s.addText(a[1], { x: 1.15, y: y + 0.03, w: 11.5, h: 0.4, fontSize: 12.5, fontFace: BFONT,
      color: "222A3F", isTextBox: true, margin: 0, valign: "middle" });
  });
  s.addNotes("The recipe exists because radio one's configuration was learned the hard way and written down each time. The channel URL is the crown jewels: it carries the encryption key, and because the channel name hashes to the frequency slot, it is also the frequency agreement. Read the four acceptance criteria aloud - declaring them before the attempt is the difference between a procedure and a hope. Criterion 2, both OLEDs reading one online, will be the first photograph.");
}

// ============================================================ SHEET 05 · VICTOR, predicted link curve
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "predicted link curve");
  title(s, "The Prediction the Range Test Will Judge");
  s.addImage({ path: D3 + "g_linkbudget.png", x: 0.5, y: 1.15, w: 6.6, h: 4.33 });
  s.addShape("rect", { x: 0.5, y: 1.15, w: 6.6, h: 4.33, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  s.addText([
    B("Transmit +22 dBm, 3 dBi at each end, free-space loss at 915 MHz: the solid curve. Terrain and clutter cost more: the dashed band."),
    B("The orange line is the wall: -131 dBm, the SF11 sensitivity from the datasheet. Where the band crosses the wall is the range prediction."),
    B("Free space says tens of kilometers; terrain will decide the real number. The range campaign plots measured RSSI points onto this exact chart.", true),
  ], { x: 7.35, y: 1.3, w: 5.45, h: 3.4, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 7.35, y: 4.85, w: 5.45, h: 1.7, fill: { color: INK } });
  s.addText([
    { text: "WHY PUBLISH THE CURVE FIRST", options: { bold: true, fontSize: 11, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "A measurement without a prior prediction is a demo. A measurement against a published curve is an experiment. Next review overlays the field points on this figure, wherever they land.", options: { color: PAPER, fontFace: BFONT } },
  ], { x: 7.55, y: 5.0, w: 5.05, h: 1.45, fontSize: 12, isTextBox: true, margin: 0 });
  s.addText("MODEL: FSPL = 32.45 + 20log(f) + 20log(d) · RSSI = 22 + 3 + 3 - FSPL - terrain   [DS Table 6-1 · AN1200.22 · TELECOM_ANALYSIS.md]",
    { x: 0.5, y: 5.62, w: 6.6, h: 0.5, fontSize: 8.5, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addNotes("Walk the chart: received power falls with distance (log scale); the orange wall is the minus 131 dBm sensitivity floor from datasheet Table 6-1; the shaded band between free space and the terrain-degraded curve is where reality lives. The claim to make carefully: free space predicts absurd range, tens of kilometers - real range is set by terrain, Fresnel clearance, and the vehicle install, which is precisely what the range campaign measures. The methodological point is the navy card: publishing the prediction before measuring converts a demo into an experiment.");
}

// ============================================================ SHEET 06 · JOSIAH, when the partner appears
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "frontend, partner-ready");
  title(s, "The Screen Is Already Partner-Shaped");
  pic(s, D3 + "p_search.jpg", 0.5, 1.25, 2.9, 2.28, "Today: honest about the gap");
  pic(s, D3 + "p_compass.jpg", 3.7, 1.25, 2.9, 2.39, "Sim preview: what fills in");
  s.addText([
    B("Every partner element exists and runs today, exercised for weeks by the simulator and by our own radio's packets: the arrow, the distance, the ages, the banners."),
    B("When radio two speaks, node_table stores a second fix and the same rendering draws it. The planned frontend change for that day is zero lines."),
    B("Queued this week instead: partner-selection screen (choose among heard nodes) and night readability with the edge light.", true),
  ], { x: 7.0, y: 1.3, w: 5.8, h: 3.1, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 4.6, w: 12.35, h: 0.95, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  s.addText("Definition of ready: the UI needs nothing from radio two's arrival except the data itself. That was the point of building on simulated partners from week one.",
    { x: 0.8, y: 4.72, w: 11.75, h: 0.72, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0, valign: "middle" });
  s.addShape("rect", { x: 0.5, y: 5.85, w: 12.35, h: 0.8, fill: { color: INK } });
  s.addText("The compass photo above is the simulator driving the real display: the partner pipeline, rehearsed nightly for three weeks.",
    { x: 0.8, y: 5.95, w: 11.75, h: 0.6, fontSize: 12.5, color: PAPER, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("The left photo is the live system being honest about the missing partner; the right photo is the same hardware running the simulator, which has fed fake partners through the real rendering since week one. So the frontend claim is unusual and strong: the plan for radio two's arrival is zero frontend changes. The queued work is the partner-selection screen (pairs with Deo's NVS design) and night readability.");
}

// ============================================================ SHEET 07 · CANNON, drive-test protocol
{
  const s = pres.addSlide();
  frame(s, "CANNON", "drive-test protocol");
  title(s, "Drive-Test Protocol, Version One");
  const phases = [
    ["P0  BENCH", "both radios on one desk: acceptance criteria 1 to 4 from sheet 04, thirty minutes of soak, zero drops expected"],
    ["P1  STATIC RANGE", "one radio fixed, one carried: log RSSI and SNR at marked distances until packets stop; plot onto sheet 05"],
    ["P2  TWO-VEHICLE DRIVE", "city loop then open road: PTR row live, ages under 15 s while moving, arrow tracks the real partner"],
    ["P3  EDGE CASES", "canyon streets, garage exit, one vehicle parked with no sky: ghosts must age honestly, links must self-heal"]];
  phases.forEach((p, i) => {
    const y = 1.25 + i * 1.02;
    s.addShape("rect", { x: 0.5, y, w: 8.6, h: 0.88, fill: { color: CARD }, line: { color: M.CANNON, width: 1.25 } });
    s.addText(p[0], { x: 0.68, y: y + 0.06, w: 2.1, h: 0.3, fontSize: 11, bold: true, fontFace: MONO,
      color: M.CANNON, isTextBox: true, margin: 0 });
    s.addText(p[1], { x: 0.68, y: y + 0.36, w: 8.25, h: 0.5, fontSize: 11, fontFace: BFONT,
      color: "222A3F", isTextBox: true, margin: 0 });
    if (i < 3) varrow(s, 1.0, y + 0.88, 0.14, M.CANNON);
  });
  s.addShape("rect", { x: 9.35, y: 1.25, w: 3.5, h: 4.0, fill: { color: PAPER }, line: { color: INK, width: 1.25 } });
  s.addText([
    { text: "LOGGED PER PACKET", options: { bold: true, fontSize: 11, color: INK, fontFace: MONO, breakLine: true, paraSpaceAfter: 6 } },
    { text: "timestamp\nnode id\nRSSI  [dBm]\nSNR   [dB]\ndistance at receipt\nage when displayed", options: { fontFace: MONO, fontSize: 11, color: "222A3F", breakLine: true, paraSpaceAfter: 6 } },
    { text: "Harness: serial capture on the display side; one dated log per test in testing/.", options: { fontFace: BFONT, fontSize: 10.5, color: MUT } },
  ], { x: 9.55, y: 1.42, w: 3.1, h: 3.7, fontSize: 11, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.6, w: 12.35, h: 1.05, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  s.addText("Every phase inherits its checks from the constraints ledger: the sky-view rule, the ignition-on rule, the one-client rule, the adapter rule. The ledger was the test plan all along.",
    { x: 0.8, y: 5.72, w: 11.75, h: 0.8, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Four phases, strictly ordered so each isolates one variable: bench removes distance, static range removes motion, the drive adds motion, edge cases add the failure modes we already catalogued. The right panel is the per-packet log schema - six fields, chosen so sheet 05's curve and sheet 08's metrics can both be computed from the same file. Close on the ledger line: the constraints sheet from last week literally becomes the checklist.");
}

// ============================================================ SHEET 08 · CANNON, metrics declared
{
  const s = pres.addSlide();
  frame(s, "CANNON", "metrics declared");
  title(s, "The Numbers That Will Judge the System");
  const mets = [
    ["PDR", "packet delivery ratio", "received / expected broadcasts per interval", "> 90% inside working range"],
    ["AGE p95", "freshness", "95th percentile of displayed partner age", "< 25 s while both move"],
    ["RECONNECT", "link resilience", "BLE self-heals after drop, no user action", "100% of drops, < 30 s"],
    ["DR ERROR", "projection honesty", "gap between projected and next real fix", "< 30 m at highway speed"],
    ["CHUTIL", "channel citizenship", "utilization with both radios broadcasting", "< 10% steady state"]];
  mets.forEach((m, i) => {
    const y = 1.25 + i * 1.02;
    s.addShape("rect", { x: 0.5, y, w: 2.3, h: 0.88, fill: { color: INK } });
    s.addText(m[0], { x: 0.5, y: y + 0.08, w: 2.3, h: 0.4, align: "center", fontSize: 13, bold: true,
      fontFace: MONO, color: ACC, isTextBox: true, margin: 0 });
    s.addText(m[1], { x: 0.5, y: y + 0.48, w: 2.3, h: 0.3, align: "center", fontSize: 9,
      fontFace: BFONT, color: ICE, isTextBox: true, margin: 0 });
    s.addText(m[2], { x: 3.0, y: y + 0.06, w: 6.1, h: 0.76, fontSize: 12, fontFace: BFONT,
      color: "222A3F", isTextBox: true, margin: 0, valign: "middle" });
    s.addShape("rect", { x: 9.3, y, w: 3.55, h: 0.88, fill: { color: CARD }, line: { color: "1F9D68", width: 1.25 } });
    s.addText(m[3], { x: 9.45, y: y + 0.06, w: 3.3, h: 0.76, fontSize: 11.5, bold: true, fontFace: MONO,
      color: "1F9D68", isTextBox: true, margin: 0, valign: "middle" });
  });
  s.addText("TARGETS SET BEFORE THE FIRST TWO-RADIO PACKET. NEXT REVIEW REPORTS EACH ROW, PASS OR FAIL.",
    { x: 0.5, y: 6.42, w: 12.35, h: 0.3, fontSize: 10, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  s.addNotes("Five metrics, each with its definition and a pre-declared pass threshold. Why declare now: after the data exists, any threshold looks chosen to flatter it. PDR is computable because broadcasts are scheduled, so expected count is known. Age p95 is the driver-facing truth. Reconnect covers the known BLE drop cases. DR error audits the dead reckoning against each next real fix. ChUtil keeps us honest citizens of the shared band. Every one computes from the six-field log on sheet 07.");
}

// ============================================================ SHEET 09 · status and next
{
  const s = pres.addSlide();
  frame(s, null, "status and next steps");
  title(s, "Status and What Comes Next");
  const stats = [["48%", "of tasks complete against a 25% week-four target"], ["10 s", "cadence verified on the road this week"],
    ["4 + 1", "layers proven + the layer this sheet set closes"], ["5", "metrics pre-declared, thresholds locked"]];
  stats.forEach((st, i) => {
    const x = 0.5 + i * 3.14;
    s.addShape("rect", { x, y: 1.2, w: 2.94, h: 1.5, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
    s.addText(st[0], { x: x + 0.2, y: 1.32, w: 2.6, h: 0.6, fontSize: 27, bold: true, color: INK,
      fontFace: HFONT, isTextBox: true, margin: 0 });
    s.addText(st[1], { x: x + 0.2, y: 1.95, w: 2.6, h: 0.65, fontSize: 10.5, color: MUT,
      fontFace: BFONT, isTextBox: true, margin: 0 });
  });
  s.addText("DONE THIS WEEK, AND NEXT IN ORDER", { x: 0.5, y: 3.05, w: 6.3, h: 0.35, fontSize: 13, bold: true, charSpacing: 1,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    B("Done: drive test verified the ten-second cadence end to end, in motion."),
    B("Next: partner selection lands in firmware (Deo), before the ambiguity arrives."),
    B("Next: radio two provisioned by the recipe; acceptance criteria checked (Victor)."),
    B("Next: bench soak, static range walk with the logging harness (Cannon); partner-selection screen and night readability (Josiah).", true),
  ], { x: 0.5, y: 3.45, w: 6.3, h: 2.3, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addText("NEXT REVIEW REPORTS", { x: 7.15, y: 3.05, w: 5.0, h: 0.35, fontSize: 13, bold: true, charSpacing: 1,
    fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    B("The before/after of the PTR row: \u201cno partner heard yet\u201d to live coordinates."),
    B("Field RSSI points overlaid on sheet 05's predicted curve."),
    B("The five metrics from sheet 08, each marked pass or fail."),
    B("Then the first two-vehicle drive test.", true),
  ], { x: 7.15, y: 3.45, w: 5.6, h: 2.3, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.5, y: 5.95, w: 12.35, h: 0.75, fill: { color: INK } });
  s.addText("Last week we showed a working machine. This week we published the exam it must pass. Next week it takes the exam.",
    { x: 0.8, y: 6.05, w: 11.75, h: 0.55, fontSize: 12.5, color: PAPER, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("The closing line is the deck's thesis: machine, then exam, then results. If asked why radio two is not already done, the honest answer is scheduling - the gantt has it in weeks 4 to 5, we are at 42 percent against a 25 percent target, and the disciplined move was to publish the acceptance criteria and metrics before touching the hardware.");
}

// ============================================================ SHEET 10 · references
{
  const s = pres.addSlide();
  frame(s, null, "references");
  title(s, "References");
  const refs = [
    ["[1]", "Semtech Corp., SX1276/77/78/79 Datasheet. SNR limit per spreading factor.", "semtech.com/products/wireless-rf/lora-connect/sx1276", "https://www.semtech.com/products/wireless-rf/lora-connect/sx1276"],
    ["[2]", "Semtech Corp., AN1200.22, LoRa Modulation Basics. Airtime and processing gain.", "info.semtech.com/find-documentation (search AN1200.22)", "https://info.semtech.com/find-documentation"],
    ["[3]", "Semtech Corp., SX1261/2 Datasheet. Sensitivity and transmit specifications.", "semtech.com/products/wireless-rf/lora-connect/sx1262", "https://www.semtech.com/products/wireless-rf/lora-connect/sx1262"],
    ["[4]", "Meshtastic Documentation, LoRa and Position Configuration.", "meshtastic.org/docs/configuration/radio/lora", "https://meshtastic.org/docs/configuration/radio/lora/"],
    ["[5]", "Meshtastic Protobufs Repository. The published message schema.", "github.com/meshtastic/protobufs", "https://github.com/meshtastic/protobufs"],
    ["[6]", "FCC Rules, 47 CFR 15.247. The 902 to 928 MHz ISM band.", "law.cornell.edu/cfr/text/47/15.247", "https://www.law.cornell.edu/cfr/text/47/15.247"],
    ["[7]", "ITU-R M.1371, Automatic Identification System. Beacon-interval precedent.", "itu.int/rec/R-REC-M.1371/en", "https://www.itu.int/rec/R-REC-M.1371/en"],
    ["[8]", "Friis/FSPL path-loss model background and haversine reference.", "movable-type.co.uk/scripts/latlong.html", "https://www.movable-type.co.uk/scripts/latlong.html"],
    ["[9]", "Bluetooth SIG, Core Specification (GATT).", "bluetooth.com/specifications/specs/core-specification", "https://www.bluetooth.com/specifications/specs/core-specification/"],
    ["[10]", "Group 9 repository: RADIO_PHY_DEEP_DIVE, TELECOM_ANALYSIS, hardware/README, testing/.", "github.com/deosgracius/offgrid-vehicle-tracker", "https://github.com/deosgracius/offgrid-vehicle-tracker"]];
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
  s.addNotes("Same verified links as last week. If the link-budget model on sheet 05 is challenged: FSPL is the standard Friis free-space form, the sensitivity floor is datasheet Table 6-1, and the full derivation is in TELECOM_ANALYSIS.md in the repository.");
}

pres.writeFile({ fileName: D3 + "Group9_Presentation4_Week4.pptx" }).then(() => console.log("written"));
