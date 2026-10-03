#!/usr/bin/env python3
"""Create an IEEE INFOCOM 2027 starter project on Overleaf."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import uuid
import zipfile
from pathlib import Path
from urllib.parse import quote
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.lib.env_file import (
    build_default_env_values,
    parse_env_file,
    papers_dir,
    write_env_file,
)
from scripts.lib.overleaf_api import load_session


PROJECT_NAME = "INFOCOM-2027-Paper"


MAIN_TEX = r"""\documentclass[conference,10pt]{IEEEtran}
\IEEEoverridecommandlockouts

\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{url}
\usepackage[hidelinks]{hyperref}

\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}

\begin{document}

\title{Paper Title for IEEE INFOCOM 2027}

\author{
\IEEEauthorblockN{First Author\IEEEauthorrefmark{1},
Second Author\IEEEauthorrefmark{1},
Third Author\IEEEauthorrefmark{2}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}Department, University, City, Country\\
Email: \{first, second\}@example.edu}
\IEEEauthorblockA{\IEEEauthorrefmark{2}Department, Institute, City, Country\\
Email: third@example.edu}
}

\maketitle

\begin{abstract}
This starter project follows the standard IEEE conference style used for
IEEE INFOCOM submissions. Replace this placeholder with a concise summary of
the problem, approach, key results, and significance.
\end{abstract}

\begin{IEEEkeywords}
computer communications, networking, measurement, systems, algorithms
\end{IEEEkeywords}

\input{sections/01_introduction}
\input{sections/02_related_work}
\input{sections/03_design}
\input{sections/04_evaluation}
\input{sections/05_conclusion}

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
"""


SECTIONS = {
    "01_introduction.tex": r"""\section{Introduction}
\label{sec:introduction}

Start with the networking problem and why it matters now. A strong INFOCOM
introduction usually makes the operational setting, technical gap, and
measurable contribution clear within the first page.

\textbf{Contributions.} Summarize the paper's contributions as concrete,
verifiable claims:
\begin{itemize}
  \item We identify ...
  \item We design ...
  \item We evaluate ...
\end{itemize}
""",
    "02_related_work.tex": r"""\section{Related Work}
\label{sec:related}

Organize prior work by technical mechanism or problem setting, not by a flat
paper-by-paper list. Use this section to clarify what existing approaches do
not address.
""",
    "03_design.tex": r"""\section{Design}
\label{sec:design}

Describe the model, assumptions, architecture, and algorithmic details. Keep
notation consistent and make every design choice traceable to the problem
statement.

\begin{figure}[t]
  \centering
  \fbox{\parbox{0.86\linewidth}{\centering Placeholder for system architecture}}
  \caption{High-level architecture. Replace this placeholder with a real figure.}
  \label{fig:architecture}
\end{figure}
""",
    "04_evaluation.tex": r"""\section{Evaluation}
\label{sec:evaluation}

State the evaluation questions first, then describe datasets, baselines,
metrics, and deployment or simulation setup.

\begin{table}[t]
  \centering
  \caption{Example evaluation summary. Replace with real results.}
  \label{tab:results}
  \begin{tabular}{lcc}
    \toprule
    Method & Metric A & Metric B \\
    \midrule
    Baseline & -- & -- \\
    Proposed & -- & -- \\
    \bottomrule
  \end{tabular}
\end{table}
""",
    "05_conclusion.tex": r"""\section{Conclusion}
\label{sec:conclusion}

Conclude with the core technical insight, what the evaluation establishes, and
the most important limitation or next step.
""",
}


REFERENCES_BIB = r"""@article{ieeetran,
  author  = {Michael Shell},
  title   = {How to Use the {IEEEtran} {\LaTeX} Class},
  journal = {Journal of {\LaTeX} Class Files},
  year    = {2015},
  volume  = {14},
  number  = {8}
}
"""


LATEXMKRC = r"""$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error %O %S';
$bibtex = 'bibtex %O %B';
"""


README = """# INFOCOM 2027 Paper

Starter Overleaf project for IEEE INFOCOM 2027 using IEEEtran conference style.

