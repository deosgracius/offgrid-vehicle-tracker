const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

const NAVY = "1E2761", ICE = "CADCFC", WHITE = "FFFFFF", AMBER = "E58E1A";
const MUT = "5B6B8A", CARD = "F2F6FC", GREEN = "1F9D68";
const M = { Deo: "1199BD", Josiah: "6D4BDB", Victor: "E58E1A", Cannon: "D9488C" };

const HDR = { fontFace: "Cambria", bold: true, color: NAVY };
const BODY = { fontFace: "Calibri", color: "222A3F" };

function title(slide, txt, dark) {
  slide.addText(txt, { x: 0.55, y: 0.28, w: 11.0, h: 0.75, fontSize: 30, ...HDR,
    color: dark ? WHITE : NAVY, isTextBox: true, margin: 0 });
}
function presenter(slide, name) {
  slide.addShape("roundRect", { x: 11.55, y: 0.38, w: 1.25, h: 0.42, rectRadius: 0.08,
    fill: { color: M[name] } });
  slide.addText(name, { x: 11.55, y: 0.44, w: 1.25, h: 0.3, align: "center", fontSize: 13,
    bold: true, color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0 });
}
function box(s, x, y, w, h, main, sub, opts = {}) {
  s.addShape("roundRect", { x, y, w, h, rectRadius: 0.07,
    fill: { color: opts.fill || WHITE }, line: { color: opts.line || NAVY, width: opts.lw || 1.5 },
    ...(opts.dash ? { line: { color: opts.line || NAVY, width: opts.lw || 1.5, dashType: "dash" } } : {}) });
  const tc = opts.tc || NAVY;
  if (sub) {
    s.addText([{ text: main, options: { bold: true, breakLine: true } },
      { text: sub, options: { fontSize: (opts.subFs || 9.5), color: opts.subc || MUT } }],
      { x: x + 0.1, y, w: w - 0.2, h, fontSize: opts.fs || 11.5, fontFace: "Calibri",
        color: tc, isTextBox: true, margin: 0, align: "center", valign: "middle" });
  } else {
    s.addText(main, { x: x + 0.1, y, w: w - 0.2, h, fontSize: opts.fs || 11.5, bold: true,
      fontFace: "Calibri", color: tc, isTextBox: true, margin: 0, align: "center", valign: "middle" });
  }
}
function harrow(s, x, y, w, label, opts = {}) {
  s.addShape("line", { x, y, w, h: 0, line: { color: opts.color || NAVY, width: opts.lw || 2,
    endArrowType: "triangle", ...(opts.both ? { beginArrowType: "triangle" } : {}),
    ...(opts.dash ? { dashType: "dash" } : {}) } });
  if (label) s.addText(label, { x: x - 0.35, y: y - 0.34, w: w + 0.7, h: 0.28, align: "center",
    fontSize: 9.5, bold: true, color: opts.color || NAVY, fontFace: "Calibri", isTextBox: true, margin: 0 });
}
function varrow(s, x, y, h, label, opts = {}) {
  s.addShape("line", { x, y, w: 0, h, line: { color: opts.color || NAVY, width: opts.lw || 2,
    endArrowType: "triangle", ...(opts.dash ? { dashType: "dash" } : {}) } });
  if (label) s.addText(label, { x: x + 0.08, y: y + h / 2 - 0.14, w: 1.6, h: 0.28,
    fontSize: 9.5, bold: true, color: opts.color || NAVY, fontFace: "Calibri", isTextBox: true, margin: 0 });
}
function dart(slide, cx, cy, r, deg, color) {
  slide.addShape("triangle", { x: cx - r * 0.55, y: cy - r * 0.62, w: r * 1.1, h: r * 1.35,
    fill: { color }, rotate: deg });
}

