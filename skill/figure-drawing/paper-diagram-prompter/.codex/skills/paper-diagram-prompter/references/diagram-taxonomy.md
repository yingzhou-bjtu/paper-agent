# Diagram Taxonomy & Chapter Map

Map of paper chapters → figure types → where to mine the content from the codebase. Covers three repo archetypes: **ML/AI**, **frontend/web app**, and **algorithm/systems/compiler**.

## Chapter → figure matrix (ML/AI repo)

| Chapter | Figure type | Purpose | Source in code |
|---|---|---|---|
| Abstract (optional) | Teaser figure | Capture the contribution in one picture | Key input/output pair from README or `examples/` |
| 1. Introduction | Problem-setting diagram | Explain the gap being closed | Motivation prose in README; problem classes in docstrings |
| 1. Introduction | Contribution overview | Visual list of "we do A, B, C" | README "contributions" bullets |
| 2. Related Work | Taxonomy tree / Venn | Position vs prior art | Citations, baselines under `baselines/`, `competing_methods/` |
| 2. Related Work | Method comparison table | Feature matrix of methods | Hand-authored; infer feature rows from code capabilities |
| 3. Method | System architecture | End-to-end block diagram | Top-level modules + their I/O |
| 3. Method | Module dependency graph | Which module imports which | Import graph from Phase A scan |
| 3. Method | Data pipeline | Raw → preprocessing → batch → model | `Dataset` subclasses + transforms |
| 3. Method | Model structure | Layer-by-layer view | `nn.Module.__init__` + `forward` |
| 3. Method | Computation graph | Forward & backward pass | Autograd graph (schematic) |
| 3. Method | Training algorithm flowchart | Loop body + branches | `train()` function body |
| 3. Method | Inference / decoding flowchart | Autoregressive or single-pass | `generate()` / `predict()` |
| 3. Method | Loss landscape / objective | Composite losses shown as a sum | Loss class hierarchy |
| 4. Experiments | Experimental setup | Hardware + dataset + baseline grid | `configs/*.yaml`, `README` |
| 4. Experiments | Training schedule | LR / batch / epochs timeline | Scheduler config |
| 4. Experiments | Compute-vs-quality Pareto | Efficiency trade-off | Model size × accuracy logs |
| 5. Results | Ablation bar chart | Effect of each component | Experiment table |
| 5. Results | Metric curve (schematic/real) | Convergence | Training logs |
| 5. Results | **Confusion matrix** | Per-class diagnostics | Eval dump + `sklearn.metrics.confusion_matrix` |
| 5. Results | **Embedding scatter (t-SNE / UMAP)** | Cluster visualization | Hidden-state dumps |
| 5. Results | **PR / ROC curve** | Classifier quality | Eval logs |
| 5. Results | Attention heatmap | Interpretability | Attention weight dump |
| 5. Results | Qualitative grid | Side-by-side outputs | Samples in `outputs/` |
| 6. Discussion | Failure-mode taxonomy | Where it breaks | Issue tracker, `TODO`s, assert() failures |

## Chapter → figure matrix (frontend / web repo)

| Chapter | Figure type | Source in code |
|---|---|---|
| 1. Introduction | User journey / problem sketch | README, landing-page copy |
| 3. Method / System | **Component tree** | `src/components/` hierarchy |
| 3. Method / System | **Route graph** | `createBrowserRouter` / `pages/` / `app/` |
| 3. Method / System | **State flow** (Redux/Zustand/etc.) | Store slices + reducers |
| 3. Method / System | **API call sequence** | `useQuery`, `fetch`, tRPC routes |
| 3. Method / System | Rendering pipeline | SSR/SSG/ISR config, hydration boundary |
| 4. Experiments / Eval | Lighthouse / Web Vitals table | Measurement logs |
| 5. Results | Perf curve (LCP, TTI, bundle size) | Log summaries |

## Chapter → figure matrix (algorithm / systems / compiler repo)

| Chapter | Figure type | Source in code |
|---|---|---|
| 1. Introduction | Problem sketch | README |
| 3. Method | **IR / AST diagram** | `enum Node` / `class .*AST` |
| 3. Method | **Pass pipeline** | Pass list, visitor chain |
| 3. Method | **Call graph / control-flow graph** | Function definitions + calls |
| 3. Method | Data-structure diagram | Hash table, trie, graph, queue layouts |
| 3. Method | Algorithm pseudocode + flowchart | Main function body |
| 4. Experiments | Benchmark setup | `bench/`, `criterion` config |
| 5. Results | Throughput / latency curves | Benchmark logs |
| 5. Results | Scaling plots | Input-size × runtime |

## AI/CS figure vocabulary (what we actually draw)

- **Block diagram**: rectangles as modules, directed arrows as data/control flow. System architecture.
- **Stacked layer diagram**: vertical stack for deep nets. Color-code by layer family (conv/attention/norm).
- **Swimlane**: horizontal lanes for parallel actors (CPU/GPU, sync/async, client/server).
- **State machine**: nodes as states, edges as transitions. Decoding strategies, task phases, protocol FSMs.
- **Tree**: taxonomy (Related Work), ablation design space, AST, search/beam decoding.
- **Grid**: N×M miniatures for qualitative sample comparison.
- **Pgfplots chart**: bar, line, scatter. Preferred over raster for arXiv.
- **Heatmap**: 2D grid colored by value. Attention, confusion matrix, pairwise similarity.
- **Embedding scatter**: 2-D projection (t-SNE / UMAP / PCA). Clusters, class separability.
- **PR / ROC curve**: classifier quality, usually with baselines overlaid.
- **Pareto front**: compute vs quality; annotate a "knee" point.

## Label policy

- Default: **English only** — compiles with `pdflatex` and the declared minimal preamble.
- Bilingual (中英双语) only when user explicitly asks. Bilingual TikZ requires XeLaTeX / LuaLaTeX + xeCJK; the cookbook files document the exact switch.
- Keep labels ≤ 4 Chinese chars or ≤ 3 English words. Spell out acronyms in the caption, not in the figure.

## Figure count guidance (typical AI/CS thesis)

| Section | # figures |
|---|---|
| Introduction | 1–2 |
| Related Work | 0–1 |
| Method | 3–5 (architecture + model + pipeline + optional algorithm) |
| Experiments | 1–2 |
| Results | 2–4 (curves + ablation + confusion matrix or qualitative) |
| **Total** | **8–12** |

If the proposed list exceeds 12, prune before drafting prompts — ask the user which can be merged into subfigures.
