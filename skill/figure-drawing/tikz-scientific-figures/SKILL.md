---
name: tikz-scientific-figures
description: >-
  Create publication-grade scientific figures and schematic diagrams with
  TikZ/PGFPlots, output as vector PDF (and SVG for visual editing). Use when the
  user wants a figure for a paper/thesis/report, a data plot (line, scatter,
  bar, error-bar, heatmap, log axis), a circuit diagram, a flowchart or block
  diagram, a free-body/force or geometry schematic, a biology figure
  (immunofluorescence/tissue, cell, signaling pathway, gene or plasmid map), a
  CS/ML figure (neural network, system architecture, finite-state machine, tree,
  graph), or a molecular structure — especially when they mention TikZ, PGFPlots,
  circuitikz, LaTeX figures, reproducible/vector/publication-quality plots, or
  editing an existing .tex figure. Produces reproducible .tex + data sources the
  user can re-edit.
---

# TikZ Scientific Figures

Generate reproducible, publication-grade figures in TikZ. One figure = one
`standalone` `.tex` file that compiles to a tightly-cropped vector PDF. Always
deliver the `.tex` (+ any data file) so the figure stays editable.

## Step 0 — check the toolchain (first run only)
```bash
bash scripts/check_env.sh
```
If tools are missing, show the user the printed install hints (OS-aware:
macOS/Windows/Linux) and stop until the toolchain is in place. Need: a LaTeX
engine (pdflatex — the scripts' default; lualatex needs luatex85), poppler
(preview), and for SVG export dvisvgm + mutool (mupdf-tools). latexmk is optional
— the scripts run the engine twice without it.

**Cross-platform note.** The recipes and TikZ code are OS-independent (identical
output on macOS/Windows/Linux). The four `.sh` scripts are portable bash: on
Windows run them from Git Bash or WSL. If no bash is available, run the
underlying commands directly — `compile` ≈ `pdflatex -interaction=nonstopmode
-halt-on-error figure.tex` (run twice), `preview` ≈ `pdftoppm -png -r 200
-singlefile figure.pdf out`, `export_svg` ≈ `dvisvgm --pdf figure.pdf`. On
Windows, MiKTeX auto-installs missing LaTeX packages on first compile, so the
"optional packages" step is usually unnecessary there.

## Workflow
1. **Pick the figure type** and read the matching recipe (only that one):
   - data plot (line/scatter/bar/hist/box/heatmap/contour/3D/log) → `references/pgfplots-recipes.md`
   - circuit → `references/circuitikz-recipes.md`
   - flowchart / block / force / geometry → `references/diagram-recipes.md`
   - biology (IF/tissue, cell, pathway, gene/plasmid map) → `references/biology-recipes.md`
   - CS/ML (neural net, architecture, automaton, tree, graph, UML, ER, Gantt) → `references/cs-recipes.md`
   - chemistry (molecule, reaction, energy profile, lattice) → `references/chemistry-recipes.md`
   - physics (ray optics, Feynman, vector field) → `references/physics-recipes.md`
   - math (commutative diagram, Venn, number line) → `references/math-recipes.md`
2b. **Composing a paper figure?** Multi-panel (a)(b)(c), insets, significance
   markers, fit+CI bands, or labelling a real microscopy/photo image →
   `references/figure-composition.md`.
2. **Start from the template.** Copy `assets/standalone-template.tex` and
   `assets/preamble.tex` into the working dir. Keep the `TUNABLES` block at the
   top — it is what lets non-experts hand-edit later.
3. **Put data in an external file** (`data.csv`) for data plots, so "editing the
   plot" means editing the CSV, not the TikZ.
4. **Compile, then self-check visually** (do not skip the look):
   ```bash
   bash scripts/compile.sh figure.tex      # -> figure.pdf  (read figure.log on error)
   bash scripts/preview.sh figure.pdf      # -> figure.preview.png — actually open & inspect it
   ```
   On errors, match `figure.log` against `references/common-errors.md`.
5. **Deliver** the PDF + `.tex` + data file together, and state the figure's
   edit state (see Editing below).

## Publication-grade rules (non-negotiable defaults)
- Vector output (PDF/SVG); never deliver only a raster.
- Colour-blind-safe palette (Okabe–Ito / viridis) — wired into `preamble.tex`.
  Never hard-code raw red/green or use the `jet` colormap.
- Size to the target: 89 mm single-column / 183 mm double-column; body font 7–9 pt.
- Every axis labelled **with units**; error bars state SD/SE/CI; multi-panel
  figures numbered (a)(b)(c).
- Render math labels in LaTeX (`$\alpha$`, `siunitx`), so they match the paper.
- Ship the source: deliver `.tex` + data, not just an image.

If the user names a target venue (IEEE, a thesis template, etc.), adjust width,
font, and `compat` in `preamble.tex` accordingly before drawing.

## Editing an existing figure
Read `references/editing-guide.md`. Summary of the rule that must not be broken:
- Default: edit the `.tex`/`.csv` in place and recompile (model-driven or via the
  `TUNABLES` block). Never redraw from scratch when a source file exists.
- For free-form visual polish, `bash scripts/export_svg.sh figure.tex` exports an
  SVG for Inkscape/TikZiT. **This forks the figure to the SVG branch** (a
  `figure.svg.frozen` marker is written): from then on the SVG is authoritative
  and the `.tex` is a frozen archive — do NOT recompile the `.tex` over the
  user's SVG edits. Always tell the user which branch a figure is on.
- After exporting, launch a local visual editor that loads the SVG and saves
  back in place:
  ```bash
  bash scripts/edit_svg.sh figure.svg   # no arg => newest *.svg in the dir
  ```
  This starts a local server (127.0.0.1, ephemeral port), opens **Method Draw**
  in the browser with the SVG pre-loaded, and **Ctrl/Cmd+S writes the edits back
  to the same `figure.svg`** (the browser's download export stays as a fallback).
  Ctrl+C in the terminal stops the server. The SVG remains the authoritative
  source (`.tex` stays frozen). Needs `python3`; on Windows run from Git Bash or
  call `python3 scripts/edit_server.py figure.svg` directly.
