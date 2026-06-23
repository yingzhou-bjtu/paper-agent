# 📄 DesignToIEEE — Claude Skill

> **A Claude skill that compiles a Software Design Document (SDD) into a complete, publication-ready IEEE research paper in LaTeX.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blueviolet)](https://claude.ai)
[![IEEE Format](https://img.shields.io/badge/Output-IEEE%20LaTeX-blue)](skill/references/latex-templates.md)

---

## What This Does

You give Claude an SDD. Claude gives you a conference-ready IEEE paper.

The skill acts as a **research paper compiler** — it extracts architecture, algorithms, module design, and rationale from your design document and transforms them into a structured IEEE LaTeX paper with:

- Formal academic prose (no bullet points in the body)
- Correctly structured sections (Abstract → Introduction → Related Work → Methodology → Implementation → Results → Discussion → Conclusion)
- Real, verifiable BibTeX citations (no hallucinated references)
- A compiled PDF output (when LaTeX is available)
- Placeholder sections where real data is missing — with your explicit confirmation

---

## Supported Input Formats

| Format | Notes |
|---|---|
| `.md` / `.txt` | Read directly |
| `.pdf` | Extracted via `pdftotext` |
| `.docx` | Extracted via `python-docx` |
| Pasted text | Works as-is |

## Output

| File | Contents |
|---|---|
| `paper.tex` | Full IEEE LaTeX source (conference or journal style) |
| `references.bib` | BibTeX bibliography with verified + TODO-flagged entries |
| `paper.pdf` | Compiled PDF (when LaTeX environment is available) |

---

## Quick Start

### 1. Install the Skill

Upload the `skill/` folder to your Claude skills directory (e.g. `/mnt/skills/user/sdd-to-ieee/`).

The trigger description in `SKILL.md` handles automatic activation. Claude will invoke this skill when you say things like:

- *"Convert my SDD to an IEEE paper"*
- *"Generate a LaTeX research paper from this design doc"*
- *"Compile my SDD into IEEE format"*

### 2. Upload Your SDD

In Claude, attach your SDD file (`.md`, `.pdf`, `.docx`, or `.txt`) and type:

```
/sdd-to-ieee
```

Or just:

```
Convert this SDD to an IEEE conference paper
```

### 3. Answer Two Questions

Claude will ask:
1. **IEEE Conference** (2-column) or **IEEE Journal/Transactions** (single-column)?
2. For any section lacking source data (e.g. Results): skip, placeholder, or provide data now?

### 4. Get Your Files

Claude outputs `paper.tex`, `references.bib`, and (if LaTeX is installed) `paper.pdf`.

---

## Compiling the PDF Yourself

If Claude couldn't compile the PDF, use one of these methods:

### Overleaf (Recommended — free, no install)
1. Go to [overleaf.com](https://www.overleaf.com) → New Project → Blank Project
2. Upload `paper.tex` and `references.bib`
3. Set compiler to **pdfLaTeX** → click **Recompile**

### Local — Linux / WSL
```bash
sudo apt-get install texlive-full
pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex
```

### Local — macOS
```bash
brew install --cask mactex
pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex
```

### Local — Windows
Install [MiKTeX](https://miktex.org) + [TeXstudio](https://www.texstudio.org), open `paper.tex`, press **F5**.

See [`skill/references/compilation-guide.md`](skill/references/compilation-guide.md) for full details.

---

## Skill Structure

```
skill/
├── SKILL.md                        ← Main skill instructions (Claude reads this)
└── references/
    ├── latex-templates.md          ← IEEE conference + journal LaTeX templates
    ├── known-references.md         ← Curated safe-to-cite foundational BibTeX entries
    └── compilation-guide.md        ← How to compile on Windows / Mac / Linux / Overleaf
```

---

## Generating Your Own SDD

Don't have an SDD yet? Use the optimized prompt in [`SDD_GENERATOR_PROMPT.md`](SDD_GENERATOR_PROMPT.md) with any AI coding assistant:

| Tool | Cost | Best For |
|---|---|---|
| [Claude Code](https://claude.ai/code) | Free tier available | Best overall output quality |
| [OpenCode](https://opencode.ai) | Free for students | Terminal-based, great for existing codebases |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Free (Google account) | Fast, large context window |
| [Kimi Code](https://kimi.moonshot.cn) | Free | Long document generation |
| [GitHub Copilot](https://github.com/features/copilot) | Free for students | IDE integration |
| [OpenAI Codex](https://platform.openai.com) | Paid | Strong technical writing |

---

## Reference Database

The skill includes a curated BibTeX database of **safe-to-cite foundational papers** organized by domain:

- Software Architecture (Bass, Fielding, GoF patterns)
- Machine Learning & AI (Goodfellow, LeCun, Vaswani)
- Databases (Codd, Bigtable, Dynamo)
- Distributed Systems (MapReduce, CAP theorem, Lamport)
- Security (Anderson, RSA)
- IEEE/ISO Standards (IEEE 830, 1016, 12207)
- NLP (Shannon entropy, TF-IDF, NLTK, scikit-learn)

See [`skill/references/known-references.md`](skill/references/known-references.md).

---

## Example Output

The [`examples/`](examples/) folder contains a complete worked example:

- [`examples/InkID-DESIGN_DOCUMENT.md`](examples/InkID-DESIGN_DOCUMENT.md) — Input SDD (stylometric authorship verification system)
- [`examples/InkID-paper.tex`](examples/InkID-paper.tex) — Generated IEEE LaTeX paper
- [`examples/InkID-references.bib`](examples/InkID-references.bib) — Generated BibTeX file

---

## Contributing

Contributions are welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

Ideas for contributions:
- Additional domain reference entries in `known-references.md`
- Support for Springer LNCS or ACM templates
- Multi-language SDD support
- Automated threshold calibration guidance

---

## License

MIT License — see [`LICENSE`](LICENSE).

---


