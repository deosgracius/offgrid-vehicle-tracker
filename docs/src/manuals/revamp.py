import io, re

p = "TECH_MANUAL.html"
s = io.open(p, encoding="utf-8").read()
miss = []
def rep(a, b, n=1):
    global s
    if a in s: s = s.replace(a, b, n)
    else: miss.append(a[:70])

# ================= 1. CSS =================
rep("h2 { font-family: \"Times New Roman\", Times, serif; font-weight: 700; font-size: 15pt; color: #000; margin: 26px 0 8px 0; page-break-after: avoid; }",
    "h2 { font-family: \"Times New Roman\", Times, serif; font-weight: 700; font-size: 15pt; color: #000; margin: 0 0 10px 0; page-break-before: always; page-break-after: avoid; padding-top: 6px; }\n h2.cont { page-break-before: auto; }")
rep("td, th { border: 1px solid #999; padding: 5px 8px; font-size: 10.5pt; vertical-align: top; }",
    "td, th { border: 1px solid #999; padding: 5px 8px; font-size: 12pt; vertical-align: top; }")
rep("th { background: #ECECEC; color: #000; font-family: \"Times New Roman\", Times, serif; font-weight: 700; text-align: left; font-size: 10pt; }",
    "th { background: #ECECEC; color: #000; font-family: \"Times New Roman\", Times, serif; font-weight: 700; text-align: left; font-size: 12pt; }")
rep(".cap { font-family: \"Times New Roman\", Times, serif; font-size: 9.5pt; color: #333; margin-top: 4px; text-align: center; }",
    ".cap { font-family: \"Times New Roman\", Times, serif; font-size: 12pt; color: #333; margin-top: 6px; text-align: center; }")
rep("code, .mono { font-family: \"Courier New\", Consolas, monospace; font-size: 10.5pt; }",
    "code, .mono { font-family: Consolas, \"Courier New\", monospace; font-size: 12pt; }")
rep("pre { background: #1B2440; color: #C9D8F0; border: none; border-radius: 6px; padding: 12px 16px; font-family: Consolas, \"Courier New\", monospace; font-size: 9.5pt; overflow-x: hidden; page-break-inside: avoid; margin: 8px 0 14px 0; }",
    "pre { background: #f6f8fa; color: #1f2328; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px 16px; font-family: Consolas, \"Courier New\", monospace; font-size: 10.5pt; overflow-x: hidden; page-break-inside: avoid; margin: 10px 0 14px 0; }")
rep(".eqimg { display: block; max-width: 100%; max-height: 58px; width: auto; height: auto; margin: 8px 0 4px 0; }",
    ".eqimg { display: block; max-width: 96%; max-height: 64px; width: auto; height: auto; margin: 18px auto 18px auto; }")

# ToC heading must not force a page (cover already breaks) and remove old post-ToC break
rep('<h2 style="text-align:left;">Table of Contents</h2>', '<h2 class="cont" style="text-align:left;">Table of Contents</h2>')
rep('</table>\n<div style="page-break-after: always;"></div>', '</table>')
# appendix/reference h2s already carry page-break-before styles; drop duplicates where inline
s = s.replace('<h2 style="page-break-before: always;">', '<h2>')

# ================= 2. recolor code highlighting: dark palette -> GitHub light =================
s = s.replace("color:#8A93A6;font-style:italic", "color:#6a737d;font-style:italic")   # comments
s = s.replace("color:#E5A05E", "color:#0a3069")                                        # strings
s = s.replace("color:#B08CFF", "color:#cf222e")                                        # keywords
s = s.replace("color:#7BD88F", "color:#0550ae")                                        # numbers

# ================= 3. architecture diagrams (rendered mermaid, as in the repo) =================
rep("An optional relay node on high ground (Section 13) drops into this picture without any change to the vehicles.</p>",
    """An optional relay node on high ground (Section 13) drops into this picture without any change to the vehicles.</p>
<div class="fig"><img src="arch_context.png" style="max-width:96%;">
<div class="cap">Figure 2-1. System context: two identical vehicle installations (docs/ARCHITECTURE.md, sec. 1).</div></div>""")

rep("the flat-battery failure class of Section 16).</p>",
    """the flat-battery failure class of Section 16).</p>
<div class="fig"><img src="arch_radio_hw.png" style="max-width:92%;">
<div class="cap">Figure 2-2. Radio node internal buses (docs/ARCHITECTURE.md, sec. 2).</div></div>
<div class="fig"><img src="arch_display_hw.png" style="max-width:88%;">
<div class="cap">Figure 2-3. Display node: ESP32-S3 driving the reflective LCD from PSRAM.</div></div>
<div class="fig"><img src="arch_power.png" style="max-width:88%;">
<div class="cap">Figure 2-4. In-cab interconnect and vehicle power.</div></div>""")

