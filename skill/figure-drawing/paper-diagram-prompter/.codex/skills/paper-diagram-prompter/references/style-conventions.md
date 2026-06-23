# Style Conventions (AI/CS papers)

Applies to all three target tools (draw.io / Excalidraw / TikZ) unless a recipe says otherwise. These are the **single source of truth** for palette roles, stroke weights, and label rules — every cookbook must match.

## Palette (paper-safe pastels)

Chosen to survive B/W printing (distinguishable after desaturation) and to avoid the "default Keynote" look.

| Role | Fill (light) | Stroke (dark) | Semantic |
|---|---|---|---|
| Data / I/O | `#dae8fc` | `#6c8ebf` | Inputs, datasets, tensors on disk |
| Preprocessing | `#fff2cc` | `#d6b656` | Tokenizers, transforms, augmentation |
| Model / Compute | `#d5e8d4` | `#82b366` | Encoders, decoders, backbones, heads |
| Loss / Objective | `#ffe6cc` | `#d79b00` | Loss heads, regularizers |
| External system | `#f8cecc` | `#b85450` | APIs, remote services, databases |
| Meta / Grouping | `#f5f5f5` | `#666666` | Swimlane backgrounds, `fit` boxes |

Use **at most 4 role colors** per figure. If a figure needs more, it's probably two figures.

**Cross-tool color sanity**: the TikZ shorthand `blue!10` / `green!10` / `orange!18` targets the same visual weight as the hex codes above; stay consistent within one figure.

## Typography

- Figure labels: **sans-serif**, 9–11 pt equivalent. In TikZ: `\small` or `\footnotesize`.
- Math variables inside labels: italics, same size. In TikZ: `$h_t$`, `$\mathcal{L}$`.
- Captions: **main paper font** (serif for IEEEtran), one size down from body. Start with "Fig. N." and end with a period.
- Acronyms: spell out in caption, not in the figure. `Fig. 3. End-to-end pipeline. BN = BatchNorm; LN = LayerNorm.`

## Arrows

- **Data flow**: filled triangle head (`-Stealth` in TikZ, `endArrow=classic` in draw.io). Solid line.
- **Gradient / feedback**: same head, **dashed** line. Label as `∇` or `update`.
- **Imports / logical dependency** (not runtime flow): **open** head (`-{Latex[open]}` in TikZ, `endArrow=open` in draw.io). Dashed.
- **Optional path**: dotted line.

### Line weight across tools

Target paper line weight: **1.2–1.6 pt**. Each tool discretizes differently:

| Tool | Setting | Actual weight (at default DPI) |
|---|---|---|
| TikZ | `thick` (default in our recipes) | ≈ 1.2 pt |
| TikZ | `very thick` | ≈ 1.6 pt |
| draw.io | `strokeWidth=1` (default) | 1 pt |
| draw.io | `strokeWidth=2` | 2 pt (use for emphasis only) |
| Excalidraw | `strokeWidth=1` | ≈ 1 pt |
| Excalidraw | `strokeWidth=2` (default in our recipes) | ≈ 1.6 pt |
| Excalidraw | `strokeWidth=4` | too heavy; avoid for body figures |

Thicker looks childish; thinner vanishes at print.

## Spacing & alignment

- Grid: use multiples of 20 px in draw.io / Excalidraw. Matches TikZ `node distance=8mm` at default DPI.
- Minimum gutter between nodes: one node-width.
- Align nodes on **columns or rows**, never both free-floating. Tools offer distribute-evenly — use it.

## Aspect ratio targets

| Figure type | Target ratio | Reason |
|---|---|---|
| System architecture | 16:9 landscape | One-column or subfigure slot |
| Model stack | 2:3 portrait | Fits alongside text column |
| Pipeline / swimlane | 16:9 | Columns span well |
| Concept / motivation | 3:2 | Generous negative space |
| Chart / plot | 4:3 or 3:2 | Readable gridlines |
| Algorithm flowchart | 2:3 | Vertical flow, fits column |
| Confusion matrix / heatmap | 1:1 | Cell legibility |

## What to avoid (paper reviewers will dock points)

- **Gradients as fills** — looks like a poster, not a paper.
- **3D extrusion / drop shadows on blocks** — distracts; a subtle shadow only on grouping boxes, if at all.
- **Rainbow of colors** — hurts B/W legibility.
- **Emoji or clip-art icons** — breaks formality. *Exception*: a single `\faIcon{}` (font-awesome) per figure is acceptable in Excalidraw / draw.io intro figures.
- **Unlabeled arrows in method figures** — every arrow carries semantics; label the non-obvious ones.
- **Mixed fonts** — pick one sans for the figure; inherit the paper serif for the caption.

## Bilingual (Chinese + English) label rules — opt-in

Bilingual labels are **off by default**; enable only when the user asks or the target venue is a Chinese thesis (毕业设计 / 校内评审).

Format:
```
Primary label (EN, normal size)
次要标签 (CN, 70% size, same color, directly below)
```

### Compilation requirements (bilingual)

- **TikZ**: switch from `pdflatex` to **XeLaTeX** or **LuaLaTeX**; add `\usepackage{xeCJK}` + `\setCJKmainfont{<CJK font>}` — see [tikz-cookbook.md](tikz-cookbook.md) §Bilingual labels.
- **draw.io**: no extra setup; label syntax is `value="&lt;b&gt;Encoder&lt;/b&gt;&lt;br/&gt;&lt;font size='10'&gt;编码器&lt;/font&gt;"` (HTML-escaped).
- **Excalidraw**: no extra setup; descriptor uses `label="Encoder\n编码器"` (literal `\n` in the text).

## Captioning templates

- Architecture: *"Fig. N. Overall architecture of <method>. <Short phrase on data flow>."*
- Model: *"Fig. N. Model structure. <dim specifics>."*
- Pipeline: *"Fig. N. Training / inference pipeline. Stages on <CPU|GPU>."*
- Algorithm: *"Fig. N. <Algorithm name> main loop. Dashed edge denotes the convergence check."*
- Ablation: *"Fig. N. Ablation of <component list>. Error bars over N=<k> seeds."*
- Curve: *"Fig. N. Validation <metric> across epochs. Solid: ours. Dashed: baseline."*
- Confusion matrix: *"Fig. N. Confusion matrix on <dataset>. Rows: ground truth; columns: predictions."*
- Embedding scatter: *"Fig. N. <t-SNE|UMAP> projection of <layer> activations on <dataset>. Colors encode class."*

## Accessibility

- Contrast ≥ 4.5:1 between stroke and fill.
- Do not rely on color alone — also use line style (solid/dashed/dotted) or shape.
- Avoid red/green-only distinctions (color-blindness); pair with orange/blue from the palette above.
