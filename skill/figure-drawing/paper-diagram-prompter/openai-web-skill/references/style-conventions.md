# Style Conventions

## Palette

| Role | Fill | Stroke | Semantic |
|---|---|---|---|
| Data / I/O | `#dae8fc` | `#6c8ebf` | inputs, datasets, tensors on disk |
| Preprocessing | `#fff2cc` | `#d6b656` | tokenizers, transforms, augmentation |
| Model / Compute | `#d5e8d4` | `#82b366` | encoders, decoders, backbones, heads |
| Loss / Objective | `#ffe6cc` | `#d79b00` | loss heads and regularizers |
| External System | `#f8cecc` | `#b85450` | APIs, remote services, databases |
| Meta / Grouping | `#f5f5f5` | `#666666` | swimlanes, fit boxes, grouping backgrounds |

Use at most four role colors per figure.

## Typography

- Figure labels: sans-serif, about 9–11 pt; in TikZ use `\small` or `\footnotesize`.
- Math variables: italic math, e.g. `$h_t$`, `$\mathcal{L}$`.
- Captions: main paper font; define acronyms in the caption, not inside the figure.

## Arrows

- Data flow: solid filled triangle arrow.
- Gradient/feedback: dashed filled triangle arrow, label `update` or `∇`.
- Imports/logical dependency: dashed open-head arrow.
- Optional path: dotted line.

## Aspect Ratios

- System architecture: 16:9 landscape.
- Model stack: 2:3 portrait.
- Pipeline/swimlane: 16:9.
- Concept/motivation: 3:2.
- Chart/plot: 4:3 or 3:2.
- Algorithm flowchart: 2:3.
- Heatmap/confusion matrix: 1:1.

## Bilingual Labels

Default is English only. Add Chinese labels only when requested. For TikZ bilingual labels, use XeLaTeX or LuaLaTeX with `xeCJK` and an installed CJK font.

## Caption Templates

- Architecture: `Fig. N. Overall architecture of <method>. <short data-flow note>.`
- Model: `Fig. N. Model structure. <dimension specifics>.`
- Pipeline: `Fig. N. Training/inference pipeline. Stages run on <CPU/GPU/etc.>.`
- Algorithm: `Fig. N. <algorithm> main loop. Dashed edge denotes <condition>.`
- Ablation: `Fig. N. Ablation of <components>. Error bars over N=<k> seeds.`
- Curve: `Fig. N. Validation <metric> across epochs. Solid: ours. Dashed: baseline.`
