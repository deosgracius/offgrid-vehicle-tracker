# Redraws the two SX1261/2 datasheet figures as clean colored diagrams
# (adapted from rev 2.2: fig 4-1 block diagram, fig 9-1 operating modes).
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

NAVY, ORANGE, GREEN, GRAY = "#16213D", "#E58E1A", "#1F9D68", "#5E6B85"
ICEBG, REDC = "#EDF3FB", "#C43A4B"
plt.rcParams.update({"font.family": "Arial", "font.size": 11})

def box(ax, x, y, w, h, label, fc=ICEBG, ec=NAVY, fs=10.5, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                facecolor=fc, edgecolor=ec, linewidth=1.6))
    ax.text(x + w/2, y + h/2, label, ha="center", va="center", fontsize=fs,
            color=tc or ec, fontweight="bold")

def arrow(ax, p1, p2, color=NAVY, lw=1.8, style="-|>"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                                 color=color, linewidth=lw))

# ================= FIG 1: block diagram =================
fig, ax = plt.subplots(figsize=(11, 5.6), dpi=170)
ax.set_xlim(0, 22); ax.set_ylim(0, 11); ax.axis("off")

ax.text(0.4, 10.5, "SX1261/2 internal architecture (adapted from datasheet rev 2.2, fig. 4-1)",
        fontsize=12.5, color=NAVY, fontweight="bold")

# antenna + front end
ax.plot([0.9, 0.9], [5.2, 7.6], color=NAVY, lw=2)
ax.plot([0.35, 1.45], [7.6, 7.6], color=NAVY, lw=2)
ax.plot([0.55, 1.25], [8.0, 8.0], color=NAVY, lw=2)
ax.text(0.9, 8.5, "ANT", ha="center", fontsize=10, color=NAVY, fontweight="bold")
box(ax, 1.8, 4.6, 2.5, 1.6, "Matching\n+ LPF")
box(ax, 5.0, 6.3, 2.2, 1.4, "LNA", ec=GREEN)
box(ax, 8.0, 6.3, 2.2, 1.4, "Mixer", ec=GREEN)
box(ax, 8.0, 3.4, 2.2, 1.4, "PLL\n(frac-N)", ec=ORANGE)
box(ax, 11.0, 6.3, 2.2, 1.4, "ADC", ec=GREEN)
box(ax, 14.0, 7.1, 2.6, 1.3, "LoRa modem\n(chirp correlator)", ec=NAVY, fs=9.5)
box(ax, 14.0, 5.4, 2.6, 1.3, "(G)FSK modem\n(unused here)", ec=GRAY, fs=9.5)
box(ax, 17.3, 5.8, 2.4, 2.2, "Protocol\nengine\n+ 256 B buffer", ec=NAVY, fs=9.5)
box(ax, 17.3, 2.6, 2.4, 1.5, "SPI + BUSY\n+ DIO IRQ", ec=NAVY, fs=9.5)
box(ax, 5.0, 2.2, 2.2, 1.4, "PA (+22 dBm)", ec=REDC, fs=9.5)
box(ax, 11.0, 2.2, 2.6, 1.4, "TX mod path", ec=REDC, fs=9.5)
box(ax, 1.8, 0.4, 3.6, 1.2, "DC-DC / LDO power", ec=GRAY, fs=9.5)
ax.text(20.8, 3.35, "to ESP32-S3\nhost MCU", fontsize=9.5, color=GRAY, ha="center")

# RX path arrows (green)
arrow(ax, (1.25, 5.4), (1.8, 5.4))
arrow(ax, (4.3, 5.6), (5.0, 6.8), GREEN)
arrow(ax, (7.2, 7.0), (8.0, 7.0), GREEN)
arrow(ax, (9.1, 4.8), (9.1, 6.3), ORANGE)
arrow(ax, (10.2, 7.0), (11.0, 7.0), GREEN)
arrow(ax, (13.2, 7.3), (14.0, 7.6), GREEN)
arrow(ax, (16.6, 7.6), (17.3, 7.2), GREEN)
arrow(ax, (18.5, 5.8), (18.5, 4.1), NAVY)
# TX path arrows (red)
arrow(ax, (17.3, 6.2), (13.6, 3.2), REDC)
arrow(ax, (11.0, 2.9), (7.2, 2.9), REDC)
arrow(ax, (5.0, 2.9), (3.0, 4.6), REDC)
ax.text(5.6, 8.3, "receive path", fontsize=9.5, color=GREEN, fontweight="bold")
ax.text(8.6, 1.6, "transmit path", fontsize=9.5, color=REDC, fontweight="bold")
fig.tight_layout(); fig.savefig("fig_sx_block.png", facecolor="white", bbox_inches="tight"); plt.close(fig)

# ================= FIG 2: operating modes =================
fig, ax = plt.subplots(figsize=(7.2, 6.6), dpi=170)
ax.set_xlim(0, 14); ax.set_ylim(0, 13); ax.axis("off")
ax.text(0.3, 12.5, "Operating modes (adapted from datasheet rev 2.2, fig. 9-1)",
        fontsize=12.5, color=NAVY, fontweight="bold")

states = {
 "SLEEP":      (2.6, 9.6, GRAY),
 "STDBY_RC":   (7.0, 10.6, NAVY),
 "STDBY_XOSC": (11.2, 9.6, NAVY),
 "FS":         (11.2, 5.6, ORANGE),
 "TX":         (8.6, 2.2, REDC),
 "RX":         (4.6, 2.2, GREEN),
 "CAD":        (1.8, 5.6, GREEN),
}
R = 1.25
for name, (x, y, c) in states.items():
    ax.add_patch(Circle((x, y), R, facecolor="white", edgecolor=c, linewidth=2.2))
    ax.text(x, y, name, ha="center", va="center", fontsize=10, color=c, fontweight="bold")

def sarrow(a, b, color=NAVY, bend=0.18):
    (x1, y1, _), (x2, y2, _) = states[a], states[b]
    import math
    dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy)
    ux, uy = dx/L, dy/L
    p1 = (x1+ux*R*1.08, y1+uy*R*1.08); p2 = (x2-ux*R*1.08, y2-uy*R*1.08)
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13,
                                 color=color, linewidth=1.6,
                                 connectionstyle=f"arc3,rad={bend}"))
sarrow("SLEEP", "STDBY_RC"); sarrow("STDBY_RC", "SLEEP")
sarrow("STDBY_RC", "STDBY_XOSC"); sarrow("STDBY_XOSC", "STDBY_RC")
sarrow("STDBY_XOSC", "FS", ORANGE)
sarrow("FS", "TX", REDC); sarrow("FS", "RX", GREEN, bend=0.3)
sarrow("TX", "STDBY_RC", GRAY, bend=0.35); sarrow("RX", "STDBY_RC", GRAY, bend=-0.35)
sarrow("RX", "CAD", GREEN); sarrow("CAD", "STDBY_RC", GRAY)
ax.text(7.0, 0.5, "No state both transmits and receives: the chip is half duplex by construction.",
        ha="center", fontsize=10, color=GRAY, style="italic")
fig.tight_layout(); fig.savefig("fig_sx_modes.png", facecolor="white", bbox_inches="tight"); plt.close(fig)
print("figures done")
