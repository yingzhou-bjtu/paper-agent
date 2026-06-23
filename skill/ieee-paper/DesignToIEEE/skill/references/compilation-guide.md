# How to Compile Your IEEE LaTeX Paper

Your `.tex` and `.bib` files are ready. Here's how to compile them into a PDF.

---

## Option 1: Overleaf (Easiest — no installation needed)

1. Go to [overleaf.com](https://overleaf.com) and create a free account
2. Click **New Project → Blank Project**
3. Upload `paper.tex` and `references.bib`
4. In the top-left dropdown, set **Compiler** to `pdfLaTeX`
5. Click **Recompile**

The PDF will appear on the right. Download it with the download button.

---

## Option 2: Local — Linux / WSL

```bash
# Install TeX Live (full, includes IEEEtran)
sudo apt-get install texlive-full

# Navigate to your paper directory
cd /path/to/paper

# Compile (run pdflatex twice + bibtex for references)
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Open the result
evince paper.pdf   # or xdg-open paper.pdf
```

---

## Option 3: Local — macOS

```bash
# Install MacTeX (includes everything)
brew install --cask mactex

# Then compile the same way as Linux:
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Open result
open paper.pdf
```

---

## Option 4: Local — Windows

1. Install [MiKTeX](https://miktex.org/download) or [TeX Live for Windows](https://tug.org/texlive/windows.html)
2. Install [TeXstudio](https://www.texstudio.org/) as an editor
3. Open `paper.tex` in TeXstudio
4. Press **F5** (Build & View) — it handles the full compile sequence automatically

---

## Troubleshooting

| Error | Fix |
|---|---|
| `IEEEtran.cls not found` | Install `texlive-publishers` or download from [IEEE Templates](https://www.ieee.org/conferences/publishing/templates.html) |
| `Citation undefined` | Run `bibtex paper` then `pdflatex` twice more |
| `Package not found` | Run `tlmgr install <package-name>` on Linux/Mac |
| `Overfull \hbox` warnings | Normal for draft; fix with `\linebreak` or shorter text |
| Missing figure file | Comment out `\includegraphics` lines until figures are ready |

---

## Adding Real Figures

If your SDD had architecture diagrams:
1. Export them as `.pdf` or `.png`
2. Place in a `figures/` subfolder next to `paper.tex`
3. Uncomment the `\includegraphics` lines in the .tex file

For drawing new diagrams, use [draw.io](https://app.diagrams.net/) (free, exports to PDF).
