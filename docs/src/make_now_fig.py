# "Now" figure: every flash read-stability measurement on both radios, 27 to 29 October 2026.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Cambria"
NAVY, RED, GREEN, MUT, ACC = "#16213D", "#C43A4B", "#1F9D68", "#5E6B85", "#E58E1A"
rows = [("SF  27 Oct\nas found", 21, "117 / 107", RED),
        ("SF  27 Oct\nafter clean erase", 0, "0 / 0", GREEN),
        ("SF  29 Oct\nafter 2 days at 0 % battery", 0, "0 / 0", GREEN),
        ("RG  27 Oct\nbaseline", 0, "0 / 0", GREEN),
        ("RG  29 Oct\nafter storage", 0, "0 / 0", GREEN)]
fig, ax = plt.subplots(figsize=(12.4, 3.4), dpi=200)
y = list(range(len(rows)))[::-1]
for yi, (lab, n, db, c) in zip(y, rows):
    ax.barh(yi, max(n, 0.25), color=c, height=0.55)
    ax.text(max(n, 0.25) + 0.3, yi, f"{n} unstable sectors   |   differing bytes {db}", va="center", fontsize=10.5, color=c, weight="bold")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=10, color=NAVY)
ax.set_xlim(0, 30); ax.set_xticks([]); 
for sp in ("top", "right", "bottom"): ax.spines[sp].set_visible(False)
ax.axvline(0, color=NAVY, lw=1.2)
ax.set_title("Five measurements, same method: three reads of the settings area with the firmware stopped, program code as control", fontsize=11, color=NAVY, loc="left", weight="bold")
plt.tight_layout(); fig.savefig("deck_assets/g_now.png", dpi=200); print("now fig ok")
