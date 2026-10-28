import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as mp
plt.rcParams["font.family"] = "Cambria"
NAVY, RED, GREEN, GRAY, ACC, ICE, MUT = "#16213D", "#C43A4B", "#1F9D68", "#C9CFDA", "#E58E1A", "#E8EDF5", "#5E6B85"

# ---------- voltage ladder ----------
fig, ax = plt.subplots(figsize=(12.4, 4.8), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(2.2, 4.4); ax.set_yticks([2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2])
ax.set_ylabel("volts", fontsize=11); ax.set_xticks([])
for s in ["top", "right", "bottom"]: ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#E6EAF2"); ax.set_axisbelow(True)
# battery column
ax.add_patch(mp.Rectangle((0.6, 3.3), 1.4, 0.9, color="#8A93A6"))
ax.text(1.3, 4.3, "Li-ion cell\n(Heltec spec 3.3 to 4.2 V)", ha="center", fontsize=9.5, color=NAVY)
ax.annotate("", xy=(1.3, 3.3), xytext=(1.3, 4.2), arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
ax.text(1.3, 3.18, "discharging", ha="center", fontsize=9, color=MUT)
# 3.3 V rail column
ax.add_patch(mp.Rectangle((3.0, 2.7), 1.4, 0.9, color=GREEN, alpha=0.85))
ax.add_patch(mp.Rectangle((3.0, 2.44), 1.4, 0.26, color=RED))
ax.text(3.7, 4.3, "3.3 V rail\n(what the ESP32-S3 and the flash see)", ha="center", fontsize=9.5, color=NAVY)
ax.text(3.7, 3.15, "flash in spec\n2.7 to 3.6 V", ha="center", va="center", fontsize=9.5, color="white", weight="bold")
ax.text(3.7, 2.57, "CPU runs, flash out of spec", ha="center", va="center", fontsize=8.6, color="white", weight="bold")
# threshold lines
for y, lab, col in [(3.6, "flash VCC max 3.6 V", MUT), (2.7, "flash VCC min 2.7 V  (BY25Q128AS: 'VCC must be held stable and within range during all operations')", RED),
                    (2.44, "ESP32-S3 brownout reset as built: level 7 = 2.44 V (sdkconfig CONFIG_ESP_BROWNOUT_DET_LVL=7)", NAVY),
                    (3.1, "Meshtastic low-battery deep-sleep trigger: cell below 3.10 V for 10 readings (no flash write on this path)", ACC)]:
    ax.plot([2.6, 9.9], [y, y], color=col, lw=1.4, ls="--" if y != 2.7 else "-")
    ax.text(4.6, y + 0.03, lab, fontsize=9.2, color=col, va="bottom")
ax.text(4.6, 2.3, "260 mV window: the CPU keeps running and writing; the flash gives no guarantee of what lands in its cells", fontsize=9.5, color=RED, weight="bold")
ax.text(7.2, 3.9, "Transmit at 27 dBm draws ~750 mA (Heltec table 3.4):\na weak cell sags under that pulse, and the firmware\nwrites device.proto on every boot.", fontsize=9.5, color=NAVY,
        bbox=dict(boxstyle="round,pad=0.4", fc="#F2F5FA", ec="#9AA7BE"))
ax.set_title("The voltage margin: the CPU is allowed to keep writing below the flash chip's minimum supply", fontsize=12, color=NAVY, loc="left", pad=22)
plt.tight_layout(); fig.savefig("deck/g_voltage.png", dpi=200)

# ---------- storage and write path ----------
fig, ax = plt.subplots(figsize=(12.4, 5.0), dpi=200); ax.set_xlim(0, 12.4); ax.set_ylim(0, 5); ax.axis("off")
def box(x, y, w, h, t, fc="#F2F5FA", ec=NAVY, fs=9.5, tc=NAVY, bold=False):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.3))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, color=tc, weight="bold" if bold else "normal", linespacing=1.3)
def arrow(x1, y1, x2, y2, col=NAVY, lab=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color=col, lw=1.4))
    if lab: ax.text((x1+x2)/2, (y1+y2)/2 + 0.12, lab, ha="center", fontsize=8.6, color=col)
