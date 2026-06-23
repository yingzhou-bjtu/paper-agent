# TikZ Cookbook

TikZ produces **vector figures that live natively inside LaTeX** — preferred for camera-ready submissions. All snippets below use **only** the packages and libraries in the following whitelist. Copy the whole block into your preamble (or add only the missing lines).

```latex
\usepackage{amsmath, amsfonts, amssymb}   % \mathbb, \mathcal, \vec
\usepackage{tikz}
\usetikzlibrary{positioning, arrows.meta, fit,
                shapes.geometric, shapes.misc, calc, matrix, shadows}
\usepackage{pgfplots}
\usepgfplotslibrary{colormaps}            % needed for colormap/viridis etc.
\pgfplotsset{compat=1.18}
```

**Compilation engine**:
- **English-only labels** (default Recipes 1–7): `pdflatex` is sufficient.
- **Bilingual (CN+EN) labels** (opt-in, §Bilingual labels below): switch to **XeLaTeX** or **LuaLaTeX** and add `\usepackage{xeCJK}` + `\setCJKmainfont{<an installed CJK font>}` (e.g. `Noto Serif CJK SC`, `SimSun`, `STSong`).

Every snippet is drop-in; wrap inside a `figure` float:

```latex
\begin{figure}[t]
  \centering
  \resizebox{\columnwidth}{!}{%
    <<SNIPPET>>
  }
  \caption{...}\label{fig:...}
\end{figure}
```

Use `\textwidth` and `figure*` for two-column spanning figures.

---

## Recipe 1 — System architecture (block diagram)

Palette roles follow [style-conventions.md](style-conventions.md): `data` = blue, `mod` = green, `loss` = orange.

```latex
\begin{tikzpicture}[
  node distance=8mm and 10mm,
  every node/.style={font=\small},
  data/.style={draw, rounded corners=2pt, align=center, minimum height=10mm, minimum width=18mm, fill=blue!10, thick},
  mod/.style ={draw, rounded corners=2pt, align=center, minimum height=10mm, minimum width=18mm, fill=green!10, thick},
  loss/.style={draw, rounded corners=2pt, align=center, minimum height=10mm, minimum width=18mm, fill=orange!18, thick},
  arr/.style ={-Stealth, thick}
]
  \node[data]                  (load) {Data Loader};
  \node[mod,  right=of load]   (enc)  {Encoder};
  \node[mod,  right=of enc]    (dec)  {Decoder};
  \node[loss, right=of dec]    (l)    {Loss};

  \draw[arr] (load) -- (enc);
  \draw[arr] (enc)  -- (dec) node[midway, above, font=\scriptsize] {$h_t$};
  \draw[arr] (dec)  -- (l);

  \node[draw, dashed, fit=(enc) (dec), inner sep=4pt,
        label=above:{\scriptsize Model}] {};
\end{tikzpicture}
```

---

## Recipe 2 — Model structure (vertical layer stack)

```latex
\begin{tikzpicture}[
  layer/.style={draw, rounded corners=2pt, minimum width=40mm, minimum height=7mm, align=center, font=\small},
  inp/.style  ={layer, fill=gray!10},
  lin/.style  ={layer, fill=blue!10},
  norm/.style ={layer, fill=violet!12},
  block/.style={layer, fill=green!12, minimum height=10mm},
  head/.style ={layer, fill=orange!15},
  out/.style  ={layer, fill=gray!10},
  arr/.style  ={-Stealth}
]
  \node[inp]                              (x)  {Input  $x \in \mathbb{R}^{B\times D}$};
  \node[lin,   below=3mm of x]            (l1) {Linear  $D \to H$};
  \node[norm,  below=3mm of l1]           (n1) {LayerNorm};
  \node[block, below=3mm of n1]           (tb) {$\times N$  Transformer Blocks};
  \node[head,  below=3mm of tb]           (h1) {MLP Head  $H \to C$};
  \node[out,   below=3mm of h1]           (y)  {Output  $\hat{y} \in \mathbb{R}^{B\times C}$};

  \draw[arr] (x)  -- (l1);
  \draw[arr] (l1) -- (n1);
  \draw[arr] (n1) -- (tb);
  \draw[arr] (tb) -- (h1);
  \draw[arr] (h1) -- (y);
\end{tikzpicture}
```