rep("(it is at version 5; Section 9.1 lists its fields).</p>",
    """(it is at version 5; Section 9.1 lists its fields).</p>
<div class="fig"><img src="arch_firmware.png" style="max-width:96%;">
<div class="cap">Figure 2-5. Display firmware: FreeRTOS tasks joined by the TrackerState contract (docs/ARCHITECTURE.md, sec. 3).</div></div>""")

rep("so a lost packet costs seconds of freshness, never correctness.</p>",
    """so a lost packet costs seconds of freshness, never correctness.</p>
<div class="fig"><img src="arch_dataflow.png" style="max-width:96%;">
<div class="cap">Figure 2-6. End-to-end data flow, one position's journey (docs/ARCHITECTURE.md, sec. 4).</div></div>""")

# replace the ASCII BLE state machine with the rendered diagram
m = re.search(r"<pre>SCANNING.*?</pre>", s, re.S)
if m:
    s = s.replace(m.group(0),
        """<div class="fig"><img src="arch_blestate.png" style="max-width:62%;">
<div class="cap">Figure 2-7. The BLE link state machine as implemented in ble_link.cpp (docs/ARCHITECTURE.md, sec. 5).</div></div>""")
else:
    miss.append("ascii state machine")

# ================= 4. completeness: exact tables from the source documents =================
rep("This is what let four people work in parallel all semester: no one's test depended on anyone's unfinished code.</p>",
    """This is what let four people work in parallel all semester: no one's test depended on anyone's unfinished code.</p>
<table>
<tr><th>Interface</th><th>Independent test (no other custom code needed)</th></tr>
<tr><td>GPS &rarr; Meshtastic</td><td>Heltec OLED + Meshtastic phone app show the fix</td></tr>
<tr><td>LoRa A &harr; B</td><td>Two phones running the Meshtastic app see each other's position</td></tr>
<tr><td>BLE Client API</td><td>Meshtastic Python CLI over BLE from a laptop proves the API before any firmware exists</td></tr>
<tr><td>TrackerState &rarr; UI</td><td>Sim feed drives the full UI with zero radios</td></tr>
<tr><td>Whole chain</td><td>Bench: walk one radio around the parking lot, watch the arrow</td></tr>
</table>""")

rep("projection never resets the age, and past 30 seconds the direction dart is drawn hollow." if False else "connectionless broadcasts without acknowledgments because staleness, which the UI displays, is the honest reliability metric for superseding data.</p>",
    """connectionless broadcasts without acknowledgments because staleness, which the UI displays, is the honest reliability metric for superseding data.</p>
<table>
<tr><th>Decision</th><th>Why, given the vehicle environment</th></tr>
<tr><td>Reflective LCD (not TFT / e-paper)</td><td>Sunlight-readable on a dash where a TFT washes out; refreshes fast enough for a rotating arrow, which e-paper is not; near-zero power</td></tr>
<tr><td>Heading from GPS course-over-ground (no compass)</td><td>A magnetometer inside a steel vehicle is unreliable; COG is accurate above ~5 mph, and a driving use case is usually moving</td></tr>
<tr><td>Separate display unit (not a phone, not the radio's OLED)</td><td>Off-grid means no phone dependency; drivers need a glanceable 4.2-inch screen; phones die in cold vehicles</td></tr>
<tr><td>12 V vehicle power (no battery management)</td><td>Both units powered whenever the vehicle runs, the exact time tracking is needed</td></tr>
<tr><td>Connectionless broadcasts, no ACKs</td><td>A newer position supersedes an older one; the meaningful metric is staleness, which the UI displays</td></tr>
</table>""")

rep("Terrain in the way: any mesh node relays automatically within the hop limit.</p>",
    """Terrain in the way: any mesh node relays automatically within the hop limit.</p>
<table>
<tr><th>Failure</th><th>Behavior</th></tr>
<tr><td>Partner out of LoRa range</td><td>Arrow holds last fix; age counts up; driver sees "4 min old"</td></tr>
<tr><td>Own GPS loses lock</td><td>Distance and bearing still computed from the last own fix; flagged</td></tr>
<tr><td>BLE drops in-cab</td><td>UI shows link-lost; ble_link re-scans and re-pairs automatically</td></tr>
<tr><td>Vehicle stationary (no COG heading)</td><td>Arrow falls back to north-referenced compass-rose mode</td></tr>
<tr><td>Terrain blocks the direct path</td><td>Any Meshtastic node in the mesh relays automatically (hop limit 3)</td></tr>
</table>""")

