// Week 5 deck, rev F — "Locking the Link", 12 slides.
// Deo: the link (02-04) · Victor: the math (05-07) · Cannon: demo + testing (08-10) · Josiah: case (11-12)
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

const TOTAL = 12;
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
  s.addText("SHEET " + String(sheetNo).padStart(2, "0") + "/" + TOTAL + "  REV F  2026-09-26",
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
function larrow(s, x, y, w, color) {
  s.addShape("line", { x, y, w, h: 0, line: { color: color || INK, width: 2.25, beginArrowType: "triangle" } });
}
function varrow(s, x, y, h, color) {
  s.addShape("line", { x, y, w: 0, h, line: { color: color || INK, width: 2.25, endArrowType: "triangle" } });
}
function pic(s, path, x, y, w, h, cap) {
  s.addImage({ path, x, y, w, h });
  s.addShape("rect", { x, y, w, h, fill: { type: "none" }, line: { color: RULE, width: 1 } });
  if (cap) s.addText(cap, { x: x - 0.25, y: y + h + 0.02, w: w + 0.5, h: 0.42, fontSize: 8.5, color: MUT,
    align: "center", fontFace: MONO, isTextBox: true, margin: 0 });
}

// ============================================================ SHEET 01 · cover
{
  const s = pres.addSlide();
  frame(s, null, "week 5 review");
  for (let gx = 0.68; gx < 13.0; gx += 0.5)
    s.addShape("line", { x: gx, y: 0.16, w: 0, h: 6.7, line: { color: "E8EDF5", width: 0.5 } });
  for (let gy = 0.66; gy < 6.86; gy += 0.5)
    s.addShape("line", { x: 0.18, y: gy, w: 12.97, h: 0, line: { color: "E8EDF5", width: 0.5 } });
  s.addText("LOCKING THE LINK", { x: 0.7, y: 1.35, w: 11.9, h: 0.9, fontSize: 46, bold: true,
    charSpacing: 3, fontFace: HFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText("HOW OUR TWO RADIOS TALK TO EACH OTHER", { x: 0.72, y: 2.3, w: 11.9, h: 0.45,
    fontSize: 18, bold: true, charSpacing: 1, fontFace: HFONT, color: ACC, isTextBox: true, margin: 0 });
  s.addText("2026-09-25: round-trip radio link established and verified on the private Group9 channel.",
    { x: 0.72, y: 2.95, w: 8.3, h: 0.4, fontSize: 13.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  const rows = [
    ["02\u201304", "DEO", "what makes it possible, and how the link happens"],
    ["05\u201307", "VICTOR", "the math: frequency, signal margin, airtime"],
    ["08\u201310", "CANNON", "live demo on the radios + how we tested"],
    ["11\u201312", "JOSIAH", "3D-printed armor for the display"]];
  rows.forEach((r, i) => {
    const y = 3.75 + i * 0.62;
    s.addShape("rect", { x: 0.72, y, w: 8.3, h: 0.52, fill: { color: i % 2 ? CARD : PAPER }, line: { color: RULE, width: 0.75 } });
    s.addText([{ text: r[0] + "  ", options: { fontFace: MONO, bold: true, color: ACC } },
      { text: r[1] + "  ", options: { fontFace: MONO, bold: true, color: M[r[1]] } },
      { text: r[2], options: { color: "222A3F" } }],
      { x: 0.95, y: y + 0.05, w: 7.9, h: 0.42, fontSize: 12.5, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  });
  const blk = [["PROJECT", "Off-Grid Vehicle Tracker"], ["SPONSOR", "Dr. Richard Gale"],
    ["MILESTONE", "Radio link ESTABLISHED"], ["HOURS", "218 of 768 logged"], ["DATE", "2026-09-26"]];
  s.addShape("rect", { x: 9.55, y: 3.3, w: 3.3, h: 3.0, fill: { color: PAPER }, line: { color: INK, width: 1.25 } });
  blk.forEach((r, i) => {
    const y = 3.37 + i * 0.575;
    if (i) s.addShape("line", { x: 9.55, y: y - 0.035, w: 3.3, h: 0, line: { color: RULE, width: 0.75 } });
    s.addText(r[0], { x: 9.7, y, w: 1.6, h: 0.28, fontSize: 9, bold: true, fontFace: MONO, color: MUT, isTextBox: true, margin: 0 });
    s.addText(r[1], { x: 9.7, y: y + 0.24, w: 3.05, h: 0.3, fontSize: 10.5, fontFace: BFONT, color: i === 2 ? GRN : INK, bold: i === 2, isTextBox: true, margin: 0 });
  });
  s.addNotes("PRESENTER PREP - Sheet 01 (~45 s, whoever opens). One headline, deliver it standing still: on September 25 the two radios completed round-trip verification on our own private channel - the tracker's radio backbone exists. Then hand out the map: Deo explains what makes two radios able to talk at all and how the link forms; Victor shows the math that decides the frequency, the signal margin, and the airtime; Cannon runs the LIVE demo on the actual radios and explains how the testing was done; Josiah closes with the 3D-printed protection for the display. Do not preview details - every claim gets its own sheet. Total run target: 15 minutes plus demo time.");
}

// ============================================================ SHEET 02 · DEO, what makes it possible
{
  const s = pres.addSlide();
  frame(s, "DEO", "what makes it possible");
  title(s, "What Makes Two Radios Able to Talk");
  [["RADIO \u201cSF\u201d", 0.7], ["RADIO \u201cRG\u201d", 9.3]].forEach(([t, x]) => {
    s.addShape("rect", { x, y: 1.45, w: 3.3, h: 2.1, fill: { color: CARD }, line: { color: INK, width: 1.5 } });
    s.addText(t, { x, y: 1.55, w: 3.3, h: 0.32, align: "center", fontSize: 13, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
    [["GPS", "own position, 10 s"], ["Meshtastic", "ESP32 + firmware"], ["LoRa radio", "SX1262, +30 dBm"]].forEach((r, i) => {
      const y = 1.95 + i * 0.5;
      s.addText([{ text: r[0] + "  ", options: { bold: true, fontFace: MONO, color: M.DEO, fontSize: 10 } },
        { text: r[1], options: { color: "222A3F", fontSize: 10.5 } }],
        { x: x + 0.25, y, w: 2.9, h: 0.4, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
    });
  });
  s.addShape("rect", { x: 4.4, y: 1.65, w: 4.5, h: 1.7, fill: { color: PAPER }, line: { color: ACC, width: 1.5, dashType: "dash" } });
  s.addText([
    { text: "NO WIRES. NO TOWERS. NO PAIRING.", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: ACC, breakLine: true, paraSpaceAfter: 4 } },
    { text: "Both radios independently tune the same frequency, speak the same modulation, and hold the same key. Agreement IS the connection.", options: { fontSize: 11.5, color: "222A3F" } }],
    { x: 4.6, y: 1.8, w: 4.1, h: 1.45, fontFace: BFONT, isTextBox: true, margin: 0 });
  harrow(s, 4.0, 2.5, 0.4, M.DEO); larrow(s, 8.9, 2.5, 0.4, M.DEO);
  const rows = [
    ["MUST MATCH", "OURS", "PROVEN BY"],
    ["Frequency \u2014 slot 43, 912.875 MHz", "channel name \u201cGroup9\u201d", "OLED frequency, both radios"],
    ["Modulation \u2014 SF11 / 250 kHz", "LONG_FAST preset", "packets decode both ways"],
    ["Encryption \u2014 AES-256 key", "shared channel key", "texts readable both ways"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 10 : 12, bold: i === 0 || j === 0,
      fontFace: i === 0 ? MONO : BFONT, color: i === 0 ? PAPER : (j === 2 ? GRN : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.7, y: 4.0, w: 11.9, colW: [4.6, 3.4, 3.9], rowH: 0.58,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addNotes("PRESENTER PREP - Sheet 02 (Deo, ~2 min). Core idea to land: LoRa has no connection in the WiFi/Bluetooth sense - no pairing, no session, no negotiation. Two radios can talk exactly when they independently agree on three things: where to listen (frequency), how symbols are shaped (modulation), and how bytes are scrambled (encryption key). Say it as the slide does: agreement IS the connection. Walk the three rows and their proof column - each one was verified this week on our hardware, not assumed. Vocabulary to have ready: LoRa = long-range chirp modulation; SF11 = spreading factor 11, each bit spread over 2048 chips which buys sensitivity at the cost of speed; AES-256 = the standard symmetric cipher, the same key on both radios; SX1262 = the radio chip; +30 dBm = one full watt of transmit power. If asked how the radios got the same settings: both were provisioned from the same channel URL - a QR-style string that carries the channel name and key. Segue to sheet 03: matching settings make talking POSSIBLE - here is how the link actually forms.");
}

// ============================================================ SHEET 03 · DEO, how the link happens
{
  const s = pres.addSlide();
  frame(s, "DEO", "how the link happens");
  title(s, "How the Link Happens: Locking On");
  const steps = [
    ["1", "ANNOUNCE", "on boot, each radio broadcasts its name + public key (NodeInfo)", INK],
    ["2", "FILE", "the receiver records it: last-heard time + signal quality", INK],
    ["3", "TRACK", "every packet refreshes the record \u2014 \u201c1 online\u201d appears", GRN],
    ["4", "ADDRESS", "with keys exchanged, private direct messages unlock", ACC]];
  steps.forEach((st, i) => {
    const y = 1.3 + i * 1.02;
    s.addShape("rect", { x: 0.7, y, w: 0.62, h: 0.8, fill: { color: st[3] } });
    s.addText(st[0], { x: 0.7, y: y + 0.1, w: 0.62, h: 0.6, align: "center", fontSize: 20, bold: true, color: PAPER, fontFace: MONO, isTextBox: true, margin: 0 });
    s.addShape("rect", { x: 1.32, y, w: 6.3, h: 0.8, fill: { color: i % 2 ? CARD : PAPER }, line: { color: RULE, width: 0.75 } });
    s.addText([{ text: st[1] + "   ", options: { bold: true, fontFace: MONO, fontSize: 11, color: st[3] } },
      { text: st[2], options: { fontSize: 11.5, color: "222A3F" } }],
      { x: 1.5, y: y + 0.06, w: 6.0, h: 0.68, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
    if (i < 3) varrow(s, 1.01, y + 0.8, 0.22, MUT);
  });
  s.addText("No step needs a human. Power two configured radios and the lock forms by itself.",
    { x: 0.7, y: 5.6, w: 6.9, h: 0.6, fontSize: 12.5, bold: true, fontFace: BFONT, color: INK, isTextBox: true, margin: 0 });
  codebox(s, 8.05, 1.3, 4.75, 2.5, "// the lock, proven on air (09-25)",
"$ meshtastic --traceroute \u2018!49b5ead4\u2019\nRoute traced towards destination:\n  !49b5bb5c --> !49b5ead4 (5.75dB)\nRoute traced back to us:\n  !49b5ead4 --> !49b5bb5c (6.25dB)", GRN);
  s.addShape("rect", { x: 8.05, y: 4.05, w: 4.75, h: 2.15, fill: { color: INK } });
  s.addText([
    { text: "WHY THIS COMMAND", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "One traceroute proves BOTH directions: the request must decode at the far radio, and its reply must decode back. Our acceptance criterion in a single line.", options: { color: PAPER, fontFace: BFONT, fontSize: 12 } }],
    { x: 8.25, y: 4.2, w: 4.35, h: 1.9, fontSize: 12, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 03 (Deo, ~2 min). The ladder is the whole acquisition story: announce, file, track, address. Emphasize there is no handshake - each radio just OVERHEARS the other's boot announcement (called NodeInfo) and starts bookkeeping: when it last heard the peer, and how strong. That bookkeeping is what the OLED's '1 online' counter reads. Step 4 nuance if asked: broadcasts (positions, channel texts) only need the shared channel key and work from the first packet; PRIVATE direct messages are encrypted per node with the public keys exchanged in step 1 - until that exchange happens a DM is refused with an error code, which we actually observed and used as a diagnostic. The code box is the milestone proof, real output: traceroute sends a request and requires the reply, so one command certifies both directions with signal-to-noise numbers per hop - 5.75 and 6.25 dB. Hand to Victor with: 'those dB numbers, the frequency, and what they buy us - that is Victor's math.'");
}

// ============================================================ SHEET 04 · DEO, staying linked
{
  const s = pres.addSlide();
  frame(s, "DEO", "staying linked");
  title(s, "Staying Linked: The Heartbeat");
  s.addImage({ path: D5 + "eq_online.png", x: 0.7, y: 1.25, w: 5.3, h: 0.6 });
  s.addText("\u201cOnline\u201d is arithmetic: heard within 2 hours. There is no live connection to display \u2014 only timestamps.",
    { x: 0.7, y: 2.05, w: 6.4, h: 0.7, fontSize: 12.5, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  const rows = [
    ["WHEN", "THE RADIO SENDS", "EVERY"],
    ["Driving", "position (the product)", "10 s / 20 m"],
    ["Parked, GPS fix", "position", "60 s"],
    ["Always", "telemetry heartbeat", "5 min"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 10 : 12, bold: i === 0 || j === 2,
      fontFace: i === 0 || j === 2 ? MONO : BFONT, color: i === 0 ? PAPER : (j === 2 ? GRN : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.7, y: 2.95, w: 6.4, colW: [1.7, 2.9, 1.8], rowH: 0.52,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText("The 5-minute heartbeat was added after bench testing: it keeps the counters honest even when a parked radio has nothing else to say.",
    { x: 0.7, y: 5.35, w: 6.4, h: 0.95, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addImage({ path: D5 + "fig_timeline.png", x: 7.35, y: 1.45, w: 5.5, h: 1.7 });
  pic(s, IMG + "10.jpg", 7.85, 3.45, 2.1, 2.8, "the trap we found: signal GOOD,\n\u201cheard 72 d ago\u201d \u2014 stale timestamp");
  s.addShape("rect", { x: 10.25, y: 3.45, w: 2.55, h: 2.8, fill: { color: INK } });
  s.addText([
    { text: "TESTED, NOT ASSUMED", options: { bold: true, fontSize: 10, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "We chased every counter lie to a stale timestamp, purged them, added the heartbeat \u2014 then watched both radios hold \u201c1 online\u201d steadily.", options: { color: PAPER, fontFace: BFONT, fontSize: 11 } }],
    { x: 10.42, y: 3.6, w: 2.2, h: 2.5, fontSize: 11, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 04 (Deo, ~90 s). Read the equation once in words: a node counts as online exactly when now minus its last-heard time is under 7200 seconds, two hours. That's it - no link state exists. Consequence one: a switched-off radio stays 'online' on the other screen for up to two hours, by design; in a broadcast mesh nothing distinguishes off from out-of-range except silence. Consequence two, the photo: if a STORED timestamp is stale, the counter lies the other way - our bench radio showed signal GOOD and 'heard 72 days ago' in the same breath, because a July record kept resurfacing. The cadence table is the cure and the design: positions every 10 seconds or 20 meters while driving - that IS the tracker experience - a gentler 60 seconds parked, and a 5-minute telemetry heartbeat always, added specifically so bench-idle radios keep re-stamping each other. Cost of the heartbeat if asked: one half-second packet per 5 minutes, about 0.17% of the channel. Timestamp vocabulary: epoch = seconds counted since Jan 1 1970.");
}

// ============================================================ SHEET 05 · VICTOR, frequency math
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "the frequency math");
  title(s, "Math I: The Name Picks the Frequency");
  s.addImage({ path: D5 + "eq_slot.png", x: 0.7, y: 1.3, w: 7.3, h: 0.78 });
  codebox(s, 8.55, 1.2, 4.25, 2.0, "// djb2 \u2014 the whole algorithm",
"h = 5381\nfor each character c:\n    h = h * 33 + c\nslot = h mod 104\n\n\u201cGroup9\u201d \u2192 slot 43 \u2192 912.875 MHz");
  s.addImage({ path: D5 + "fig_slots.png", x: 0.7, y: 2.6, w: 9.0, h: 2.85 });
  s.addShape("rect", { x: 0.7, y: 5.75, w: 12.1, h: 0.85, fill: { color: CARD }, line: { color: ACC, width: 1.25 } });
  s.addText([{ text: "WHY IT MATTERS  ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: ACC } },
    { text: "two radios with identical keys but different primary channel names sit MHz apart and never hear each other \u2014 we proved this the hard way, then fixed it. The OLED LoRa screen shows the live frequency: our truth-teller.", options: { fontSize: 11.5, color: "222A3F" } }],
    { x: 0.95, y: 5.85, w: 11.6, h: 0.68, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("PRESENTER PREP - Sheet 05 (Victor, ~2 min). Read the equation left to right: start of the US band (902 MHz), plus half a channel width so the slot sits centered, plus the hash of the channel NAME times the channel width. 104 slots because the band is 26 MHz wide and each LONG_FAST channel takes 250 kHz. The hash is djb2 - the five lines in the code box are the complete algorithm. WHO IS BERNSTEIN (know this cold): Daniel J. Bernstein is a famous living cryptographer - a math professor in Chicago, known online as 'djb'. He is not part of our project or of Meshtastic; he published this tiny text-to-number recipe on Usenet in the 1990s and programmers named it djb2 after his initials. The same way engineers use Ohm's law without Ohm, software uses Bernstein's hash without Bernstein. Bonus tie-in: his OTHER famous invention, the Curve25519 encryption curve - used by WhatsApp and Signal - is what Meshtastic uses for private direct messages. Two parts of our stack, one mathematician, zero involvement. Calibration proof if challenged: the default channel name hashes to slot 19 = 906.875 MHz, the published US default - so the formula checks out against a known constant before we trust it for Group9 = 43 = 912.875. Close with the banner: this math is why a NAME mismatch is a FREQUENCY mismatch, which is exactly the failure we diagnosed and fixed this week.");
}

// ============================================================ SHEET 06 · VICTOR, signal margin math
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "the margin math");
  title(s, "Math II: What 6 dB of Signal Buys");
  const gx = 0.7, gy = 1.9, gw = 7.2;
  s.addText("MEASURED SNR vs THE SF11 DECODE FLOOR", { x: gx, y: gy - 0.42, w: gw, h: 0.3, fontSize: 11, bold: true, fontFace: MONO, color: INK, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: gx, y: gy, w: gw, h: 0.6, fill: { color: CARD }, line: { color: RULE, width: 0.75 } });
  const lo = -22, hi = 10, X = v => gx + (v - lo) / (hi - lo) * gw;
  s.addShape("rect", { x: gx, y: gy, w: X(-17.5) - gx, h: 0.6, fill: { color: "FBEEEF" } });
  s.addShape("line", { x: X(-17.5), y: gy - 0.12, w: 0, h: 0.85, line: { color: RED, width: 2.25 } });
  s.addText("decode floor: \u221217.5 dB", { x: X(-17.5) - 1.3, y: gy + 0.78, w: 2.6, h: 0.26, fontSize: 9.5, fontFace: MONO, color: RED, align: "center", isTextBox: true, margin: 0 });
  s.addShape("line", { x: X(6), y: gy - 0.12, w: 0, h: 0.85, line: { color: GRN, width: 2.5 } });
  s.addText("measured: ~6 dB", { x: X(6) - 1.0, y: gy - 0.42, w: 2.0, h: 0.26, fontSize: 9.5, bold: true, fontFace: MONO, color: GRN, align: "center", isTextBox: true, margin: 0 });
  s.addShape("line", { x: X(-17.5), y: gy + 1.3, w: X(6) - X(-17.5), h: 0, line: { color: INK, width: 1.75, beginArrowType: "triangle", endArrowType: "triangle" } });
  s.addText("23.5 dB of margin \u2014 SF11 still decodes 17.5 dB BELOW the noise floor",
    { x: gx, y: gy + 1.45, w: gw, h: 0.35, fontSize: 11.5, bold: true, fontFace: BFONT, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    { text: "Rule of thumb: every 6 dB of margin \u2248 double the free-space distance.", options: { fontSize: 12.5, bold: true, color: "222A3F", breakLine: true, paraSpaceAfter: 6 } },
    { text: "Desk numbers that look ordinary translate to kilometers outdoors \u2014 the margin is the range.", options: { fontSize: 12, color: "222A3F" } }],
    { x: 0.7, y: 4.1, w: 7.2, h: 1.1, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.7, y: 5.35, w: 7.2, h: 1.2, fill: { color: CODEBG } });
  s.addText([{ text: "dB DECODER  ", options: { bold: true, fontFace: MONO, fontSize: 10, color: ACC } },
    { text: "dB = a ratio on a log scale (+3 dB \u2248 \u00d72, +10 dB = \u00d710) \u00b7 dBm = power vs 1 milliwatt \u00b7 SNR = signal-to-noise ratio, how far the signal stands above the static.", options: { color: ICE, fontSize: 11 } }],
    { x: 0.9, y: 5.45, w: 6.8, h: 1.0, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addImage({ path: D5 + "fig_linkbudget.png", x: 8.25, y: 1.3, w: 4.55, h: 3.1 });
  s.addShape("rect", { x: 8.25, y: 4.7, w: 4.55, h: 1.85, fill: { color: INK } });
  s.addText([
    { text: "THE RANGE PREDICTION", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "+30 dBm out, \u2212131 dBm decodable = 161 dB budget. With 20 dB reserved for streets and terrain: a 3\u20135 km design range. The drive test measures where reality lands.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 8.45, y: 4.85, w: 4.15, h: 1.6, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 06 (Victor, ~2 min). Start with the bar: the red line is where SF11 stops decoding - minus 17.5 dB, meaning the signal can be 17.5 dB WEAKER than the noise and still come through. That is the superpower of chirp spread spectrum: each bit is spread over 2048 chips, and the receiver adds them back up coherently. Our measured 6 dB positive leaves 23.5 dB of headroom. Give the audience the conversion rule slowly: 6 dB of margin doubles free-space range - so 23.5 dB is roughly 2 to 4 doublings, which is how a boring desk measurement promises kilometers outside. The dB decoder box is for the room: dB is always a ratio (log scale, +3 is double, +10 is ten times), dBm pins that ratio to one milliwatt, SNR is how far the signal stands above the static. Right graph: transmit power +30 dBm (one watt) minus the -131 dBm sensitivity gives a 161 dB total budget; free-space alone would reach absurd distances, so we reserve 20 dB for buildings, terrain, and fading, landing on the honest 3-5 km design range. The W8-W9 drive data gets plotted onto this exact chart.");
}

// ============================================================ SHEET 07 · VICTOR, airtime math
{
  const s = pres.addSlide();
  frame(s, "VICTOR", "the airtime math");
  title(s, "Math III: Airtime Is the Budget");
  s.addImage({ path: D5 + "eq_toa.png", x: 0.65, y: 1.25, w: 7.6, h: 0.72 });
  s.addText([
    { text: "Every packet costs ~0.5 s of air. The channel throttles at 25% busy.", options: { fontSize: 13, bold: true, color: "222A3F", breakLine: true, paraSpaceAfter: 8 } },
    { text: "Two moving vehicles at 10 s cadence = 10% \u2014 but the mesh default RELAYS every packet, doubling it to ~20%. With only two radios a relay reaches no one.", options: { fontSize: 12, color: "222A3F", breakLine: true, paraSpaceAfter: 8 } },
    { text: "Fix, verified on the bench: role CLIENT_MUTE \u2014 hear everything, repeat nothing. Utilization halved: 9\u201313% \u2192 ~5\u20136%.", options: { fontSize: 12, color: "222A3F" } }],
    { x: 0.7, y: 2.3, w: 7.4, h: 2.6, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 0.7, y: 5.15, w: 7.4, h: 1.4, fill: { color: CODEBG } });
  s.addText([{ text: "SYMBOL DECODER  ", options: { bold: true, fontFace: MONO, fontSize: 10, color: ACC } },
    { text: "T_sym = time per symbol: 2\u00b9\u00b9 chips \u00f7 250,000/s = 8.19 ms \u00b7 N_pre = preamble symbols the receiver locks onto \u00b7 N_payload = data symbols \u00b7 ChUtil = % of the last minute the channel carried radio energy.", options: { color: ICE, fontSize: 10.5 } }],
    { x: 0.9, y: 5.25, w: 7.0, h: 1.2, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addImage({ path: D5 + "fig_chutil.png", x: 8.5, y: 1.3, w: 4.35, h: 2.85 });
  s.addShape("rect", { x: 8.5, y: 4.45, w: 4.35, h: 2.1, fill: { color: INK } });
  s.addText([
    { text: "WHY IT MATTERED", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "Above 25% busy, Meshtastic suppresses position broadcasts \u2014 our core packet \u2014 exactly when both vehicles move. CLIENT_MUTE keeps us at 2.5\u00d7 headroom. Revert to CLIENT if a third radio ever joins.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 8.7, y: 4.6, w: 3.95, h: 1.85, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 07 (Victor, ~90 s). The equation first: symbol time is 2-to-the-SF divided by bandwidth - 8.19 milliseconds at our settings - and a packet is just a count of symbols times that, roughly half a second for a position. That makes airtime the scarce resource, and Meshtastic enforces it: above about 25% channel utilization it starts suppressing position broadcasts. Now the discovery from our own bench: two IDLE radios were burning 9-13% - because a flood mesh relays by default, and with exactly two nodes every relay is pure waste, there is no third radio to reach. Project the vehicle case: 10% of legitimate traffic becomes 20% with relaying - brushing the throttle right when both vehicles move. The fix costs nothing: CLIENT_MUTE role, radios still hear and send everything but repeat nothing; measured utilization halved same day. The revert condition is documented: a third node or relay joins, both radios go back to CLIENT. Hand off to Cannon: 'that is the theory and the numbers - Cannon shows you the real thing.'");
}

// ============================================================ SHEET 08 · CANNON, demo I
{
  const s = pres.addSlide();
  frame(s, "CANNON", "live demo: messaging");
  title(s, "Live Demo I: Send It, Receive It");
  s.addShape("rect", { x: 0.7, y: 1.15, w: 12.1, h: 0.5, fill: { color: M.CANNON } });
  s.addText("LIVE ON THE RADIOS \u2014 slides show the bench captures; the demo repeats them in front of you",
    { x: 0.7, y: 1.2, w: 12.1, h: 0.4, align: "center", fontSize: 11.5, bold: true, color: PAPER, fontFace: MONO, isTextBox: true, margin: 0 });
  // demo flow: 3 stages
  s.addShape("rect", { x: 0.7, y: 2.0, w: 3.6, h: 4.3, fill: { color: PAPER }, line: { color: M.CANNON, width: 1.5, dashType: "dash" } });
  s.addText([
    { text: "STEP 1 \u00b7 LIVE", options: { bold: true, fontFace: MONO, fontSize: 11, color: M.CANNON, breakLine: true, paraSpaceAfter: 6 } },
    { text: "On radio SF: open the canned-message menu with the user button, scroll to \u201cHi\u201d, send.", options: { fontSize: 12, color: "222A3F", breakLine: true, paraSpaceAfter: 8 } },
    { text: "15 presets loaded on both radios: OK \u00b7 Yes \u00b7 No \u00b7 Hi \u00b7 How are you? \u00b7 All good \u00b7 Need help \u00b7 Are you injured? \u00b7 Send position \u00b7 Position updated \u00b7 On my way \u00b7 Wait there \u00b7 Arrived \u00b7 Low battery \u00b7 Heading home", options: { fontSize: 10.5, color: MUT } }],
    { x: 0.95, y: 2.2, w: 3.1, h: 3.9, fontFace: BFONT, isTextBox: true, margin: 0 });
  pic(s, IMG + "2.jpg", 4.75, 2.0, 3.2, 4.27, "STEP 2: the text lands on RG \u2014 no phone, no tower, radio to radio");
  pic(s, IMG + "27.jpg", 8.4, 2.0, 3.2, 4.27, "STEP 3: RG\u2019s Last-Heard list re-stamps \u2014 \u201cSF \u00b7 1m\u201d \u2014 the link bookkeeping updating live");
  s.addNotes("PRESENTER PREP - Sheet 08 (Cannon, demo ~3 min). Bring both radios charged and already on. Choreography: hold SF up, press the user button to open the canned-message menu, scroll to 'Hi', send - then walk to RG (or have a teammate hold it) and show the message popping up, then flip RG to the Last-Heard screen and show SF's entry reading seconds ago. Narrate what is NOT there: no phone, no SIM, no tower, no internet - the text crossed on our private 912.875 MHz channel, encrypted with our key. If the room is RF-noisy or a send is missed, the slide's bench captures are the backstop - same screens, captured during the week's testing. Mention why canned messages exist: while driving nobody types; every question in the preset chain has its answer preset too (How are you? -> All good / Need help; Are you injured? -> Yes / No). Timing note: leave the radios visible for sheet 09, where we walk the rest of the screens.");
}

// ============================================================ SHEET 09 · CANNON, demo II
{
  const s = pres.addSlide();
  frame(s, "CANNON", "live demo: reading the radio");
  title(s, "Live Demo II: Reading the Radio");
  const cells = [
    [IMG + "13.jpg", "DISTANCE \u2014 fills when both\nradios hold a GPS fix"],
    [IMG + "12.jpg", "BEARING \u2014 compass direction\nto the partner vehicle"],
    [IMG + "20.jpg", "POSITION \u2014 sats, fix, altitude\n(indoors: No Fix, honestly)"],
    [IMG + "27.jpg", "LAST HEARD \u2014 seconds since\neach node spoke"],
    [IMG + "9.jpg", "LORA \u2014 preset, live frequency,\nchannel utilization"],
    [IMG + "22.jpg", "SYSTEM \u2014 firmware, memory\n(ver 2.7.26 on both)"],
    [IMG + "7.jpg", "TIME \u2014 GPS-disciplined clock\n(needs a fix to be right)"],
    [IMG + "10.jpg", "NODE PAGE \u2014 per-peer signal\nquality: SF as seen by RG"]];
  cells.forEach((c, i) => {
    const x = 0.7 + (i % 4) * 3.1, y = i < 4 ? 1.25 : 4.0;
    pic(s, c[0], x + 0.35, y, 1.72, 2.29, c[1]);
  });
  s.addNotes("PRESENTER PREP - Sheet 09 (Cannon, ~2-3 min with radios in hand). Walk the OLED screens in this order on a live radio - short-press the user button cycles pages: DISTANCE and BEARING - the tracker's core outputs, straight-line meters and compass direction to the partner; they show '?' indoors because geometry needs BOTH positions - say that plainly, it is honesty, not failure. POSITION - satellites, fix state, altitude. LAST HEARD - the liveness list Deo explained, now live. LORA - the contract sheet in hardware: preset, the actual synthesizer frequency (912.875 = our private slot; this screen is the truth-teller from Victor's math), and channel utilization. SYSTEM - firmware 2.7.26, identical on both radios, deliberately. TIME - GPS-disciplined; mention it also drives the timestamps behind 'online'. NODE PAGE - per-peer signal bars: RG's view of SF. If a screen looks different live than on the slide, better: the captures are from mid-debug week; the live radios are the fixed, final configuration.");
}

// ============================================================ SHEET 10 · CANNON, how we tested
{
  const s = pres.addSlide();
  frame(s, "CANNON", "how the testing was done");
  title(s, "How the Testing Was Done");
  const rows = [
    ["TECHNIQUE", "WHAT IT MEANS", "WHAT IT CAUGHT / PROVED"],
    ["One variable per trial", "change one setting, retest, log", "isolated the frequency-slot mismatch"],
    ["A/B regression", "retreat to a known-good config, rebuild", "default channel worked \u2192 fault was in ours"],
    ["Machine probes", "traceroute + node-table dumps, not eyeballs", "round-trip proof, timestamps, SNR"],
    ["Read-back + OLED verify", "every config write checked twice", "caught silently reverting writes"],
    ["Log every error", "NAK codes treated as data", "a NAK that ARRIVES proves the RF path"]];
  const tbl = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: { fontSize: i === 0 ? 9.5 : 11, bold: i === 0 || j === 0,
      fontFace: i === 0 ? MONO : BFONT, color: i === 0 ? PAPER : (j === 2 ? GRN : "222A3F"),
      fill: { color: i === 0 ? INK : (i % 2 ? CARD : PAPER) }, valign: "middle" } })));
  s.addTable(tbl, { x: 0.7, y: 1.25, w: 7.6, colW: [2.2, 2.8, 2.6], rowH: 0.62,
    border: { type: "solid", color: RULE, pt: 0.75 } });
  s.addText("Every fix is committed to the repo with its gotcha documented \u2014 the next person hits none of these twice.",
    { x: 0.7, y: 5.35, w: 7.6, h: 0.7, fontSize: 12, fontFace: BFONT, color: "222A3F", isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 8.65, y: 1.25, w: 4.15, h: 2.5, fill: { color: CARD }, line: { color: M.CANNON, width: 1.5 } });
  s.addText([
    { text: "NEXT: TWO-VEHICLE DRIVE TEST", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: M.CANNON, breakLine: true, paraSpaceAfter: 5 } },
    { text: "convoy \u2192 split to 0.5/1/2 km \u2192 rejoin \u2192 stop-and-message. Metrics declared in advance: p95 position age \u2264 15 s moving; reacquire \u2264 60 s.", options: { fontSize: 11.5, color: "222A3F" } }],
    { x: 8.85, y: 1.4, w: 3.75, h: 2.25, fontFace: BFONT, isTextBox: true, margin: 0 });
  s.addShape("rect", { x: 8.65, y: 4.0, w: 4.15, h: 2.55, fill: { color: INK } });
  s.addText([
    { text: "STATUS", options: { bold: true, fontSize: 10.5, color: ACC, fontFace: MONO, breakLine: true, paraSpaceAfter: 5 } },
    { text: "All prerequisites met 09-25: two-way link, full drive spec on both radios, honest counters, airtime headroom. Gantt: drive test 0% \u2192 20%; link milestone closed at 100%.", options: { color: PAPER, fontFace: BFONT, fontSize: 11.5 } }],
    { x: 8.85, y: 4.15, w: 3.75, h: 2.3, fontSize: 11.5, isTextBox: true, margin: 0 });
  s.addNotes("PRESENTER PREP - Sheet 10 (Cannon, ~2 min). This sheet is the credibility of everything before it: the link works because the testing was disciplined, not lucky. Walk the five techniques with their catches: changing ONE variable per trial is what finally isolated the frequency mismatch after config comparisons showed nothing; the A/B regression - dropping both radios to the known-good default channel - split the world in half in one test (hardware fine, our channel config guilty); machine-checkable probes (traceroute, node database dumps over USB) replaced squinting at screens and produced numbers we could commit; every configuration write got verified twice - read back over serial AND cross-checked on the OLED - because we caught writes silently reverting; and error codes were treated as evidence - a refusal that arrives BY RADIO proves the radio path even while the app layer says no. p95 explainer for the metrics box: the 95th percentile - all but the worst 5% of samples must beat the bar - so one bad sample cannot fake a pass, and one lucky one cannot hide a problem. Close: every gotcha is committed to the repo README, so none of them can bite twice.");
}

// ============================================================ SHEET 11 · JOSIAH, the case
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "display armor: the case");
  title(s, "Protecting the Display: The Case");
  s.addShape("rect", { x: 0.7, y: 1.25, w: 6.5, h: 1.05, fill: { color: "FBEEEF" }, line: { color: RED, width: 1.5 } });
  s.addText([{ text: "WHY  ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: RED } },
    { text: "our first display arrived cracked and dead. The replacement rides in armor.", options: { fontSize: 12.5, color: "222A3F" } }],
    { x: 0.9, y: 1.35, w: 6.15, h: 0.85, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  const rows = [
    ["Keeps working", "USB-C \u00b7 SD card \u00b7 all 3 buttons \u00b7 battery bay \u00b7 speaker"],
    ["Zero RF impact", "plastic body \u2014 invisible to the BLE radio link"],
    ["Model", "\u201cSymmetrical case\u201d by AWSW \u00b7 Printables 1610004 \u00b7 CC BY-NC 4.0"],
    ["Cost", "~40 g filament (\u2248 $1) \u00b7 one overnight print"]];
  rows.forEach((r, i) => {
    const y = 2.6 + i * 0.78;
    s.addShape("rect", { x: 0.7, y, w: 6.5, h: 0.66, fill: { color: i % 2 ? CARD : PAPER }, line: { color: RULE, width: 0.75 } });
    s.addText([{ text: r[0] + "   ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: M.JOSIAH } },
      { text: r[1], options: { fontSize: 11.5, color: "222A3F" } }],
      { x: 0.92, y: y + 0.04, w: 6.1, h: 0.58, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  });
  s.addText("No commercial case exists for this panel \u2014 printing is the only option, and the community already solved it.",
    { x: 0.7, y: 5.9, w: 6.5, h: 0.65, fontSize: 11.5, fontFace: BFONT, color: MUT, isTextBox: true, margin: 0 });
  pic(s, D5 + "case_front.jpg", 7.7, 1.25, 5.05, 3.79, "the model assembled \u2014 glass fully framed, screen fully visible (author\u2019s photo)");
  s.addNotes("PRESENTER PREP - Sheet 11 (Josiah, ~90 s). Open with the incident, one sentence: the first display arrived cracked and non-functional - that is why this exists, not cosmetics. Then the four rows: everything the firmware needs stays reachable (USB-C for flashing and logs, SD for future logging, the three board buttons via printed caps, battery bay and speaker open at the rear); the body is thermoplastic so it is invisible to the 2.4 GHz BLE link between display and radio; the model is an existing open design - 'Symmetrical case for the WaveShare ESP32-S3 4.2 inch RLCD' by the maker AWSW on Printables, model 1610004, licensed Creative Commons Attribution-NonCommercial, which our class use satisfies with exactly this credit; and the whole thing costs about a dollar of filament and one overnight print. Anticipate 'why not design our own?': validating a proven fit costs zero schedule; the license allows remixing later if the vehicle mount needs changes. RLCD if asked: reflective LCD - reads by ambient light, no backlight, hence sunlight-readable on a dash.");
}

// ============================================================ SHEET 12 · JOSIAH, print + assembly
{
  const s = pres.addSlide();
  frame(s, "JOSIAH", "print + assembly");
  title(s, "Print It, Screw It, Done");
  const rows = [
    ["7 parts", "front frame \u00b7 2-piece back \u00b7 3 button caps (+ feet)"],
    ["Settings", "0.2 mm layers \u00b7 organic supports \u00b7 fuzzy-skin walls \u00b7 no brim"],
    ["Material", "PETG \u2014 survives dashboard heat where PLA softens"],
    ["Assembly", "seat panel \u2192 clip backs \u2192 4\u00d7 M2.5\u00d76 screws \u2192 press caps"],
    ["\u26a0 One rule", "6 mm screws MAX \u2014 longer screws press on the glass"]];
  rows.forEach((r, i) => {
    const y = 1.3 + i * 0.82;
    const warn = i === 4;
    s.addShape("rect", { x: 0.7, y, w: 6.5, h: 0.7, fill: { color: warn ? "FBEEEF" : (i % 2 ? CARD : PAPER) }, line: { color: warn ? RED : RULE, width: warn ? 1.5 : 0.75 } });
    s.addText([{ text: r[0] + "   ", options: { bold: true, fontFace: MONO, fontSize: 10.5, color: warn ? RED : M.JOSIAH } },
      { text: r[1], options: { fontSize: 11.5, color: "222A3F" } }],
      { x: 0.92, y: y + 0.05, w: 6.1, h: 0.6, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  });
  s.addShape("rect", { x: 0.7, y: 5.6, w: 6.5, h: 0.95, fill: { color: INK } });
  s.addText([{ text: "ACCEPTANCE  ", options: { bold: true, fontFace: MONO, fontSize: 10, color: GRN } },
    { text: "zero pressure on glass \u00b7 every port/button usable \u00b7 BLE signal within 2 dB of bare \u00b7 survives a 1 m drop", options: { color: PAPER, fontSize: 11 } }],
    { x: 0.9, y: 5.7, w: 6.1, h: 0.75, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  pic(s, D5 + "case_printbed.jpg", 7.7, 1.25, 5.05, 3.5, "author\u2019s plate on a Prusa MK3 \u2014 organic supports, small parts sequential");
  pic(s, D5 + "case_ports.jpg", 7.7, 5.32, 1.4, 1.05, "USB-C + SD open");
  s.addShape("rect", { x: 9.35, y: 5.32, w: 3.4, h: 1.05, fill: { color: CARD }, line: { color: M.JOSIAH, width: 1.25 } });
  s.addText([{ text: "PLAN  ", options: { bold: true, fontFace: MONO, fontSize: 9.5, color: M.JOSIAH } },
    { text: "print the night the replacement panel ships \u2014 armor on before first power-up.", options: { fontSize: 10.5, color: "222A3F" } }],
    { x: 9.52, y: 5.4, w: 3.1, h: 0.9, fontFace: BFONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("PRESENTER PREP - Sheet 12 (Josiah, ~90 s). Keep it brisk - five rows, one warning, one photo. Seven printed parts; the back is deliberately TWO pieces so the battery bay and speaker stay reachable without disassembly. Settings vocabulary, one breath each: 0.2 mm layers - each deposited slice a fifth of a millimeter, the strength/speed workhorse; organic supports - tree-shaped sacrificial scaffolding under overhangs, snapped off after; fuzzy skin - the nozzle deliberately jitters to texture the outer walls, hiding layer lines and adding grip; no brim - the helper skirt for bed adhesion isn't needed here. Material: PETG over PLA because a Texas dashboard exceeds PLA's roughly 60-degree softening point; PETG holds to about 80. Assembly is four moves ending in the ONE RULE row - the screw holes are in the display's own back, so 6 mm maximum length or the screws press the glass; this is the model author's own warning. Acceptance is measurable, same discipline as the radio sheets: no pressure on glass, everything usable, BLE within 2 dB of the bare panel, survives a 1-meter drop. Plan: the print runs the night the replacement panel ships.");
}

pres.writeFile({ fileName: "C:/Users/deogr/Documents/Fall Project/Off-Grid Vehicle dection project/docs/presentations/Group9_Presentation5_RadioLink.pptx" })
  .then(() => console.log("deck 5 rev F written"));
