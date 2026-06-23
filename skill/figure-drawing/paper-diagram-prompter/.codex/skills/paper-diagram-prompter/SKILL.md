---
name: paper-diagram-prompter
description: Extract figures-worthy artifacts (architecture, module graph, data pipeline, training/inference loop, model structure, ablation results) from a source codebase and emit ready-to-paste prompts or source for draw.io (mxGraph XML), Excalidraw (scene descriptor / Mermaid fallback), and TikZ (LaTeX source). Use ONLY for paper figures and diagrams — thesis (毕业设计), ML/AI conference/journal paper, arXiv preprint, system-design writeup. Output is prompt / source text only; the skill never renders, compiles, exports, or invokes any image / AI-diagram plugin itself. Pair with `arxiv-paper-writer` when you also need manuscript drafting, citation work, or full paper scaffolding — this skill stays strictly in the figure lane.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Paper Diagram Prompter

Turns a source codebase into a full set of **paper-ready figure prompts** for draw.io, Excalidraw, and TikZ. Optimized for AI / CS theses and ML/AI papers, with graceful degradation for non-ML CS repos (frontend apps, algorithms, compilers, systems).

## When to use

- User says: "帮我画架构图 / 画模型结构 / 出毕业设计的图 / 给我论文配图的 prompt".
- User points at a repo and wants figures for: system overview, module dependency, data pipeline, training loop, inference loop, model internals, ablation comparison, confusion matrix, t-SNE/UMAP embedding, PR/ROC curve, compute-vs-quality Pareto.
- User is writing a LaTeX paper (IEEEtran / arXiv) and needs **LaTeX-embeddable** TikZ source or editor-pastable prompts.

## When NOT to use

- User asks to **render** a real PNG/SVG/PDF, or to call DALL·E / Imagen / Excalidraw-AI / draw.io export. This skill is text-only; actual rendering is the user's job.
- User wants to **draft prose, manage citations, or scaffold a full LaTeX project** — delegate to `arxiv-paper-writer` or `latex-rhythm-refiner`.
- User has no code to scan and only wants a hand-drawn concept sketch — use a general design skill instead.
- Repo is non-technical (marketing, docs only) — the value of code-driven extraction collapses.

## Inputs

