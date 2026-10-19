# Document build sources

Durable home for the Technical Manual, Device User Guide, and Technical Report
build pipeline (HTML sources, asset generators, and generated assets). The
scratchpad copies get cleaned between sessions; THIS is the source of truth.

- manuals/: TECH_MANUAL.html, REPORT.html, gen_eq.py (14 equations),
  gen_figs.py (SX1262 figures), conv_docx.py (Word export), eq_*.png, fig_*.png
- guide/: GUIDE.html, gen_mocks.py (23 device screens), build_doc.py
  (two-pass ToC + page numbers + image-count verification), mock/*.png

Rebuild: run build_doc.py guide|manual (paths inside point at the scratchpad
working copies; copy this tree there, or update the paths, if the scratchpad
was cleaned).
