import re, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Cambria"
NAVY, RED, GREEN, GRAY, ACC = "#16213D", "#C43A4B", "#1F9D68", "#5E6B85", "#E58E1A"
PAT = re.compile(r"\[ui\] pg0 arrow\s+([+-]?\d+\.\d+) deg dist\s+(\d+) m age\s+(\d+)s")

def series(path):
    d, ages = [], []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = PAT.search(line)
        if m:
            d.append(int(m.group(2))); ages.append(int(m.group(3)))
    return d, ages

d2, a2 = series("../display2_diag.log")
d1, a1 = series("../display1_diag.log")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 4.6), dpi=200)
for ax, d, a, title, note in [
    (ax1, d2, a2, "Display 2 (paired to RG), 14:16  -  SF radio's fix scattering",
     "two radios on one desk read 0.21 mi apart;\ndistance walks 1 m/s with age: dead reckoning\non the GPS's phantom 1.4 m/s"),
    (ax2, d1, a1, "Display 1 (paired to SF), 14:22  -  RG radio's phantom drive",
     "RG reported 50 mph eastbound for ~60 s\n(spd 23.9 -> 14.7 m/s, track 75 deg), then\nsnapped back to 24 m when the fix recovered")]:
    t = list(range(len(d)))
    ax.plot(t, [x / 1609.344 for x in d], color=NAVY, lw=2.0)
    fresh = [i for i, x in enumerate(a) if x == 0]
    ax.scatter(fresh, [d[i] / 1609.344 for i in fresh], color=GREEN, s=28, zorder=3, label="packet received (age 0)")
    ax.set_title(title, fontsize=12, color=NAVY, loc="left")
    ax.set_xlabel("seconds since reset", fontsize=10.5)
    ax.set_ylabel("displayed separation (miles)", fontsize=10.5)
    ax.grid(axis="y", color="#E6EAF2"); ax.set_axisbelow(True)
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)
    ax.text(0.02, 0.97, note, transform=ax.transAxes, va="top", fontsize=9.5, color=RED, linespacing=1.3)
    ax.legend(loc="lower right", fontsize=9.5, frameon=False)
ax1.set_ylim(0, 0.5)
ax2.set_ylim(0, 1.4)
ax2.annotate("true separation: 24 m", xy=(len(d1) - 20, 24 / 1609.344), xytext=(len(d1) - 2, 0.42),
             fontsize=10, color=GREEN, ha="right", arrowprops=dict(arrowstyle="->", color=GREEN))
fig.suptitle("Both displays rendered exactly what the radios sent: the fault was in the GPS fixes, indoors", fontsize=13, color=NAVY, weight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("deck/g_lcddiag.png", dpi=200)
print("ok", len(d2), len(d1))
