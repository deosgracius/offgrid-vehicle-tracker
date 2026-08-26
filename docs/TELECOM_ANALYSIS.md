# Telecommunications Analysis — Off-Grid Vehicle Tracker

How to treat this project as a communications system: layer by layer, with a link budget
you can compute on paper and then verify in the field. Numbers marked ~ are estimates to
be confirmed by measurement (Victor's range tests) — confirming them IS the experiment.

---

## 1. The protocol stack

| Layer | This project | The telecom concepts involved |
|---|---|---|
| Application | Position payload (lat/lon/course, protobuf-encoded, ~30–40 B) | source coding, payload efficiency |
| Transport/Network | Meshtastic managed flooding, hop limit 3, AES-256 | routing vs flooding, TTL, rebroadcast suppression |
| MAC | CSMA with SNR-weighted random backoff (listen-before-talk) | ALOHA/CSMA, contention, airtime fairness |
| PHY | LoRa chirp spread spectrum, 915 MHz ISM, SX1262 | modulation, spreading gain, sensitivity, FEC |
| Local link | BLE GATT (Heltec → display), 2.4 GHz | short-range wireless, GATT services |

Two radio links, very different regimes:
- **LoRa (the hard one):** km-scale, non-line-of-sight, low rate (~1 kbps) — coverage-limited
- **BLE (the easy one):** 1 m inside the cab, Mbps-class — never the bottleneck

## 2. Physical layer: why LoRa reaches kilometers at milliwatt-class power

LoRa is **chirp spread spectrum (CSS)**: each symbol is a frequency sweep across the
bandwidth, and the receiver correlates against known chirps. Spreading factor SF means
2^SF chips per symbol → correlation (processing) gain lets the receiver decode **below the
noise floor**. This is the whole trade: sensitivity is bought with data rate.

Receiver noise floor: `N = -174 + 10·log10(BW) + NF ≈ -174 + 54 + 6 ≈ -114 dBm` (250 kHz, NF~6 dB).
Yet SX1262 sensitivity reaches −129 dBm at SF11/250k — i.e. decoding ~15 dB *below* noise,
thanks to spreading gain. Add coding rate 4/5 Hamming FEC on top.

Meshtastic radio presets (US 915, all values per Semtech SX126x datasheet):

| Preset | SF / BW | Bit rate | Sensitivity | Use |
|---|---|---|---|---|
| SHORT_FAST | SF7 / 250 kHz | ~11 kbps | ~−121 dBm | short range, fast |
| **LONG_FAST (default)** | SF11 / 250 kHz | ~1.07 kbps | ~−129 dBm | our starting point |
| LONG_SLOW | SF12 / 125 kHz | ~0.18 kbps | ~−137 dBm | max range, last resort |

Each SF step ≈ +2.5–3 dB link margin at half the rate. This is the knob Victor turns if
range tests come up short: LONG_FAST → LONG_SLOW buys ~8 dB ≈ roughly 2× range in
cluttered terrain, at 6× the airtime.

## 3. Link budget (the core calculation)

`P_rx = P_tx + G_tx + G_rx − L_path − L_misc` ; link works when `P_rx > sensitivity`; the
difference is **link margin**.

Our numbers (Heltec V4 high-power, roof-mounted 3 dBi whips, ~1 dB cable/connector loss each side):

```
P_tx = 28 dBm   G_tx = G_rx = 3 dBi   L_misc ≈ 2 dB   Sens = −129 dBm (LONG_FAST)
Maximum allowable path loss = 28 + 3 + 3 − 2 − (−129) = 161 dB
```

**Model 1 — Free space** (`FSPL = 32.45 + 20log10(f_MHz) + 20log10(d_km)`, so 91.7 dB + 20log10(d) at 915 MHz):

| d | FSPL | P_rx | Margin |
|---|---|---|---|
| 1 km | 91.7 dB | −59.7 dBm | 69 dB |
| 8 km | 109.7 dB | −77.7 dBm | 51 dB |
| 50 km | 125.6 dB | −93.6 dBm | 35 dB |

Free space says hundreds of km. That's the ridge-to-ridge, line-of-sight case — and it's
why a relay node on high ground is so effective.

**Model 2 — Two-ray / ground-level reality.** With both antennas ~1.5–2 m high, beyond the
breakpoint distance the ground reflection cancels the direct wave and path loss grows at
**40 log10(d)**, not 20: `L ≈ 40log10(d) − 20log10(h_tx·h_rx)` (d, h in meters). At h=2 m:

| d | L (two-ray) | Margin |
|---|---|---|
| 2 km | 120 dB | 41 dB |
| 5 km | 136 dB | 25 dB |
| 10 km | 148 dB | 13 dB |
| 20 km | 160 dB | ~1 dB |

**Model 3 — Terrain.** A single ridge in the path adds 10–30+ dB knife-edge diffraction
loss; dense wet forest adds ~0.1–0.5 dB/100 m. This is why the honest prediction is
**"2–8 km typical at ground level, tens of km with line of sight, possibly <1 km in a deep
valley"** — and why the range tests report terrain context with every data point.

Sanity notes for the report: antenna height beats antenna gain (raising h from 1 m to 3 m
is ~19 dB in the two-ray model — more than the entire TX power budget); a whip inside a
metal vehicle body can cost 10–20 dB, which is why roof mounts are non-negotiable.

## 4. MAC & network layer

- **Airtime:** a ~40 B position packet at LONG_FAST ≈ 0.5 s on air (SF12/125k: ~2.5 s).
  With a 30 s broadcast interval, 2 nodes: channel utilization ≈ 2·0.5/30 ≈ **3%** —
  comfortably in the regime where CSMA/ALOHA-style access has negligible collision loss.
  This calculation is the justification for the 30–60 s interval choice.
- **Multiple access:** Meshtastic does listen-before-talk with randomized backoff weighted
  by SNR (far nodes rebroadcast first) — a neat contention-resolution heuristic worth a
  paragraph in the report.
- **Network:** no routing tables — **managed flooding** with hop limit (default 3) and
  duplicate-packet suppression by packet ID. Simple, stateless, and exactly right for a
  2–5 node sparse mobile mesh. A relay node needs zero configuration.
- **Regulatory:** 915 MHz US ISM band, FCC Part 15.247. No license, no duty-cycle cap
  (unlike EU 868), power within limits as shipped. One sentence in the report shows you
  checked.

## 5. Reliability & information flow

- The application needs ~50 B every 30 s = **13 bit/s of goodput** — the system runs at
  ~1% of even LONG_FAST's capacity. Deliberate: capacity is traded for link margin.
- No ACK/retransmit for position broadcasts — and none needed: positions supersede each
  other, so the correct reliability metric is not per-packet delivery but **staleness**
  (age of newest fix). This justifies the data-age indicator as a system requirement.
- End-to-end latency ≈ airtime (0.5 s) + per-hop rebroadcast delays; irrelevant at driving
  timescales next to the 30 s sampling interval.

## 6. The measurement campaign (Victor + Cannon — this is the report's data)

For each test: log **RSSI, SNR, packet delivery ratio (PDR)** vs distance (Meshtastic
reports RSSI/SNR per packet — the phone app or CLI exports them).

1. **Calibration:** short-range test to verify TX power and antenna install (compare
   measured RSSI to link-budget prediction; a 15 dB gap means a connector/antenna problem).
2. **Open-terrain sweep:** drive-away test on flat road, log RSSI/SNR/PDR every km →
   plot measured path loss vs the 20log/40log models; find the breakpoint.
3. **Terrain cases:** repeat over a hill, in trees, in town — quantify the extra loss.
4. **Preset comparison:** re-run the edge-of-range points at LONG_SLOW → measure the real
   sensitivity gain.
5. **Relay test:** third node on high ground; show PDR recovery beyond direct range.

Plot RSSI (dBm) vs log-distance with the free-space and two-ray lines overlaid — one
figure that demonstrates the entire analysis. Define usable range as **PDR ≥ 90% over
5 min** (i.e. staleness ≤ ~60 s), not "last packet heard."

## 7. Framing for the final report

> "We designed and validated a low-rate, wide-area telemetry link: an application
> requiring 13 bit/s of goodput, delivered over a chirp-spread-spectrum PHY operating up
> to 15 dB below the noise floor, with an ALOHA-class MAC at 3% channel utilization and a
> flooding mesh network layer — and we verified the link budget against field
> measurements across four terrain classes."

That sentence maps every classic telecom topic — link budget, modulation & spreading,
noise & sensitivity, FEC, multiple access, routing, and measurement — onto a system we
built and drove around. The link budget above makes the *prediction*; the measurement
campaign *tests* it; the gap between them is the discussion section.
