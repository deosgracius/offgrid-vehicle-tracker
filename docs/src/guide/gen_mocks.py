# Regenerates the 23 device-screen recreations for the Device User Guide.
# Radio (Heltec OLED): cyan-on-black, 1024x512. Display (Waveshare RLCD):
# ink-on-paper, 1200x900. Course-up compass per the shipped firmware.
import math, os
from PIL import Image, ImageDraw, ImageFont

CY, OBG = (96, 232, 232), (6, 24, 27)          # oled cyan / near-black
INK, PAPER = (28, 36, 48), (226, 231, 227)     # rlcd ink / paper
F = lambda sz: ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", sz)
FB = lambda sz: ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", sz)

os.makedirs("mock", exist_ok=True)

# ---------------- radio screens ----------------
def radio(name, title, lines, sel=None, bar=True, batt="100%", clock="16:41"):
    img = Image.new("RGB", (1024, 512), OBG)
    d = ImageDraw.Draw(img)
    if bar:
        d.text((28, 16), batt, font=FB(40), fill=CY)
        w = d.textlength(title, font=FB(40))
        d.text(((1024 - w) / 2, 16), title, font=FB(40), fill=CY)
        d.text((1024 - 28 - d.textlength(clock, font=FB(40)), 16), clock, font=FB(40), fill=CY)
        d.line([24, 76, 1000, 76], fill=CY, width=3)
    y = 110 if bar else 60
    for i, ln in enumerate(lines):
        if sel is not None and i == sel:
            d.rectangle([20, y - 6, 1004, y + 52], fill=CY)
            d.text((40, y), ln, font=FB(44), fill=OBG)
        else:
            d.text((40, y), ln, font=F(44), fill=CY)
        y += 64
    img.save(f"mock/{name}.png")

radio("r_home", "SF", [
    "Meshtastic ead4 (SF)", "0 online   No Sats", "#Group9",
    "ChUtil 2%   Up 0:01", "", "USER: next   hold: menu"])
radio("r_lora", "LoRa", [
    "@ 1/2        BLE: ead4", "Role: Client Mute", "US / LongFast",
    "Freq: 912.875MHz", "ChUtil [=       ]  2%"])
radio("r_position", "Position", [
    "No Fix", "Searching...  Sats 3", "Needs open sky",
    "Last: 34.9098 -101.9176", "Alt 1102m"])
radio("r_lastheard", "Last Heard", [
    "RG            45s ago", "", "(this radio: SF)"])
radio("r_bearings", "Bearings", [
    "RG   134\u00b0 SE   0.83mi", "", "? = no position yet"])
radio("r_system", "System", [
    "Ver 2.7.26", "Flash 34%   Heap 61%", "PSRAM ok", "Up 1h 12m"])
radio("r_clock", "Clock", ["", "    16:41:07", "", "      CDT   (GPS time)"])
radio("r_msgaction", "Msg Action", [
    "Reply", "Mute Channel", "View Chats", "Dismiss"], sel=0)
radio("r_dest", "Destination", [
    "#Group9", "RG", "Free Text"], sel=0)
radio("r_presets", "Preset", [
    "On my way", "Turn left", "Turn right", "Stop here", "Help!"], sel=0)
radio("r_sending", "Messages", [
    "", "   Sending...", "", "   to #Group9"])
radio("r_chat", "#Group9", [
    "SF: On my way      \u2713", "RG: OK             \u2713", "",
    "hold: message action"])
radio("r_reply", "Reply", [
    "Reply to Last Msg", "With Preset", "With Free Text"], sel=1)
radio("r_nodeaction", "Node Action", [
    "Favorite", "Ignore", "Reset NodeDB"], sel=2)
radio("r_loraactions", "LoRa Action", [
    "Region", "Modem Preset", "Channel URL", "!! do not change !!"], sel=0)
radio("r_sysaction", "Sys Action", [
    "Sleep Screen", "Reboot", "Shutdown"], sel=2)
radio("r_shutdown", "Shutdown", [
    "", "  Shutting down...", "", "  Settings saved"])
radio("r_failed", "#Group9", [
    "SF: Help!          \u2717", "", "Message failed",
    "Max retransmission"])

# ---------------- display screens ----------------
def dsp_base():
    img = Image.new("RGB", (1200, 900), PAPER)
    d = ImageDraw.Draw(img)
    return img, d

