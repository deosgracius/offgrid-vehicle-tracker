# Two-pass document builder: ToC page numbers + stamped page numbers.
import subprocess, sys, time, os
import pymupdf

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render(html, pdf):
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file:///" + html.replace("\\", "/")],
                   capture_output=True)
    # wait until the page count is STABLE across two polls (Edge can return
    # while the file is still being written; an early read sees fewer pages)
    last = -1
    for _ in range(30):
        time.sleep(1)
        try:
            d = pymupdf.open(pdf)
            n = len(d); d.close()
        except Exception:
            continue
        if n > 0 and n == last:
            return n
        last = n
    raise RuntimeError("render failed or never stabilized")

def build(html_path, pdf_path, anchors, sentinel, skip_toc=True, min_images=0):
    src = open(html_path, encoding="utf-8").read()
    tmp_html = html_path + ".pass1.html"
    open(tmp_html, "w", encoding="utf-8").write(src)
    tmp_pdf = pdf_path + ".pass1.pdf"
    render(tmp_html, tmp_pdf)
    d = pymupdf.open(tmp_pdf)
    # verify content current
    all_text = "".join(p.get_text() for p in d)
    assert sentinel in all_text, "sentinel missing - stale render"
    texts = [p.get_text().replace(" ", " ") for p in d]
    pages = {}
    for entry in anchors:
        token, needle = entry[0], entry[1]
        minpage = entry[2] if len(entry) > 2 else 0
        for i, t in enumerate(texts):
            if skip_toc and i == 1:
                continue
            if i + 1 < minpage:
                continue
            if needle in t:
                pages[token] = i + 1
                break
        else:
            print("MISSING anchor:", needle); pages[token] = 0
    d.close()
    out = src
    for entry in sorted(anchors, key=lambda e: -len(e[0])):
        out = out.replace(entry[0], str(pages[entry[0]]))
    final_html = html_path + ".final.html"
    open(final_html, "w", encoding="utf-8").write(out)
    render(final_html, pdf_path)
    # stamp page numbers (skip cover page 1)
    d = pymupdf.open(pdf_path)
    for i in range(1, len(d)):
        p = d[i]
        w = p.rect.width
        p.insert_text((w/2 - 8, p.rect.height - 22), str(i + 1),
                      fontname="tiro", fontsize=12, color=(0.25, 0.3, 0.4))
    d.saveIncr()
    n = len(d)
    n_img = sum(len(pg.get_images()) for pg in d)
    d.close()
    assert n_img >= min_images, f"IMAGE CHECK FAILED: {n_img} < {min_images} (assets missing?)"
    print("built", pdf_path, "pages:", n, "images:", n_img, "toc:", pages)
    return n

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "guide":
        base = r"C:\Users\deogr\AppData\Local\Temp\claude\C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project\eca057db-c8d2-4bae-87d3-8a6c4f6c4af6\scratchpad\guide"
        anchors = [("@P1", "1  The Devices and Their Buttons"),
                   ("@P2", "2  Powering On"),
                   ("@P3", "3  The Two-Second Pre-Flight Check"),
                   ("@P4", "4  The Radio's Screens"),
                   ("@P5", "5  Sending a Message"),
                   ("@P6", "6  The Display While You Drive"),
                   ("@P7", "7  More Things You Can Do"),
                   ("@P8", "8  How Far It Reaches"),
                   ("@P9", "9  Menus to Leave Alone"),
                   ("@P10", "10  Powering Off and Charging"),
                   ("@P11", "11  When Something Looks Wrong"),
                   ("@P12", "12  Quick Reference"),
                   ("@P13", "Appendix A  Abbreviations and Acronyms")]
        build(os.path.join(base, "GUIDE.html"), os.path.join(base, "DEVICE_USER_GUIDE.pdf"),
              anchors, "How Far It Reaches", min_images=23)
    elif which == "manual":
        base = r"C:\Users\deogr\AppData\Local\Temp\claude\C--Users-deogr-Documents-Fall-Project-Off-Grid-Vehicle-dection-project\e8b2e8fa-1513-4aa8-a8f6-ce4fcd20e664\scratchpad\manuals"
        anchors = [("@T1", "1. System overview: the stack"),
                   ("@T2", "2. System architecture"),
                   ("@T3", "3. Hardware inventory and identification"),
                   ("@T4", "4. The physical layer: inside the SX1262"),
                   ("@T5", "5. The link layer: budget, airtime"),
                   ("@T6", "6. Channel sharing: collision avoidance"),
                   ("@T7", "7. The protocol layer: Meshtastic"),
                   ("@T8", "8. The transport layer: Bluetooth LE"),
                   ("@T9", "9. The application layer: display firmware"),
                   ("@T10", "10. Navigation mathematics"),
                   ("@T11", "11. Timing, liveness, and honesty"),
                   ("@T12", "12. Range characterization: the two campaigns"),
                   ("@T13", "13. Extending the range"),
                   ("@T14", "14. Build, flash, and test procedures"),
                   ("@T15", "15. Verification record"),
                   ("@T16", "16. Failure modes and recovery"),
                   ("@TA", "Appendix A: acronyms and abbreviations", 20),
                   ("@TB", "Appendix B: repository guide", 20),
                   ("@TR", "References", 20)]
        build(os.path.join(base, "TECH_MANUAL.html"), os.path.join(base, "TECHNICAL_MANUAL.pdf"),
              anchors, "Operator-facing functions", skip_toc=False, min_images=24)
