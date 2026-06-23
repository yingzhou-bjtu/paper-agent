# IEEE LaTeX Templates

## IEEE Conference Style (IEEEtran, 2-column)

```latex
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{booktabs}
\usepackage{hyperref}

\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  captionpos=b
}

\begin{document}

\title{<PAPER TITLE>}

\author{
  \IEEEauthorblockN{<Author Name>}
  \IEEEauthorblockA{
    \textit{<Department>} \\
    \textit{<Institution>} \\
    <City, Country> \\
    <email@domain.com>
  }
}

\maketitle

\begin{abstract}
<150–250 word abstract. Single paragraph. Problem → solution → contribution → outcome.>
\end{abstract}

\begin{IEEEkeywords}
<keyword1, keyword2, keyword3, keyword4, keyword5>
\end{IEEEkeywords}

\section{Introduction}
<Motivate the problem. State the system's purpose. List contributions. Outline paper.>

% \section{Related Work}   % Uncomment if related work section is needed

\section{System Architecture}
<Describe overall architecture, components, data flow, design decisions.>

\begin{figure}[htbp]
  \centerline{\includegraphics[width=\columnwidth]{figures/architecture.png}}
  \caption{System architecture diagram.}
  \label{fig:arch}
\end{figure}

\section{Implementation}
<Technology stack, module breakdown, key code or configuration details.>

\begin{table}[htbp]
\caption{Technology Stack}
\begin{center}
\begin{tabular}{ll}
\toprule
\textbf{Component} & \textbf{Technology} \\
\midrule
Backend & <e.g., Node.js / Django> \\
Database & <e.g., PostgreSQL> \\
Frontend & <e.g., React> \\
Deployment & <e.g., Docker / AWS> \\
\bottomrule
\end{tabular}
\end{center}
\label{tab:stack}
\end{table}

% \section{Results}   % Uncomment if benchmark/test data is present

\section{Conclusion}
<Summarize system and contributions. Restate outcomes. Mention future work.>

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

---

## IEEE Journal / Transactions Style (single-column)

```latex
\documentclass[journal]{IEEEtran}

\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{booktabs}
\usepackage{hyperref}

\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  captionpos=b
}

\begin{document}

\title{<PAPER TITLE>}

\author{
  \IEEEmembership{Member, IEEE}
  <Author Name>,~\IEEEmembership{Member,~IEEE}
  \thanks{Manuscript received <Month DD, YYYY>.}
  \thanks{<Author> is with the Department of <X>, <Institution>, <City>, <Country>. E-mail: <email>.}
}

\markboth{IEEE TRANSACTIONS ON <FIELD>,~VOL.~XX,~NO.~X,~<MONTH YEAR>}%
{<Short Author Name>: <Short Title>}

\maketitle

\begin{abstract}
<150–250 word abstract.>
\end{abstract}

\begin{IEEEkeywords}
<keyword1, keyword2, keyword3, keyword4, keyword5>
\end{IEEEkeywords}

\IEEEpeerreviewmaketitle

\section{Introduction}
\IEEEPARstart{T}{his} paper presents...

% Sections follow same structure as conference template above

\bibliographystyle{IEEEtran}
\bibliography{references}

\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{figures/author.png}}]{Author Name}
Brief biography of the author here.
\end{IEEEbiography}

\end{document}
```

---

## Notes

- Both templates use `IEEEtran.cls` — available via `texlive-publishers` or [IEEE's website](https://www.ieee.org/conferences/publishing/templates.html)
- Always use `\bibliographystyle{IEEEtran}` with `IEEEtran.bst`
- For figures: prefer vector formats (PDF, EPS) over raster; use `\columnwidth` for 2-column layouts
- Algorithms: use the `algorithm` + `algorithmic` packages
- Math: use `align` environment, not `eqnarray`
- Tables: use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) for professional appearance