---

## Recipe 3 — Data pipeline (horizontal swimlane)

```latex
\begin{tikzpicture}[
  node distance=6mm and 8mm,
  stage/.style={draw, rounded corners=2pt, minimum height=8mm, minimum width=22mm, align=center, font=\small},
  lane/.style ={draw=gray!60, dashed, inner sep=3mm},
  arr/.style  ={-Stealth}
]
  \node[stage, fill=yellow!10] (r)  {Raw};
  \node[stage, fill=yellow!10, right=of r]  (t)  {Tokenize};
  \node[stage, fill=yellow!10, right=of t]  (b)  {Batch};
  \node[lane, fit=(r) (t) (b), label=left:{\scriptsize CPU}] (cpu) {};

  \node[stage, fill=blue!10,   below=15mm of r]   (m)  {Model};
  \node[stage, fill=orange!12, right=of m]        (l)  {Loss};
  \node[stage, fill=blue!10,   right=of l]        (o)  {Optim};
  \node[lane, fit=(m) (l) (o), label=left:{\scriptsize GPU}] (gpu) {};

  \draw[arr] (r) -- (t);
  \draw[arr] (t) -- (b);
  \draw[arr] (b) -- (m);
  \draw[arr] (m) -- (l);
  \draw[arr] (l) -- (o);
  \draw[arr] (o.north) |- ++(0,5mm) -| (m.north)
        node[near start, above, font=\scriptsize] {update};
\end{tikzpicture}
```

---

## Recipe 4 — Algorithm flowchart

The `rounded rectangle` shape used for the start/end pill requires `\usetikzlibrary{shapes.misc}` (already in the whitelist above).

```latex
\begin{tikzpicture}[
  node distance=7mm,
  start/.style ={draw, rounded rectangle, fill=black, text=white, minimum width=16mm},
  proc/.style  ={draw, rounded corners=2pt, minimum width=36mm, minimum height=8mm, align=center, font=\small},
  dec/.style   ={draw, diamond, aspect=2, minimum width=30mm, align=center, font=\small\itshape},
  arr/.style   ={-Stealth, thick}
]
  \node[start]                         (s)  {Start};
  \node[proc,  below=of s]             (p1) {Sample mini-batch};
  \node[proc,  below=of p1]            (p2) {Forward + Loss $\mathcal{L}$};
  \node[proc,  below=of p2]            (p3) {Backward + Step};
  \node[dec,   below=of p3]            (d1) {converged?};
  \node[start, below=of d1]            (e)  {End};

  \draw[arr] (s)  -- (p1);
  \draw[arr] (p1) -- (p2);
  \draw[arr] (p2) -- (p3);
  \draw[arr] (p3) -- (d1);
  \draw[arr] (d1) -- node[right]{yes} (e);
  \draw[arr] (d1.west) -| ++(-20mm,0) |- (p1.west)
        node[pos=0.25, left, font=\scriptsize]{no};
\end{tikzpicture}
```

---

## Recipe 5 — Ablation bar chart

```latex
\begin{tikzpicture}
  \begin{axis}[
    ybar, width=0.95\columnwidth, height=45mm,
    bar width=6mm, enlarge x limits=0.18,
    ylabel={Accuracy (\%)},
    symbolic x coords={Full, -A, -B, -C, Base},
    xtick=data, ymin=70, ymax=92,
    nodes near coords, nodes near coords style={font=\scriptsize},
    legend style={font=\scriptsize, at={(1,1)}, anchor=north east},
  ]
    \addplot coordinates {(Full,89.4) (-A,86.1) (-B,84.7) (-C,82.3) (Base,75.0)};
    \legend{Ours}
  \end{axis}
\end{tikzpicture}
```

---

## Recipe 6 — Attention / confusion-matrix heatmap

