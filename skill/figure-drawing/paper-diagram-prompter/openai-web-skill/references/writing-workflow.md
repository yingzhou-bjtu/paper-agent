# Writing Workflow

## Inputs

- Required: topic or existing LaTeX project path.
- Optional: venue, page limit, author/affiliation block, date range, section constraints, target citation count, preferred title, and whether to include literature notes.

## Outputs

- `main.tex`, `ref.bib`, and an IEEEtran-compatible class/template when scaffolding.
- `plan/<timestamp>-<slug>.md` and `issues/<timestamp>-<slug>.csv` for new papers.
- Figures/tables and a compiled `main.pdf` when a LaTeX toolchain is available.
- A citation/QA report for validation-only tasks.

## Gated New-Paper Workflow

### Gate 0 — Research Snapshot and Draft Plan

1. Clarify constraints: venue, page limit, audience, author block, date range, and paper type.
2. Translate the topic into search keywords and run a light discovery pass of 10–20 key papers.
3. Propose 2–4 candidate titles.
4. Create a project scaffold with `main.tex`, `ref.bib`, `plan/`, `issues/`, `figures/`, and `notes/` folders.
5. Create a framework skeleton in `main.tex`: section headings, 2–4 bullets per section, and seed citations only. Do not write prose yet.
6. Draft the plan file with outline, visual plan, citation targets, risks, and clarification questions.
7. Return the outline, planned visuals, and questions. Stop until the user approves or delegates decisions.

### Gate 1 — Issues CSV

After approval:

1. Mark the plan gate as approved.
2. Create an issues CSV as the execution contract.
3. Validate that each row has an ID, phase, title, acceptance criteria, status, and citation target.
4. Use statuses `TODO`, `DOING`, `DONE`, or `SKIP`.
5. Add or split issue rows when scope grows; do not do untracked work.

### Phase 2 — Per-Issue Writing Loop

For each writing issue:

1. Research 8–12 section-specific papers.
2. Verify each source before citing it.
3. Write evidence-first prose. Never allow three consecutive substantive sentences without citations.
4. Add visuals when the content calls for a taxonomy, timeline, pipeline, architecture, comparison table, curve, or decision tree.
5. Update issue status and verified-citation count.
6. Compile after meaningful changes when a LaTeX toolchain is available.
7. Fix undefined citations and `Overfull \hbox` warnings before marking an issue done.

### Phase 3 — Rhythm Refinement

After all writing issues are complete:

- Vary paragraph and sentence length.
- Remove filler phrases.
- Preserve citations and technical meaning.
- Keep claims qualified and evidence-bound.

### Phase 4 — QA Gate

Check:

- Project compiles without undefined citations.
- Main text is within the requested page range.
- Every figure/table is referenced.
- Every non-trivial claim has citation support.
- `ref.bib` contains no duplicates or unverified entries.
- Recent-work target is met when applicable, e.g. 70%+ citations from the last three years for fast-moving ML/AI surveys.
- No `Overfull \hbox` warnings remain in `main.log`.

## Existing Paper Citation Workflow

1. Treat the provided path as the LaTeX project root.
2. Extract all `\cite{...}` keys from `.tex` files.
3. Compare with `ref.bib` to find missing and orphaned entries.
4. Verify every BibTeX entry online by exact title, author, and year.
5. Correct metadata, remove duplicates, and report any unresolved citations.
6. Compile if requested and a LaTeX toolchain is available.

## BibTeX Hygiene

- Required fields should match entry type.
- Escape special characters and accented names correctly.
- Prefer stable DOI, arXiv, venue, and publisher metadata.
- Do not bulk-add unverified BibTeX.

## Layout Hygiene

- Keep IEEEtran margins and fonts intact.
- Use single-column figures with `\columnwidth` by default.
- Use `figure*` and `\textwidth` only when labels or wide tables require it.
- Prefer `booktabs` for tables.
- Prefer `p{...}` column widths and `\tabcolsep` tuning over indiscriminate `\resizebox`.
- Break long equations with `split`, `multline`, `aligned`, or `IEEEeqnarray`.

## Success Targets

Typical ML/AI review-paper targets:

- 6–10 pages of main text unless the user specifies otherwise.
- 60–80 total verified citations.
- At least five distinct visualization/table types.
- All issues are `DONE` or explicitly `SKIP`.