ax.text(0.1, 4.75, "16 MB SPI NOR flash (Boya BY25Q128AS), partition table read from the chip", fontsize=11, color=NAVY, weight="bold")
box(0.2, 3.7, 1.5, 0.75, "nvs 20 KB\nboot counter,\nArduino prefs", fc=ICE, fs=8.8)
box(1.9, 3.7, 2.6, 0.75, "app0 6.4 MB  |  app1 6.4 MB\nMeshtastic firmware (OTA pair)\nreads back identical", fc=ICE, fs=8.8)
box(4.7, 3.7, 4.3, 0.75, "spiffs 3.4 MB = LittleFS at 0xC90000\n/prefs/config.proto 181 B   channels.proto 96 B   device.proto 117 B\nmodule.proto 100 B   nodes.proto 712 B   cannedConf.proto 197 B", fc="#FDECEA", ec=RED, fs=8.0)
box(9.2, 3.7, 1.2, 0.75, "coredump\n64 KB", fc=ICE, fs=8.8)
ax.text(0.1, 3.3, "Save path (SafeFile, ESP32)", fontsize=10.5, color=NAVY, weight="bold")
box(0.2, 2.35, 2.0, 0.7, "powerHAL_isPowerLevelSafe()\nweak stub: always true", fc="#FDECEA", ec=RED, fs=8.0, tc=RED)
box(2.5, 2.35, 1.5, 0.7, "write file.tmp\n(XOR running hash)", fs=8.6)
box(4.3, 2.35, 1.6, 0.7, "re-read .tmp,\ncompare 1-byte XOR", fs=8.6)
box(6.2, 2.35, 1.4, 0.7, "rename .tmp\nover original", fs=8.6)
box(7.9, 2.35, 2.1, 0.7, "fullAtomic=false for nodes.proto:\noriginal deleted BEFORE write", fc="#FDECEA", ec=RED, fs=8.0, tc=RED)
box(10.3, 2.35, 1.9, 0.7, "close() result ignored:\n'Can't write prefs!' then\nreturn okay", fc="#FDECEA", ec=RED, fs=8.0, tc=RED)
for x in (2.2, 4.0, 5.9, 7.6, 10.0): arrow(x, 2.7, x + 0.3, 2.7)
ax.text(0.1, 1.95, "Load path at boot", fontsize=10.5, color=NAVY, weight="bold")
box(0.2, 1.0, 1.8, 0.7, "open /prefs/x.proto", fs=9)
box(2.3, 1.0, 2.2, 0.7, "missing or 'can't decode protobuf'\n(a torn or unstable sector)", fc="#FDECEA", ec=RED, fs=8.6, tc=RED)
box(4.8, 1.0, 2.4, 0.7, "installDefaultConfig / Channels /\nDeviceState / ModuleConfig", fc="#FDECEA", ec=RED, fs=8.6, tc=RED)
box(7.5, 1.0, 2.2, 0.7, "defaults saved to flash:\nthe loss is now permanent", fc="#FDECEA", ec=RED, fs=8.6, tc=RED)
box(10.0, 1.0, 2.2, 0.7, "screens look healthy;\nradio on 906.875, name 'ead4',\nBluetooth Random PIN", fs=8.4)
for x in (2.0, 4.5, 7.2, 9.7): arrow(x, 1.35, x + 0.3, 1.35, RED)
ax.text(0.1, 0.55, "No backup copy is consulted on failure (restorePreferences exists but only when an operator triggers it). device.proto is re-saved on every boot ('Save /prefs/device.proto' in our boot log).", fontsize=9, color=MUT)
ax.text(0.1, 0.25, "What the firmware does protect: the low-battery deep-sleep path calls doDeepSleep(..., skipSaveNodeDb=true), so a clean low-battery shutdown does not write. The damage happens in the reboot churn around it.", fontsize=9, color=GREEN)
plt.tight_layout(); fig.savefig("deck/g_storage.png", dpi=200)

# ---------- causal chain ----------
fig, ax = plt.subplots(figsize=(12.4, 2.6), dpi=200); ax.set_xlim(0, 12.4); ax.set_ylim(0, 2.6); ax.axis("off")
steps = [("Battery runs\nflat in storage", ICE, NAVY), ("Charger or rebound\nrestarts the radio;\nTX pulse sags the rail", ICE, NAVY),
         ("Boot writes\ndevice.proto;\nrail between 2.44\nand 2.7 V", "#FDECEA", RED), ("Program/erase torn:\ncells left between\nstates (unstable reads)", "#FDECEA", RED),
         ("Next boot: CRC or\nprotobuf decode fails\non that file", "#FDECEA", RED), ("Firmware installs\nfactory defaults\nand SAVES them", "#FDECEA", RED),
         ("Healthy screens,\nwrong frequency,\nsilent partner", ICE, NAVY)]
w = 1.6
for i, (t, fc, tc) in enumerate(steps):
    x = 0.15 + i * 1.75
    ax.add_patch(mp.FancyBboxPatch((x, 0.5), w, 1.6, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=tc, lw=1.3))
    ax.text(x + w/2, 1.3, t, ha="center", va="center", fontsize=9, color=tc, linespacing=1.3)
    if i < len(steps) - 1: ax.annotate("", xy=(x + w + 0.15, 1.3), xytext=(x + w, 1.3), arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))
ax.text(0.15, 2.35, "The chain of causation as the evidence now supports it (hardware, physics, firmware policy)", fontsize=11, color=NAVY, weight="bold")
ax.text(0.15, 0.15, "Breaking any one link stops the loss. The fix plan attacks three of them: the write under low voltage, the defaults policy, and the sectors already left marginal.", fontsize=9.5, color=MUT)
plt.tight_layout(); fig.savefig("deck/g_chain.png", dpi=200)
print("figs ok")
