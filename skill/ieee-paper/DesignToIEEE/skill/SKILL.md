---
name: DesignToIEEE
description: >
  Converts a Software Design Document (SDD) into a complete, publication-ready IEEE research paper
  in LaTeX format. Use this skill whenever the user uploads or pastes an SDD and wants to generate
  an academic paper, research paper, IEEE paper, conference paper, journal submission, or any
  formal LaTeX document from it. Also trigger when the user says things like "turn my design doc
  into a paper", "write a paper about my system", "compile my SDD into IEEE format", or "generate
  LaTeX from my design". Supports PDF, Word (.docx), Markdown, and plain text inputs. Outputs a
  .tex file and attempts to compile a PDF using pdflatex. Handles both IEEE Conference
  (IEEEtran, 2-column) and IEEE Journal/Transactions (single-column) styles.
---

# SDD → IEEE Research Paper Skill

This skill acts as a **compiler for research papers**: it takes a raw Software Design Document
as input and produces a clean, publication-ready IEEE LaTeX paper as output.

---

## Step 0 — Read the Input File

Before doing anything else, read the SDD using the appropriate method:

| Input format | How to read |
|---|---|
| `.pdf` | Use the `pdf-reading` skill or `pdftotext` via bash |
| `.docx` | Use `python-docx` via bash: `python3 -c "import docx; print(docx.Document('file.docx').paragraphs[0].text)"` or loop over all paragraphs |
| `.md` / `.txt` | Read directly with bash `cat` |
| Pasted text | Already in context — proceed |

Extract the full text before any analysis.

---

## Step 1 — Ask the User (if not already specified)

If the user has not yet said which IEEE style they want, ask:
- **IEEE Conference** (IEEEtran, 2-column) — for conference submissions
- **IEEE Journal/Transactions** (single-column) — for journal/transactions submissions

This affects the `\documentclass` and column layout. Default to Conference if unclear.

---

## Step 2 — Extract and Map SDD Content

Carefully read the full SDD and extract the following, noting what is **present** vs **absent**:

### Mandatory extractions
- **System name / project title** → paper title
- **System purpose / problem statement** → Abstract + Introduction motivation
- **Architecture overview** (components, layers, modules) → Methodology / System Design
- **Key algorithms or logic** → Methodology
- **Technology stack** (languages, frameworks, DBs) → Implementation
- **Module breakdown** (classes, services, APIs) → Implementation
- **Design decisions and rationale** → Discussion / Conclusion

### Conditional extractions (only include if present)
- **Performance data, benchmarks, test results** → Results section
- **Comparison with existing systems** → Related Work section
- **References cited in the SDD** → Bibliography seed
- **Diagrams or figure descriptions** → Figure placeholders in LaTeX

### Sections where SDD data is insufficient — ask the user

After analysing the SDD, identify any optional sections (Results, Related Work, Discussion) for
which there is **not enough source material** to write real content. For each such section,
**ask the user explicitly** before proceeding:

> "Your SDD doesn't include benchmark or test data, so I don't have enough material for a
> Results section. Would you like to:
> (a) Skip it entirely
> (b) Include a placeholder Results section you can fill in later
> (c) Provide the data now so I can write it properly"

Apply the same question pattern for Related Work and Discussion if they lack content.

**Never fabricate data, metrics, or comparisons.** Only write a section if the user confirms
they want it and either provides content or explicitly accepts a placeholder.

---

## Step 3 — Generate the LaTeX Paper

Use the template and guidance in `references/latex-templates.md` for both styles.

### Section writing rules
- Write in **formal academic third-person** ("The proposed system…", "This paper presents…")
- **Never use bullet points in the final paper body** — convert to flowing prose
- Each section must be ≥ 2 paragraphs of real content (not filler)
- Use `\cite{}` for any claims that need support — see references policy below

### Section order and content

**Abstract** (150–250 words, single paragraph)
- Problem + proposed solution + key contribution + result/outcome (if available)

