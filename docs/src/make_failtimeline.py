import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date

plt.rcParams["font.family"] = "Cambria"
NAVY, RED, GREEN, GRAY = "#16213D", "#C43A4B", "#1F9D68", "#5E6B85"

# (date, label, tier) - tier staggers label height so neighbours don't collide
FAILS = [
    (date(2026, 8, 30), "Waveshare boot-loop\n(wrong platform)", 3),
    (date(2026, 8, 31), "BLE: bonded radio\nstops advertising", 1),
    (date(2026, 9, 1),  "Drive 1: 6 km grid,\n2-min GPS, km/h", 2),
    (date(2026, 9, 3),  "Wrong firmware\nflashed onto radio", 4),
    (date(2026, 9, 25), "\"0 online\": silent\nfrequency revert", 3),
    (date(2026, 9, 27), "Stale public key;\nhalf-alive wedge", 1),
    (date(2026, 9, 30), "Battery death\nreverts config (x2)", 2),
    (date(2026, 10, 4), "Compass must be\nrotated by hand", 1),
    (date(2026, 10, 17), "USB-C one-way;\nradio NVS revert", 2),
    (date(2026, 10, 24), "SF revert #3:\nsix settings gone", 1),
]
TESTS = [
    (date(2026, 8, 31), "Bench: live GPS\ndecoded end-to-end", 2),
    (date(2026, 9, 25), "Two-radio link\n6.75 / 5.75 dB", 1),
    (date(2026, 10, 5), "Open road\n3.26 / 3.75 mi", 2),
    (date(2026, 10, 18), "Canyon\n1.29 mi .. 4.7 mi", 1),
]
PENDING = (date(2026, 10, 26), "New Mexico\n(rained out)")

fig, ax = plt.subplots(figsize=(13.2, 5.6), dpi=200)
ax.axhline(0, color=NAVY, lw=2.2, zorder=1)
TIER_UP = {1: 1.0, 2: 2.0, 3: 3.0, 4: 4.0}
TIER_DN = {1: -1.1, 2: -2.2}
for d, lab, t in FAILS:
    y = TIER_UP[t]
    ax.plot([d, d], [0, y - 0.12], color=RED, lw=1.3, zorder=2)
    ax.plot(d, 0, "o", color=RED, ms=8, zorder=3)
    ax.text(d, y, lab, ha="center", va="bottom", fontsize=9.5, color=RED, linespacing=1.15, zorder=4, bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
for d, lab, t in TESTS:
    y = TIER_DN[t]
    ax.plot([d, d], [0, y + 0.12], color=GREEN, lw=1.3, zorder=2)
    ax.plot(d, 0, "^", color=GREEN, ms=10, zorder=3)
    ax.text(d, y, lab, ha="center", va="top", fontsize=9.5, color=GREEN, linespacing=1.15, zorder=4, bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
d, lab = PENDING
ax.plot(d, 0, "^", mfc="white", mec=GREEN, mew=1.8, ms=12, zorder=3)
ax.text(d, -0.55, lab, ha="center", va="top", fontsize=9.5, color=GREEN, style="italic", linespacing=1.15)

ax.text(date(2026, 8, 27), 5.15, "FAILURES  (reproduced or root-caused, then written down)", fontsize=11.5, color=RED, weight="bold", va="bottom")
ax.text(date(2026, 8, 27), -3.45, "TESTS  (field campaigns and link milestones)", fontsize=11.5, color=GREEN, weight="bold", va="top")
ax.set_xlim(date(2026, 8, 26), date(2026, 10, 30))
ax.set_ylim(-3.9, 5.9)
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 15]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.tick_params(axis="x", labelsize=11, colors=NAVY, length=5)
ax.set_yticks([])
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(NAVY)
ax.spines["bottom"].set_position(("data", -3.7))
plt.tight_layout()
fig.savefig("deck_assets/g_failtimeline.png", dpi=200)
print("ok")