// ================================================== S1 · Objective & Roles
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  dart(s, 11.6, 1.5, 1.4, 38, ICE);
  s.addText("OFF-GRID VEHICLE TRACKER", { x: 0.7, y: 0.75, w: 10.2, h: 0.8,
    fontSize: 40, ...HDR, color: WHITE, isTextBox: true, margin: 0 });
  s.addText("System Architecture Review  ·  Weeks 1–2  ·  Group 9  ·  Sponsor: Dr. Richard Gale",
    { x: 0.7, y: 1.62, w: 11.0, h: 0.45, fontSize: 17, fontFace: "Calibri", color: ICE,
      isTextBox: true, margin: 0 });

  s.addShape("roundRect", { x: 0.7, y: 2.35, w: 11.9, h: 1.25, rectRadius: 0.1, fill: { color: "2A3575" } });
  s.addText("Objective — design, build, and field-validate a fully off-grid system that continuously shows a driver the direction and distance to a partner vehicle, across multi-km terrain, with no communications infrastructure.",
    { x: 1.0, y: 2.5, w: 11.3, h: 0.95, fontSize: 15.5, color: WHITE, fontFace: "Calibri",
      isTextBox: true, margin: 0 });

  const roles = [
    ["Deo", "Protocol Firmware", "Meshtastic BLE client · protobuf decode · TrackerState feed"],
    ["Josiah", "Display & Navigation", "RLCD rendering · arrow UI · distance/bearing math"],
    ["Victor", "Radio & Hardware", "Meshtastic config · GNSS · antennas · range campaign"],
    ["Cannon", "Integration & Test", "bench rig · logging harness · drive tests · reports"]];
  roles.forEach((r, i) => {
    const x = 0.7 + i * 3.02;
    s.addShape("roundRect", { x, y: 3.95, w: 2.8, h: 1.6, rectRadius: 0.09, fill: { color: "2A3575" } });
    s.addShape("roundRect", { x, y: 3.95, w: 2.8, h: 0.1, rectRadius: 0.0, fill: { color: M[r[0]] } });
    s.addText(r[0], { x, y: 4.12, w: 2.8, h: 0.35, align: "center", fontSize: 16, bold: true,
      color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0 });
    s.addText(r[1], { x, y: 4.47, w: 2.8, h: 0.32, align: "center", fontSize: 12, bold: true,
      color: M[r[0]] === "E58E1A" ? AMBER : ICE, fontFace: "Calibri", isTextBox: true, margin: 0 });
    s.addText(r[2], { x: x + 0.15, y: 4.82, w: 2.5, h: 0.65, align: "center", fontSize: 10,
      color: ICE, fontFace: "Calibri", isTextBox: true, margin: 0 });
  });

  s.addText("Today: the full system architecture — context, hardware, firmware, data flow, link state machine — plus schedule and effort.",
    { x: 0.7, y: 6.1, w: 11.9, h: 0.5, fontSize: 14, italic: true, color: ICE,
      fontFace: "Calibri", isTextBox: true, margin: 0 });
}

