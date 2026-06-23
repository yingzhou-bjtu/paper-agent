# Style Baseline

## Purpose

Define the academic writing style for IEEE technical reports.

## Style Source

Derived from IEEE conference paper conventions and standard academic writing practices.

## What To Apply

- IEEE conference paper format (`\documentclass[conference]{IEEEtran}`)
- Report language as specified by the user (default: English)
- Section hierarchy: `\section{}` and `\subsection{}`
- IEEE `algorithm` environment for pseudocode
- `\cite{}` references with BibTeX
- Placeholder figures using `\fbox{}` blocks
- Tables using `booktabs` style (`\toprule`, `\midrule`, `\bottomrule`)

## Heading Style

- Main sections: Roman numeral style (I. INTRODUCTION, II. RELATED WORK...)
- Subsections: Lettered style (A. Subsection, B. Subsection...)
- IEEEtran class handles this automatically

## Vocabulary Rules

Use domain-level terms, not implementation-level identifiers:

| Use (Domain Term) | Do NOT Use (Code Term) |
|---|---|
| algorithm | algorithm class |
| module | module file |
| layer | layer directory |
| mechanism | service |
| component | component class |
| data access layer | repository |
| user interface layer | widget tree / view controller |
| core logic | controller |
| local database | sqlite instance |
| configuration | .json / .yaml file |

## Practical Rule

Every paragraph in the final output must be understandable by a reader who has never seen the codebase. No implementation-level identifiers allowed.