Official notes checked during setup:

- IEEE INFOCOM 2027 is scheduled for 24-27 May 2027 in Honolulu, Hawaii.
- The Call for Technical Papers deadline shown by IEEE ComSoc is 31 July 2026.
- INFOCOM submission guidelines state papers are in English, up to 10 printed pages, using standard IEEE templates.
- The project uses `\\documentclass[conference,10pt]{IEEEtran}`.

Before submission, re-check the live INFOCOM 2027 submission guidelines and update title, authors, anonymity, page count, and PDF metadata requirements.
"""


def _write_template(source_dir: Path) -> None:
    if source_dir.exists():
        shutil.rmtree(source_dir)
    (source_dir / "sections").mkdir(parents=True, exist_ok=True)
    (source_dir / "figures").mkdir(parents=True, exist_ok=True)
    (source_dir / "main.tex").write_text(MAIN_TEX, encoding="utf-8")
    (source_dir / "references.bib").write_text(REFERENCES_BIB, encoding="utf-8")
    (source_dir / ".latexmkrc").write_text(LATEXMKRC, encoding="utf-8")
    (source_dir / "README.md").write_text(README, encoding="utf-8")
    (source_dir / "figures" / ".gitkeep").write_text("", encoding="utf-8")
    for name, content in SECTIONS.items():
        (source_dir / "sections" / name).write_text(content, encoding="utf-8")


def _zip_template(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir).as_posix())


def _multipart_body(
    fields: dict[str, str],
    file_field: str,
    filename: str,
    content: bytes,
) -> tuple[bytes, str]:
    boundary = f"----paper-agent-{uuid.uuid4().hex}"
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode(),
                b"\r\n",
            ]
        )
    parts.extend(
        [
            f"--{boundary}\r\n".encode(),
            (
                f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
                "Content-Type: application/octet-stream\r\n\r\n"
            ).encode(),
            content,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return b"".join(parts), boundary


def _json_request(
    session,
    method: str,
    route: str,
    body: dict | None = None,
    *,
    csrf_header: bool = False,
) -> dict:
    data = None
    headers = {
        "Cookie": session.identity["cookies"],
        "Connection": "keep-alive",
        "User-Agent": "paper-agent/1.0",
    }
    if body is not None:
        data = json.dumps({"_csrf": session.identity["csrfToken"], **body}).encode()
        headers["Content-Type"] = "application/json"
    if csrf_header:
        headers["X-Csrf-Token"] = session.identity["csrfToken"]
    request = Request(
        session.server_url.rstrip("/") + "/" + route.lstrip("/"),
        data=data,
        method=method,
        headers=headers,
    )
    try:
        with urlopen(request, timeout=120) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Overleaf request failed ({exc.code}) {route}: {detail[:1000]}") from exc
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _upload_project_zip(zip_path: Path, project_name: str | None = None) -> str:
    session = load_session()
    content = zip_path.read_bytes()
    upload_id = uuid.uuid4()
    filename = zip_path.name
    # Overleaf's zip import validates a `name` form field; without it the request
    # fails with `expected string, received undefined at "body.name"` (HTTP 400).
    fields = {"name": project_name} if project_name else {}
    body, boundary = _multipart_body(fields, "qqfile", filename, content)
    url = (
        session.server_url.rstrip("/")
        + "/project/new/upload"
        + f"?_csrf={quote(session.identity['csrfToken'])}"
        + f"&qquuid={upload_id}"
        + f"&qqfilename={quote(filename)}"
        + f"&qqtotalfilesize={len(content)}"
    )
    request = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Cookie": session.identity["cookies"],
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
            "User-Agent": "paper-agent/1.0",
        },
    )
    try:
        with urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Overleaf upload failed ({exc.code}): {detail[:1000]}") from exc
    project_id = payload.get("project_id")
    if not project_id:
        raise RuntimeError(f"Overleaf did not return project_id: {payload}")
    return project_id


def _create_blank_project(project_name: str) -> str:
    session = load_session()
    payload = _json_request(
        session,
        "POST",
        "project/new",
        {"projectName": project_name, "template": "none"},
    )
    project_id = payload.get("project_id")
    if not project_id:
        raise RuntimeError(f"Overleaf did not return project_id: {payload}")
    return project_id


def _root_folder_id(project_id: str) -> str:
    session = load_session()
    payload = _json_request(session, "GET", f"project/{project_id}/entities")
    root = payload["entities"]["rootFolder"][0]
    return root["_id"]


def _add_folder(project_id: str, parent_folder_id: str, name: str) -> str:
    session = load_session()
    payload = _json_request(
        session,
        "POST",
        f"project/{project_id}/folder",
        {"name": name, "parent_folder_id": parent_folder_id},
    )
    return payload["entity"]["_id"]


def _upload_file(project_id: str, parent_folder_id: str, path: Path) -> None:
    session = load_session()
    content = path.read_bytes()
    filename = path.name
    mime_type = "text/plain" if path.suffix.lower() in {".tex", ".bib", ".md", ".txt"} else "application/octet-stream"
    body, boundary = _multipart_body(
        {
            "targetFolderId": parent_folder_id,
            "name": filename,
            "type": mime_type,
        },
        "qqfile",
        filename,
        content,
    )
    request = Request(
        session.server_url.rstrip("/") + f"/project/{project_id}/upload?folder_id={parent_folder_id}",
        data=body,
        method="POST",
        headers={
            "Cookie": session.identity["cookies"],
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
            "User-Agent": "paper-agent/1.0",
            "X-Csrf-Token": session.identity["csrfToken"],
        },
    )
    try:
        with urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Overleaf file upload failed ({exc.code}) {path}: {detail[:1000]}") from exc
    if not payload.get("success", True):
        raise RuntimeError(f"Overleaf file upload failed for {path}: {payload}")


def _populate_blank_project(project_id: str, source_dir: Path) -> None:
    root_id = _root_folder_id(project_id)
    sections_id = _add_folder(project_id, root_id, "sections")
    figures_id = _add_folder(project_id, root_id, "figures")

    for name in ("main.tex", "references.bib", "README.md", ".latexmkrc"):
        _upload_file(project_id, root_id, source_dir / name)
    for path in sorted((source_dir / "sections").glob("*.tex")):
        _upload_file(project_id, sections_id, path)
    _upload_file(project_id, figures_id, source_dir / "figures" / ".gitkeep")


def _upload_project(project_name: str, source_dir: Path, zip_path: Path) -> str:
    try:
        return _upload_project_zip(zip_path, project_name)
    except RuntimeError as exc:
        print(f"Zip upload failed, falling back to blank project upload: {exc}")
        project_id = _create_blank_project(project_name)
        _populate_blank_project(project_id, source_dir)
        return project_id


def _update_env(project_id: str, project_name: str) -> Path:
    env_path = ROOT / ".env"
    existing = parse_env_file(env_path)
    existing["OVERLEAF_PROJECT_NAME"] = project_name
    existing["OVERLEAF_PROJECT_ID"] = project_id
    if not existing.get("OVERLEAF_METHOD_A_DIR"):
        existing["OVERLEAF_METHOD_A_DIR"] = f"../papers/{project_name}/method-a"
    values = build_default_env_values(existing)
    return write_env_file(values, env_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default=PROJECT_NAME, help="Overleaf project name")
    args = parser.parse_args(argv)

    project_name = args.name.strip() or PROJECT_NAME
    project_root = papers_dir() / project_name
    source_dir = project_root / "source-template"
    zip_path = project_root / f"{project_name}.zip"

    _write_template(source_dir)
    _zip_template(source_dir, zip_path)
    project_id = _upload_project(project_name, source_dir, zip_path)
    env_path = _update_env(project_id, project_name)

    print(f"Created Overleaf project: {project_name}")
    print(f"Project ID: {project_id}")
    print(f"Local template: {source_dir}")
    print(f"Uploaded zip: {zip_path}")
    print(f"Updated env: {env_path}")
    print(f"Overleaf URL: https://www.overleaf.com/project/{project_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
