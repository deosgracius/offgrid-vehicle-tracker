# Part I figures for the combined deck (REV D): bring-up flow, position precision, frequency slots.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as mp, math
plt.rcParams["font.family"] = "Cambria"
NAVY, RED, GREEN, GRAY, ACC, ICE, MUT = "#16213D", "#C43A4B", "#1F9D68", "#8A93A6", "#E58E1A", "#E8EDF5", "#5E6B85"

# ---- 1. bring-up: where failures 1-3 sit on the start-up path ----
fig, ax = plt.subplots(figsize=(12.4, 2.7), dpi=200)
stages = ["Power on", "Boot", "Find the radio\n(BLE scan)", "Pair\n(encrypt the link)", "Write config,\nstream GPS", "Tracking"]
xs = [0.6, 2.6, 4.9, 7.3, 9.7, 11.8]
for i, (x, t) in enumerate(zip(xs, stages)):
    col = GREEN if i == 5 else NAVY
    ax.add_patch(mp.FancyBboxPatch((x-0.75, 2.05), 1.5, 0.9, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=col, lw=1.6))
    ax.text(x, 2.5, t, ha="center", va="center", fontsize=10, color=col, weight="bold", linespacing=1.15)
    if i < 5: ax.annotate("", xy=(xs[i+1]-0.78, 2.5), xytext=(x+0.78, 2.5), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.4))
faults = [(2.6, "1  BOOT-LOOP", "wrong platform / memory mode", "pioarduino, dio_opi"),
          (4.9, "2  RADIO INVISIBLE", "a stored bond stops advertising", "Just-Works, no stored bond"),
          (7.3, "3  PAIRING REFUSED", "random PIN, no keypad: rc=1284", "radios run NO_PIN")]
for x, t, why, fix in faults:
    ax.plot([x, x], [2.0, 1.55], color=RED, lw=1.4)
    ax.plot(x, 2.0, "o", color=RED, ms=7)
    ax.text(x, 1.42, t, ha="center", va="top", fontsize=10, color=RED, weight="bold")
    ax.text(x, 1.02, why, ha="center", va="top", fontsize=9.5, color=NAVY)
    ax.text(x, 0.58, "fix: " + fix, ha="center", va="top", fontsize=9.5, color=GREEN, weight="bold")
ax.set_xlim(-0.3, 12.8); ax.set_ylim(0.3, 3.05); ax.axis("off")
plt.tight_layout(); fig.savefig("deck_assets/g_bringup.png", dpi=200)

# ---- 2. position precision: grid-cell size for each setting ----
bits = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 32]
km = [2**(32-b) * 1e-7 * 111.32 for b in bits]
fig, ax = plt.subplots(figsize=(12.4, 2.7), dpi=200)
cols = [RED if b == 13 else (GREEN if b == 32 else GRAY) for b in bits]
bars = ax.bar(range(len(bits)), km, color=cols, width=0.62)
ax.set_yscale("log"); ax.set_ylim(5e-6, 300)
ax.set_xticks(range(len(bits))); ax.set_xticklabels([str(b) for b in bits], fontsize=10, color=NAVY)
ax.set_xlabel("position_precision: how many of the 32 bits of latitude and longitude are sent", fontsize=10, color=NAVY)
ax.set_ylabel("grid cell (km)", fontsize=9.5, color=MUT)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", labelsize=8.5, colors=MUT)
def lab(k): return f"{k:.0f} km" if k >= 10 else (f"{k:.1f} km" if k >= 1 else (f"{k*1000:.0f} m" if k >= 0.01 else "1 cm"))
for i, (b, k) in enumerate(zip(bits, km)):
    ax.text(i, k*1.6, lab(k), ha="center", fontsize=9, color=cols[i], weight="bold" if b in (13, 32) else None)
ax.text(3, 40, "default 13:\nevery broadcast snapped to the\ncentre of a 5.8 km cell", ha="center", va="bottom", fontsize=9.5, color=RED, weight="bold", linespacing=1.2)
ax.text(10, 0.002, "ours 32:\nexact fix", ha="center", va="bottom", fontsize=9.5, color=GREEN, weight="bold")
plt.tight_layout(); fig.savefig("deck_assets/g_precision.png", dpi=200)

# ---- 3. frequency slots: the name is the frequency ----
fig, ax = plt.subplots(figsize=(12.4, 2.7), dpi=200)
f0, bw, n = 902.0, 0.25, 104
for i in range(n):
    f = f0 + bw/2 + i*bw
    c = ICE
    if abs(f - 906.875) < 1e-6: c = RED
    if abs(f - 912.875) < 1e-6: c = GREEN
    ax.add_patch(mp.Rectangle((f - bw/2 + 0.02, 1.0), bw - 0.04, 0.8, color=c, lw=0))
ax.set_xlim(901.5, 928.5); ax.set_ylim(-0.2, 3.3); ax.axis("off")
for f in (902, 907, 912, 917, 922, 928):
    ax.text(f, 0.82, f"{f}", ha="center", va="top", fontsize=9, color=MUT)
ax.text(915, 0.45, "US 915 band, 902 to 928 MHz, 104 slots of 250 kHz (LONG_FAST)", ha="center", va="top", fontsize=9.5, color=MUT)
ax.annotate("public default 'LongFast'\n906.875 MHz: where a reverted\nradio ends up", xy=(906.875, 1.8), xytext=(904.3, 2.95), fontsize=9.5, color=RED, weight="bold", ha="left", va="top", linespacing=1.2,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3))
ax.annotate("Group9: slot 43 = djb2('Group9') mod 104\n902.125 + 43 x 0.25 = 912.875 MHz", xy=(912.875, 1.8), xytext=(913.6, 2.95), fontsize=9.5, color=GREEN, weight="bold", ha="left", va="top", linespacing=1.2,
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3))
ax.text(901.5, 3.3, "The channel NAME sets the frequency. Same key on two different slots: total silence, healthy screens, identical read-backs.", fontsize=11, color=NAVY, weight="bold", va="top")
plt.tight_layout(); fig.savefig("deck_assets/g_slots.png", dpi=200)
print("part1 figs ok", [round(k, 3) for k in km[:4]])
