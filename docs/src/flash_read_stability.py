# Flash read-stability check: read the settings partition three times inside ONE esptool
# connection (the board resets when the port closes), plus 1 MB of program code as a control.
# Records counts and sector numbers only; raw dumps are never written.
# usage: python docs/src/flash_read_stability.py COM4 SF "after two days at 0 % battery" out.json
import sys, json, time, datetime, collections
sys.path.insert(0, "C:/p/packages/tool-esptoolpy")
import esptool
port, radio, note, out = sys.argv[1:5]
SET, SETLEN, APP, APPLEN = 0xC90000, 0x360000, 0x10000, 0x100000
esp = esptool.cmds.detect_chip(port, 115200, "default_reset", False, 7)
esp = esp.run_stub(); esp.change_baud(460800)
def rd(a, n):
    for k in range(4):
        try: return esp.read_flash(a, n)
        except Exception as e:
            print("  read retry", k, type(e).__name__); time.sleep(1)
    raise SystemExit("read failed")
t0 = time.time()
S = [rd(SET, SETLEN) for _ in range(3)]; print("  settings x3 done", round(time.time()-t0), "s")
A = [rd(APP, APPLEN) for _ in range(2)]; print("  app x2 done", round(time.time()-t0), "s")
esp.hard_reset()
def diff(x, y):
    u = collections.Counter(); n = 0
    for i in range(len(x)):
        if x[i] != y[i]: n += 1; u[i // 4096] += 1
    return n, u
d12, u12 = diff(S[0], S[1]); d23, u23 = diff(S[1], S[2]); a12, _ = diff(A[0], A[1])
unstable = sorted(set(u12) | set(u23))
data = sum(1 for i in range(SETLEN // 4096) if any(b != 0xFF for b in S[0][i*4096:(i+1)*4096]))
rec = {"radio": radio, "date": datetime.date.today().isoformat(), "after": note,
       "differing_bytes": {"read1_vs_read2": d12, "read2_vs_read3": d23, "app_read1_vs_read2": a12},
       "unstable_sectors": unstable, "sectors_with_data": data}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps(rec, indent=1))
