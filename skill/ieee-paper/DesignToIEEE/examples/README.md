# Examples

This folder contains a complete worked example of the `DesignToIEEE` skill.

## InkID — Stylometric Authorship Verification System

| File | Description |
|---|---|
| `InkID-DESIGN_DOCUMENT.md` | Input SDD — a full 16-section software design document for InkID, a system that performs stylometric authorship verification and AI text detection |
| `InkID-paper.tex` | Output — the generated IEEE Conference (IEEEtran, 2-column) LaTeX paper |
| `InkID-references.bib` | Output — the BibTeX bibliography with verified and TODO-flagged entries |

### How to Compile

```bash
pdflatex InkID-paper.tex
bibtex InkID-paper
pdflatex InkID-paper.tex
pdflatex InkID-paper.tex
```

Or upload both files to [Overleaf](https://overleaf.com) and click Recompile.

### What the Skill Generated

- **7 fully written sections** from SDD content (Introduction, Related Work, Architecture, Methodology, Implementation, Discussion, Conclusion)
- **1 placeholder section** (Results — the SDD had no benchmark data; user chose placeholder)
- **3 placeholder tables** ready to fill with real evaluation numbers
- **15 BibTeX entries** — 8 verified, 7 marked TODO for human confirmation
- **Compiled to PDF in the same session** (6 pages, IEEE 2-column)

---

*Want to add your own example? See [CONTRIBUTING.md](../CONTRIBUTING.md).*
