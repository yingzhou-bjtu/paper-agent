# Diagram Workflow

## Inputs

- Required: path to a source codebase or a repository description.
- Optional: paper chapter list, target tool subset (`drawio`, `excalidraw`, `tikz`), desired figure count, language, and whether to save the report.

## Outputs

A Markdown report with one section per figure:

1. figure ID and caption,
2. chapter placement and rationale,
3. design notes,
4. draw.io XML or structured fallback,
5. Excalidraw scene descriptor or Mermaid snippet,
6. compilable TikZ source,
7. paste instructions.

## Phase A — Read-Only Scan

Bound the scan to representative files and architectural signal, not exhaustive reading.

1. Read `README*`, package metadata, and workspace files.
2. Inventory relevant source files: Python, TypeScript, JavaScript, Go, Rust, C/C++, Java, Kotlin, Swift, Markdown, YAML, TOML, and JSON.
3. Find entry points such as `main`, CLI commands, app/router initialization, or exported app components.
4. Classify the repo:
   - ML/AI: PyTorch/TensorFlow imports, `nn.Module`, `Dataset`, `Trainer`, training/inference loops.
   - frontend/web: React/Vue/Svelte/Next/Vite, routes, components, state stores, API clients.
   - algorithm/systems/compiler: passes, visitors, AST/IR types, benchmark harnesses, pipeline/stage concepts.
5. Record import graph and configuration surface.
6. Skip secrets: `.env*`, `secrets.*`, private keys, certificates, and credentials.

## Phase B — Classify Figures

Load `diagram-taxonomy.md`. Produce a list like:

```text
F1. system architecture (method section, driven by src/model.py and train.py)
F2. data pipeline (method section, driven by dataset.py)
```

If more than eight figures are proposed, pause for confirmation. If eight or fewer, proceed directly unless the user asked to choose.

## Phase C — Draft Prompts

Use the cookbooks:

- draw.io: `drawio-cookbook.md`
- Excalidraw: `excalidraw-cookbook.md`
- TikZ: `tikz-cookbook.md`
- style: `style-conventions.md`

Default labels are English only. Use bilingual labels only on explicit request and warn about XeLaTeX/LuaLaTeX for TikZ.

Fallback rules:

- draw.io: full XML for small figures; structured natural-language fallback if over 30 nodes or about 150 XML lines.
- Excalidraw: scene descriptor by default; Mermaid for dependency graphs, flowcharts, and state machines.
- TikZ: always provide self-contained source using the cookbook whitelist.

## Phase D — Assemble Report

Default to inline output. Save to `diagrams/<date>-<project-slug>-prompts.md` only when explicitly requested.

## Phase E — Self-Audit

Before returning:

- TikZ uses only whitelisted packages and every referenced node/style exists.
- draw.io XML is a complete `<mxfile>` with valid root cells and escaped HTML.
- Excalidraw descriptors include coordinates, sizes, edges, arrow directions, and roughness hints.
- Palette follows `style-conventions.md`.
- Captions define acronyms.
- No feature is claimed unless present in the scanned code or marked illustrative.

## Guardrails

- Do not render, compile, export, or call image tools as part of this workflow.
- Do not modify the scanned repo.
- The only optional write is the diagram report file under `diagrams/` when requested.
