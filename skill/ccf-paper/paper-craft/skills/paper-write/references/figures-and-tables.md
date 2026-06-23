# Figures and Tables Guide

## Content-Driven Design Principle (Rule 17)

Every figure/table must answer: "What claim does this prove?"

- If a figure doesn't support a specific claim, remove it
- If a claim needs visualization, create a figure for it
- Don't use generic templates — design each visual for its specific purpose

## LaTeX Table Template

```latex
\begin{table}[t]
\centering
\caption{[Description]. Best results are in \textbf{bold}.}
\label{tab:[label]}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccccc}
\toprule
Method & Metric1 & Metric2 & Metric3 & Metric4 & Avg. \\
\midrule
Baseline 1 & 82.1 & 75.3 & 68.9 & 71.5 & 74.5 \\
Baseline 2 & 84.5 & 77.8 & 71.2 & 74.3 & 77.0 \\
\midrule
Ours (w/o A) & 85.1 & 78.6 & 72.8 & 75.9 & 78.1 \\
Ours & \textbf{87.3} & \textbf{81.2} & \textbf{75.8} & \textbf{78.1} & \textbf{80.6} \\
\bottomrule
\end{tabular}%
}
\end{table}
```

## matplotlib Code Template

```python
import matplotlib.pyplot as plt
import numpy as np

# Color-blind friendly palette (Okabe-Ito)
colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

fig, ax = plt.subplots(figsize=(5, 3.5))
# ... plotting code ...
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
plt.tight_layout()
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

## TikZ Method Overview Template

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}[
    box/.style={draw, rounded corners, minimum width=2cm, minimum height=0.8cm, align=center},
    arrow/.style={->, thick, >=stealth}
]
\node[box, fill=blue!10] (input) {Input};
\node[box, fill=green!10, right=1.5cm of input] (module1) {Module 1};
\node[box, fill=orange!10, right=1.5cm of module1] (module2) {Module 2};
\node[box, fill=red!10, right=1.5cm of module2] (output) {Output};

\draw[arrow] (input) -- (module1);
\draw[arrow] (module1) -- (module2);
\draw[arrow] (module2) -- (output);
\end{tikzpicture}
\caption{Overview of our proposed method.}
\label{fig:overview}
\end{figure}
```

## CS Paper Figure Norms

- **Color-blind friendly**: Use Okabe-Ito palette, viridis, or ColorBrewer Set2. NEVER use red-green only.
- **Vector format**: Save as PDF (not PNG/JPG). All text and lines stay sharp at any zoom.
- **Minimum font size**: 8pt in final printed size. After IEEE/ACM column width reduction, check that text is still readable.
- **Label axes**: Always include axis labels with units.
- **No decorative elements**: Remove chartjunk (3D effects, unnecessary gridlines, drop shadows).
- **Consistent style**: Same font, same color scheme, same line width across all figures in the paper.
- **Caption completeness**: Figure caption should be self-contained — reader should understand the figure without reading the text.
