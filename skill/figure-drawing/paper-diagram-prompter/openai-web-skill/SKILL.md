---
name: paper-skill-latex
description: create, revise, validate, and compile latex paper projects, especially ml/ai review papers for arxiv using ieeetran-style structure, verified bibtex citations, plan/issues workflow, and two-column layout hygiene. also use when scanning a codebase to produce paper-ready figure prompts and source for draw.io, excalidraw, and tikz. triggers include requests to write an arxiv review article, scaffold a latex paper, validate citations, compile/qa a paper, generate paper diagrams from a repo, create tikz figures, or produce thesis/research-paper architecture diagrams.
---

# Paper Skill LaTeX

## Overview

Use this skill for two related workflows adapted from `Fanceir/paper-skill-latex`:

1. **paper writing**: scaffold and develop an IEEEtran-style LaTeX review paper with a gated plan, issues CSV, verified BibTeX citations, visuals, QA, and compilation.
2. **paper figures**: scan a source codebase and emit paper-ready prompts/source for draw.io, Excalidraw, and TikZ without rendering images.

Default to the user's language. For formal Chinese writing, avoid unnecessary mixed Chinese-English unless technical terms require it.

## Workflow Decision Tree

1. **New ML/AI review paper or arXiv article?** Follow [writing-workflow.md](references/writing-workflow.md).
2. **Existing LaTeX project citation/QA/compile task?** Follow the citation and QA sections in [writing-workflow.md](references/writing-workflow.md).
3. **Repo-to-paper figures, architecture diagrams, model diagrams, or TikZ source?** Follow [diagram-workflow.md](references/diagram-workflow.md).
4. **Need output templates or tool-specific paste instructions?** Load the relevant cookbook in `references/`.

## Non-Negotiable Rules

- Never fabricate citations, paper metadata, experimental results, modules, layers, or metrics.
- Verify every citation using web search/source pages before adding BibTeX or making literature claims.
- For a new paper, do not write full prose in `main.tex` until the plan is approved and the issues CSV exists.
- Do not overwrite user files without explicit confirmation.
- Keep LaTeX projects self-contained with relative paths.
- For diagrams, output text/source only unless the user separately asks for an image generation task outside this skill.
- Use English-only figure labels by default for `pdflatex`; use bilingual labels only when requested and warn that TikZ needs XeLaTeX or LuaLaTeX with CJK support.

## Bundled References

- `references/writing-workflow.md`: gated paper-writing workflow, citation verification, QA, and layout hygiene.
- `references/diagram-workflow.md`: source-code scanning and figure-prompt workflow.
- `references/diagram-taxonomy.md`: map from repo type and paper chapter to figure types.
- `references/style-conventions.md`: paper-safe palette, typography, arrows, captions, and bilingual-label rules.
- `references/tikz-cookbook.md`: TikZ package whitelist, recipes, and paste/compile instructions.
- `references/drawio-cookbook.md`: draw.io XML/fallback format and paste instructions.
- `references/excalidraw-cookbook.md`: Excalidraw descriptor/Mermaid formats and paste instructions.

## Output Standards

For writing tasks, deliver concrete files or patch-ready content plus a concise status summary: plan state, issue progress, citation verification status, compile/QA result, and remaining TODOs.

For diagram tasks, provide one Markdown report. For every figure include: figure ID, caption, chapter placement, rationale, design notes, draw.io output, Excalidraw output, TikZ output, and paste instructions. Do not claim a feature exists unless found in the scanned code or clearly marked as illustrative.