**I. Introduction**
- Motivate the problem in general terms
- State what the system does
- List the paper's contributions as a numbered list (`\begin{enumerate}`)
- Briefly outline the paper structure: "The remainder of this paper is organized as follows…"

**II. Related Work** *(omit if SDD has no prior-art content)*
- Situate the system in the existing literature
- Cite real, well-known papers from IEEE/ACM (see references policy)
- Contrast with the proposed system

**III. System Architecture / Methodology**
- Describe the overall architecture (layers, components, data flow)
- If a diagram is described in the SDD, add a `\begin{figure}` placeholder with caption
- Explain key design decisions and why they were made

**IV. Implementation**
- Technology stack (formatted as a `\begin{table}` if ≥ 3 items)
- Module-level breakdown with responsibilities
- Code snippets if present in SDD (use `\begin{lstlisting}`)

**V. Results** *(omit if no benchmark/test data)*
- Present performance metrics, test results, or evaluation outcomes
- Use `\begin{table}` for structured data

**VI. Discussion** *(include if meaningful content exists)*
- Interpret design choices and trade-offs
- Limitations of the current system
- Future work

**VII. Conclusion**
- Summarize the system and its contributions
- Restate key outcomes

---

## Step 4 — References Policy (Critical)

**Never hallucinate references.** Follow this strict policy:

### Allowed citation patterns
1. **Cite foundational technologies used** — if the system uses REST APIs, cite Fielding's dissertation. If it uses neural networks, cite LeCun et al. 1998 or Goodfellow et al. 2016. These are verifiable.
2. **Cite well-known IEEE/ACM papers** only when you are confident they exist (seminal papers, Turing Award work, widely known standards).
3. **Cite IEEE and ISO standards** when relevant (e.g., IEEE 830 for SRS, IEEE 1016 for SDD).

### What to do when unsure
- Use a `\cite{placeholder_TOPIC}` with a `% TODO: verify this reference` comment in the .bib entry
- Add a note at the end of the .tex file listing which references need human verification

### BibTeX format
Always output a `.bib` file alongside the `.tex` file. For each entry, use this format:
```bibtex
@article{fielding2000rest,
  author    = {Fielding, Roy Thomas},
  title     = {Architectural Styles and the Design of Network-based Software Architectures},
  year      = {2000},
  school    = {University of California, Irvine},
  note      = {Doctoral dissertation}
}
```

---

## Step 5 — Write the Output Files

Always produce **two source files**:
1. `paper.tex` — the full LaTeX source
2. `references.bib` — the BibTeX bibliography

Save both to `/mnt/user-data/outputs/`.

**Then always attempt to compile a PDF.** This is part of the required output, not optional:

```bash
# Install texlive if not present (may take a few minutes first time)
apt-get install -y texlive-full 2>/dev/null || true

# Compile — run the full sequence for correct references
cd /mnt/user-data/outputs
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

**If compilation succeeds:** present `paper.pdf`, `paper.tex`, and `references.bib` to the user.
**If compilation fails:** present `paper.tex` and `references.bib`, show the LaTeX error log excerpt,
and direct the user to `references/compilation-guide.md` for Overleaf/local instructions.

Do not silently skip compilation — always attempt it and report the outcome.

---

## Step 6 — Summary to User

After outputting files, tell the user:
1. Which sections were generated and why any were omitted
2. Which references are marked `% TODO: verify`
3. How to compile if PDF wasn't generated
4. Suggested next steps (add real figures, fill TODOs, target a specific venue)

---

## Reference Files

- `references/latex-templates.md` — Full IEEEtran LaTeX templates for both conference and journal styles
- `references/compilation-guide.md` — How to compile locally on Windows/Mac/Linux/Overleaf
- `references/known-references.md` — Curated list of safe-to-cite foundational papers by domain

Read these files when needed — don't load all of them upfront.
