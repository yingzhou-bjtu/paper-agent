# Image Policy

## Goal

Define figure handling rules that ensure every report includes meaningful visual content while keeping figures as author-managed placeholders.

## Decision Flow

1. Every report MUST include at least 3 figure entries.
2. All figures are inserted as labeled placeholders with capture intent.
3. Real images are added MANUALLY by the author after report generation.
4. Never generate, embed, or pretend images are real captures.

## Required Figure Set (Default)

Every report should include placeholder entries for at minimum:
- System architecture overview diagram
- At least 2 key result or UI screen captures
- Additional figures as needed by the project scope

## Placeholder Format (LaTeX)

```latex
\begin{figure}[H]
  \centering
  \fbox{\parbox{0.9\linewidth}{
    \centering
    \textbf{[PLACEHOLDER --- DESCRIPTION]}\\[0.5em]
    \small Source: [where this will be captured from]\\
    Expected content: [content description]
  }}
  \caption{[Figure caption]}
  \label{fig:label}
\end{figure}
```

## Replacement Instructions

When replacing placeholders with real images:

```latex
\begin{figure}[H]
  \centering
  \setlength{\fboxsep}{0pt}\fbox{\includegraphics[width=0.57\linewidth]{images/screenshot.png}}
  \caption{[Figure caption]}
  \label{fig:label}
\end{figure}
```

Recommended post-replacement practice for IEEE two-column layouts:
- UI screenshots often read better around `0.55\linewidth` to `0.60\linewidth` than near full width.
- A thin black frame (`\fbox` with `\fboxsep=0pt`) helps screenshots stand apart from light report backgrounds.
- If several screenshots are nearby, avoid forcing all of them into the same local area; distribute them between adjacent subsections to reduce visible white-space gaps.

## Consistency Rules

- Same figure IDs and captions in both markdown and LaTeX outputs.
- Each placeholder must define: capture target, source, and expected content.
- Never drop the figure section even if no images are available.
