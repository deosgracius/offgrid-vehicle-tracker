import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as mp, collections
from datetime import date
plt.rcParams["font.family"] = "Cambria"
NAVY, RED, GREEN, GRAY, ACC, ICE, MUT = "#16213D", "#C43A4B", "#1F9D68", "#8A93A6", "#E58E1A", "#E8EDF5", "#5E6B85"
SP = "C:/Users/deogr/AppData/Local/Temp/claude/C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project/eca057db-c8d2-4bae-87d3-8a6c4f6c4af6/scratchpad/nvs"

# ---- incident timeline ----
ev = [(date(2026,9,3),  "SF", "CLI reset mid-save\nregion, Bluetooth", ACC),
      (date(2026,9,30), "RG + SF", "flat batteries\nRG: channels | SF: all", RED),
      (date(2026,10,17),"SF", "flat, a week idle\nBluetooth, channel, name", RED),
      (date(2026,10,24),"SF", "flat in transit\nchannel, key, cadence,\nowner, presets, node DB", RED)]
fig, ax = plt.subplots(figsize=(12.4, 2.9), dpi=200)
ax.axhline(0, color=NAVY, lw=2); ax.set_ylim(-1.2, 2.6); ax.set_xlim(date(2026,8,28), date(2026,10,30))
for i,(d, who, what, col) in enumerate(ev):
    ax.plot(d, 0, "o", color=col, ms=13, zorder=3)
    ax.text(d, 0.45, who, ha="center", fontsize=11, weight="bold", color=col)
    ha = "right" if i == 2 else ("left" if i == 3 else "center")
    ax.text(d, 0.95, what, ha=ha, va="bottom", fontsize=9.5, color=NAVY, linespacing=1.3)
    ax.text(d, -0.55, d.strftime("%b %d"), ha="center", fontsize=10, color=MUT)
ax.axis("off")
ax.text(date(2026,8,28), 2.45, "Four configuration losses. Three follow a flat battery; the fourth is a known reset-during-write race. SF accounts for three.", fontsize=11, color=NAVY, weight="bold", va="top")
plt.tight_layout(); fig.savefig("deck/g_events.png", dpi=200)

# ---- SF before vs RG sector maps ----
def load(path):
    R = open(path, "rb").read(); return R
def unstable_of(a, b, c):
    u = collections.Counter()
    for x, y in ((a, b), (b, c)):
        for i in range(len(x)):
            if x[i] != y[i]: u[i//4096] += 1
    return u
sf = [load(f"{SP}/fsS{i}.bin") for i in (1,2,3)]
rg = [load(f"{SP}/rg_fsS{i}.bin") for i in (1,2,3)]
def draw(ax, R, unstable, live, title, sub):
    n = len(R[0])//4096; cols = 48; rows = (n+cols-1)//cols
    erased = [all(x==0xFF for x in R[0][i*4096:(i+1)*4096]) for i in range(n)]
    for i in range(n):
        r, c = divmod(i, cols)
        col = GREEN if i in live else (RED if unstable.get(i) else (GRAY if not erased[i] else ICE))
        ax.add_patch(mp.Rectangle((c, rows-1-r), 0.9, 0.9, color=col, lw=0))
    ax.set_xlim(0, cols); ax.set_ylim(0, rows); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=12, color=NAVY, loc="left", weight="bold")
    ax.text(0, -1.4, sub, fontsize=10, color=MUT)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 3.6), dpi=200)
draw(a1, sf, unstable_of(*sf), {25, 26, 470}, "SF, as found (before repair)", "21 unstable sectors, 12 heavily  |  117 / 107 differing bytes between reads")
draw(a2, rg, unstable_of(*rg), {151, 548}, "RG, baseline (same day, same method)", "0 unstable sectors  |  0 / 0 differing bytes  |  112 sectors holding data")
leg = [mp.Patch(color=GREEN, label="live config files"), mp.Patch(color=RED, label="unstable between reads"), mp.Patch(color=GRAY, label="stale data, stable"), mp.Patch(color=ICE, label="erased")]
fig.legend(handles=leg, loc="lower center", ncol=4, fontsize=9.5, frameon=False, bbox_to_anchor=(0.5, -0.02))
plt.tight_layout(rect=[0, 0.06, 1, 1]); fig.savefig("deck/g_maps_compare.png", dpi=200)
print("figs2 ok")
