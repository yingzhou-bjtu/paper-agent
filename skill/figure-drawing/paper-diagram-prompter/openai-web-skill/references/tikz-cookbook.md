# TikZ Cookbook

## Package Whitelist

```latex
\usepackage{amsmath, amsfonts, amssymb}
\usepackage{tikz}
\usetikzlibrary{positioning, arrows.meta, fit, shapes.geometric, shapes.misc, calc, matrix, shadows}
\usepackage{pgfplots}
\usepgfplotslibrary{colormaps}
\pgfplotsset{compat=1.18}
```

English-only labels compile with `pdflatex`. Bilingual labels require XeLaTeX or LuaLaTeX plus `xeCJK`.

## System Architecture

```latex
\begin{tikzpicture}[
  node distance=8mm and 10mm,
  every node/.style={font=\small},
  data/.style={draw, rounded corners=2pt, align=center, minimum height=10mm, minimum width=18mm, fill=blue!10, thick},
  mod/.style ={draw, rounded corners=2pt, align=center, minimum height=10mm, minimum width=18mm, fill=green!10, thick},
  loss/.style={draw, rounded corners=2pt, align=center, minimum height=10mm, minimum width=18mm, fill=orange!18, thick},
  arr/.style ={-Stealth, thick}
]
  \node[data] (load) {Data Loader};
  \node[mod, right=of load] (enc) {Encoder};
  \node[mod, right=of enc] (dec) {Decoder};
  \node[loss, right=of dec] (l) {Loss};
  \draw[arr] (load) -- (enc);
  \draw[arr] (enc) -- (dec) node[midway, above, font=\scriptsize] {$h_t$};
  \draw[arr] (dec) -- (l);
  \node[draw, dashed, fit=(enc) (dec), inner sep=4pt, label=above:{\scriptsize Model}] {};
\end{tikzpicture}
```

## Model Stack

```latex
\begin{tikzpicture}[
  layer/.style={draw, rounded corners=2pt, minimum width=40mm, minimum height=7mm, align=center, font=\small},
  inp/.style={layer, fill=gray!10}, lin/.style={layer, fill=blue!10},
  norm/.style={layer, fill=violet!12}, block/.style={layer, fill=green!12, minimum height=10mm},
  head/.style={layer, fill=orange!15}, out/.style={layer, fill=gray!10}, arr/.style={-Stealth}
]
  \node[inp] (x) {Input $x$};
  \node[lin, below=3mm of x] (l1) {Linear $D\to H$};
  \node[norm, below=3mm of l1] (n1) {LayerNorm};
  \node[block, below=3mm of n1] (tb) {$\times N$ Transformer Blocks};
  \node[head, below=3mm of tb] (h1) {MLP Head $H\to C$};
  \node[out, below=3mm of h1] (y) {Output $\hat{y}$};
  \draw[arr] (x)--(l1); \draw[arr] (l1)--(n1); \draw[arr] (n1)--(tb); \draw[arr] (tb)--(h1); \draw[arr] (h1)--(y);
\end{tikzpicture}
```

## Algorithm Flowchart

```latex
\begin{tikzpicture}[
  node distance=7mm,
  start/.style={draw, rounded rectangle, fill=black, text=white, minimum width=16mm},
  proc/.style={draw, rounded corners=2pt, minimum width=36mm, minimum height=8mm, align=center, font=\small},
  dec/.style={draw, diamond, aspect=2, minimum width=30mm, align=center, font=\small\itshape},
  arr/.style={-Stealth, thick}
]
  \node[start] (s) {Start};
  \node[proc, below=of s] (p1) {Sample mini-batch};
  \node[proc, below=of p1] (p2) {Forward + Loss $\mathcal{L}$};
  \node[proc, below=of p2] (p3) {Backward + Step};
  \node[dec, below=of p3] (d1) {converged?};
  \node[start, below=of d1] (e) {End};
  \draw[arr] (s)--(p1); \draw[arr] (p1)--(p2); \draw[arr] (p2)--(p3); \draw[arr] (p3)--(d1);
  \draw[arr] (d1)--node[right]{yes}(e);
  \draw[arr] (d1.west)-|++(-20mm,0)|-(p1.west) node[pos=0.25,left,font=\scriptsize]{no};
\end{tikzpicture}
```

## Paste Instructions

1. Add the whitelist package block to the preamble.
2. Wrap the snippet in a `figure` or `figure*` environment.
3. Use `\resizebox{\columnwidth}{!}{...}` for single-column figures or `\textwidth` for wide figures.
4. Compile with `pdflatex` for English-only labels; use `xelatex` for bilingual labels.
