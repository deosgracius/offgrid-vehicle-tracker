# Presenter's companion to `Group9_Presentation.pptx` (REV D, 20 sheets)

Plain-language explanations of the things on the sheets that are easy to say wrong, the glossary the audience may ask about, and the attribution wording. Read this once before presenting; the speaker notes in the deck carry the shorter version.

## Part I

### Sheet 2: what "the catalog" is

The catalog is Section 16 of the Technical Manual, "Failure modes and recovery (the scar catalog)". It is a table with four columns: number, **symptom** (what you see, written the way a stranger would see it), **root cause**, **recovery** (the exact steps). Eleven entries. Every entry is something that happened on our hardware and was reproduced or root-caused before it was written down. Sheet 2 shows entry 1 as the example. When you say "signature" you mean the symptom column: the thing that lets the next person recognise the failure in minutes.

### Sheet 4: "SM confirm mismatch, rc=1284"

Bluetooth Low Energy pairing is handled by a part of the stack called the Security Manager (SM). When two devices pair with a PIN, each side computes a "confirm value" from the PIN and random numbers and they compare them. Our radio shipped in RANDOM_PIN mode: it shows a six-digit PIN on its screen and expects the other side to type it. The display has no keypad, so it could not enter the PIN, the two confirm values did not match, and the stack reported return code 1284. In the NimBLE stack that number is 0x500 + 4: 0x500 means "a Security Manager error on our side", and error 4 is "confirm value failed". Fix: provision the radio with `bluetooth.mode NO_PIN` (Just-Works pairing, still encrypted). That is why a radio that forgets its settings shows up on the display's log as `status 261, insufficient authentication`: the radio has gone back to wanting a PIN.

### Sheet 5: "precision 13 truncates every broadcast"

Meshtastic sends latitude and longitude as 32-bit integers in units of 1e-7 degree. Each channel has a `position_precision` setting that says how many of those 32 bits to keep; the rest are zeroed and the position is set to the centre of the resulting cell. The default for a private channel is 13 bits. The cell is then 2^(32-13) x 1e-7 degree = 0.0524 degree, which is 5.8 km of latitude (about 4.9 km of longitude at Lubbock). So every broadcast landed on the centre of a 6 km cell and the partner looked frozen until it crossed into the next cell. We set precision 32: full resolution, about 1 cm.

### Sheet 5: GPS jitter

A parked GPS receiver does not report exactly the same position every second. Satellite geometry, the atmosphere and reflections off buildings move the fix by a few metres between readings. The receiver turns that movement into a speed, so a parked car reads 1 to 3 mph. We ignore any speed under 4.5 km/h (the deadband). Indoors the same effect is much larger: weak signals through a roof scatter the fix by 100 to 400 m, and the receiver can report a coherent but completely false velocity. That is what produced the "0.21 mi between two radios on one desk" observation on October 24. Rule: judge distances only with a sky view.

### Sheet 6: "phone-app QR path when no laptop is at hand"

The Meshtastic phone app can take the whole channel (name, key, precision) from a QR code. The Group9 QR is in the private README. Recovery without a laptop: open the app, connect to the radio over Bluetooth, scan the QR to restore the channel, then set the region to US and Bluetooth pairing to No PIN. User Guide Section 12.1 has the steps. With a laptop the faster path is `meshtastic --configure sf-config.yaml` run twice (Section 12.2).

### Sheet 6: frequency slots

The US band runs 902 to 928 MHz and the LONG_FAST preset cuts it into 104 slots of 250 kHz. Meshtastic picks the slot from a hash of the channel **name** (djb2 of "Group9" mod 104 = 43, which is 902.125 + 43 x 0.25 = 912.875 MHz). A radio that reverts to the default channel name moves to 906.875 MHz. Same key, different slot: nothing is heard, both screens look healthy, and the CLI reads back the intended configuration. The OLED frequency is the only honest instrument, hence the pre-flight rule.

## Part II

### Sheet 9: the three meanings of "the memory itself"

The settings live in a 3.4 MB corner of a 16 MB flash chip. "The memory is at fault" could mean: (1) **worn out**, cells exhausted by too many writes, which would show as scattered damage everywhere; (2) **defective cells**, fixed bad spots that stay bad even after being rewritten; (3) **written under bad conditions**, healthy cells that were left half-written because the supply voltage sagged during a write, which show as fixed bad spots that heal once rewritten. Each needs a different fix (replace the part; avoid the sectors; never write under low voltage), so the whole of Part II is about telling them apart.

### Sheet 10: how the settings are stored; LittleFS

The firmware keeps six small files (channel, config, device, module settings, node list, presets) in a file system called **LittleFS**. LittleFS is a tiny file system designed for microcontrollers that is meant to survive power loss: it writes new data before deleting old. That protection only works if the chip itself stores what it was told to store. The firmware rewrites one of those files (device.proto) on every boot with no check of the supply voltage, and if a file will not read it does not retry or consult the backup: it writes factory settings over it and carries on. The one protection that exists is that the firmware's own low-battery shutdown skips the write, which shows the authors knew the danger.

