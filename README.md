# Off-Grid Vehicle Tracker — Group 9

**Capstone Project Lab · Aug 24 – Dec 10, 2026 · Sponsor: Dr. Richard Gale**

Fully off-grid system that shows the **direction and distance** to a partner vehicle on a
driver-visible dashboard screen — no cell service or WiFi required (Alaska use case).
LoRa/Meshtastic radios exchange GPS positions between vehicles; a sunlight-readable
reflective LCD shows a live arrow + distance to the partner.

Full architecture, hardware verification, math, and risks: **[DESIGN.md](DESIGN.md)**

## Team & roles

| Member | Role | Owns |
|---|---|---|
| **Deo** | Protocol firmware | Meshtastic BLE client on the display board: NimBLE central, pairing, protobuf (nanopb) decode, `TrackerState` feed |
| **Josiah** | Display & navigation firmware | RLCD rendering, arrow/distance UI, haversine + bearing + heading math |
| **Victor** | Radio & hardware lead | Heltec/Meshtastic flashing & config, GNSS modules, antennas, range testing |
| **Cannon** | Systems & test lead | Vehicle power, mounting/enclosures, integration + drive tests, parts tracking, reports |

Ground rules:
- The `TrackerState` struct (see DESIGN.md §7) is the **contract** between Deo's and
  Josiah's code — agreed week 2, changed only by mutual agreement.
- Everyone flashes their own boards; no single "person with the hardware."
- All work goes through this repo.

## Repo layout

```
DESIGN.md            System design, architecture decision, risks, schedule
planning/            Gantt chart (tasks.json → build_gantt.py → Group9_Gantt.html)
firmware-display/    Waveshare RLCD firmware (Deo: protocol/, Josiah: ui/ + nav/)
hardware/            Victor — radio configs, antenna notes, range-test logs
testing/             Cannon — power, mounting, integration & drive-test logs
```

## Gantt chart

Open [planning/Group9_Gantt.html](planning/Group9_Gantt.html) in a browser.
To change the plan: edit [planning/tasks.json](planning/tasks.json), then run
`planning/Update_Gantt.bat` (or `python planning/build_gantt.py`) and commit both files.
