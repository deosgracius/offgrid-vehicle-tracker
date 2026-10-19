# Regenerates the 14 typeset equations used by TECH_MANUAL.html and REPORT.html.
# Black ink, matplotlib mathtext, Times-like (STIX) faces.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"mathtext.fontset": "stix", "font.family": "STIXGeneral"})

EQS = {
 "eq_tsym":
   r"$T_{sym} = \dfrac{2^{SF}}{BW} = \dfrac{2^{11}}{250\,\mathrm{kHz}} = 8.19\ \mathrm{ms}$",
 "eq_npay":
   r"$N_{payload} = 8 + \max\!\left(\left\lceil \dfrac{8PL - 4SF + 28 + 16\,CRC - 20H}{4(SF - 2DE)} \right\rceil (CR + 4),\ 0\right)$",
 "eq_tpkt":
   r"$N_{payload} = 8 + \left\lceil \frac{8(40) - 44 + 28 + 16}{44} \right\rceil \times 5 = 48,"
   r"\quad T_{pkt} = (16 + 4.25 + 48)\,T_{sym} = 68.25 \times 8.19\ \mathrm{ms} \approx 0.56\ \mathrm{s}$",
 "eq_prx":
   r"$P_{rx} = P_{tx} + G_{tx} + G_{rx} - FSPL, \qquad FSPL = 20\log_{10} d + 20\log_{10} f - 147.55\ \ (d\ \mathrm{in\ m},\ f\ \mathrm{in\ Hz})$",
 "eq_fsplworked":
   r"$FSPL_{1\,km} = 60 + 179.2 - 147.55 = 91.7\ \mathrm{dB}\ \Rightarrow\ P_{rx} = -61.7\ \mathrm{dBm};"
   r"\qquad FSPL_{5\,km} = 105.7\ \mathrm{dB}\ \Rightarrow\ P_{rx} = -75.7\ \mathrm{dBm}$",
 "eq_margin":
   r"$\frac{d_2}{d_1} = 10^{\Delta/20}\ \Rightarrow\ \Delta = 6\ \mathrm{dB} \approx \times 2\ \mathrm{distance},"
   r"\qquad \mathrm{margin} = SNR_{meas} - SNR_{floor} = 6 - (-17.5) = 23.5\ \mathrm{dB}$",
 "eq_airtime":
   r"$U = \dfrac{N \cdot T_{pkt}}{T_{report}} = \dfrac{2 \times 0.56\ \mathrm{s}}{10\ \mathrm{s}} \approx 11.2\%$",
 "eq_slot":
   r"$slot = \mathrm{djb2}(name) \ \mathrm{mod}\ 104, \qquad f = 902.0\ \mathrm{MHz} + 0.125\ \mathrm{MHz} + slot \times 0.25\ \mathrm{MHz}$",
 "eq_slot43":
   r"$f = 902.0 + 0.125 + 43 \times 0.25 = 912.875\ \mathrm{MHz}$",
 "eq_haversine":
   r"$a = \sin^2\!\frac{\Delta\varphi}{2} + \cos\varphi_1 \cos\varphi_2 \sin^2\!\frac{\Delta\lambda}{2},"
   r"\qquad d = 2R\,\arcsin\sqrt{a}$",
 "eq_bearing":
   r"$\theta = \mathrm{atan2}\!\left(\sin\Delta\lambda\,\cos\varphi_2,\ \cos\varphi_1 \sin\varphi_2 - \sin\varphi_1 \cos\varphi_2 \cos\Delta\lambda\right),"
   r"\qquad arrow = \mathrm{wrap}_{\pm 180}(\theta - \psi)$",
 "eq_dr":
   r"$\varphi(t) = \varphi_0 + \dfrac{v\,\Delta t\,\cos\psi}{R}, \qquad \lambda(t) = \lambda_0 + \dfrac{v\,\Delta t\,\sin\psi}{R\,\cos\varphi}$",
 "eq_ema":
   r"$\bar{r} \leftarrow 0.1\,r + 0.9\,\bar{r}, \qquad \bar{r} > 0 \Rightarrow \mathrm{closing},\ \ \bar{r} < 0 \Rightarrow \mathrm{apart}$",
 "eq_online":
   r"$\mathrm{online}(n) \Longleftrightarrow (t_{now} - t_{last\,heard}(n)) < 7200\ \mathrm{s}$",
}

for name, tex in EQS.items():
    fig = plt.figure(figsize=(10, 1.1), dpi=200)
    fig.patch.set_facecolor("white")
    fig.text(0.01, 0.5, tex, fontsize=15, color="#000000", va="center", ha="left")
    fig.savefig(f"{name}.png", bbox_inches="tight", pad_inches=0.06, facecolor="white")
    plt.close(fig)
    print("wrote", name)
print("done:", len(EQS))
