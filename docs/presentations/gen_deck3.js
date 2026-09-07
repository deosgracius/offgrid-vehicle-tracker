const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

const NAVY = "1E2761", ICE = "CADCFC", WHITE = "FFFFFF", AMBER = "E58E1A";
const MUT = "5B6B8A", CARD = "F2F6FC", GREEN = "1F9D68", CODEBG = "222A3F";
const M = { Deo: "1199BD", Josiah: "6D4BDB", Victor: "E58E1A", Cannon: "D9488C" };
const HDR = { fontFace: "Cambria", bold: true, color: NAVY };
const BODY = { fontFace: "Calibri", color: "222A3F" };
const D3 = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/scratchpad/deck3/";
const MPNG = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/scratchpad/mermaid_png/";

function title(s, txt) {
  s.addText(txt, { x: 0.55, y: 0.26, w: 11.0, h: 0.7, fontSize: 28, ...HDR, isTextBox: true, margin: 0 });
}
function presenter(s, name) {
  s.addShape("roundRect", { x: 11.55, y: 0.34, w: 1.25, h: 0.42, rectRadius: 0.08, fill: { color: M[name] } });
  s.addText(name, { x: 11.55, y: 0.4, w: 1.25, h: 0.3, align: "center", fontSize: 13, bold: true,
    color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0 });
}
function codebox(s, x, y, w, h, label, code, labelColor) {
  s.addShape("roundRect", { x, y, w, h, rectRadius: 0.07, fill: { color: CODEBG } });
  s.addText(label, { x: x + 0.15, y: y + 0.06, w: w - 0.3, h: 0.26, fontSize: 10, bold: true,
    color: labelColor || AMBER, fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addText(code, { x: x + 0.15, y: y + 0.32, w: w - 0.3, h: h - 0.42, fontSize: 10,
    fontFace: "Courier New", color: ICE, isTextBox: true, margin: 0, valign: "top" });
}
function varrow(s, x, y, h, color) {
  s.addShape("line", { x, y, w: 0, h, line: { color: color || NAVY, width: 2.25, endArrowType: "triangle" } });
}
function harrow(s, x, y, w, color) {
  s.addShape("line", { x, y, w, h: 0, line: { color: color || NAVY, width: 2.25, endArrowType: "triangle" } });
}
function pic(s, path, x, y, w, h, cap) {
  s.addImage({ path, x, y, w, h });
  if (cap) s.addText(cap, { x, y: y + h + 0.02, w, h: 0.3, fontSize: 10, italic: true, color: MUT,
    align: "center", fontFace: "Calibri", isTextBox: true, margin: 0 });
}

// ================================================== S1 · Title
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText("WEEK 3 — FROM ARCHITECTURE TO A WORKING TRACKER", { x: 0.7, y: 0.8, w: 12.0, h: 0.8,
    fontSize: 33, ...HDR, color: WHITE, isTextBox: true, margin: 0 });
  s.addText("Off-Grid Vehicle Tracker  ·  Group 9  ·  Sponsor: Dr. Richard Gale",
    { x: 0.7, y: 1.62, w: 11.0, h: 0.4, fontSize: 16, fontFace: "Calibri", color: ICE, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.7, y: 2.3, w: 11.9, h: 1.15, rectRadius: 0.1, fill: { color: "2A3575" } });
  s.addText("This week: the display shows a live partner — arrow, distance, freshness — decoded end-to-end from real radio packets. Each section: the sector's architecture, then the working hardware and the code behind it.",
    { x: 1.0, y: 2.45, w: 11.3, h: 0.85, fontSize: 15, color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0 });
  const roles = [
    ["Deo", "Backend — protocol/", "BLE link · nanopb decode · TrackerState"],
    ["Josiah", "Frontend — ui/ + nav/", "arrow math · two-page UI · dead reckoning"],
    ["Victor", "Radio & PHY", "LoRa physics · real-time vs 10 s · antennas"],
    ["Cannon", "Integration & Test", "constraints ledger · test protocol"]];
  roles.forEach((r, i) => {
    const x = 0.7 + i * 3.02;
    s.addShape("roundRect", { x, y: 3.85, w: 2.8, h: 1.6, rectRadius: 0.09, fill: { color: "2A3575" } });
    s.addShape("roundRect", { x, y: 3.85, w: 2.8, h: 0.1, fill: { color: M[r[0]] } });
    s.addText(r[0], { x, y: 4.02, w: 2.8, h: 0.35, align: "center", fontSize: 16, bold: true,
      color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0 });
    s.addText(r[1], { x, y: 4.38, w: 2.8, h: 0.3, align: "center", fontSize: 12, bold: true,
      color: r[0] === "Victor" ? AMBER : ICE, fontFace: "Calibri", isTextBox: true, margin: 0 });
    s.addText(r[2], { x: x + 0.15, y: 4.7, w: 2.5, h: 0.65, align: "center", fontSize: 10,
      color: ICE, fontFace: "Calibri", isTextBox: true, margin: 0 });
  });
  s.addText("Schedule check: 29% complete vs ~19% target at week 3 — ahead of plan · 60 h logged",
    { x: 0.7, y: 5.95, w: 11.9, h: 0.4, fontSize: 14, italic: true, color: ICE, fontFace: "Calibri", isTextBox: true, margin: 0 });
}

// ================================================== S2 · Deo — sector diagram
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Backend — protocol/ : The Data Spine");
  presenter(s, "Deo");
  s.addImage({ path: MPNG + "diag5.png", x: 0.7, y: 1.15, w: 11.9, h: 3.36 }); // firmware architecture
  s.addText([
    { text: "Left chain is the backend: ble_link (NimBLE central, direct-connect by NVS address) → proto_decode (nanopb) → node_table (own + partner fixes, GPS clock, re-broadcast dedupe) → writes TrackerState v2.", options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: "One writer, one reader, one mutex — the halves never call each other; the sim feed can replace the whole backend and the frontend cannot tell.", options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: "Status: live-proven. Bonded link, full config-dump handshake, positions decoding at the 10 s broadcast cadence, automatic reconnect after drops.", options: { bullet: true } },
  ], { x: 0.7, y: 4.75, w: 12.0, h: 1.6, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });
  s.addNotes("Sector map first: the yellow protocol box is mine. Emphasize the single interface (TrackerState v2, mutex-protected) and that everything on the left half is now road-tested: direct connect by remembered address, Just Works encryption, drain-until-empty, duplicate re-broadcast detection for honest ages.");
}

