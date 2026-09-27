// Week 5 deck, rev E — "Locking the Link": how two radios find, verify, and keep each other.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

const INK = "16213D", PAPER = "FFFFFF", ACC = "E58E1A", MUT = "5E6B85";
const RULE = "9AA7BE", CARD = "F2F5FA", CODEBG = "1B2440", ICE = "C9D8F0";
const GRN = "1F9D68", RED = "C43A4B";
const M = { DEO: "1199BD", JOSIAH: "6D4BDB", VICTOR: "E58E1A", CANNON: "D9488C" };
const HFONT = "Arial", BFONT = "Arial", MONO = "Courier New";
const D5 = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/scratchpad/deck5/";
const IMG = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664/images/";

const TOTAL = 18;
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
  s.addText("SHEET " + String(sheetNo).padStart(2, "0") + "/" + TOTAL + "  REV E  2026-09-25",
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
function larrow(s, x, y, w, color) { // left-pointing: head on the start end, positive width only
  s.addShape("line", { x, y, w, h: 0, line: { color: color || INK, width: 2.25, beginArrowType: "triangle" } });
}
function varrow(s, x, y, h, color) {
  s.addShape("line", { x, y, w: 0, h, line: { color: color || INK, width: 2.25, endArrowType: "triangle" } });
}
function pic(s, path, x, y, w, h, cap) {
  s.addImage({ path, x, y, w, h });
  s.addShape("rect", { x, y, w, h, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  if (cap) s.addText(cap, { x: x - 0.3, y: y + h + 0.03, w: w + 0.6, h: 0.3, fontSize: 9, color: MUT,
    align: "center", fontFace: MONO, isTextBox: true, margin: 0 });
}
const B = (text, last) => ({ text, options: { bullet: { code: "25AA" }, breakLine: !last, paraSpaceAfter: last ? 0 : 6 } });

// ============================================================ SHEET 01 · cover
{
  const s = pres.addSlide();
  frame(s, null, "rf link deep dive, week 5");
  for (let gx = 0.68; gx < 13.0; gx += 0.5)
    s.addShape("line", { x: gx, y: 0.16, w: 0, h: 6.7, line: { color: "E8EDF5", width: 0.5 } });
  for (let gy = 0.66; gy < 6.86; gy += 0.5)
    s.addShape("line", { x: 0.18, y: gy, w: 12.97, h: 0, line: { color: "E8EDF5", width: 0.5 } });
  s.addText("LOCKING THE LINK", { x: 0.7, y: 1.1, w: 11.9, h: 0.9, fontSize: 44, bold: true,
    charSpacing: 3, fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText("HOW TWO RADIOS FIND, VERIFY, AND KEEP EACH OTHER", { x: 0.72, y: 2.0, w: 11.9, h: 0.45,
    fontSize: 17, bold: true, charSpacing: 1, fontFace: HFONT, color: ACC, isTextBox: true, margin: 0 });
  s.addText("On 2026-09-25 the two Heltec V4 radios completed round-trip traceroutes on the private Group9 channel. This review is the engineering record of the acquisition process: the frequency mathematics that decides whether two radios can hear each other at all, the cryptographic and node-discovery handshakes that turn hearing into a link, the timestamp bookkeeping that decides what \u201conline\u201d means, and the airtime budget that keeps the channel usable at vehicle rates.",
    { x: 0.72, y: 2.6, w: 8.3, h: 1.55, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  const rows = [
    ["SHEETS", "QUESTION ANSWERED"],
    ["02-04", "which frequency, which key: why matched configs can still be deaf"],
    ["05-06", "acquisition: NodeInfo, public keys, and two-way proof by traceroute"],
    ["07-08", "liveness: what \u201c1 online\u201d actually computes, and its heartbeat"],
    ["09-10", "airtime and link budget: SF11 time-on-air, CLIENT_MUTE, range margin"],
    ["11-13", "JOSIAH \u00b7 3D-printed armor for the RLCD display: model, print, assembly"],
    ["14-16", "CANNON \u00b7 drive-test protocol, bench evidence, as-built configuration"],
    ["17-18", "nomenclature: every acronym, formula, and symbol, explained"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 0 ? MONO : BFONT,
      color: i === 0 ? PAPER : (j === 0 ? ACC : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.72, y: 4.28, w: 8.3, colW: [1.35, 6.95], rowH: 0.31,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  const blk = [["PROJECT", "Off-Grid Vehicle Tracker"], ["SPONSOR", "Dr. Richard Gale"],
    ["COURSE", "Capstone Project Lab"], ["MILESTONE", "Radio link ESTABLISHED"],
    ["HOURS", "186 of 768 logged"], ["DATE", "2026-09-25"]];
  s.addShape("rect", { x: 9.55, y: 2.6, w: 3.3, h: 3.55, fill: { color: PAPER }, line: { color: INK, width: 1.25 } });
  blk.forEach((r, i) => {
    const y = 2.67 + i * 0.575;
    if (i) s.addShape("line", { x: 9.55, y: y - 0.035, w: 3.3, h: 0, line: { color: RULE, width: 0.75 } });
    s.addText(r[0], { x: 9.7, y, w: 1.4, h: 0.28, fontSize: 9, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
    s.addText(r[1], { x: 9.7, y: y + 0.24, w: 3.05, h: 0.3, fontSize: 10.5, fontFace: BFONT, color: i === 3 ? GRN : INK, bold: i === 3, isTextBox: true, margin: 0 });
  });
  s.addNotes("Opening: last review published the plan; this one reports the milestone. Both radios now hold a verified two-way link on our private channel. But the headline is not 'it works' - it is WHY it did not work for a day with byte-identical configurations, and what that taught us about how LoRa mesh radios actually lock onto each other. Every claim on these sheets was measured on our own hardware this week, most of it twice.");
}

// ============================================================ SHEET 02 · system: two radios, one contract
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "the rf contract");
  title(s, "Two Radios, One Contract: What Must Match");
  // node boxes
  [["RADIO 1  \u201cSF\u201d  !49b5ead4", 0.6], ["RADIO 2  \u201cRG\u201d  !49b5bb5c", 9.0]].forEach(([t, x]) => {
    s.addShape("rect", { x, y: 1.35, w: 3.7, h: 2.5, fill: { color: CARD }, line: { color: INK, width: 1.5 } });
    s.addText(t, { x: x + 0.15, y: 1.45, w: 3.4, h: 0.3, fontSize: 11, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
    [["GNSS", "u-blox, 10 s fix rate"], ["MCU", "ESP32-S3, Meshtastic 2.7.26"], ["PHY", "SX1262, +30 dBm, SMA whip"]].forEach((r, i) => {
      const y = 1.85 + i * 0.62;
      s.addShape("rect", { x: x + 0.15, y, w: 3.4, h: 0.52, fill: { color: PAPER }, line: { color: RULE, width: 0.75 } });
      s.addText([{ text: r[0] + "  ", options: { bold: true, fontFace: MONO, color: M.VICTOR } },
        { text: r[1], options: { color: "222A3F" } }],
        { x: x + 0.28, y: y + 0.03, w: 3.2, h: 0.46, fontSize: 10.5, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
    });
  });
  // air interface between them
  s.addShape("rect", { x: 4.75, y: 1.7, w: 3.8, h: 1.85, fill: { color: PAPER }, line: { color: ACC, width: 1.5, dashType: "dash" } });
  s.addText("THE AIR INTERFACE", { x: 4.9, y: 1.78, w: 3.5, h: 0.28, fontSize: 10, bold: true, fontFace: MONO, color: ACC, isTextBox: true, margin: 0 });
  s.addText([
    { text: "912.875 MHz  (slot 43)", options: { bold: true, breakLine: true } },
    { text: "LoRa SF11 / 250 kHz / CR 4:5", options: { breakLine: true } },
    { text: "AES-256, Group9 pre-shared key", options: { breakLine: true } },
    { text: "8.19 ms symbol \u00b7 ~0.5 s per packet", options: {} }],
    { x: 4.9, y: 2.1, w: 3.5, h: 1.35, fontSize: 11, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
  harrow(s, 4.3, 2.6, 0.45, M.VICTOR); larrow(s, 8.55, 2.6, 0.45, M.VICTOR);
  // the contract table
  s.addText("EVERY ROW MUST MATCH ON BOTH RADIOS \u2014 ONE MISMATCH = TOTAL SILENCE", { x: 0.6, y: 4.15, w: 12.2, h: 0.3,
    fontSize: 11.5, bold: true, fontFace: MONO, color: RED, isTextBox: true, margin: 0 });
  const rows = [
    ["LAYER", "PARAMETER", "OUR VALUE", "IF MISMATCHED"],
    ["Frequency", "region + slot (from channel name hash)", "US, slot 43 = 912.875 MHz", "radios literally tuned apart"],
    ["Modulation", "preset: SF / bandwidth / coding rate", "LONG_FAST: SF11 / 250 kHz / 4:5", "chirps undecodable"],
    ["Encryption", "channel name + AES-256 PSK", "Group9, 256-bit key", "packets heard, dropped on decrypt"],
    ["Identity", "per-node public key (fw 2.5+)", "exchanged via NodeInfo", "direct messages NAK"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 2 ? MONO : BFONT,
      color: i === 0 ? PAPER : (j === 3 ? RED : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.6, y: 4.5, w: 12.2, colW: [1.5, 4.0, 3.5, 3.2], rowH: 0.42,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addNotes("Frame the sheet as a contract: LoRa has no negotiation, no handshake at the PHY - both sides must independently arrive at identical radio parameters from their own stored config. The table is ordered like the OSI stack: frequency first (can you even receive energy), then modulation (can you demodulate chirps), then channel crypto (can you read the payload), then per-node identity (can you address a specific radio). Our failure lived in row one - the least visible layer, because every tool reports the CONFIG, not the synthesizer frequency. Segue: so where does that frequency actually come from? Next sheet is the math.");
}

// ============================================================ SHEET 03 · frequency slot math
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "frequency slot derivation");
  title(s, "The Channel Name IS the Frequency");
  s.addText([
    B("Meshtastic never stores a frequency. Each radio derives its slot from a hash of the primary channel NAME."),
    B("US-915 band, LONG_FAST bandwidth 250 kHz \u2192 104 slots. The name picks one deterministically.", true)],
    { x: 0.6, y: 1.15, w: 7.6, h: 0.95, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addImage({ path: D5 + "eq_slot.png", x: 0.7, y: 2.15, w: 7.3, h: 0.78 });
  codebox(s, 8.55, 1.15, 4.25, 2.3, "// djb2 \u2014 the exact hash",
"unsigned h = 5381;\nfor (char c : name)\n    h = h * 33 + c;\nslot = h % 104;\n\ndjb2(\"LongFast\") % 104 = 19\ndjb2(\"Group9\")   % 104 = 43");
  s.addImage({ path: D5 + "fig_slots.png", x: 0.7, y: 3.3, w: 9.0, h: 2.85 });
  s.addShape("rect", { x: 9.95, y: 3.45, w: 2.85, h: 2.55, fill: { color: INK } });
  s.addText([
    { text: "CONSEQUENCE", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Rename the channel and the radio RETUNES. Two radios can share every key byte and still sit 6 MHz apart \u2014 the name hash is part of the RF contract.", options: { color: PAPER, fontFace: BFONT, fontSize: 11 } }],
    { x: 10.12, y: 3.6, w: 2.55, h: 2.3, fontSize: 11, isTextBox: true, margin: 0 });
  s.addNotes("Walk the equation left to right: start of band, plus half a bandwidth so the slot is centered, plus slot index times bandwidth. The slot index is a plain djb2 string hash of the channel name modulo the slot count - show the six-line loop, this is the entire algorithm. Verify it live if asked: LongFast hashes to 19, which is 906.875 - the published US default, so the math is calibrated against a known constant. Group9 hashes to 43 = 912.875. Point at the band figure: the two markers are 6 MHz apart. A radio on one marker receives effectively nothing from the other - at 250 kHz bandwidth, 6 MHz off-tune is total isolation. That is the trap: the name looks like a label, but it is a tuning word.");
}

// ============================================================ SHEET 04 · failure matrix + root cause
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "root cause analysis");
  title(s, "Root Cause: Same Key, Different Slot");
  // 2x2 matrix
  const mx = 0.7, my = 1.5, cw = 2.9, ch = 1.25;
  s.addText("KEY MATCHES \u2192", { x: mx + cw * 0.5, y: my - 0.32, w: cw * 1.6, h: 0.28, fontSize: 10, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
  const cells = [
    ["slot =, key =", "LINK WORKS", GRN, "traceroute 6 dB both ways"],
    ["slot =, key \u2260", "heard, not read", ACC, "counters tick, payloads drop"],
    ["slot \u2260, key =", "TOTAL SILENCE", RED, "our bug: 0 online, 0% ChUtil"],
    ["slot \u2260, key \u2260", "strangers", MUT, "different networks entirely"]];
  cells.forEach((c, i) => {
    const x = mx + (i % 2) * (cw + 0.12), y = my + Math.floor(i / 2) * (ch + 0.12);
    s.addShape("rect", { x, y, w: cw, h: ch, fill: { color: i === 2 ? "FBEEEF" : (i === 0 ? "EDF7F1" : CARD) }, line: { color: c[2], width: i === 2 ? 2.25 : 1.25 } });
    s.addText([{ text: c[0], options: { fontFace: MONO, fontSize: 9.5, color: MUT, breakLine: true } },
      { text: c[1], options: { bold: true, fontSize: 13, color: c[2], breakLine: true } },
      { text: c[3], options: { fontSize: 9.5, color: "222A3F" } }],
      { x: x + 0.14, y: y + 0.1, w: cw - 0.28, h: ch - 0.2, fontSize: 11, fontFace: BFONT, isTextBox: true, margin: 0 });
  });
  s.addText("what happened on the bench: a channel write silently reverted (serial port-close resets the MCU mid-save), leaving one radio\u2019s primary on the default slot while its saved URL read back \u201cGroup9\u201d.",
    { x: 0.7, y: 4.35, w: 6.0, h: 1.0, fontSize: 11.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.7, y: 5.5, w: 6.0, h: 1.1, fill: { color: CARD }, line: { color: GRN, width: 1.5 } });
  s.addText([{ text: "THE TRUTH-TELLER  ", options: { bold: true, fontFace: MONO, color: GRN } },
    { text: "the OLED LoRa screen prints the synthesizer frequency. Config tools report intent; the screen reports reality. Group9 must read 912.875.", options: { color: "222A3F" } }],
    { x: 0.88, y: 5.6, w: 5.65, h: 0.92, fontSize: 11, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  pic(s, IMG + "15.jpg", 7.3, 1.5, 2.6, 3.4, "mid-debug: radio believed \u201cGroup9\u201d,\nradiated on 906.875 (default slot)");
  codebox(s, 10.15, 1.5, 2.65, 3.4, "// the proof, both ways",
"Group9 (pre-fix):\n traceroute \u2192\n  MAX_RETRANSMIT\n\ndefault channel:\n ead4\u2192bb5c  7.25 dB\n bb5c\u2192ead4  6.0  dB\n\nGroup9 (post-fix):\n bb5c\u2192ead4  5.75 dB\n ead4\u2192bb5c  6.25 dB", ICE);
  s.addNotes("The 2x2 matrix is the whole diagnosis space. Top-left is health. Top-right - same slot, wrong key - still updates 'last heard' counters because packet headers are cleartext; only payloads drop. Bottom-left is OUR cell and the cruelest: byte-identical keys, verified configs, zero RF coupling, because the radios were 6 MHz apart. Every software check reads back the intended config while the synthesizer sits on the old slot until a clean save+reboot. Method that isolated it: A/B regression - both radios moved to the known-good default channel, link immediately proven with round-trip traceroute; both moved to Group9 with the OLED frequency verified at 912.875, link proven again. Two variables, tested one at a time.");
}

// ============================================================ SHEET 05 · acquisition sequence
{
  const s = pres.addSlide();
  frame(s, "DEO", "node acquisition sequence");
  title(s, "Locking On: From First Packet to Addressable Peer");
  const steps = [
    ["1", "BOOT \u2192 ANNOUNCE", "each radio broadcasts NodeInfo: long/short name, hardware, PUBLIC KEY", INK],
    ["2", "STAMP", "receiver files the node: last_heard = rx_time, SNR recorded, \u201conline\u201d begins", INK],
    ["3", "KEY EXCHANGE", "NodeInfo carries the Curve25519 public key \u2014 stored in the peer\u2019s node DB", INK],
    ["4", "CHANNEL TRAFFIC", "broadcasts (positions, texts, telemetry) need only the shared AES channel key", GRN],
    ["5", "DIRECT MESSAGES", "PKC-encrypted per node (fw 2.5+): impossible until step 3 has happened", ACC]];
  steps.forEach((st, i) => {
    const y = 1.25 + i * 0.98;
    s.addShape("rect", { x: 0.6, y, w: 0.62, h: 0.78, fill: { color: st[3] } });
    s.addText(st[0], { x: 0.6, y: y + 0.08, w: 0.62, h: 0.6, align: "center", fontSize: 20, bold: true, color: PAPER, fontFace: MONO, isTextBox: true, margin: 0 });
    s.addShape("rect", { x: 1.22, y, w: 6.55, h: 0.78, fill: { color: i % 2 ? CARD : PAPER }, line: { color: RULE, width: 0.75 } });
    s.addText([{ text: st[1] + "   ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: st[3] } },
      { text: st[2], options: { fontSize: 11, color: "222A3F" } }],
      { x: 1.4, y: y + 0.05, w: 6.25, h: 0.68, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
    if (i < 4) varrow(s, 0.91, y + 0.78, 0.2, MUT);
  });
  codebox(s, 8.05, 1.25, 4.75, 2.9, "// captured this week \u2014 the NAKs teach the protocol",
"DM before key exchange:\n \u2192 NAK PKI_SEND_FAIL_PUBLIC_KEY\n   (sender has no pubkey for peer)\n\nDM after peer\u2019s node DB reset:\n \u2192 NAK NO_CHANNEL\n   (peer cannot decrypt PKC \u2014 but the\n    NAK itself ARRIVED OVER RF: the\n    link is proven even as the app fails)", ICE);
  s.addShape("rect", { x: 8.05, y: 4.4, w: 4.75, h: 1.75, fill: { color: INK } });
  s.addText([
    { text: "DESIGN INSIGHT", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Our tracker rides on step 4 only: position broadcasts under the channel key. The v2v link needs no pairing, no session, no per-node state \u2014 a radio that hears one broadcast is fully in the system.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 8.25, y: 4.55, w: 4.35, h: 1.5, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("This is the 'locking' the title promises, and the key point is what is NOT here: no connection, no association, no session like WiFi or Bluetooth. Acquisition is one-directional bookkeeping - I heard you, I filed you, I kept your public key. Steps 4 and 5 split the traffic classes: broadcasts need only the shared channel key (works from the first packet), direct messages are individually encrypted to a node's public key and fail with the exact NAKs shown until NodeInfo has crossed. Both NAKs in the code box are our real captures. The second one is a diagnostic gem: an error REPLY that arrives by radio proves the RF path while the application layer is still refusing - we used it as a link test when nothing else would talk.");
}

// ============================================================ SHEET 06 · two-way proof
{
  const s = pres.addSlide();
  frame(s, "DEO", "verification by traceroute");
  title(s, "Proof of Lock: Round-Trip Traceroute");
  // diagram: request/reply with SNR
  const bx = 0.7, by = 1.45;
  [["SF  !49b5ead4", bx], ["RG  !49b5bb5c", bx + 7.0]].forEach(([t, x]) => {
    s.addShape("rect", { x, y: by, w: 2.3, h: 0.85, fill: { color: CARD }, line: { color: INK, width: 1.5 } });
    s.addText(t, { x, y: by + 0.06, w: 2.3, h: 0.7, align: "center", fontSize: 12, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0, valign: "middle" });
  });
  harrow(s, bx + 2.3, by + 0.22, 4.7, M.DEO);
  s.addText("traceroute request \u00b7 heard at RG with SNR 5.75 dB", { x: bx + 2.5, y: by - 0.14, w: 4.4, h: 0.28, fontSize: 10, fontFace: MONO, color: M.DEO, isTextBox: true, margin: 0 });
  larrow(s, bx + 2.3, by + 0.62, 4.7, GRN);
  s.addText("reply \u00b7 heard back at SF with SNR 6.25 dB", { x: bx + 2.5, y: by + 0.72, w: 4.4, h: 0.28, fontSize: 10, fontFace: MONO, color: GRN, isTextBox: true, margin: 0 });
  codebox(s, 0.7, 2.9, 5.9, 1.85, "$ meshtastic --traceroute \u2018!49b5ead4\u2019",
"Route traced towards destination:\n  !49b5bb5c --> !49b5ead4 (5.75dB)\nRoute traced back to us:\n  !49b5ead4 --> !49b5bb5c (6.25dB)", GRN);
  s.addText([
    B("One command certifies BOTH directions: the request must decode at the peer, the reply must decode back."),
    B("Runs on the routing layer under the channel key \u2014 works before public keys exchange, unlike a DM."),
    B("SNR is reported per hop by the receiver\u2019s demodulator: our link\u2019s health number, logged from day one.", true)],
    { x: 0.7, y: 5.0, w: 5.9, h: 1.6, fontSize: 11.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  // SNR margin bar
  const gx = 7.1, gy = 2.9, gw = 5.6;
  s.addText("WHAT 6 dB MEANS AT SF11", { x: gx, y: gy - 0.38, w: gw, h: 0.3, fontSize: 11, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: gx, y: gy, w: gw, h: 0.55, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  const lo = -22, hi = 10, X = v => gx + (v - lo) / (hi - lo) * gw;
  s.addShape("rect", { x: gx, y: gy, w: X(-17.5) - gx, h: 0.55, fill: { color: "FBEEEF" } });
  s.addShape("line", { x: X(-17.5), y: gy - 0.12, w: 0, h: 0.8, line: { color: RED, width: 2 } });
  s.addText("-17.5 dB demod floor (SF11)", { x: X(-17.5) - 1.3, y: gy + 0.72, w: 2.6, h: 0.26, fontSize: 9, fontFace: MONO, color: RED, align: "center", isTextBox: true, margin: 0 });
  s.addShape("line", { x: X(6), y: gy - 0.12, w: 0, h: 0.8, line: { color: GRN, width: 2.5 } });
  s.addText("measured ~6 dB", { x: X(6) - 1.0, y: gy - 0.42, w: 2.0, h: 0.26, fontSize: 9.5, bold: true, fontFace: MONO, color: GRN, align: "center", isTextBox: true, margin: 0 });
  s.addShape("line", { x: X(-17.5), y: gy + 1.25, w: X(6) - X(-17.5), h: 0, line: { color: INK, width: 1.75, beginArrowType: "triangle", endArrowType: "triangle" } });
  s.addText("23.5 dB of margin before decode fails \u2014 SF11 keeps decoding 17.5 dB BELOW the noise floor",
    { x: gx, y: gy + 1.4, w: gw, h: 0.55, fontSize: 10.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: gx, y: 5.35, w: gw, h: 1.25, fill: { color: INK } });
  s.addText([{ text: "ACCEPTANCE CRITERION 2 \u2014 MET", options: { bold: true, fontSize: 11, color: GRN, fontFace: MONO, breakLine: true, paraSpaceAfter: 4 } },
    { text: "\u201cBoth radios see each other\u201d: round-trip proof on the private channel, repeated after every config change.", options: { color: PAPER, fontSize: 11, fontFace: BFONT } }],
    { x: gx + 0.2, y: 5.5, w: gw - 0.4, h: 1.0, isTextBox: true, margin: 0 });
  s.addNotes("Why traceroute and not a text message: a text proves one direction and needs a human at the far screen; traceroute is machine-checkable, round-trip, and reports per-hop SNR from the receiving demodulator. Explain the margin bar: LoRa's spreading gain means SF11 decodes down to 17.5 dB BELOW the noise floor - that is the negative-SNR magic of chirp spread spectrum. At +6 dB measured, we hold 23.5 dB of margin; every 6 dB of margin is roughly a doubling of free-space distance, which is why the same numbers that look boring on a desk translate to kilometers outdoors. This measurement is the baseline for the W8-W9 range characterization: same command, growing distance, log SNR vs range.");
}

// ============================================================ SHEET 07 · liveness & the ghost
{
  const s = pres.addSlide();
  frame(s, "DEO", "liveness bookkeeping");
  title(s, "\u201cOnline\u201d Is an Equation, Not a Connection");
  s.addImage({ path: D5 + "eq_online.png", x: 0.7, y: 1.2, w: 5.6, h: 0.62 });
  s.addText([
    B("No link-state exists to display \u2014 the counter recomputes this inequality per node, per redraw."),
    B("A radio gone silent stays \u201conline\u201d for up to 2 h; a radio with a STALE STAMP looks dead while talking."),
    B("Bench ghost: a stored July 14 record kept resurfacing from flash after reboots \u2192 \u201c72 d ago\u201d, 0 online \u2014 while texts flowed both ways.", true)],
    { x: 0.7, y: 2.0, w: 6.9, h: 1.8, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addImage({ path: D5 + "fig_timeline.png", x: 0.7, y: 3.9, w: 9.2, h: 2.75 });
  pic(s, IMG + "10.jpg", 10.2, 1.2, 2.6, 3.4, "the ghost on glass: Sig GOOD,\n\u201cHeard: 72d ago\u201d \u2014 same minute");
  s.addShape("rect", { x: 10.2, y: 4.95, w: 2.6, h: 1.6, fill: { color: CARD }, line: { color: ACC, width: 1.25 } });
  s.addText([{ text: "FIXES APPLIED", options: { bold: true, fontFace: MONO, fontSize: 9.5, color: ACC, breakLine: true, paraSpaceAfter: 3 } },
    { text: "purge stored stale positions \u00b7 sync clocks \u00b7 reset node DBs \u00b7 add heartbeat (sheet 08)", options: { fontSize: 10, color: "222A3F" } }],
    { x: 10.33, y: 5.05, w: 2.35, h: 1.42, fontSize: 10, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addNotes("The photo is the sheet: signal GOOD and 'heard 72 days ago' in the same breath - both true, because they answer different questions. Signal quality is measured per packet; 'online' is arithmetic on a stored timestamp against the local clock. Three ways that arithmetic lied to us in one afternoon: a node with no GPS fix rebroadcast its STORED position carrying the old fix time, dragging the peer's last-heard back to July; a reboot reloaded month-old records from flash because the node DB only persists on its own schedule; and after a clock-less reboot the same stale records counted as ONLINE - the screen said 17 online from a two-month-old node list. Same inequality, three failure modes, all timestamp hygiene. None of this can occur in a vehicle with sky view - fresh fixes stamp fresh times continuously.");
}

// ============================================================ SHEET 08 · cadence & heartbeat
{
  const s = pres.addSlide();
  frame(s, "DEO", "traffic cadence design");
  title(s, "The Heartbeat: Designed Traffic Cadence");
  const rows = [
    ["PACKET", "TRIGGER", "INTERVAL", "ROLE IN THE SYSTEM"],
    ["Position", "moving (smart broadcast)", "10 s AND 20 m", "the product: live v2v tracking"],
    ["Position", "stationary, with GPS fix", "60 s", "parked-vehicle presence"],
    ["Device telemetry", "always", "300 s (was 1800)", "liveness floor \u2014 keeps counters honest"],
    ["NodeInfo", "boot + periodic", "~3 h", "names + public keys"],
    ["Text / canned", "operator", "on demand", "15-preset chain, both radios"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 11, bold: i === 0 || j === 2,
      fontFace: i === 0 || j === 2 ? MONO : BFONT,
      color: i === 0 ? PAPER : (i === 3 && j === 2 ? GRN : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.6, y: 1.25, w: 12.2, colW: [2.1, 3.3, 2.3, 4.5], rowH: 0.46,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText([
    B("Why 300 s: worst-case bench radio (parked, indoors, no fix) says nothing else \u2014 30 min gaps let stale flash records flap the counters. A 5-min floor re-stamps peers 24\u00d7 inside the 2 h window."),
    B("Why not faster: liveness costs airtime like everything else \u2014 one ~0.5 s packet per 300 s is 0.17% of the channel; the same packet at 30 s would burn 10\u00d7 that for no product value."),
    B("The design rule: every periodic packet must name the failure it prevents. Position \u2192 tracking staleness. Telemetry \u2192 counter lies. NodeInfo \u2192 unaddressable peers.", true)],
    { x: 0.6, y: 4.35, w: 8.6, h: 2.3, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 9.55, y: 4.35, w: 3.25, h: 2.25, fill: { color: INK } });
  s.addText([
    { text: "MEASURED RESULT", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "With the 5-min heartbeat both OLEDs hold \u201c1 online\u201d steadily on the bench \u2014 first time all week. Verified over 20+ min unplugged.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 9.75, y: 4.5, w: 2.9, h: 2.0, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("This table IS the protocol design of the product - everything else is plumbing. Two rates matter for the demo: 10 s / 20 m while moving (the tracking experience) and the 300 s telemetry floor (the honesty guarantee). The smart broadcast is an AND gate: at highway speed the 20 m distance gate is crossed in under a second, so the 10 s timer dominates; walking pace flips it. Defend the 300 s choice with the two arguments in the bullets: it is 6x denser than the failure window it patches, and 60x cheaper than the channel budget cares about. The rule in the last bullet is worth stating out loud to the sponsor: no packet flows on this channel without a named failure it prevents.");
}

// ============================================================ SHEET 09 · airtime
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "airtime economics");
  title(s, "Airtime: Every Packet Costs Half a Second");
  s.addImage({ path: D5 + "eq_toa.png", x: 0.65, y: 1.18, w: 7.6, h: 0.72 });
  s.addText([
    B("SF11 trades speed for sensitivity: 2\u00b9\u00b9 = 2048 chips/symbol \u2192 8.19 ms/symbol \u2192 ~0.5 s per position packet."),
    B("Flood mesh default: every node REBROADCASTS what it hears (hop limit 3) \u2014 with 2 nodes, each packet flies twice for zero coverage gain."),
    B("Fix: role CLIENT_MUTE on both \u2014 send + receive everything, relay nothing. Utilization halved on the spot: 9\u201313% \u2192 ~5\u20136%.", true)],
    { x: 0.65, y: 2.1, w: 7.55, h: 2.35, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.65, y: 4.6, w: 7.55, h: 1.95, fill: { color: CARD }, line: { color: RULE, width: 1 } });
  s.addText("VEHICLE-RATE BUDGET (both moving, 10 s cadence)", { x: 0.85, y: 4.7, w: 7.2, h: 0.28, fontSize: 10.5, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    { text: "2 \u00d7 (0.5 s / 10 s) = 10%   with relay:   ~20%  \u2014 brushes the throttle", options: { fontFace: MONO, fontSize: 10.5, breakLine: true, paraSpaceAfter: 4, color: RED } },
    { text: "2 \u00d7 (0.5 s / 10 s) = 10%   CLIENT_MUTE:  ~10%  \u2014 2.5\u00d7 headroom held", options: { fontFace: MONO, fontSize: 10.5, breakLine: true, paraSpaceAfter: 6, color: GRN } },
    { text: "Meshtastic suppresses position broadcasts above ~25% utilization \u2014 the throttle would have eaten our 10 s cadence exactly when both vehicles moved.", options: { fontSize: 10.5, color: "222A3F" } }],
    { x: 0.85, y: 5.02, w: 7.2, h: 1.45, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addImage({ path: D5 + "fig_chutil.png", x: 8.5, y: 1.3, w: 4.35, h: 2.85 });
  s.addShape("rect", { x: 8.5, y: 4.4, w: 4.35, h: 2.15, fill: { color: INK } });
  s.addText([
    { text: "REVERT CONDITION", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "CLIENT_MUTE is correct only while the mesh has exactly two nodes. Add a third radio or a relay and both must return to CLIENT \u2014 written into the provisioning recipe.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 8.7, y: 4.55, w: 3.95, h: 1.9, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("Time-on-air is the currency of everything on this channel. Walk the equation: symbol time is two-to-the-SF over bandwidth - at SF11/250k that is 8.19 ms, so even a lean position packet spends around half a second on air. Then the observation that surprised us on the bench: channel utilization ran 9-13% with two IDLE radios, because a flood mesh relays by default and with exactly two nodes every relay is a perfect waste - there is no third radio for the echo to reach. The budget box is the punchline: at drive-test rates the default behavior lands on ~20%, brushing the 25% duty throttle that silently suppresses position broadcasts - the product's core packet - precisely when both vehicles move. CLIENT_MUTE buys the headroom back for free, with the revert condition documented.");
}

// ============================================================ SHEET 10 · link budget
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "link budget");
  title(s, "Link Budget: From Bench Meters to Field Kilometers");
  s.addImage({ path: D5 + "eq_budget.png", x: 0.65, y: 1.18, w: 8.2, h: 0.66 });
  s.addImage({ path: D5 + "fig_linkbudget.png", x: 0.65, y: 2.05, w: 6.55, h: 4.4 });
  const rows = [
    ["TERM", "VALUE", "SOURCE"],
    ["TX power", "+30 dBm", "config, verified both radios"],
    ["Antenna gains", "~0 dBi \u00d7 2", "stock SMA whips"],
    ["Sensitivity S", "\u2212131 dBm", "SX1262 DS, SF11/250 kHz"],
    ["Total budget", "161 dB", "P_tx \u2212 S"],
    ["Free-space limit", "~10\u00b2 km", "where the curve crosses S"],
    ["Design target", "3\u20135 km", "with 20 dB terrain margin"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j === 1,
      fontFace: i === 0 || j === 1 ? MONO : BFONT,
      color: i === 0 ? PAPER : (i >= 5 ? ACC : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 7.5, y: 2.05, w: 5.35, colW: [1.7, 1.45, 2.2], rowH: 0.44,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText("Free space flatters: real streets add clutter, Fresnel blockage, and fading. The 20 dB margin line is the honest design curve \u2014 the W8\u2013W9 range test measures where reality sits between the two.",
    { x: 7.5, y: 5.35, w: 5.35, h: 1.2, fontSize: 11, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addNotes("Read the graph left to right: received power falls 6 dB per doubling of distance; the red dashed line is the SX1262's decode floor at our modulation. The gap between the blue curve and the red line IS the link margin - at bench range it is enormous (about 100 dB), which is why nothing about a desk test predicts range. The dotted green line moves the requirement 20 dB up to absorb real-world fading and obstruction; where the blue curve meets THAT line is the honest few-kilometer design expectation, matching our 3-5 km target for the v2v use case. The free-space crossing near 100 km is a math fact, not a claim - treat it as an upper bound that terrain will spend. Range test protocol: fixed SF11, log traceroute SNR vs GPS distance, plot against this exact chart.");
}

// ============================================================ SHEET 11 · JOSIAH, case requirement
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "display enclosure: requirement");
  title(s, "The Display Needs Armor: Case Selection");
  s.addShape("rect", { x: 0.6, y: 1.2, w: 6.6, h: 1.15, fill: { color: "FBEEEF" }, line: { color: RED, width: 1.5 } });
  s.addText([{ text: "WHY NOW  ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: RED } },
    { text: "our first Waveshare RLCD arrived with a cracked, non-functional panel. The replacement will NOT ride bare: a naked glass panel in a vehicle is a repeat incident waiting to happen.", options: { fontSize: 11.5, color: "222A3F" } }],
    { x: 0.8, y: 1.3, w: 6.25, h: 0.95, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addText([
    B("REQUIREMENTS — protect the glass and edges; keep USB-C + SD card reachable (setup and logs);"),
    B("keep all 3 board buttons usable; keep 18650 battery bay, speaker and rear connector open;"),
    B("plastic body only — zero RF shielding of the BLE antenna; printable overnight on a hobby printer.", true)],
    { x: 0.6, y: 2.55, w: 6.6, h: 1.6, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  const rows = [
    ["FIELD", "SELECTED MODEL"],
    ["Name", "Symmetrical case for WaveShare ESP32-S3 4.2″ RLCD"],
    ["Author / source", "AWSW · Printables model 1610004"],
    ["License", "CC BY-NC 4.0 (attribution, non-commercial) — fits a class project"],
    ["Parts", "7 printed pieces: front frame, 2-piece back, 3 button caps (+ feet)"],
    ["Fasteners", "4× M2.5×6 machine screws into the panel’s existing rear holes"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 0 ? MONO : BFONT,
      color: i === 0 ? PAPER : "222A3F",
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.6, y: 4.35, w: 6.6, colW: [1.75, 4.85], rowH: 0.385,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  pic(s, D5 + "case_front.jpg", 7.65, 1.35, 5.1, 3.82, "the model, assembled: symmetrical bezel, glass fully framed (author’s photo, Printables 1610004)");
  s.addShape("rect", { x: 7.65, y: 5.6, w: 5.1, h: 1.0, fill: { color: INK } });
  s.addText([{ text: "BUY vs PRINT  ", options: { bold: true, fontFace: MONO, fontSize: 10, color: ACC } },
    { text: "no commercial case exists for this panel. Printing one costs ~40 g of filament (~$1) and one printer-night.", options: { color: PAPER, fontSize: 11 } }],
    { x: 7.85, y: 5.7, w: 4.7, h: 0.82, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("PRESENTER PREP - Sheet 11 (Josiah, ~90 s). Open with the incident: our first display arrived cracked and dead - that is not an abstract risk, it already cost us a replacement request to the sponsor. State the requirement set as engineering constraints, not wishes: every port and button the firmware needs must stay reachable, and the case must add zero RF attenuation around the BLE antenna - plastic, not metal, which is why 3D printing fits. Explain the selection: an existing open model by the maker AWSW on Printables (model number 1610004) matches the exact panel; the license is Creative Commons Attribution-NonCommercial 4.0, which permits our academic use with credit - hence the attribution printed on this sheet. Vocabulary to be ready for: RLCD = reflective LCD, the sunlight-readable panel type; 18650 = the cylindrical lithium cell size the board's holder takes; M2.5x6 = metric screw, 2.5 mm thread diameter, 6 mm length; BLE = Bluetooth Low Energy, the radio link between display and Heltec. Question you may get: 'why not design our own?' - answer: zero schedule cost beats originality; we validate fit first, and we can remix later because the license allows derivatives.");
}

// ============================================================ SHEET 12 · JOSIAH, print engineering
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "print engineering");
  title(s, "Print Engineering: Parts, Settings, Slicing");
  const rows = [
    ["PART FILE", "ROLE", "PRINT NOTE"],
    ["front.3mf", "display frame — the armor", "largest part; fuzzy-skin outer walls"],
    ["leftback / rightback.3mf", "two-piece rear cover", "splits to keep battery bay open"],
    ["button1/2/3.3mf", "cap extensions for the 3 board buttons", "tiny — printed sequentially"],
    ["*-with-settings.3mf", "author’s pre-sliced plates", "settings embedded, our starting point"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 0 ? MONO : BFONT,
      color: i === 0 ? PAPER : "222A3F",
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.6, y: 1.2, w: 7.0, colW: [2.15, 2.65, 2.2], rowH: 0.46,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText([
    B("0.2 mm layers, speed profile — layer height: the vertical slice thickness; 0.2 is the strength/time workhorse."),
    B("Organic supports, bed-only — supports: sacrificial scaffolding under overhangs; ‘organic’ = tree-shaped, less scar."),
    B("Fuzzy skin on outer walls — the nozzle jitters to texture the surface: hides layer lines, adds grip."),
    B("No brim; satin sheet — brim: a helper skirt for bed adhesion (not needed); sheet = the print-bed surface finish."),
    B("Sequential (‘separate part’) printing — each small part completes alone: one failure cannot ruin the plate.", true)],
    { x: 0.6, y: 3.75, w: 7.0, h: 2.85, fontSize: 11.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  pic(s, D5 + "case_printbed.jpg", 7.95, 1.2, 4.8, 3.6, "author’s plate on a Prusa MK3: frame with organic supports, buttons + feet printed sequentially");
  pic(s, D5 + "case_buttons.jpg", 7.95, 5.05, 2.1, 1.4, "fuzzy skin + button caps");
  s.addShape("rect", { x: 10.45, y: 5.05, w: 2.3, h: 1.4, fill: { color: CARD }, line: { color: M.JOSIAH, width: 1.25 } });
  s.addText([{ text: "OUR PLAN", options: { bold: true, fontFace: MONO, fontSize: 9.5, color: M.JOSIAH, breakLine: true, paraSpaceAfter: 3 } },
    { text: "PETG, black, 0.2 mm · ~40 g · one overnight run · print when replacement panel ships", options: { fontSize: 10, color: "222A3F" } }],
    { x: 10.6, y: 5.15, w: 2.05, h: 1.25, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 12 (Josiah, ~2 min). Walk the parts table first - seven pieces, and the reason the back is TWO pieces is functional: the split leaves the 18650 battery bay and speaker reachable without disassembly. Then translate every slicer term on the sheet, because the room will not all be printer people: 3MF is the modern print file format (geometry PLUS settings, unlike bare STL); layer height 0.2 mm means each deposited slice is a fifth of a millimeter; supports are sacrificial scaffolding for overhangs and 'organic' means tree-like trunks that touch less surface, so less scarring; fuzzy skin is deliberate nozzle jitter for texture; a brim is a one-layer skirt that fights warping - this model doesn't need one; sequential printing finishes each small part before starting the next so a mid-plate failure cannot wreck everything. Material call: PETG over PLA for a vehicle - a dashboard in Texas sun exceeds PLA's ~60 C glass transition; PETG holds to ~80 C. Point at the bed photo: that is the author's actual plate on a Prusa MK3 - organic supports visible inside the frame. Our plan box: one overnight run, about a dollar of filament, timed to the replacement panel's arrival.");
}

// ============================================================ SHEET 13 · JOSIAH, assembly & integration
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "assembly + integration");
  title(s, "Assembly, Access, and Vehicle Fit");
  const steps = [
    ["1", "Seat panel in front frame", "glass fully captured by the symmetrical bezel"],
    ["2", "Clip on left + right back halves", "battery bay, speaker, rear connector stay open"],
    ["3", "Drive 4× M2.5×6 into existing holes", "⚠ longer screws can crack the panel — 6 mm max"],
    ["4", "Press 3 button caps into top row", "BOOT / RESET / USER stay clickable through the case"]];
  steps.forEach((st, i) => {
    const y = 1.25 + i * 0.88;
    s.addShape("rect", { x: 0.6, y, w: 0.55, h: 0.7, fill: { color: M.JOSIAH } });
    s.addText(st[0], { x: 0.6, y: y + 0.07, w: 0.55, h: 0.56, align: "center", fontSize: 18, bold: true, color: PAPER, fontFace: MONO, isTextBox: true, margin: 0 });
    s.addShape("rect", { x: 1.15, y, w: 6.05, h: 0.7, fill: { color: i % 2 ? CARD : PAPER }, line: { color: RULE, width: 0.75 } });
    s.addText([{ text: st[1] + "   ", options: { bold: true, fontSize: 11 } },
      { text: st[2], options: { fontSize: 10, color: i === 2 ? RED : MUT } }],
      { x: 1.32, y: y + 0.04, w: 5.75, h: 0.62, fontFace: BFONT, color: INK, isTextBox: true, margin: 0, valign: "middle" });
  });
  s.addText([
    B("RF check: PETG/PLA are radio-transparent — BLE link budget unchanged (verified vs bare panel after build)."),
    B("Vehicle fit: flat base for dash mounting; optional angled feet for bench; USB-C exits sideways for strain relief."),
    B("Thermals: RLCD is reflective — no backlight heat; ESP32-S3 dissipates <1 W; vented enough by port openings.", true)],
    { x: 0.6, y: 5.05, w: 6.6, h: 1.6, fontSize: 11.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  pic(s, D5 + "case_ports.jpg", 7.65, 1.25, 5.1, 3.82, "access preserved under armor: USB-C and SD card reachable without opening the case");
  s.addShape("rect", { x: 7.65, y: 5.5, w: 5.1, h: 1.1, fill: { color: INK } });
  s.addText([{ text: "ACCEPTANCE  ", options: { bold: true, fontFace: MONO, fontSize: 10, color: GRN } },
    { text: "case closes with zero pressure on glass · all ports/buttons usable · BLE RSSI within 2 dB of bare panel · survives a 1 m drop onto carpet", options: { color: PAPER, fontSize: 10.5 } }],
    { x: 7.85, y: 5.6, w: 4.7, h: 0.92, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("PRESENTER PREP - Sheet 13 (Josiah, ~90 s). Assembly is four steps and one warning: the M2.5 holes are IN the display's own back, so screw length is a hard limit - the author flags that overlong screws press the glass; 6 mm, no substitutes. Explain what stays reachable and why it matters operationally: USB-C is how we flash and read logs, the SD slot is future data logging, the three buttons are BOOT (bootloader entry for flashing), RESET, and the user button. RF point for the sponsor: the enclosure is thermoplastic, effectively transparent at 2.4 GHz, so the BLE link to the Heltec is untouched - but we still verify by comparing RSSI (received signal strength indicator) cased vs bare, budgeting 2 dB as the pass line. Thermal point: this is a REFLECTIVE LCD - it uses ambient light, no backlight, so the panel adds almost no heat; the ESP32-S3 under load is below a watt, and the port cutouts provide the airflow. Close on the acceptance box - four measurable checks, same discipline as the radio sheets: nothing counts as done until each line is ticked on the bench.");
}

// ============================================================ SHEET 14 · CANNON, drive test protocol
{
  const s = pres.addSlide();
  frame(s, "CANNON", "two-vehicle drive test plan");
  title(s, "Next Milestone: Two-Vehicle Drive Test");
  const rows = [
    ["PHASE", "PROCEDURE", "WHAT IS LOGGED"],
    ["Static A", "both vehicles parked 100 m apart, engines on", "SNR baseline, 10 consecutive traceroutes"],
    ["Convoy", "follow at 2–5 car lengths, 20 min city loop", "update age on display, every position packet"],
    ["Split", "diverge to 0.5 / 1 / 2 km separations", "SNR + delivery vs GPS-measured distance"],
    ["Rejoin", "converge from max range back to convoy", "reacquisition time after silence"],
    ["Stop test", "both parked, exchange canned messages", "two-way texts, counter honesty check"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j === 0,
      fontFace: i === 0 || j === 0 ? MONO : BFONT,
      color: i === 0 ? PAPER : "222A3F",
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.6, y: 1.2, w: 7.4, colW: [1.3, 3.3, 2.8], rowH: 0.5,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText([
    B("Metrics declared in advance (same rule as Week 4): p95 partner-position age ≤ 15 s while moving;"),
    B("zero silent link drops in convoy; reacquisition after split ≤ 60 s; counters honest at every stop."),
    B("Instrumentation: one laptop per vehicle is NOT required — the radios log to their node DBs; we pull tables after each phase over USB.", true)],
    { x: 0.6, y: 4.35, w: 7.4, h: 1.9, fontSize: 11.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 8.35, y: 1.2, w: 4.45, h: 2.6, fill: { color: CARD }, line: { color: M.CANNON, width: 1.5 } });
  s.addText([
    { text: "PREREQUISITES — ALL MET 09-25", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: M.CANNON, breakLine: true, paraSpaceAfter: 5 } },
    { text: "✓ two-way link on Group9 (sheet 06)\n✓ both radios full drive spec, verified\n✓ honest liveness counters (sheet 08)\n✓ airtime headroom held (sheet 09)\n✓ canned message chain for stop tests", options: { fontSize: 11, color: "222A3F" } }],
    { x: 8.55, y: 1.35, w: 4.1, h: 2.3, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 8.35, y: 4.05, w: 4.45, h: 2.55, fill: { color: INK } });
  s.addText([
    { text: "GANTT STATE", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "“Two-vehicle drive tests” moved 0% → 20% (prep complete). The W8–W9 range characterization inherits the Split-phase SNR-vs-distance log and plots it against sheet 10’s predicted curve.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 8.55, y: 4.2, w: 4.1, h: 2.3, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 14 (Cannon, ~2 min). This is the test we could not run until this week - every prerequisite in the pink box was closed on September 25. Walk the five phases in order and give each its purpose: Static A calibrates what 'good' looks like at trivial range; Convoy is the actual product experience - the display's partner age should tick 10-15 s continuously; Split turns distance into data - we drive apart in steps and log SNR (signal-to-noise ratio) against GPS distance, which becomes the measured curve to overlay on the link-budget prediction; Rejoin measures how fast the pair re-locks after real silence - our acceptance is under a minute; Stop test exercises the canned-message chain end to end. Emphasize the discipline line: metrics are declared BEFORE the drive, so success cannot be redefined afterward - p95 means the 95th percentile, i.e., all but the worst 5% of samples must beat 15 seconds. Instrumentation point: the radios themselves are the loggers; node databases are pulled over USB between phases, no laptop rigs in cars. Hand-off: the same logs seed the Week 8-9 formal range characterization.");
}

// ============================================================ SHEET 15 · bench evidence
{
  const s = pres.addSlide();
  frame(s, "CANNON", "bench evidence");
  title(s, "The Bench Record: Four Screens, One Story");
  pic(s, IMG + "19.jpg", 0.7, 1.35, 2.75, 3.6, "BEFORE: 18-node ghost table,\npeers \u201c52\u201377 d\u201d stale");
  pic(s, IMG + "2.jpg", 3.85, 1.35, 2.75, 3.6, "text RX on the bench link \u2014\nmessages flow both ways");
  pic(s, IMG + "27.jpg", 7.0, 1.35, 2.75, 3.6, "AFTER: peer heard \u201c1m\u201d ago \u2014\nfresh stamp, honest counter");
  pic(s, IMG + "23.jpg", 10.15, 1.35, 2.75, 3.6, "home screen: uptime, voltage,\nChUtil \u2014 the health dashboard");
  s.addShape("rect", { x: 0.7, y: 5.45, w: 12.2, h: 1.15, fill: { color: CARD }, line: { color: RULE, width: 1 } });
  s.addText([
    { text: "TEST DISCIPLINE THAT FOUND EVERY BUG THIS WEEK   ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: M.CANNON, breakLine: true, paraSpaceAfter: 4 } },
    { text: "change one variable per trial \u00b7 verify writes with a read-back, then with the OLED \u00b7 prefer machine-checkable probes (traceroute, node DB dumps) over eyeballs \u00b7 log every NAK \u2014 errors localize faults better than successes", options: { fontSize: 11.5, color: "222A3F" } }],
    { x: 0.95, y: 5.55, w: 11.7, h: 0.95, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addNotes("Four photos, chronological. One: the as-received node table - eighteen nodes from the sponsor's summer mesh, all months stale, the raw material of every counter lie on sheet 07. Two: a text landing during the debug session - the moment we knew the RF layer was healthy and the fault was bookkeeping. Three: the same table after the cleanup - peer heard one minute ago, and it stays that way. Four: the home screen we now read as a dashboard - uptime catches silent reboots, voltage catches the charging state, channel utilization catches airtime regressions. The discipline banner is the transferable result: one variable per trial, read-back plus OLED verification, machine-checkable probes, and treat every NAK as data.");
}

// ============================================================ SHEET 12 · config record + references
{
  const s = pres.addSlide();
  frame(s, "CANNON", "configuration + references");
  title(s, "As-Built Configuration and References");
  const rows = [
    ["PARAMETER", "BOTH RADIOS", "PARAMETER", "BOTH RADIOS"],
    ["channel / slot", "Group9 \u00b7 43 \u00b7 912.875 MHz", "gps_update_interval", "10 s"],
    ["preset", "LONG_FAST (SF11/250k/4:5)", "smart broadcast", "10 s AND 20 m"],
    ["tx_power / region", "+30 dBm \u00b7 US", "telemetry heartbeat", "300 s"],
    ["role", "CLIENT_MUTE (2-node)", "position precision", "32 bit (full)"],
    ["bluetooth (SF only)", "NO_PIN, for display", "canned messages", "15-preset chain"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 10.5, bold: i === 0 || j % 2 === 0,
      fontFace: MONO, color: i === 0 ? PAPER : (j % 2 ? GRN : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.6, y: 1.25, w: 12.2, colW: [2.5, 3.6, 2.8, 3.3], rowH: 0.42,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText("Every value --get verified after its write AND cross-checked on the OLED. Full recipe + gotcha log: hardware/README.md (7 commits this week).",
    { x: 0.6, y: 3.85, w: 12.2, h: 0.35, fontSize: 11, fontFace: BFONT, color: MUT, isTextBox: true, margin: 0 });
  const refs = [
    ["[1] Semtech SX1262 Datasheet rev 2.2 \u2014 sensitivity, SNR floors, PA limits", "https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/2R000000Un7F/yT.fKdAr9ZAo3cJLc4F2cBdUsMftpT2vsOICP7NmvMo"],
    ["[2] Meshtastic docs \u2014 Channels & frequency slot calculation", "https://meshtastic.org/docs/overview/radio-settings/"],
    ["[3] Meshtastic docs \u2014 Mesh broadcast algorithm (flood, CSMA, hop limit)", "https://meshtastic.org/docs/overview/mesh-algo/"],
    ["[4] Meshtastic docs \u2014 Device roles (CLIENT / CLIENT_MUTE)", "https://meshtastic.org/docs/configuration/radio/device/"],
    ["[5] Meshtastic docs \u2014 Telemetry module & intervals", "https://meshtastic.org/docs/configuration/module/telemetry/"],
    ["[6] Meshtastic docs \u2014 Encryption: AES-256 channels, PKC direct messages", "https://meshtastic.org/docs/overview/encryption/"],
    ["[7] Semtech AN1200.13 \u2014 LoRa modem time-on-air calculation", "https://www.semtech.com/design-support/lora-calculator"],
    ["[8] 47 CFR \u00a7 15.247 \u2014 US 902\u2013928 MHz ISM rules (Cornell LII)", "https://www.law.cornell.edu/cfr/text/47/15.247"],
    ["[9] AWSW \u2014 Symmetrical case for WaveShare ESP32-S3 4.2\u2033 RLCD, Printables 1610004, CC BY-NC 4.0", "https://www.printables.com/model/1610004-symmetrical-case-for-waveshare-esp32-s3-42inch-rl"]];
  refs.forEach((r, i) => {
    const y = 4.32 + i * 0.27;
    s.addText(r[0], { x: 0.6, y, w: 12.2, h: 0.27, fontSize: 10, fontFace: BFONT, color: "1155CC",
      hyperlink: { url: r[1] }, isTextBox: true, margin: 0 });
  });
  s.addNotes("Close on the as-built table - this is the contract the drive test inherits, every row verified twice (read-back plus OLED). References: [1] backs every sensitivity and SNR number quoted; [2] and [6] together explain the root-cause sheets - name-derived frequency and layered encryption; [3] and [4] back the airtime sheet; [5] the heartbeat; [7] the time-on-air equation; [8] the regulatory envelope for +30 dBm in this band. Next milestones on the board: two-vehicle drive test (in progress, 20%), then range characterization W8-W9 plotted against sheet 10's predicted curve.");
}

// ============================================================ SHEET 17 · nomenclature I
{
  const s = pres.addSlide();
  frame(s, null, "nomenclature I");
  title(s, "Nomenclature I: Acronyms & Abbreviations");
  const L = [
    ["LoRa", "\u201cLong Range\u201d \u2014 chirp spread-spectrum radio modulation"],
    ["SF", "Spreading Factor \u2014 chips per symbol = 2^SF; higher = slower, more sensitive"],
    ["BW", "Bandwidth \u2014 RF channel width; ours 250 kHz"],
    ["CR", "Coding Rate \u2014 forward-error-correction ratio; 4:5 = 1 parity per 4 data bits"],
    ["PHY", "Physical layer \u2014 the radio chip + modulation level of the stack"],
    ["MCU", "Microcontroller Unit \u2014 the ESP32-S3 processor"],
    ["GNSS / GPS", "Global Navigation Satellite System / the US constellation"],
    ["BLE", "Bluetooth Low Energy \u2014 display\u2194radio link at 2.4 GHz"],
    ["RLCD", "Reflective LCD \u2014 sunlight-readable, backlight-free panel"],
    ["OLED", "Organic LED \u2014 the small status screen on each Heltec radio"],
    ["ISM", "Industrial-Scientific-Medical \u2014 license-free band (US: 902\u2013928 MHz)"],
    ["FCC / CFR", "US radio regulator / Code of Federal Regulations (\u00a715.247 is our rule)"],
    ["SMA", "SubMiniature-A \u2014 the screw-on antenna connector"]];
  const R = [
    ["AES-256", "Advanced Encryption Standard, 256-bit key \u2014 channel encryption"],
    ["PSK", "Pre-Shared Key \u2014 the secret both radios hold in the channel URL"],
    ["PKC", "Public-Key Cryptography \u2014 per-node keys used by direct messages"],
    ["DM", "Direct Message \u2014 addressed to one node (vs broadcast to all)"],
    ["ACK / NAK", "ACKnowledge / Negative-AcKnowledge \u2014 delivery yes / delivery failed"],
    ["SNR", "Signal-to-Noise Ratio \u2014 signal strength above the noise, in dB"],
    ["dB / dBm / dBi", "ratio in decibels / power vs 1 milliwatt / antenna gain vs isotropic"],
    ["ChUtil", "Channel Utilization \u2014 % of the last minute the channel carried RF"],
    ["ToA", "Time on Air \u2014 how long one packet occupies the channel"],
    ["CSMA", "Carrier-Sense Multiple Access \u2014 listen before transmit"],
    ["djb2", "Daniel J. Bernstein\u2019s string hash \u2014 picks our frequency slot"],
    ["DTR", "Data Terminal Ready \u2014 serial pin whose toggle hard-resets the ESP32"],
    ["3MF / PETG / PLA", "3D print file format / two thermoplastic filament materials"]];
  [[L, 0.6], [R, 6.75]].forEach(([rows, x]) => {
    const tbl = rows.map((r, i) => r.map((c, j) => ({
      text: c, options: { fontSize: 9.5, bold: j === 0,
        fontFace: j === 0 ? MONO : BFONT, color: j === 0 ? INK : "222A3F",
        fill: { color: i % 2 ? CARD : PAPER }, valign: "middle" } })));
    s.addTable(tbl, { x, y: 1.2, w: 6.0, colW: [1.5, 4.5], rowH: 0.415,
      border: { type: "solid", color: RULE, pt: 0.75 } });
  });
  s.addNotes("PRESENTER PREP - Sheet 17 (whoever fields questions; do not read aloud). This sheet exists so no acronym in the deck is unexplained - point the audience to it once, early ('everything shorthand is decoded on sheet 17'), then leave it for Q&A. Highest-value entries to know cold if asked: SF (spreading factor) - 2 to the SF chips encode each symbol, which is why SF11 is slow but decodes below the noise; dB vs dBm vs dBi - a dB is always a RATIO, dBm anchors it to one milliwatt of power, dBi anchors antenna gain to a perfect point radiator; PSK vs PKC - the channel key everyone shares versus the per-node keypair used only for direct messages - our week's NAKs came from the second one; djb2 - a 1990s string hash, five lines of code, that quietly doubles as Meshtastic's frequency planner. RLCD deserves one sentence: reflective LCD uses ambient light instead of a backlight - that is why it is readable in direct sun on a dashboard and why the case has no thermal problem.");
}

// ============================================================ SHEET 18 · nomenclature II
{
  const s = pres.addSlide();
  frame(s, null, "nomenclature II");
  title(s, "Nomenclature II: Every Formula, Symbol by Symbol");
  const blocks = [
    ["FREQUENCY SLOT  (sheet 03)", "eq_slot.png", 5.9, [
      ["f_slot", "the RF frequency the radio tunes to"],
      ["f_start", "bottom of the US band = 902.0 MHz"],
      ["BW/2", "half a channel \u2014 centers the slot"],
      ["djb2(name) mod N", "hash of the channel name, wrapped to 0..103"],
      ["N_slots = 104", "26 MHz of band \u00f7 250 kHz per channel"]]],
    ["LIVENESS  (sheet 07)", "eq_online.png", 4.4, [
      ["\u21d4", "\u201cif and only if\u201d \u2014 true exactly when the right side holds"],
      ["t_now", "the radio\u2019s own clock, seconds since 1970 (epoch)"],
      ["t_last_heard(n)", "stored timestamp of the last packet from node n"],
      ["7200 s", "the 2-hour \u201conline\u201d window"]]],
    ["TIME ON AIR  (sheet 09)", "eq_toa.png", 5.9, [
      ["T_sym = 2^SF/BW", "seconds per symbol: 2048 chips \u00f7 250,000 chips/s = 8.19 ms"],
      ["N_pre + 4.25", "preamble symbols the receiver locks onto"],
      ["8 + N_payload", "fixed header + payload symbol count"],
      ["T_pkt", "total channel time one packet costs (~0.5 s)"]]],
    ["LINK BUDGET  (sheet 10)", "eq_budget.png", 5.9, [
      ["P_rx / P_tx", "received / transmitted power, in dBm"],
      ["G_tx, G_rx", "antenna gains in dBi (~0 for our whips)"],
      ["20log\u2081\u2080d + 20log\u2081\u2080f \u2212 147.55", "free-space path loss: +6 dB per doubled distance"],
      ["S = \u2212131 dBm", "SX1262 sensitivity: weakest decodable signal at SF11/250k"]]]];
  const pos = [[0.6, 1.15], [6.9, 1.15], [0.6, 4.0], [6.9, 4.0]];
  blocks.forEach((b, k) => {
    const [x, y] = pos[k];
    s.addText(b[0], { x, y, w: 5.9, h: 0.26, fontSize: 10.5, bold: true, fontFace: MONO, color: ACC, isTextBox: true, margin: 0 });
    s.addImage({ path: D5 + b[1], x, y: y + 0.28, w: b[2], h: b[2] > 5 ? 0.52 : 0.5 });
    const tbl = b[3].map((r, i) => r.map((c, j) => ({
      text: c, options: { fontSize: 8.8, bold: j === 0, fontFace: j === 0 ? MONO : BFONT,
        color: j === 0 ? INK : "222A3F", fill: { color: i % 2 ? CARD : PAPER }, valign: "middle" } })));
    s.addTable(tbl, { x, y: y + 0.88, w: 5.9, colW: [2.05, 3.85], rowH: 0.335,
      border: { type: "solid", color: RULE, pt: 0.5 } });
  });
  s.addNotes("PRESENTER PREP - Sheet 18 (reference; walk it only if asked). Each quadrant re-prints one of the deck's four equations and decodes it term by term. Frequency slot: read it as 'start of band, plus half a channel to sit centered, plus hash-of-the-name channels up' - the whole root cause of our silent week lives in that middle term. Liveness: the double arrow means equivalence - 'online' is nothing but this comparison; epoch means seconds counted from January 1st 1970, the universal computer clock. Time on air: the only non-obvious constant is 4.25 - a fixed fraction of the preamble the LoRa standard adds beyond the counted symbols; everything else is symbol counting times 8.19 ms. Link budget: minus 147.55 looks magic but is just the unit bookkeeping of meters and hertz in free-space path loss; the physical content is '+6 dB of loss per doubling of distance'. If someone asks why sensitivity is negative: dBm is logarithmic, so -131 dBm is a tenth of a millionth of a millionth of a milliwatt - the radio decodes signals that small because SF11 spreads each bit across 2048 chips.");
}

pres.writeFile({ fileName: "C:/Users/deogr/Documents/Fall Project/Off-Grid Vehicle dection project/docs/presentations/Group9_Presentation5_RadioLink.pptx" })
  .then(() => console.log("deck 5 written"));
