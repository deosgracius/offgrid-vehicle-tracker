# Evidence figure for the cancelled New Mexico drive, 25 October 2026.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams["font.family"] = "Cambria"
NAVY, MUT, RED = "#16213D", "#5E6B85", "#C43A4B"
def crop(im, box): return im.crop(box)
m = Image.open("deck_assets/nm/map_apple.jpg");   m = crop(m, (120, 560, 1220, 1660))      # square: Capitan range, dot west of the peaks
s = Image.open("deck_assets/nm/sky3.jpg");       s = crop(s, (0, 280, 768, 1048))          # square
t = Image.open("deck_assets/nm/truck.jpg");      t = crop(t, (0, 200, 576, 968))           # 0.75
panels = [(m, "Below the Capitan Mountains, north of Capitan, NM"), (s, "The cloud deck on the peaks at the planned start"), (t, "The access road; the drive was called off here")]
fig, axes = plt.subplots(1, 3, figsize=(8.4, 3.0), dpi=200, gridspec_kw={"width_ratios": [1.0, 1.0, 0.75]})
for ax, (im, cap) in zip(axes, panels):
    ax.imshow(im); ax.axis("off")
    ax.set_title(cap, fontsize=7.8, color=NAVY, loc="left", pad=4)
plt.tight_layout(w_pad=0.5); fig.savefig("deck_assets/g_nm_cancel.png", dpi=200)
a2 = Image.open("deck_assets/nm/nws_alert.jpg").crop((40, 60, 1290, 510)); a2.save("deck_assets/g_nm_alert.jpg", quality=90)
print("nm fig ok")