- **Required**: path to a source codebase (default: current working directory).
- **Optional**: paper chapter list (defaults to: Introduction, Related Work, Method, Experiments, Results, Discussion); target tool subset (`drawio` / `excalidraw` / `tikz` — default: all three); language (default: match user's language; bilingual CN+EN only on explicit request).

## Outputs

A single Markdown report containing, **per figure**:

1. **Figure ID + Caption** (ready for `\caption{}`).
2. **Chapter placement** and rationale.
3. **Design notes**: visual hierarchy, palette role mapping, aspect ratio, layer order.
4. **Three parallel prompts**:
   - `drawio`: complete `<mxfile>` document (paste-ready) or structured natural-language description when the XML would exceed ~150 lines or ~30 nodes.
   - `excalidraw`: scene descriptor with explicit coordinates, **or** a Mermaid flowchart snippet (for the built-in *Mermaid to Excalidraw* converter).
   - `tikz`: compilable LaTeX source using only the packages listed in [tikz-cookbook.md](references/tikz-cookbook.md).
5. **How to paste**: concrete, tool-specific paste steps.

## Workflow

### Phase A — Scan (read-only)

1. **Stack & workspace detection** (first, cheap):
   - `Read` of `README*`, `pyproject.toml` / `package.json` / `go.mod` / `Cargo.toml` / `requirements.txt`, and — for monorepos — `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, or the `workspaces` field.
   - If a monorepo is detected, treat each package as a mini-repo: scan 1–3 representative files per package before descending.
2. **File inventory**: `Glob "**/*.{py,ts,tsx,js,jsx,go,rs,cpp,h,java,kt,swift,md,yaml,toml,json}"`.
3. **Entry points**: `Grep` for `if __name__ == "__main__"`, `def main`, `fn main`, `func main`, `export default`, `app.listen`, `@click.command`, `@app.command`.
4. **Extract architecture signals — pick the branch that matches the repo type**:

   **B1 — ML/AI repo** (trigger: PyTorch/TF imports, `nn.Module`, `Trainer`, `Dataset`):
   - Model blocks: `Grep` for `class .*(nn\.Module|Module|tf\.keras\.Model|torch\.nn)`; read `__init__` + `forward`.
   - Data pipeline: `Grep` for `Dataset`, `DataLoader`, `collate_fn`, `tf.data`, `load_dataset`, `.map(`, `.filter(`, `.batch(`.
   - Training loop: `Grep` for `optimizer`, `loss.backward`, `.step()`, `trainer.train`, `accelerator`.
   - Inference: `Grep` for `@torch\.no_grad`, `model.eval`, `generate(`, `predict(`.

   **B2 — Frontend / web repo** (trigger: React/Vue/Svelte imports, `src/main.tsx`, Vite/Next config):
   - Route tree: `Grep` for `createBrowserRouter`, `<Route`, `pages/`, `app/` (Next.js).
   - State store: `Grep` for `createStore`, `atom(`, `useStore`, `Provider`, `Redux`, `zustand`, `jotai`.
   - API client: `Grep` for `fetch(`, `axios`, `useQuery`, `trpc`, `graphql`.
   - Component tree: largest-by-LOC component files under `src/components` or `app/`.

   **B3 — Algorithm / systems / compiler repo** (trigger: no ML and no frontend):
   - Call graph / pass pipeline: `Grep` for `Pass`, `Visitor`, `pipeline`, `stage`.
   - IR / AST types: `Grep` for `enum .*Node`, `class .*AST`, algebraic-data-type definitions.
   - Benchmark harness: look for `bench/`, `benchmarks/`, `criterion`, `pytest-benchmark`.

   In all branches also record: **import graph** (`Grep -n "^(import|from|require|use) "`) and **config surface** (`argparse`, `hydra`, `OmegaConf`, `pydantic.BaseSettings`, `.env`, `*.toml` keys).

5. **Bound the scan** to ~15 representative files OR ~30 s of investigation — goal is architectural signal, not exhaustive reading. Largest-by-LOC subtrees and documented entry points first. **If no README exists**, fall back to: package metadata description, CLI `--help` output (via `Bash`), top-of-file comments, and test names as motivation proxies.

### Phase B — Classify (assign figures to chapters)

Open [diagram-taxonomy.md](references/diagram-taxonomy.md). Pick the taxonomy that matches the repo type (ML, frontend, or algorithm/systems). Produce a plain list:

```
F1. <title> (chapter X, figure type Y, driven by <source in code>)
F2. ...
```

If > 8 figures are proposed, present the list and **pause** for confirmation before drafting prompts. If ≤ 8, proceed directly.

### Phase C — Draft prompts

For each approved figure, load the relevant cookbook entry:
- [drawio-cookbook.md](references/drawio-cookbook.md) — pick matching recipe (system-architecture, module-graph, pipeline, flowchart, …).
- [excalidraw-cookbook.md](references/excalidraw-cookbook.md) — matching hand-drawn recipe, **or** Mermaid fallback.
- [tikz-cookbook.md](references/tikz-cookbook.md) — matching LaTeX recipe.
- [style-conventions.md](references/style-conventions.md) — apply palette role mapping / typography / aspect-ratio defaults.

Fill the recipe with data harvested in Phase A.

**Label language — strict defaults**:
- Default labels: **English only** (works with `pdflatex` and the bare preamble).
- Add Chinese second-line labels **only when the user explicitly asks for 双语 / bilingual / 中文** — and always warn that bilingual TikZ requires switching to **XeLaTeX / LuaLaTeX + xeCJK** (see `tikz-cookbook.md` §Bilingual labels).

**Fallback rules (deterministic)**:
- draw.io: emit full `<mxfile>` XML when the figure has **≤ 30 nodes AND would produce ≤ 150 lines**; otherwise emit the NL fallback format defined in the cookbook.
- Excalidraw: emit **scene descriptor** by default; emit **Mermaid flowchart** instead when the figure is a pure dependency graph, flowchart, or state machine — Excalidraw has a built-in *Mermaid to Excalidraw* converter.
- TikZ: never fall back — always emit compilable source. If it exceeds ~80 lines, split into sub-tikzpictures using `\subfloat`.

### Phase D — Assemble report

Print the report inline by default. **Only when the user explicitly asks to save**, write it to `diagrams/<YYYY-MM-DD>-<project-slug>-prompts.md` (slug derives from the scanned repo's basename; if the file already exists append `-v2`, `-v3`, …). Structure:

```markdown
# Figure Prompts — <project name>

## F1. <Caption> — Ch.<n>
**Design notes**: <palette role mapping, layout, aspect ratio>
### draw.io
<xml or NL description>
### Excalidraw
<scene descriptor or Mermaid snippet>
### TikZ
```latex
<compilable snippet>
```
**Paste instructions**: <per-tool paste steps>
---
## F2. …
```

### Phase E — Self-audit

Before returning, verify for every figure:
- [ ] TikZ snippet uses only the whitelisted packages declared in [tikz-cookbook.md](references/tikz-cookbook.md); math macros (`\mathbb`, `\mathcal`, `\vec`) have matching `\usepackage{amsmath, amsfonts, amssymb}` in the declared preamble.
- [ ] draw.io XML is a complete `<mxfile><diagram><mxGraphModel><root>…</root></mxGraphModel></diagram></mxfile>`; `<root>` contains `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`; every other cell has `parent="1"`; all embedded HTML in `value="…"` is entity-escaped (`&lt;b&gt;`, `&lt;br/&gt;`); every edge cell has a `<mxGeometry relative="1" as="geometry"/>` child.
- [ ] Excalidraw descriptor lists: node labels, shapes, `(x,y)` of **top-left corner in pixels**, size in pixels, edge list with arrow direction, `roughness` hint. Mermaid fallback, when used, parses under `graph TD` / `graph LR` / `stateDiagram-v2`.
- [ ] Palette role mapping matches [style-conventions.md](references/style-conventions.md): **Data = blue, Model = green, Loss = orange, Preprocess = yellow, External = red, Meta = gray.**
- [ ] No figure claims a feature absent from the scanned code.
- [ ] Every in-figure acronym is defined in the caption.

## Output contract (strict)

- **Never** invoke any renderer, compiler, exporter, headless browser, DALL·E / Imagen / Excalidraw-AI plugin, or MCP image tool — even if asked. If the user requests rendering, politely emit the source and instruct them to paste.
- **Never** fabricate modules, layers, or metrics. If the code lacks signal, mark the figure "schematic / illustrative" in the caption.
- **Always** emit all three target formats for every figure unless the user restricts the target set.
- **Always** keep TikZ snippets self-contained (no `\input{}` to unknown files) and under the declared package whitelist.

## Safety & guardrails

- Read-only on the scanned codebase; never modify source files during Phase A–C.
- The only write is the optional report file under `diagrams/` (and only when explicitly asked).
- Skip files matching `*.env`, `*.env.*`, `secrets.*`, `*.pem`, `*.p12`, `id_rsa*`; log the skip in the report.
- `Bash` is permitted only for deterministic reads (e.g., `cat --help`, `ls`, running the skill's own report-writing step). **Never** use it to shell out to renderers (`pdflatex`, `draw.io`, `chromium`, `playwright`).

## References

- [Diagram taxonomy & chapter map](references/diagram-taxonomy.md)
- [draw.io cookbook](references/drawio-cookbook.md)
- [Excalidraw cookbook](references/excalidraw-cookbook.md)
- [TikZ cookbook](references/tikz-cookbook.md)
- [Style conventions (palette / typography / aspect)](references/style-conventions.md)