// ================================================== S3 · Deo — the connection in code
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "How the Pieces Connect — the Actual Code Path");
  presenter(s, "Deo");
  codebox(s, 0.55, 1.2, 6.0, 1.5, "ble_link.cpp — drain the radio's GATT queue",
`for (;;) {
  NimBLEAttValue v = s_fromRadio->readValue();
  if (v.size() == 0) break;      // queue empty
  proto_decode_from_radio(v.data(), v.size());
}`, M.Deo);
  codebox(s, 6.9, 1.2, 5.9, 1.5, "proto_decode.cpp — bytes -> named fields (nanopb)",
`if (pb_decode(&is, meshtastic_Position_fields, &pos))
  node_table_position(pkt->from,
      pos->latitude_i, pos->longitude_i, ...,
      pos->ground_speed, pos->time);`, M.Deo);
  varrow(s, 3.55, 2.7, 0.4, M.Deo);
  varrow(s, 9.85, 2.7, 0.4, M.Deo);
  codebox(s, 0.55, 3.1, 6.0, 1.55, "node_table.cpp — publish the contract (1 Hz)",
`TrackerState st;
st.self = s_self.fix;   st.partner = s_partner.fix;
st.ble_connected = connected;
st.utc_epoch = s_utc_epoch;      // GPS wall clock
tracker_store_set(&st);          // the ONE writer`, M.Deo);
  codebox(s, 6.9, 3.1, 5.9, 1.55, "ui_render.cpp — frontend picks it up (2 Hz)",
`tracker_store_get(&st);          // the ONE reader
dr_apply(&st);   // dead-reckon fixes forward
NavOutput nav = nav_compute(&st);
// -> arrow angle, distance, ages, clock`, M.Josiah);
  harrow(s, 6.55, 3.87, 0.35, NAVY);
  s.addText("mutex boundary", { x: 5.65, y: 4.1, w: 2.2, h: 0.26, fontSize: 9.5, bold: true, color: MUT,
    align: "center", fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 5.05, w: 12.25, h: 1.75, rectRadius: 0.1, fill: { color: CARD }, line: { color: "C9D9EE", width: 1 } });
  s.addText([
    { text: "Four files, one direction of flow, one shared struct. The blue boxes are backend (Deo), the purple box is frontend (Josiah) — they meet only at tracker_store_set / tracker_store_get, which take the mutex internally so locked access is the only possible access.", options: { breakLine: true, paraSpaceAfter: 8 } },
    { text: "Field-hardened this week: km/h→m/s wire units, GPS-jitter speed deadband (<4.5 km/h reads 0), bit-identical re-broadcast detection so a radio with no GPS lock cannot reset the data age, and a monotonic guard so the clock never runs backwards.", options: {} },
  ], { x: 0.85, y: 5.25, w: 11.7, h: 1.45, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });
  s.addNotes("Walk the arrows: GATT read loop until empty (one notify can mean many frames); nanopb decode generated from Meshtastic's own schema; node_table publishes once a second; UI reads its own snapshot at 2 Hz, dead-reckons it forward, computes the arrow. The bottom card is the week's debugging harvest - every item came from a real drive test.");
}

