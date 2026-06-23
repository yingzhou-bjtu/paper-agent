# Contributing to sdd-to-ieee

Thank you for your interest in contributing! This skill gets better with more domain coverage, better templates, and community-tested prompts.

## Ways to Contribute

### 1. Add References to `known-references.md`
The reference database is the most impactful place to contribute. Add well-known, verifiable BibTeX entries for domains not yet covered (e.g. cybersecurity, embedded systems, IoT, computer vision, HCI).

**Rules:**
- Only add references you are confident exist (seminal papers, widely cited work, IEEE/ACM standards)
- Include the BibTeX entry in the exact format used in the file
- Group entries under an appropriate domain heading
- Never add references you cannot personally verify

### 2. Add LaTeX Templates
If you want to add support for Springer LNCS, ACM, or other formats, add a new section to `skill/references/latex-templates.md` and update `skill/SKILL.md` to reference it.

### 3. Add Worked Examples
Add a real SDD → IEEE paper pair to the `examples/` folder. Include:
- `examples/YourSystem-DESIGN_DOCUMENT.md` — the input SDD
- `examples/YourSystem-paper.tex` — the generated LaTeX
- `examples/YourSystem-references.bib` — the bibliography

### 4. Improve the SDD Generator Prompt
If you find phrasings that produce better SDD output from a specific tool (Claude Code, Gemini CLI, etc.), open a PR with the improved prompt and note which tool it was tested with.

### 5. Bug Reports
If the skill produces incorrect LaTeX, hallucinated references, or misses a section — open an issue with:
- The SDD you used (or a minimal reproduction)
- What the skill output
- What you expected

## Pull Request Process

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test LaTeX templates by compiling with `pdflatex` locally or on Overleaf
5. Open a PR with a clear description of what changed and why

## Code of Conduct

Be respectful. Academic integrity matters — do not add fake or unverifiable references under any circumstances.
