# Diagram Taxonomy

## ML/AI Repo

| Chapter | Figure Type | Source in Code |
|---|---|---|
| Introduction | teaser/problem-setting/contribution overview | README, examples, contribution bullets |
| Related Work | taxonomy tree, Venn, method comparison table | baselines, citations, competing methods |
| Method | system architecture | top-level modules and I/O |
| Method | module dependency graph | import graph |
| Method | data pipeline | Dataset/DataLoader/transforms |
| Method | model structure | model class `__init__` and `forward` |
| Method | training algorithm flowchart | training loop |
| Method | inference flowchart | `generate`, `predict`, or eval loop |
| Experiments | setup table, schedule, compute-quality plot | configs and logs |
| Results | ablation bar chart, curves, confusion matrix, heatmap, qualitative grid | eval logs and outputs |
| Discussion | failure-mode taxonomy | issues, TODOs, assertions, error handling |

## Frontend/Web Repo

| Chapter | Figure Type | Source in Code |
|---|---|---|
| Introduction | user journey/problem sketch | README and landing copy |
| Method/System | component tree | `src/components`, `app`, `pages` |
| Method/System | route graph | router, Next.js pages/app tree |
| Method/System | state flow | Redux/Zustand/Jotai/store slices |
| Method/System | API sequence | `fetch`, `axios`, tRPC, GraphQL, `useQuery` |
| Evaluation | web vitals/performance table or curve | measurement logs |

## Algorithm/Systems/Compiler Repo

| Chapter | Figure Type | Source in Code |
|---|---|---|
| Introduction | problem sketch | README |
| Method | IR/AST diagram | `enum Node`, AST classes, algebraic data types |
| Method | pass pipeline | pass list and visitor chain |
| Method | call graph/control-flow graph | function definitions and calls |
| Method | data-structure diagram | core structures |
| Method | algorithm pseudocode/flowchart | main function body |
| Experiments | benchmark setup | `bench`, `benchmark`, `criterion`, pytest-benchmark |
| Results | throughput/latency/scaling curves | benchmark logs |

## Typical Figure Count

A CS/AI thesis or paper often uses 8–12 figures total. If the proposed list exceeds 12, prune or merge into subfigures before drafting prompts.