// ================================================== S2 · Shared Foundations
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Weeks 1–2 · Shared Foundations", false);
  s.addText("The interface contract (agreed W1–W2)", { x: 0.55, y: 1.2, w: 6.0, h: 0.4,
    fontSize: 17, ...HDR, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 1.65, w: 6.0, h: 2.35, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText(
`struct TrackerState {
  Fix  self;     // own GPS: lat lon course speed
  Fix  partner;  // via LoRa: lat lon age_s
  bool ble_connected;
};`,
    { x: 0.8, y: 1.85, w: 5.6, h: 2.0, fontSize: 13, fontFace: "Courier New",
      color: ICE, isTextBox: true, margin: 0 });
  s.addText("One writer (protocol task) · one reader (UI task) · changed only by joint commit. This is what lets all four lanes build in parallel.",
    { x: 0.55, y: 4.15, w: 6.0, h: 0.65, fontSize: 12.5, italic: true, color: MUT,
      fontFace: "Calibri", isTextBox: true, margin: 0 });

  s.addText("Process: every interface testable in isolation", { x: 7.0, y: 1.2, w: 5.8, h: 0.4,
    fontSize: 17, ...HDR, isTextBox: true, margin: 0 });
  const rows = [
    ["Interface", "Independent test (no custom code)"],
    ["GPS → radio", "Fix visible on radio OLED + phone app"],
    ["LoRa A ↔ B", "Two phone apps see each other's position"],
    ["BLE Client API", "Meshtastic Python CLI from a laptop"],
    ["State → UI", "Simulated TrackerState scenarios"]];
  const tableRows = rows.map((r, i) => r.map(c => ({
    text: c, options: { fontSize: 12, bold: i === 0, fontFace: "Calibri",
      color: i === 0 ? WHITE : "222A3F", fill: { color: i === 0 ? NAVY : (i % 2 ? CARD : WHITE) },
      valign: "middle" } })));
  s.addTable(tableRows, { x: 7.0, y: 1.65, w: 5.8, colW: [1.85, 3.95], rowH: 0.44,
    border: { type: "solid", color: "C9D9EE", pt: 0.75 } });

  s.addText("Foundations in place", { x: 0.55, y: 5.2, w: 5.0, h: 0.4, fontSize: 17, ...HDR, isTextBox: true, margin: 0 });
  const badges = ["Shared git repo + CI-ready layout", "PlatformIO toolchain (ESP32-S3)",
    "nanopb + Meshtastic protobuf schema", "Equipment received & bench-verified"];
  badges.forEach((b, i) => {
    const x = 0.55 + (i % 2) * 6.25, y = 5.7 + Math.floor(i / 2) * 0.62;
    s.addShape("ellipse", { x, y: y + 0.05, w: 0.28, h: 0.28, fill: { color: AMBER } });
    s.addText(b, { x: x + 0.42, y, w: 5.7, h: 0.42, fontSize: 13.5, ...BODY, isTextBox: true, margin: 0 });
  });
}

// ================================================== S3 · Complete System Diagram
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "The Complete System — One Page", false);
  // Eraser export is ~1:1 aspect (2374×2385) — fit by height, left side.
  s.addImage({ path: "C:/Users/deogr/Documents/Fall Project/Off-Grid Vehicle dection project/docs/system-diagram.png",
    x: 0.4, y: 1.05, w: 6.28, h: 6.31 });
  s.addText("How to read it", { x: 7.1, y: 1.3, w: 5.6, h: 0.4, fontSize: 17, ...HDR, isTextBox: true, margin: 0 });
  s.addText([
    { text: "Left — one vehicle's hardware: GNSS → Heltec radio (stock Meshtastic) → roof antenna, plus the Waveshare display, all on vehicle 12 V.", options: { bullet: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Right — inside the display firmware: Deo's protocol/ chain writes TrackerState; Josiah's nav/ + ui/ chain reads it. One writer, one reader.", options: { bullet: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Bottom — the same system seen as telecom layers: ~40 B application payload · managed-flooding MAC with AES-256 · LoRa CSS PHY decoding 15 dB below the noise floor.", options: { bullet: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Vehicle B is an identical copy — the symmetry IS the design: no server, no master, no single point of failure.", options: { bullet: true } },
  ], { x: 7.1, y: 1.8, w: 5.65, h: 4.2, fontSize: 13.5, ...BODY, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 7.1, y: 6.15, w: 5.65, h: 0.95, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText("Everything blue/green on the right is the team's only custom code. Everything else ships tested.",
    { x: 7.35, y: 6.25, w: 5.2, h: 0.75, fontSize: 12.5, color: WHITE, fontFace: "Calibri",
      isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Single-page system view (drawn in Eraser, kept in docs/system-diagram.png). Walk left to right: hardware per vehicle, then the firmware split with TrackerState as the contract, then the telecom-layer view at the bottom. Vehicle B is identical.");
}

// ================================================== S4 · System Context (Deo)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "System Context — Nothing Is a Server", false);
  presenter(s, "Deo");

  function miniVehicle(x, label) {
    s.addShape("roundRect", { x, y: 2.3, w: 3.2, h: 2.7, rectRadius: 0.1,
      fill: { color: CARD }, line: { color: NAVY, width: 1.25 } });
    s.addText(label, { x, y: 2.4, w: 3.2, h: 0.32, align: "center", fontSize: 13, bold: true,
      color: NAVY, fontFace: "Calibri", isTextBox: true, margin: 0 });
    box(s, x + 0.25, 2.8, 2.7, 0.75, "Radio node", "Meshtastic · GNSS", {});
    varrow(s, x + 1.6, 3.55, 0.5, "BLE", { color: AMBER });
    box(s, x + 0.25, 4.05, 2.7, 0.75, "Display node", "custom firmware", { line: "6D4BDB" });
  }
  miniVehicle(1.0, "VEHICLE A");
  miniVehicle(5.15, "VEHICLE B");
  harrow(s, 4.2, 3.2, 0.95, "LoRa 915 MHz", { both: true, lw: 2.5 });
  s.addText("Position broadcasts flow symmetrically — identical installs, no master.",
    { x: 1.0, y: 5.2, w: 7.4, h: 0.35, fontSize: 11.5, italic: true, color: MUT,
      fontFace: "Calibri", isTextBox: true, margin: 0 });

  // relay node
  s.addShape("roundRect", { x: 3.35, y: 1.15, w: 2.6, h: 0.8, rectRadius: 0.35,
    fill: { color: WHITE }, line: { color: GREEN, width: 1.5, dashType: "dash" } });
  s.addText([{ text: "optional relay node", options: { bold: true, breakLine: true } },
    { text: "any Meshtastic device on high ground", options: { fontSize: 9, color: MUT } }],
    { x: 3.45, y: 1.15, w: 2.4, h: 0.8, fontSize: 10.5, fontFace: "Calibri", color: GREEN,
      isTextBox: true, margin: 0, align: "center", valign: "middle" });
  s.addShape("line", { x: 2.6, y: 1.95, w: 0.8, h: 0.85, flipH: true, line: { color: GREEN, width: 1.5, dashType: "dash" } });
  s.addShape("line", { x: 5.9, y: 1.95, w: 0.85, h: 0.85, line: { color: GREEN, width: 1.5, dashType: "dash" } });

  s.addText("Context facts", { x: 9.15, y: 1.3, w: 3.6, h: 0.4, fontSize: 17, ...HDR, isTextBox: true, margin: 0 });
  s.addText([
    { text: "Radios broadcast position every 30–60 s on a shared AES-256 channel.", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Managed flooding, hop limit 3 — a relay needs zero configuration.", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Each display consumes its own radio's node database over BLE.", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Scales without redesign: a 3rd vehicle or base camp just joins the mesh.", options: { bullet: true } },
  ], { x: 9.15, y: 1.75, w: 3.65, h: 3.6, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });

  s.addShape("roundRect", { x: 1.0, y: 5.85, w: 11.8, h: 1.0, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText("Design consequence: the system has no single point of failure outside a vehicle's own pair — losing any node degrades only that vehicle's view, never the mesh.",
    { x: 1.3, y: 6.0, w: 11.2, h: 0.7, fontSize: 13, color: WHITE, fontFace: "Calibri",
      isTextBox: true, margin: 0, valign: "middle" });
}

// ================================================== S5 · Hardware Architecture (Deo)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Hardware Architecture — One Vehicle", false);
  presenter(s, "Deo");

  // Panel A: radio node
  s.addText("Radio node — Heltec WiFi LoRa 32 V4 (stock Meshtastic)", { x: 0.55, y: 1.15, w: 8.4, h: 0.35,
    fontSize: 14, ...HDR, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 1.55, w: 8.5, h: 1.75, rectRadius: 0.1,
    fill: { color: CARD }, line: { color: "C9D9EE", width: 1 } });
  box(s, 0.85, 1.8, 1.7, 0.7, "GNSS module", "1.25 mm 8-pin conn.");
  harrow(s, 2.55, 2.15, 0.75, "UART (NMEA)");
  box(s, 3.3, 1.8, 1.7, 0.7, "ESP32-S3", "runs Meshtastic");
  harrow(s, 5.0, 2.15, 0.75, "SPI");
  box(s, 5.75, 1.8, 1.55, 0.7, "SX1262", "LoRa transceiver");
  harrow(s, 7.3, 2.15, 0.5, "");
  box(s, 7.8, 1.8, 1.05, 0.7, "antenna", "915 MHz roof", { line: AMBER, tc: "B06207" });
  varrow(s, 4.15, 2.5, 0.45, "I2C");
  box(s, 3.3, 2.95, 1.7, 0.28, "0.96″ OLED — field debug for free", null, { fs: 8.5, lw: 1 });

  // Panel B: display node
  s.addText("Display node — Waveshare ESP32-S3-RLCD-4.2 (our firmware)", { x: 0.55, y: 3.55, w: 8.4, h: 0.35,
    fontSize: 14, ...HDR, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 3.95, w: 8.5, h: 1.15, rectRadius: 0.1,
    fill: { color: CARD }, line: { color: "C9D9EE", width: 1 } });
  box(s, 0.85, 4.15, 2.3, 0.75, "ESP32-S3", "16 MB flash · 8 MB PSRAM", { line: "6D4BDB" });
  harrow(s, 3.15, 4.52, 1.3, "SPI · framebuffer in PSRAM", { color: "6D4BDB" });
  box(s, 4.45, 4.15, 2.5, 0.75, "4.2″ reflective LCD", "400×300 · 1 bpp · sunlight-readable", { line: "6D4BDB" });

  // Panel C: interconnect
  s.addText("In-cab interconnect & power", { x: 0.55, y: 5.35, w: 5.0, h: 0.35,
    fontSize: 14, ...HDR, isTextBox: true, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 5.75, w: 8.5, h: 1.15, rectRadius: 0.1,
    fill: { color: CARD }, line: { color: "C9D9EE", width: 1 } });
  box(s, 0.85, 5.95, 1.9, 0.75, "Vehicle 12 V", "→ USB-C 5 V");
  harrow(s, 2.75, 6.2, 0.7, "");
  box(s, 3.45, 5.95, 1.7, 0.75, "Radio node", null, {});
  harrow(s, 5.15, 6.32, 1.15, "BLE 2.4 GHz (~1 m)", { color: AMBER, both: true });
  box(s, 6.3, 5.95, 1.7, 0.75, "Display node", null, { line: "6D4BDB" });
  harrow(s, 2.75, 6.5, 3.55, "", { lw: 1 });

  s.addText("Notes that matter", { x: 9.35, y: 1.15, w: 3.4, h: 0.4, fontSize: 15, ...HDR, isTextBox: true, margin: 0 });
  s.addText([
    { text: "The only antenna leaving the cab is the LoRa antenna — roof-mounted, the single biggest range factor.", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Both boards are ESP32-S3 → one toolchain (PlatformIO) for the whole team.", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "The radio's OLED shows node count, GPS lock, last RSSI — a built-in field-debug display, zero work.", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "GPS antenna on the dash (sky view); BLE lives happily inside.", options: { bullet: true } },
  ], { x: 9.35, y: 1.6, w: 3.45, h: 4.6, fontSize: 12, ...BODY, isTextBox: true, margin: 0 });
}

// ================================================== S6 · Firmware Architecture (Deo)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Firmware Architecture — Display Node", false);
  presenter(s, "Deo");

  // protocol column
  s.addShape("roundRect", { x: 0.55, y: 1.3, w: 3.9, h: 4.35, rectRadius: 0.1,
    fill: { color: CARD }, line: { color: M.Deo, width: 1.5 } });
  s.addText("protocol/  (Deo)", { x: 0.75, y: 1.42, w: 3.5, h: 0.32, fontSize: 13, bold: true,
    color: M.Deo, fontFace: "Calibri", isTextBox: true, margin: 0 });
  box(s, 0.85, 1.85, 3.3, 1.0, "ble_link task — NimBLE central",
    "scan → connect → bond → subscribe → drain FromRadio", { line: M.Deo, subFs: 10 });
  varrow(s, 2.5, 2.85, 0.4, "");
  box(s, 0.85, 3.25, 3.3, 0.85, "proto_decode (nanopb)",
    "FromRadio → Position · NodeInfo · MyNodeInfo", { line: M.Deo, subFs: 10 });
  varrow(s, 2.5, 4.1, 0.4, "");
  box(s, 0.85, 4.5, 3.3, 0.85, "node_table",
    "own + partner fix · age tracking", { line: M.Deo, subFs: 10 });

  // TrackerState center
  s.addShape("roundRect", { x: 5.0, y: 3.2, w: 2.85, h: 1.5, rectRadius: 0.15, fill: { color: NAVY } });
  s.addText([{ text: "TrackerState", options: { bold: true, fontSize: 15, breakLine: true } },
    { text: "mutex-protected\nself · partner · ble_connected", options: { fontSize: 10.5, color: ICE } }],
    { x: 5.1, y: 3.2, w: 2.65, h: 1.5, fontFace: "Calibri", color: WHITE, isTextBox: true,
      margin: 0, align: "center", valign: "middle" });
  harrow(s, 4.45, 3.95, 0.55, "");
  harrow(s, 7.85, 3.95, 0.55, "");
  s.addText("ONE writer", { x: 4.3, y: 4.15, w: 1.0, h: 0.26, fontSize: 9, bold: true, color: MUT,
    fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addText("ONE reader", { x: 7.75, y: 4.15, w: 1.0, h: 0.26, fontSize: 9, bold: true, color: MUT,
    fontFace: "Calibri", isTextBox: true, margin: 0 });

  // ui column
  s.addShape("roundRect", { x: 8.85, y: 1.3, w: 3.9, h: 4.35, rectRadius: 0.1,
    fill: { color: CARD }, line: { color: M.Josiah, width: 1.5 } });
  s.addText("ui/ + nav/  (Josiah)", { x: 9.05, y: 1.42, w: 3.5, h: 0.32, fontSize: 13, bold: true,
    color: M.Josiah, fontFace: "Calibri", isTextBox: true, margin: 0 });
  box(s, 9.15, 1.85, 3.3, 1.0, "nav engine",
    "haversine · bearing · COG heading + stationary fallback", { line: M.Josiah, subFs: 10 });
  varrow(s, 10.8, 2.85, 0.4, "");
  box(s, 9.15, 3.25, 3.3, 0.85, "ui_render task (2 Hz)",
    "arrow · distance · data age · link status", { line: M.Josiah, subFs: 10 });
  box(s, 9.15, 4.5, 3.3, 0.85, "sim feed (dev only)",
    "5 fake-data scenarios — UI runs with zero radios", { line: M.Josiah, dash: true, subFs: 10 });
  s.addShape("line", { x: 7.85, y: 4.45, w: 1.3, h: 0.45, flipH: true, flipV: true,
    line: { color: M.Josiah, width: 1.5, dashType: "dash", endArrowType: "triangle" } });

  // NVS
  box(s, 5.0, 5.35, 2.85, 0.6, "NVS config", "radio BLE addr · units · partner ID (planned)", { dash: true, subFs: 9.5 });

  s.addText([
    { text: "One writer, one reader — a single mutex, no ordering bugs, and the halves never call each other.", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "The sim feed is a first-class component: the entire UI is testable on a bench with no radios.", options: { bullet: true, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Pairing is configuration, not code — the same firmware runs in both vehicles.", options: { bullet: true } },
  ], { x: 0.55, y: 6.15, w: 12.2, h: 1.2, fontSize: 12, ...BODY, isTextBox: true, margin: 0 });
}

// ================================================== S7 · End-to-End Data Flow (Deo)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "End-to-End Data Flow — Partner Fix to Arrow", false);
  presenter(s, "Deo");

  // ONE continuous pipeline, numbered 1→7, both rows reading left to right.
  s.addText("Across vehicles", { x: 0.55, y: 1.25, w: 3.0, h: 0.35, fontSize: 14, ...HDR, isTextBox: true, margin: 0 });
  box(s, 0.55, 1.7, 1.8, 0.95, "1 · GPS fix", "partner vehicle · 1 Hz NMEA", {});
  harrow(s, 2.35, 2.17, 0.55, "UART");
  box(s, 2.9, 1.7, 2.0, 0.95, "2 · Meshtastic B", "builds Position packet", {});
  harrow(s, 4.9, 2.17, 1.55, "LoRa · every 30–60 s", { color: "B06207", lw: 2.5 });
  s.addText("~0.5 s airtime · AES-256 · mesh relay", { x: 4.6, y: 2.45, w: 2.2, h: 0.5, align: "center",
    fontSize: 9, color: "B06207", fontFace: "Calibri", isTextBox: true, margin: 0 });
  box(s, 6.45, 1.7, 1.95, 0.95, "3 · Meshtastic A", "receives · node DB · queues FromRadio", { subFs: 9 });
  harrow(s, 8.4, 2.17, 1.3, "BLE notify → drain", { color: AMBER });
  box(s, 9.7, 1.7, 3.05, 0.95, "4 · protocol/ (Deo)", "read FromRadio until empty · nanopb decode → node_table", { line: M.Deo, subFs: 9 });

  // elbow: out of step 4, down and across to step 5
  s.addShape("line", { x: 11.22, y: 2.65, w: 0, h: 0.7, line: { color: NAVY, width: 2 } });
  s.addShape("line", { x: 1.9, y: 3.35, w: 9.32, h: 0, line: { color: NAVY, width: 2 } });
  s.addShape("line", { x: 1.9, y: 3.35, w: 0, h: 0.5, line: { color: NAVY, width: 2, endArrowType: "triangle" } });

  s.addText("Inside the display node", { x: 2.1, y: 3.44, w: 4.0, h: 0.32, fontSize: 14, ...HDR, isTextBox: true, margin: 0 });
  box(s, 0.55, 3.85, 2.7, 0.95, "5 · TrackerState", "self · partner · ages · clock (mutex · 1 Hz publish)", { fill: NAVY, tc: WHITE, subc: ICE, subFs: 9 });
  harrow(s, 3.25, 4.32, 0.6, "");
  box(s, 3.85, 3.85, 3.1, 0.95, "6 · nav engine (Josiah)", "d = haversine · arrow = θ − COG · rose fallback when stopped", { line: M.Josiah, subFs: 9 });
  harrow(s, 6.95, 4.32, 0.6, "");
  box(s, 7.55, 3.85, 3.3, 0.95, "7 · RLCD redraw @ 2 Hz", "arrow · miles · age · link · local clock", { line: M.Josiah });

  s.addShape("roundRect", { x: 0.55, y: 5.25, w: 12.2, h: 1.6, rectRadius: 0.1, fill: { color: CARD },
    line: { color: "C9D9EE", width: 1 } });
  s.addText([
    { text: "Own position rides the SAME pipeline minus steps 2–3 — the local radio streams its own GPS over BLE too, so ME and PARTNER stay symmetric.", options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: "No ACKs anywhere: a newer position supersedes an older one; the reliability metric is data age, shown to the driver.", options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: "End-to-end latency ≈ airtime (~0.5 s) — negligible next to the 30–60 s broadcast cadence.", options: { bullet: true } },
  ], { x: 0.8, y: 5.42, w: 11.7, h: 1.3, fontSize: 11.5, ...BODY, isTextBox: true, margin: 0 });

  s.addNotes("One packet's journey, numbered: (1) partner GNSS computes a fix, 1 Hz NMEA over UART. (2) Meshtastic B builds a Position packet — lat/lon, speed, track, GPS time — and broadcasts over LoRa every 30-60 s (smart: 30 s / 50 m while moving). (3) Meshtastic A decrypts, files it in its node DB, queues it on FromRadio, rings the FromNum doorbell. (4) protocol/ drains the queue over BLE and nanopb-decodes each frame into node_table. (5) node_table publishes TrackerState once a second — one writer. (6) nav engine reads it — one reader — haversine distance, bearing minus own COG. (7) ui_render redraws at 2 Hz. Full narrative with code: docs/BLE_LINK_WALKTHROUGH.md.");
}

// ================================================== S8 · BLE Link State Machine (Deo)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "BLE Link State Machine — The Risky Component, Made Explicit", false);
  presenter(s, "Deo");

  const states = [
    ["SCANNING", "direct connect by NVS addr · scan fallback", 0.7, CARD, NAVY],
    ["CONNECTING", "3 tries · 10 s timeout", 3.15, CARD, NAVY],
    ["BONDING", "encrypted pairing (Just Works, NO_PIN)", 5.6, "FDF1E2", "B06207"],
    ["SUBSCRIBED", "fromNum notify + want_config handshake", 8.05, "E7F5EE", GREEN],
    ["DRAINING", "read FromRadio → empty", 10.5, "E7F5EE", GREEN]];
  states.forEach(st => {
    box(s, st[2], 2.2, 2.15, 1.0, st[0], st[1], { fill: st[3], line: st[4], tc: st[4], subFs: 9.5 });
  });
  harrow(s, 2.85, 2.7, 0.3, "");
  harrow(s, 5.3, 2.7, 0.3, "");
  harrow(s, 7.75, 2.7, 0.3, "");
  // subscribed <-> draining
  harrow(s, 10.2, 2.5, 0.3, "", { color: GREEN });
  s.addShape("line", { x: 10.2, y: 2.95, w: 0.3, h: 0, flipH: true, line: { color: GREEN, width: 2, endArrowType: "triangle" } });
  s.addText("notify / empty", { x: 9.95, y: 3.25, w: 1.4, h: 0.26, fontSize: 9, bold: true,
    color: GREEN, fontFace: "Calibri", isTextBox: true, margin: 0, align: "center" });

  // failure edges back to scanning
  s.addShape("line", { x: 4.2, y: 3.2, w: 0, h: 0.9, line: { color: "C0392B", width: 1.75 } });
  s.addShape("line", { x: 6.7, y: 3.2, w: 0, h: 0.9, line: { color: "C0392B", width: 1.75 } });
  s.addShape("line", { x: 9.1, y: 3.2, w: 0, h: 0.9, line: { color: "C0392B", width: 1.75 } });
  s.addShape("line", { x: 1.75, y: 4.1, w: 7.35, h: 0, line: { color: "C0392B", width: 1.75 } });
  s.addShape("line", { x: 1.75, y: 3.2, w: 0, h: 0.9, flipV: true, line: { color: "C0392B", width: 1.75, endArrowType: "triangle" } });
  s.addText("connect fail (backoff) · bond fail · disconnect → back to SCANNING",
    { x: 2.3, y: 4.18, w: 6.5, h: 0.3, fontSize: 10.5, bold: true, color: "C0392B",
      fontFace: "Calibri", isTextBox: true, margin: 0 });

  s.addShape("roundRect", { x: 0.7, y: 5.0, w: 5.9, h: 1.8, rectRadius: 0.1, fill: { color: NAVY } });
  s.addText("Degradation rule", { x: 0.95, y: 5.15, w: 5.4, h: 0.32, fontSize: 13, bold: true,
    color: AMBER, fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addText("The UI always renders — last known data plus an honest age and link flag — no matter what state the BLE link is in. Link loss degrades the display; it never blanks it.",
    { x: 0.95, y: 5.5, w: 5.4, h: 1.2, fontSize: 12.5, color: WHITE, fontFace: "Calibri",
      isTextBox: true, margin: 0 });

  s.addShape("roundRect", { x: 6.9, y: 5.0, w: 5.9, h: 1.8, rectRadius: 0.1, fill: { color: CARD },
    line: { color: AMBER, width: 1.25 } });
  s.addText("Risk gate — Week 5", { x: 7.15, y: 5.15, w: 5.4, h: 0.32, fontSize: 13, bold: true,
    color: "B06207", fontFace: "Calibri", isTextBox: true, margin: 0 });
  s.addText("BONDING is the highest-uncertainty transition. If pairing is still blocked after two weeks, the transport swaps to Meshtastic's identical API over WiFi/TCP :4403 — decoder, state, and UI untouched.",
    { x: 7.15, y: 5.5, w: 5.4, h: 1.2, fontSize: 12.5, ...BODY, isTextBox: true, margin: 0 });

  s.addNotes("How each state works in the shipped code (docs/BLE_LINK_WALKTHROUGH.md has the full excerpts): SCANNING - direct connect to the radio address remembered in NVS first (a Meshtastic radio only general-advertises from boot until its first disconnect, so a scan alone can never reconnect); 1.5 s scan fallback handles first pairing and radio replacement, exponential backoff 1-8 s. CONNECTING - 3 attempts, 10 s each; +9 dBm TX because default power was marginal; MTU 517 so a protobuf frame fits one read. BONDING - Just Works encrypted pairing on every connect; no stored bond ON PURPOSE: a bonded Meshtastic peripheral stops advertising entirely (bench-proven trap). SUBSCRIBED - subscribe FromNum (the doorbell), then write want_config_id with a random nonce so the radio replays its whole node DB; nonce back = snapshot complete. DRAINING - read FromRadio until a zero-length read; one notify can mean many queued frames. Every failure funnels through one teardown back to SCANNING - no state can wedge. Road-proven: mid-carry disconnect on Sep 1 self-recovered with no user action.");
}

// ================================================== S9 · Gantt & Hours
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Semester Timeline, Effort & Budget", false);

  const gx = 1.75, gw = 11.0, wk = gw / 16, gy = 1.7, rh = 0.62;
  const week2x = (w) => gx + (w - 1) * wk;
  [1, 4, 8, 12, 16].forEach(w => {
    s.addShape("line", { x: week2x(w), y: gy - 0.25, w: 0, h: 3.35, line: { color: "E3EAF5", width: 1 } });
    s.addText("W" + w, { x: week2x(w) - 0.25, y: gy - 0.52, w: 0.6, h: 0.26, align: "center",
      fontSize: 10, color: MUT, fontFace: "Calibri", isTextBox: true, margin: 0 });
  });
  const lanes = [
    ["Deo", [[2, 7, "protocol core"], [8, 10, "hardening"]]],
    ["Victor", [[1, 5, "bring-up + antennas"], [8, 9, "range tests"], [12, 13, "final char."]]],
    ["Josiah", [[1, 7, "display + nav + arrow UI"], [10, 11, "polish"]]],
    ["Cannon", [[1, 5, "bench"], [6, 9, "integration + drives"], [10, 12, "install"], [14, 16, "report"]]]];
  lanes.forEach((lane, i) => {
    const y = gy + i * rh;
    s.addText(lane[0], { x: 0.55, y: y + 0.03, w: 1.1, h: 0.3, fontSize: 12, bold: true,
      color: M[lane[0]], fontFace: "Calibri", isTextBox: true, margin: 0 });
    lane[1].forEach(seg => {
      const bx = week2x(seg[0]), bw = (seg[1] - seg[0] + 1) * wk - 0.04;
      s.addShape("roundRect", { x: bx, y: y, w: bw, h: 0.34, rectRadius: 0.06, fill: { color: M[lane[0]] } });
      s.addText(seg[2], { x: bx + 0.06, y: y + 0.04, w: bw - 0.1, h: 0.26, fontSize: 9.5,
        color: WHITE, fontFace: "Calibri", isTextBox: true, margin: 0 });
    });
  });
  const miles = [[5, "risk gate"], [7, "bench demo"], [16, "Demo Day"]];
  miles.forEach(m => {
    const mx = week2x(m[0]) + wk / 2;
    s.addShape("diamond", { x: mx - 0.11, y: gy + 4 * rh + 0.08, w: 0.22, h: 0.22, fill: { color: AMBER } });
    s.addText(m[1], { x: mx - 0.7, y: gy + 4 * rh + 0.34, w: 1.4, h: 0.28, align: "center",
      fontSize: 10, bold: true, color: AMBER, fontFace: "Calibri", isTextBox: true, margin: 0 });
  });

  const stats = [["28 h", "logged weeks 1–2 (7 h × 4 members)"], ["$37.4k", "budget estimate (labor + materials + rental)"],
    ["$9.5k", "computing — direct materials"], ["46", "tasks on the live Gantt tracker"]];
  stats.forEach((st, i) => {
    const x = 0.55 + i * 3.12;
    s.addShape("roundRect", { x, y: 5.6, w: 2.92, h: 1.45, rectRadius: 0.1, fill: { color: CARD } });
    s.addText(st[0], { x: x + 0.2, y: 5.72, w: 2.6, h: 0.6, fontSize: 30, bold: true, color: NAVY,
      fontFace: "Cambria", isTextBox: true, margin: 0 });
    s.addText(st[1], { x: x + 0.2, y: 6.35, w: 2.6, h: 0.6, fontSize: 10.5, color: MUT,
      fontFace: "Calibri", isTextBox: true, margin: 0 });
  });
}

pres.writeFile({ fileName: "Group9_Presentation2_Weeks1-2.pptx" }).then(() => console.log("written"));