### Sheet 11: the 260 mV window (what the sheet achieves)

This is the mechanism, the reason a perfectly good chip can end up holding garbage. The CPU keeps running down to 2.44 V, where its brownout detector resets it. The flash chip only guarantees to store data above 2.70 V. Between those two numbers, 260 mV, the CPU is alive and can order a write, but the chip may not finish it correctly. A sector erase takes 50 ms and a transmit pulse draws about 750 mA; on a nearly flat cell that pulse can drag the 3.3 V rail through the window and back without the CPU ever resetting. A flash cell stores a small charge and a read compares it with a threshold; a write cut short leaves the charge near the threshold, so the same cell reads 1 one time and 0 the next. That is the fingerprint the measurement looks for.

### Sheet 12: the "#" numbers

`#4555` is issue number 4555 in the public bug tracker at github.com/meshtastic/firmware/issues. Each issue is a report from a user, with the maintainers' replies. A **PR** (pull request) is a proposed code change; PR #11872 is the change that fixed the same problem on the nRF52 family of boards in 2026. There is no equivalent change for the ESP32 boards we run.

### Sheet 14: the method

Stop the firmware (the esptool "stub" takes over the chip), read the whole 3.4 MB settings area three times in a row through one open USB connection, and compare the three copies. A healthy chip returns identical bytes every time. The controls are a megabyte of program code, the NVS partition and the bootloader read the same way: they came back identical, so the method is sound and any difference in the settings area is the chip's doing. The pitfall: this board resets whenever the USB serial port closes, so running three separate esptool commands would hide a boot, and a boot-time write, between the reads. Only reads inside one open connection count.

### Sheet 15: reading the sector maps

Each small square is one 4 KB sector; there are 864 in the settings area. Red squares gave different bytes on consecutive reads with nothing running, the same squares every time and at both serial speeds. Green squares held the live settings files that day (they happened to be clean, which is why SF was still working). Grey is stale data that read stably; pale is erased. SF had 21 red squares, RG had none.

### Sheet 16: numbers, decisive test, repair

117 and 107 bytes differed between reads one and two and reads two and three; 118 bits flipped, in both directions; zero differences in the controls. The decisive test erased two of the worst sectors (free in the file system, so nothing was lost), programmed three patterns (all zeros, alternating A5/5A, random) and read each five times: zero mismatches. Cells that were worn out or defective would have failed again; these held every pattern once written on a healthy supply. So the memory was disturbed by how it was written, not broken. The repair was a clean erase of the settings area on USB power and the snapshot applied twice; afterwards three reads gave zero differing bytes.

### Sheet 18: fix 1 in plain words

Meshtastic ships with factory settings: the public channel, a random PIN, no name. We rebuilt the firmware from source so that **its** factory settings are **our** settings (Group9 at 912.875 MHz, No PIN, CLIENT_MUTE, named SF or RG, our GPS cadence). The firmware's failure path still "resets to defaults", but the defaults are now right, so a future revert is invisible to the driver. Proven on SF on 28 October: after a factory reset the radio came back fully configured with zero commands. Two things the compiled defaults cannot carry are the smart-broadcast minimums and the 21 canned presets; the snapshot restores those and the node key pair. The channel key is compiled into the binary, so the images and the jsonc files never leave the private repository.

## Attribution: how to say where sheets 13 to 17 came from

Say exactly who supplied what, in this order:

1. **The hypothesis** came from a Qualcomm engineer during a recruiting conversation in October 2026. (Ask before using their name; "a Qualcomm engineer" is fine without it.)
2. **The experiment design, the flash-reading scripts and the analysis** were drafted with Claude (Anthropic) used as an AI assistant, under the team's direction.
3. **The hardware, the authorisation of every erase or write, and the checking of every result** against the raw records were the team's: Deo ran every measurement on the team's radios.
4. **Reproducibility**: every script and record is in the repository (`docs/src/flash_forensics`, `docs/src/*.py`), so anyone can repeat the sector map in four minutes without the AI.

This is on sheet 14 (short) and sheet 19 (full). It is a strength, not a confession: the recruiter asked a good question, the team used a tool to answer it quickly, and the answer is checkable.

## One-line glossary

- **Flash**: the 16 MB chip that holds the firmware and the settings; keeps data without power.
- **Sector**: a 4 KB block of flash, the smallest unit that can be erased.
- **Partition**: a named region of the flash (settings, program code, NVS, bootloader).
- **LittleFS**: the small power-loss-tolerant file system that holds the six settings files.
- **NVS**: a separate 20 KB key-value store used by the Arduino core; not where Meshtastic keeps its settings.
- **Brownout reset**: the CPU resets itself when its supply falls below a set level (2.44 V as built).
- **Rail**: the 3.3 V supply line shared by the CPU and the flash.
- **esptool stub**: a small helper program loaded into the chip's RAM that reads flash with the firmware stopped.
- **userPrefs.jsonc**: the file Meshtastic reads at build time to set compiled-in defaults.
- **Snapshot**: the per-radio YAML exported with `--export-config`; restores everything with `--configure`, run twice.