rep("<h3>5.4 The system as a telecommunications design</h3>",
    """<h3>5.4 The system as a telecommunications design</h3>
<table>
<tr><th>Layer</th><th>This project</th><th>Telecom concepts involved</th></tr>
<tr><td>Application</td><td>Position payload (lat/lon/course, protobuf, ~30-40 B)</td><td>Source coding, payload efficiency</td></tr>
<tr><td>Transport / network</td><td>Meshtastic managed flooding, hop limit 3, AES-256</td><td>Routing vs flooding, TTL, rebroadcast suppression</td></tr>
<tr><td>MAC</td><td>CSMA with SNR-weighted random backoff</td><td>ALOHA/CSMA, contention, airtime fairness</td></tr>
<tr><td>PHY</td><td>LoRa chirp spread spectrum, 915 MHz ISM, SX1262</td><td>Modulation, spreading gain, sensitivity, FEC</td></tr>
<tr><td>Local link</td><td>BLE GATT (radio to display), 2.4 GHz</td><td>Short-range wireless, GATT services</td></tr>
</table>""")

rep("On the return leg, reacquisition was automatic: ages back in the teens by 0.85 mi with the dart at twelve o'clock at 37 mph.</p>",
    """On the return leg, reacquisition was automatic: ages back in the teens by 0.85 mi with the dart at twelve o'clock at 37 mph.</p>
<table>
<tr><th>Separation</th><th>Screen evidence</th><th>Reading</th></tr>
<tr><td>19 ft</td><td>"at 11 o'clock, age 15s", both kits together</td><td>Baseline, GNSS scatter only</td></tr>
<tr><td>610 ft</td><td>"at 3 o'clock, apart 24 mph", CHANGE COURSE banner</td><td>Off-course warning fires correctly</td></tr>
<tr><td>0.64-0.74 mi</td><td>"apart 46 mph" then "apart 56 mph"</td><td>Separation rate = sum of both speeds; trend correct</td></tr>
<tr><td>1.58 mi</td><td>"N of you, apart 17 mph", single-digit age</td><td>Live tracking, fresh data</td></tr>
<tr><td>3.26 mi</td><td>LINK CONNECTED; both coordinate sets live; age 1m (parked cadence)</td><td>Full health at 5.25 km; displayed distance matches the coordinate delta exactly</td></tr>
<tr><td>3.75 mi</td><td>SF DATA STALE, age 2m inverted; "Message failed"</td><td>The edge, flagged honestly on both devices</td></tr>
<tr><td>0.85 mi (return)</td><td>"at 12 o'clock, age 14s, you 37 mph"</td><td>Reacquired on the drive back, dart dead ahead</td></tr>
<tr><td>127 ft</td><td>"at 2 o'clock, age 3s"</td><td>Reunion; ages back to seconds</td></tr>
</table>""")

rep("in agreement with the two-ray height arithmetic of Section 5.3.</p>",
    """in agreement with the two-ray height arithmetic of Section 5.3.</p>
<table>
<tr><th>Time (CDT)</th><th>Separation</th><th>Data age</th><th>Reading</th></tr>
<tr><td>7:27a</td><td>2.78 mi</td><td>2 min, STALE</td><td>Outbound; canyon wall between vehicles</td></tr>
<tr><td>7:30a</td><td>4.28 mi</td><td>1 min</td><td>Age reset while stale: one packet through a ridge gap</td></tr>
<tr><td>7:31a</td><td>~3.92 mi</td><td>2 min</td><td>Stale again, vehicle nearly stopped</td></tr>
<tr><td>7:32a</td><td>4.46 mi</td><td>3 min, STALE</td><td>Turnaround; the outage ultimately ran 7 minutes</td></tr>
<tr><td>7:38a</td><td>2.90 mi</td><td>54 s</td><td>Return leg; reacquisition beginning</td></tr>
<tr><td>7:42a</td><td>1.45 mi</td><td>11 s</td><td>Fully live, partner at 12 o'clock, closing 45 mph</td></tr>
<tr><td>~7:44a</td><td>0.33 mi</td><td>21 s</td><td>Guided final approach</td></tr>
</table>""")

rep("The vehicles' radios stay in CLIENT_MUTE exactly as provisioned: vehicle A's broadcast reaches the repeater, the repeater rebroadcasts once, vehicle B hears it one hop later.",
    """The vehicles' radios stay in CLIENT_MUTE exactly as provisioned: vehicle A's broadcast reaches the repeater, the repeater rebroadcasts once, vehicle B hears it one hop later.</p>
<pre>python -m meshtastic --port COMx --set lora.region US
python -m meshtastic --port COMx --seturl "&lt;Group9 channel URL - hardware/README.md&gt;"
python -m meshtastic --port COMx --set device.role ROUTER
python -m meshtastic --port COMx --set-owner "RPT" --set-owner-short "RPT"
python -m meshtastic --port COMx --set position.position_broadcast_secs 900</pre>
<p>""")

