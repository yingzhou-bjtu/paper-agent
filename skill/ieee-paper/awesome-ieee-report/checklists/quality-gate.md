# Quality Gate Checklist

Run this loop before finalizing report outputs.

## Checklist

- [ ] Required sections are present and in order (from requirement document or standard IEEE baseline).
- [ ] **ZERO code artifacts**: No file paths, class names, function names, variable names, directory structures, or source file extensions anywhere in the report body.
- [ ] All technical claims describe systems, algorithms, and mechanisms in academic prose — not implementation code.
- [ ] Vocabulary uses domain terms (algorithm, module, layer, mechanism, component) NOT code terms (Controller, Repository, Widget, Service).
- [ ] At least 3 figure entries are present as labeled placeholders with capture intent.
- [ ] Each placeholder figure has: label, caption, and description of what should be captured.
- [ ] Core algorithmic flows use IEEE `algorithm` environment with pseudocode — no raw code blocks.
- [ ] All external references use `\cite{}` with matching BibTeX entries.
- [ ] Requirement/assignment document is used for coverage control only and is not automatically included in the bibliography.
- [ ] Report prose is an original academic synthesis and does not track the wording or framing of the assignment handout too closely.
- [ ] Dense enumerations and repeated option sets are reviewed for possible table conversion where this improves two-column readability.
- [ ] Large figures/tables are not stacked in a way that creates obvious white-space holes before the next subsection.
- [ ] Test/evaluation section describes tested BEHAVIORS, not test file names or commands.
- [ ] Report language matches the user's preference throughout.
- [ ] Report reads as a self-contained academic paper — understandable without seeing the codebase.
- [ ] Report is substantive enough to fill at least 4 pages in IEEE two-column format when compiled. (Verify after LaTeX compilation — cannot be confirmed from source alone.)

## Feedback Loop

1. Run checklist.
2. If any item fails, fix content.
3. Re-run checklist.
4. Finalize only when all items pass.

## Fast Failure Rules

Reject draft as incomplete if any condition is true:
- Any file path or code identifier appears in the report body
- Fewer than 3 figure placeholders
- Missing evaluation/results section
- Missing architecture/methodology section
- Raw source code block in any section