// ================================================== S4 · Josiah — sector diagram + math
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Frontend — ui/ + nav/ : From Struct to Arrow");
  presenter(s, "Josiah");
  // drawn sector flow
  function fbox(x, y, w, h, main, sub, line) {
    s.addShape("roundRect", { x, y, w, h, rectRadius: 0.07, fill: { color: WHITE }, line: { color: line || M.Josiah, width: 1.5 } });
    s.addText([{ text: main, options: { bold: true, breakLine: true } },
      { text: sub, options: { fontSize: 9.5, color: MUT } }],
      { x: x + 0.08, y, w: w - 0.16, h, fontSize: 11.5, fontFace: "Calibri", color: NAVY,
        isTextBox: true, margin: 0, align: "center", valign: "middle" });
  }
  fbox(0.55, 1.3, 2.3, 0.95, "TrackerState v2", "snapshot copy (mutex)", NAVY);
  harrow(s, 2.85, 1.77, 0.5, M.Josiah);
  fbox(3.35, 1.3, 2.4, 0.95, "dr_apply()", "dead reckoning: project fixes fwd");
  harrow(s, 5.75, 1.77, 0.5, M.Josiah);
  fbox(6.25, 1.3, 2.4, 0.95, "nav_compute()", "distance · bearing · arrow");
  harrow(s, 8.65, 1.77, 0.5, M.Josiah);
  fbox(9.15, 1.3, 3.5, 0.95, "render @ 2 Hz", "compass page ⇄ status page (KEY tap) · hold = reset");
  s.addText("The nav math (nav.c — unit-tested, 12/12 native tests pass):", { x: 0.55, y: 2.55, w: 8.0, h: 0.35, fontSize: 14, ...HDR, isTextBox: true, margin: 0 });
  codebox(s, 0.55, 2.95, 6.0, 1.35, "nav.c — the arrow in three lines",
`d       = haversine(self, partner);      // meters
bearing = initial_bearing(self, partner); // deg true
arrow   = wrap180(bearing - self.course); // 0 = ahead`, M.Josiah);
  codebox(s, 6.9, 2.95, 5.9, 1.35, "dead_reckon.c — 1 Hz feel between 10 s fixes",
`d = speed * min(age, 120);   // meters traveled
lat += d*cos(course)/111320;
lon += d*sin(course)/(111320*cos(lat));`, M.Josiah);
  s.addText([
    { text: "Heading comes from GPS course-over-ground — no magnetometer (unreliable inside a steel cab). Below 5 mph the arrow falls back to a north-up compass rose: course is noise when parked.", options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: "Every element is state-driven from the struct: CHANGE COURSE engages after 5 s off-course and clears on recovery; blinker chevrons show turn direction; STALE banner past 120 s; the clock derives its timezone from position.", options: { bullet: true } },
  ], { x: 0.55, y: 4.55, w: 12.2, h: 1.3, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 6.0, w: 12.25, h: 0.85, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText("Dead reckoning is why the screen feels live: measurements arrive every 10 s, but the display re-projects both vehicles every second along their last course and speed — and every real fix snaps it back to truth.",
    { x: 0.85, y: 6.12, w: 11.7, h: 0.65, fontSize: 12.5, color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Sector flow left to right, then the two code fragments that do all the work. Emphasize testability: nav.c and dead_reckon.c are pure C, unit-tested on the laptop with no hardware (12/12 passing).");
}

// ================================================== S5 · Josiah — the UI live (photos)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "The UI, Running on Real Packets");
  presenter(s, "Josiah");
  pic(s, D3 + "p_compass.jpg", 0.55, 1.2, 4.4, 3.63, "Driving view: partner 2.41 mi · CHANGE COURSE + turn chevron · age 15 s");
  pic(s, D3 + "p_stopped.jpg", 5.25, 1.2, 4.35, 2.85, "Stopped → north-up rose fallback (course is noise at 0 mph)");
  pic(s, D3 + "p_close.jpg", 5.25, 4.5, 3.4, 2.48, "Close range: 0.2 mi, oversized arrow");
  pic(s, D3 + "p_status.jpg", 9.85, 1.2, 2.95, 1.99, "Status page (KEY tap): live ME/PTR coordinates");
  s.addShape("roundRect", { x: 9.85, y: 3.6, w: 2.95, h: 3.3, rectRadius: 0.1, fill: { color: CARD }, line: { color: "C9D9EE", width: 1 } });
  s.addText([
    { text: "Why these shots matter", options: { bold: true, fontSize: 13, color: NAVY.toString(), breakLine: true, paraSpaceAfter: 6 } },
    { text: "Every value on these screens arrived by radio and was decoded by our stack — no simulator.", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Reflective LCD: readable in direct sun, sharper in more light — the opposite of a phone.", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "age / updated-ago is the honesty metric: the driver always knows how fresh the data is.", options: { bullet: true } },
  ], { x: 10.05, y: 3.75, w: 2.6, h: 3.0, fontSize: 11, ...BODY, isTextBox: true, margin: 0 });
  s.addNotes("All four photos are the real display running on decoded radio packets. Point out the state machine at work: banner + chevron in the driving view, automatic rose fallback when stopped, the diagnostic page with raw coordinates for debugging.");
}

// ================================================== S6 · Victor — sector + hardware
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Radio & PHY — the Long-Range Link");
  presenter(s, "Victor");
  s.addText("Radio node — Heltec V4 (stock Meshtastic)", { x: 0.55, y: 1.1, w: 8.0, h: 0.32, fontSize: 13, ...HDR, isTextBox: true, margin: 0 });
  s.addImage({ path: MPNG + "diag2.png", x: 0.55, y: 1.45, w: 7.6, h: 1.55 });
  pic(s, D3 + "p_rig.jpg", 8.45, 1.1, 2.0, 2.67, "The rig: radio + 915 MHz antenna");
  pic(s, D3 + "p_oled.jpg", 10.65, 1.1, 2.15, 1.13, "OLED: 9 sats · ChUtil 0%");
  s.addText([
    { text: "LONG_FAST preset: SF11 · BW 250 kHz · FEC 4/5 · 915 MHz ISM · AES-256 private channel (position_precision 32 — full resolution).", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Smart broadcast: every 10 s / 20 m while moving, 60 s parked; GPS refresh 10 s so every broadcast carries a NEW fix.", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "The OLED is the free field debugger: satellites, nodes heard, channel utilization, RSSI of last packet.", options: { bullet: true } },
  ], { x: 0.55, y: 3.25, w: 7.7, h: 1.7, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 5.1, w: 12.25, h: 1.7, rectRadius: 0.1, fill: { color: "FDF1E2" }, line: { color: AMBER, width: 1.25 } });
  s.addText([
    { text: "Provisioning discipline (hardware/README.md)", options: { bold: true, fontSize: 13, color: "B06207", breakLine: true, paraSpaceAfter: 5 } },
    { text: "Radio #2 must join with the exact channel URL (embeds the AES key + precision) or the radios cannot decrypt each other. Two documented traps: reboot-triggering CLI writes silently revert (port-close resets the chip mid-save — verify every setting), and identical ESP32-S3 boards demand explicit upload ports when flashing.", options: {} },
  ], { x: 0.85, y: 5.25, w: 11.7, h: 1.45, fontSize: 12, ...BODY, isTextBox: true, margin: 0 });
  s.addNotes("Radio sector: hardware diagram, then the configuration that came out of three road tests: 10 s / 20 m smart broadcast with 10 s GPS refresh, full-precision positions on the private AES channel. The amber card is the provisioning recipe for radio #2 - the channel URL is the crown jewels.");
}

// ================================================== S7 · Victor — the math
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Real Time vs 10 Seconds — the Physics");
  presenter(s, "Victor");
  function eq(y, label, img, iw, ih) {
    s.addText(label, { x: 0.55, y, w: 2.6, h: 0.55, fontSize: 11.5, bold: true, color: NAVY,
      fontFace: "Calibri", isTextBox: true, margin: 0, valign: "middle" });
    s.addImage({ path: D3 + img, x: 3.3, y: y + 0.02, w: iw, h: ih });
  }
  // aspect ratios: airtime 2192x115, util 2555x118, sens 2653x90, dr 1757x101, latency 2481x90
  eq(1.25, "1 · Airtime per position", "eq_airtime.png", 8.9, 0.47);
  eq(2.05, "2 · Channel utilization", "eq_util.png", 9.3, 0.43);
  eq(2.85, "3 · Sensitivity (15 dB below noise)", "eq_sens.png", 9.3, 0.32);
  eq(3.6, "4 · Info latency vs sample period", "eq_latency.png", 9.3, 0.34);
  eq(4.35, "5 · Dead reckoning fills the gap", "eq_dr.png", 6.9, 0.4);
  s.addShape("roundRect", { x: 0.55, y: 5.25, w: 12.25, h: 1.6, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText([
    { text: "The verdict", options: { bold: true, fontSize: 13.5, color: AMBER, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Information reaches the driver ~1 s after it exists (eq. 4) — that IS real time. But a new measurement can only be taken every 10 s, because each broadcast costs 0.5 s of shared airtime (eq. 1–2): at 1 Hz two vehicles would demand 100% of the channel. The range comes from decoding 15 dB below the noise floor (eq. 3) — and the 10 s gaps are filled at 1 Hz by projection (eq. 5). Rate and range are the same currency; we spent it on kilometers.", options: { color: WHITE } },
  ], { x: 0.85, y: 5.38, w: 11.7, h: 1.4, fontSize: 12, fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addNotes("This is the slide that answers 'why not every second'. Walk eq 1: symbol time 2^SF/BW, SF11 means 2048-chip symbols, ~0.5 s per position packet. Eq 2: two vehicles at 1 Hz = 100% channel = collapse; at 10 s it is 10%, healthy. Eq 3: the same spreading factor buys -131 dBm sensitivity, 15 dB below thermal noise - that is where the kilometers come from. Eq 4: latency ~1 s (airtime + BLE + render) - the system IS real-time in information delay; 10 s is the sampling period. Eq 5: dead reckoning projects both vehicles at 1 Hz between fixes. AIS ships beacon at 2-30 s and every chartplotter animates between reports - same trick.");
}

// ================================================== S8 · Cannon — constraints
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Integration Constraints — the Ledger");
  presenter(s, "Cannon");
  s.addImage({ path: MPNG + "diag1.png", x: 0.55, y: 1.1, w: 6.3, h: 2.16 }); // system context
  s.addText("Every constraint below is bench- or road-verified, not theoretical — each one shaped the design.",
    { x: 7.1, y: 1.25, w: 5.6, h: 0.9, fontSize: 13, italic: true, color: MUT, fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addText("Integration test sequence: radio #2 provisioning → bench two-radio decode → two-vehicle drive test → range characterization.",
    { x: 7.1, y: 2.2, w: 5.6, h: 1.0, fontSize: 13, bold: true, color: NAVY, fontFace: "Calibri", isTextBox: true, margin: 0 });
  const cons = [
    ["RADIO / PHY", "0.5 s airtime per packet → ≥10 s cadence · ~25% utilization cap · region US must be set or TX is disabled · roof antenna is the #1 range factor"],
    ["GPS", "needs sky view (windshield works, desks don't) · cold start = minutes · indoor multipath fakes 1–3 km/h phantom speed → deadband · fix rate must match broadcast rate"],
    ["BLE LINK", "radio advertises ONLY from boot until first disconnect → power both together (ignition-on) · exactly ONE client at a time — a phone app or USB CLI steals/mutes the link"],
    ["DISPLAY", "1-bit reflective panel: no grayscale, needs ambient light at night (edge-light planned) · 2 Hz full-frame redraw budget"],
    ["POWER", "cheap 12 V→USB adapters cut off on the radio's low draw — validate every adapter · both units must share vehicle power timing"],
    ["PROVISIONING", "channel URL (AES key + precision) must match on every radio · node IDs derive from MAC — survive reflashes · every config write must be read back and verified"]];
  cons.forEach((c, i) => {
    const x = 0.55 + (i % 3) * 4.18, y = 3.5 + Math.floor(i / 3) * 1.75;
    s.addShape("roundRect", { x, y, w: 3.98, h: 1.6, rectRadius: 0.08, fill: { color: CARD }, line: { color: M.Cannon, width: 1.25 } });
    s.addText(c[0], { x: x + 0.15, y: y + 0.08, w: 3.7, h: 0.28, fontSize: 11.5, bold: true, color: M.Cannon,
      fontFace: "Calibri", isTextBox: true, margin: 0 });
    s.addText(c[1], { x: x + 0.15, y: y + 0.38, w: 3.7, h: 1.16, fontSize: 9.5, ...BODY, isTextBox: true, margin: 0 });
  });
  s.addNotes("Cannon's role: every one of these constraints becomes a test-protocol line item. The strongest point: none are guesses - phantom speed, the advertise-once trap, the charger cutoff, the config-revert trap were all discovered on the bench or on the road and are documented in the repo with their fixes.");
}

// ================================================== S9 · Week 3 scoreboard
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Week 3 Status & Next");
  const stats = [["29%", "complete vs ~19% week-3 target — ahead"], ["60 h", "logged (8 h × 4 this week)"],
    ["12/12", "native unit tests passing"], ["10 s / 1 s", "measured cadence / on-screen motion"]];
  stats.forEach((st, i) => {
    const x = 0.55 + i * 3.12;
    s.addShape("roundRect", { x, y: 1.25, w: 2.92, h: 1.5, rectRadius: 0.1, fill: { color: CARD } });
    s.addText(st[0], { x: x + 0.2, y: 1.38, w: 2.6, h: 0.6, fontSize: 28, bold: true, color: NAVY,
      fontFace: "Cambria", isTextBox: true, margin: 0 });
    s.addText(st[1], { x: x + 0.2, y: 2.0, w: 2.6, h: 0.62, fontSize: 10.5, color: MUT,
      fontFace: "Calibri", isTextBox: true, margin: 0 });
  });
  s.addText("Proven end-to-end this week", { x: 0.55, y: 3.1, w: 6.0, h: 0.4, fontSize: 16, ...HDR, isTextBox: true, margin: 0 });
  s.addText([
    { text: "GPS fix → LoRa broadcast → BLE → decode → arrow, at 10 s cadence with 1 Hz dead-reckoned motion", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Location-aware clock (timezone from position) · honest data ages · ghost re-broadcast detection", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Automatic reconnect (NVS direct-connect) survived every drop, drive test after drive test", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Full radio recovery drill executed and documented — flash → provision → verify, in minutes", options: { bullet: true } },
  ], { x: 0.55, y: 3.55, w: 6.3, h: 2.3, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });
  s.addText("Next (W4–5)", { x: 7.2, y: 3.1, w: 5.0, h: 0.4, fontSize: 16, ...HDR, isTextBox: true, margin: 0 });
  s.addText([
    { text: "Victor: provision radio #2 from the README recipe → first two-radio bench decode", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Cannon: turn the constraints ledger into the drive-test protocol + logging harness", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Deo/Josiah: partner-selection UI (NVS-persisted node ID) · night readability", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Team: first two-vehicle drive test — the arrow points at a real partner", options: { bullet: true } },
  ], { x: 7.2, y: 3.55, w: 5.5, h: 2.3, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 6.1, w: 12.25, h: 0.85, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText("One radio still talks to itself — but every layer between a GPS fix and the driver's arrow is now real, tested code. Radio #2 turns this into a tracker.",
    { x: 0.85, y: 6.22, w: 11.7, h: 0.65, fontSize: 12.5, color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0, valign: "middle" });
}

pres.writeFile({ fileName: D3 + "Group9_Presentation3_Week3.pptx" }).then(() => console.log("written"));