# ================= 5. section 14: full fleet-flash procedure =================
rep("<h2>14. Build, flash, and test procedures</h2>\n<p>The commands below",
    "<h2>14. Build, flash, and test procedures</h2>\n<h3>14.1 Daily quick reference</h3>\n<p>The commands below")

rep("Bring-up of a new display follows the checklist in <code>firmware-display/README.md</code>: SIM proof, BLE link, partner tracking, the position-re",
    "Bring-up of a new display follows the checklist in <code>firmware-display/README.md</code>: SIM proof, BLE link, partner tracking, the position-re")

FLASH = """
<h3>14.2 Flashing the entire fleet from a clean checkout</h3>
<p>This procedure takes a fresh computer from nothing to a fully flashed and provisioned fleet, using only the repository and publicly available tools. It assumes Windows; the commands are identical on macOS or Linux apart from port names.</p>
<p><b>Step 1, tools.</b> Install Git, Python 3.11 or newer, and VS Code with the PlatformIO extension (or <code>pip install platformio</code> for the command line alone). Then install the radio tooling:</p>
<pre>pip install meshtastic esptool
git clone https://github.com/deosgracius/offgrid-vehicle-tracker.git
cd offgrid-vehicle-tracker</pre>
<p><b>Step 2, identify every board before touching anything.</b> All four boards share USB VID:PID 303A:1001, so the serial number (the MAC) is the only safe identity. Plug in one device at a time and read it from Device Manager (the USB Composite Device's instance ID) or <code>pio device list</code>:</p>
<table>
<tr><th>Unit</th><th>MAC (SER=)</th><th>Firmware it must carry</th></tr>
<tr><td>Radio SF</td><td>8C:FD:49:B5:EA:D4</td><td>Stock Meshtastic 2.7.26 (heltec-v4)</td></tr>
<tr><td>Radio RG</td><td>8C:FD:49:B5:BB:5C</td><td>Stock Meshtastic 2.7.26 (heltec-v4)</td></tr>
<tr><td>Display 1</td><td>A4:CB:8F:D0:7D:40</td><td>This repository, env <code>display-ble</code></td></tr>
<tr><td>Display 2</td><td>94:A9:90:DD:14:3C</td><td>This repository, env <code>display-ble</code></td></tr>
</table>
<p>Flashing the wrong firmware onto a radio erases Meshtastic (scar catalog entry 8). Never let a tool auto-pick the port.</p>
<p><b>Step 3, flash a display.</b> From the repository root:</p>
<pre>cd firmware-display
pio run -e display-ble -t upload --upload-port COMx
pio device monitor --port COMx --baud 115200   # expect: "RLCD init OK", "[ble] init done"</pre>
<p>The pioarduino platform and <code>dio_opi</code> memory flags in <code>platformio.ini</code> are mandatory; the stock espressif32 platform boot-loops this panel. The display needs no further configuration: it learns its radio's address by scanning and stores it in NVS.</p>
<p><b>Step 4, flash a radio.</b> Use the official web flasher at flasher.meshtastic.org (select Heltec V4, firmware 2.7.26), or from the command line with the factory binary from the Meshtastic firmware release archive:</p>
<pre>esptool --port COMx erase_flash
esptool --port COMx write_flash 0x0 firmware-heltec-v4-2.7.26.factory.bin</pre>
<p>The node number is derived from the MAC, so it survives re-flashing and the display reconnects unchanged.</p>
<p><b>Step 5, provision the radio.</b> Run the complete recipe in <code>hardware/README.md</code>: region, the Group9 channel URL, position cadence, Bluetooth mode NO_PIN, and the owner name. Reverts arrive in batches, so always run the whole block, verify every value by read-back, power-cycle, and verify again (Section 16, entries 2, 6, and 10).</p>
<p><b>Step 6, verify the fleet.</b> Both radio OLEDs read 912.875 MHz; each display pairs within the radio's first advertising minute and shows the link tag; <code>pio test -e native</code> passes 12 of 12; and a round-trip traceroute between the radios returns single-digit dB SNR at desk range. The fleet is now exactly the configuration every measurement in this manual was made on.</p>"""
rep("<h2>15. Verification record</h2>", FLASH + "\n<h2>15. Verification record</h2>")

io.open(p, "w", encoding="utf-8").write(s)
print("missed:", miss)