pgfplots needs one `(x y v)` record per physical line for `matrix plot`; cramming multiple records per line yields malformed input. `colormap/viridis` needs `\usepgfplotslibrary{colormaps}` (already in the whitelist).

```latex
\begin{tikzpicture}
  \begin{axis}[
    width=0.9\columnwidth, height=0.9\columnwidth,
    enlargelimits=false, axis on top,
    xlabel={Key position}, ylabel={Query position},
    colorbar, colormap/viridis,
    point meta min=0, point meta max=1,
  ]
    \addplot[matrix plot, mesh/cols=4, point meta=explicit] table[meta=v]{
      x y v
      0 0 0.9
      1 0 0.1
      2 0 0.0
      3 0 0.0
      0 1 0.2
      1 1 0.6
      2 1 0.2
      3 1 0.0
      0 2 0.1
      1 2 0.3
      2 2 0.5
      3 2 0.1
      0 3 0.0
      1 3 0.1
      2 3 0.2
      3 3 0.7
    };
  \end{axis}
\end{tikzpicture}
```

For real attention / confusion data, replace the inline `table{...}` with `table{data.dat};` pointing at a whitespace-separated file with the same `x y v` schema.

---

## Recipe 7 — Metric curve (schematic or real)

```latex
\begin{tikzpicture}
  \begin{axis}[
    width=0.95\columnwidth, height=50mm,
    xlabel={Epoch}, ylabel={Validation Loss},
    legend style={font=\scriptsize, at={(0.98,0.98)}, anchor=north east},
    grid=both, minor tick num=1, grid style={dotted, gray!40}
  ]
    \addplot[thick, blue]           coordinates {(0,2.30) (5,1.62) (10,1.21) (20,0.94) (30,0.81) (40,0.76) (50,0.74)};
    \addplot[thick, orange, dashed] coordinates {(0,2.30) (5,1.80) (10,1.55) (20,1.30) (30,1.15) (40,1.08) (50,1.05)};
    \legend{Ours, Baseline}
  \end{axis}
\end{tikzpicture}
```

---

## Compilation check (self-audit)

Before handing any snippet to the user, verify:

1. Every node referenced in `\draw`/`\path` exists above it.
2. Every named `.style` in `[...]` appears in the `\begin{tikzpicture}[...]` options.
3. Every shape used (`rounded rectangle`, `diamond`, `parallelogram`, …) has its library loaded in the whitelist.
4. Every math macro (`\mathbb`, `\mathcal`, `\vec`, `\boldsymbol`) is covered by `amsmath, amsfonts, amssymb`.
5. Every `pgfplots` colormap, `matrix plot`, or `groupplots` use has its `\usepgfplotslibrary{...}` line.
6. The figure aspect roughly matches the slot defined in [style-conventions.md](style-conventions.md).

---

## Bilingual labels (opt-in)

Default recipes are English-only so they compile with `pdflatex`. To add a Chinese second-line label, two things change:

1. **Preamble**:
   ```latex
   % Compile with XeLaTeX or LuaLaTeX
   \usepackage{xeCJK}
   \setCJKmainfont{Noto Serif CJK SC}  % or SimSun / STSong / any installed CJK font
   ```
2. **Label swap-in**: replace `{Encoder}` with `{Encoder\\\scriptsize 编码器}` — the `\\` line-break is TikZ-native, `\scriptsize` pulls the CJK line to ~70% of the primary label.

Example:

```latex
\node[mod, right=of enc] (dec) {Decoder\\\scriptsize 解码器};
```

---

## Paste instructions (emit verbatim to user)

1. Ensure the preamble has the whitelist block (only add missing `\usepackage{...}` / `\usetikzlibrary{...}` / `\usepgfplotslibrary{...}` lines).
2. Drop the snippet into the relevant `\begin{figure}[t] ... \end{figure}` block with a `\caption{}` and `\label{fig:...}`.
3. Compile:
   - English only: `pdflatex <paper>.tex` (twice if you have refs).
   - Bilingual: `xelatex <paper>.tex` (twice).
4. Inspect the PDF; if nodes collide, tweak `node distance=...` in the tikzpicture options rather than individual coordinates.