def dsp_chrome(d, partner="RG", tag="SF<->RG OK", clock="7:32a CDT", up="up 2229s", foot="link OK - tap:next hold:reset"):
    d.text((24, 16), clock, font=F(26), fill=INK)
    w = d.textlength(partner, font=FB(44))
    d.text(((1200 - w) / 2, 10), partner, font=FB(44), fill=INK)
    d.text((1200 - 24 - d.textlength(tag, font=F(26)), 20), tag, font=F(26), fill=INK)
    d.text((24, 858), foot, font=F(26), fill=INK)
    d.text((1200 - 24 - d.textlength(up, font=F(26)), 858), up, font=F(26), fill=INK)

# d_searching: boot screen
img, d = dsp_base()
d.text((140, 330), "GROUP 9 TRACKER", font=FB(96), fill=INK)
d.text((140, 470), "starting up...", font=F(56), fill=INK)
img.save("mock/d_searching.png")

# d_linksearch: status page while acquiring
img, d = dsp_base()
dsp_chrome(d, partner="OVERALL TRACKER", tag="", clock="7:02a CDT", up="up 40s", foot="tap:messages hold:reset")
d.text((330, 120), "LINK CONNECTED", font=FB(56), fill=INK)
d.text((250, 210), "radios: waiting for first packet", font=F(34), fill=INK)
d.text((180, 330), "SF   waiting for GPS fix", font=FB(44), fill=INK)
d.text((180, 430), "RG   PTR not heard yet", font=FB(44), fill=INK)
d.text((330, 600), "normally live in ~2 min", font=F(34), fill=INK)
img.save("mock/d_linksearch.png")

# d_compass: COURSE-UP driving view (per shipped firmware)
img, d = dsp_base()
dsp_chrome(d, up="up 2789s", clock="7:42a CDT")
cx, cy, R = 330, 480, 210
d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=INK, width=6)
course = 135.0  # heading SE -> cardinals rotate
for i, card in enumerate(["N", "E", "S", "W"]):
    a = math.radians(i * 90 - course)
    lx = cx + math.sin(a) * (R + 46); ly = cy - math.cos(a) * (R + 46)
    f = FB(44)
    d.text((lx - d.textlength(card, font=f)/2, ly - 24), card, font=f, fill=INK)
# nose index at 12 o'clock
d.polygon([(cx-18, cy-R+4), (cx+18, cy-R+4), (cx, cy-R+34)], fill=INK)
# dart: partner dead ahead (filled = fresh)
d.polygon([(cx, cy-150), (cx+62, cy+120), (cx, cy+70), (cx-62, cy+120)], fill=INK)
d.text((700, 150), "1.45 Mi", font=FB(110), fill=INK)
d.text((700, 300), "at 12 o'clock", font=FB(52), fill=INK)
d.text((700, 390), "age 11s", font=F(48), fill=INK)
d.text((700, 470), "you 48 mph", font=F(48), fill=INK)
d.text((700, 550), "closing 45 mph", font=F(48), fill=INK)
d.text((700, 680), "needle = SF", font=F(30), fill=INK)
d.text((700, 720), "dart   = RG", font=F(30), fill=INK)
img.save("mock/d_compass.png")

# d_status
img, d = dsp_base()
dsp_chrome(d, partner="OVERALL TRACKER", tag="", clock="7:44a CDT", up="up 2915s", foot="tap:messages hold:reset")
d.text((330, 110), "LINK CONNECTED", font=FB(56), fill=INK)
d.text((230, 195), "radios: SF<->RG COMMUNICATING", font=F(34), fill=INK)
d.text((110, 290), "RG  34.87012 -101.76491", font=FB(48), fill=INK)
d.text((190, 360), "spd 0 mph - 21s - 50%", font=F(40), fill=INK)
d.text((110, 460), "SF  34.86751 -101.76222", font=FB(48), fill=INK)
d.text((320, 530), "age 4s", font=F(40), fill=INK)
d.text((330, 620), "0.35 Mi", font=FB(100), fill=INK)
d.text((300, 760), "RG IS NE OF SF", font=FB(48), fill=INK)
img.save("mock/d_status.png")

# d_messages
img, d = dsp_base()
dsp_chrome(d, partner="MESSAGES", tag="SF<->RG OK", clock="7:45a CDT", up="up 2970s", foot="tap:next hold:clear history")
rows = [("RG: On my way", "2m"), ("RG: Turn left", "9m"), ("RG: OK", "14m"), ("RG: Stop here", "21m")]
y = 160
for t, age in rows:
    d.text((80, y), t, font=FB(52), fill=INK)
    d.text((1000, y), age, font=F(44), fill=INK)
    d.line([80, y+76, 1120, y+76], fill=(150, 158, 152), width=2)
    y += 120
d.text((240, 700), "received texts, newest first", font=F(36), fill=INK)
img.save("mock/d_messages.png")

print("mocks:", len(os.listdir("mock")))
