# Figure Placeholders Template

## Rules

1. Every report must include at least 3 figure placeholders.
2. Figures are NEVER generated or embedded — only placeholders are created.
3. Real images are added manually by the author after report generation.
4. Each placeholder must specify: ID, caption, capture target, and expected content.

## Standard Placeholder Set

### FIG-01: Architecture Diagram

| Field | Value |
|---|---|
| ID | fig:architecture |
| Caption | Overall system architecture |
| Source | To be drawn by the author or exported from a diagram tool |
| Content | Layered architecture: UI → Core Logic → Data Access |

### FIG-02: Main Screen / Primary Result

| Field | Value |
|---|---|
| ID | fig:main_screen |
| Caption | [Main screen or primary result view of the project] |
| Source | Screenshot from emulator, device, or application |
| Content | [Description of what the main functional screen shows] |

### FIG-03: Secondary Screen / Result 1

| Field | Value |
|---|---|
| ID | fig:screen_2 |
| Caption | [Secondary screen or result view] |
| Source | Screenshot from emulator, device, or application |
| Content | [Description of the relevant screen or result] |

### FIG-04: Secondary Screen / Result 2

| Field | Value |
|---|---|
| ID | fig:screen_3 |
| Caption | [Third screen or result view] |
| Source | Screenshot from emulator, device, or application |
| Content | [Description of the relevant screen or result] |

## LaTeX Placeholder Format

```latex
\begin{figure}[H]
  \centering
  \fbox{\parbox{0.9\linewidth}{
    \centering
    \textbf{[PLACEHOLDER --- DESCRIPTION]}\\[0.5em]
    \small Source: [source description]\\
    Expected content: [content description]
  }}
  \caption{[Caption]}
  \label{fig:label}
\end{figure}
```

## Replacing with Real Image

```latex
\begin{figure}[H]
  \centering
  \setlength{\fboxsep}{0pt}\fbox{\includegraphics[width=0.57\linewidth]{images/filename.png}}
  \caption{[Caption]}
  \label{fig:label}
\end{figure}
```
