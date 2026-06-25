"""Load and write paper-agent .env configuration."""

from __future__ import annotations

import os
import platform
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
EXAMPLE_PATH = ROOT / ".env.example"

_SENSITIVE_KEYS = frozenset(
    {
        "OVERLEAF_COOKIE",
        "S2_API_KEY",
    }
)


def project_root() -> Path:
    raw = os.environ.get("PAPER_AGENT_ROOT", "").strip()
    if not raw or raw in {".", "./"}:
        return ROOT.resolve()
    path = Path(raw).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (ROOT / path).resolve()


def resolve_config_path(value: str, *, base: Path | None = None) -> Path:
    """Expand ~ and resolve paths relative to the project root."""
    base = (base or project_root()).resolve()
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (base / path).resolve()


def papers_dir() -> Path:
    """Sibling ``papers/`` directory next to the repo (workspace layout)."""
    return project_root().parent / "papers"


def default_method_a_dir() -> Path:
    name = env_get("OVERLEAF_PROJECT_NAME")
    base = papers_dir()
    if name:
        return base / name / "method-a"
    return base / "method-a"


def default_method_a_dir_value(project_name: str = "") -> str:
    """Portable .env value: replica under ``../papers/<project>/method-a``."""
    name = project_name or env_get("OVERLEAF_PROJECT_NAME")
    if name:
        return f"../papers/{name}/method-a"
    return ""


def method_a_replica_dir() -> Path:
    custom = env_get("OVERLEAF_METHOD_A_DIR")
    if custom:
        return resolve_config_path(custom)
    return default_method_a_dir().expanduser().resolve()


def default_references_dir() -> Path:
    return project_root() / "参考文献"


def default_experiment_code_dir() -> Path:
    return project_root() / "实验代码"


def build_default_env_values(
    existing: dict[str, str] | None = None,
    *,
    root: Path | None = None,
) -> dict[str, str]:
    """Build a full .env value map from defaults and optional existing entries."""
    existing = dict(existing or {})
    base_root = (root or ROOT).resolve()
    project_id = existing.get("OVERLEAF_PROJECT_ID") or ""
    project_name = existing.get("OVERLEAF_PROJECT_NAME") or ""
    method_a = existing.get("OVERLEAF_METHOD_A_DIR")
    if not method_a and project_name:
        method_a = default_method_a_dir_value(project_name)
    return {
        "PAPER_AGENT_ROOT": existing.get("PAPER_AGENT_ROOT", ""),
        "CURSOR_USER_DATA_DIR": existing.get("CURSOR_USER_DATA_DIR", ""),
        "CURSOR_EXTENSIONS_DIR": existing.get("CURSOR_EXTENSIONS_DIR", ""),
        "OVERLEAF_SERVER_NAME": existing.get("OVERLEAF_SERVER_NAME") or "www.overleaf.com",
        "OVERLEAF_SERVER_URL": existing.get("OVERLEAF_SERVER_URL") or "https://www.overleaf.com/",
        "OVERLEAF_PROJECT_NAME": project_name,
        "OVERLEAF_PROJECT_ID": project_id,
        "OVERLEAF_USER_EMAIL": existing.get("OVERLEAF_USER_EMAIL") or "",
        "OVERLEAF_COOKIE": existing.get("OVERLEAF_COOKIE") or "",
        "OVERLEAF_METHOD_A_DIR": method_a or "",
        "REFERENCES_DIR": existing.get("REFERENCES_DIR") or "参考文献",
        "EXPERIMENT_CODE_DIR": existing.get("EXPERIMENT_CODE_DIR") or "实验代码",
        "OPENALEX_POLITE_EMAIL": existing.get("OPENALEX_POLITE_EMAIL") or "",
        "CROSSREF_POLITE_EMAIL": existing.get("CROSSREF_POLITE_EMAIL") or "",
        "S2_API_KEY": existing.get("S2_API_KEY") or "",
    }


def default_cursor_user_data_dir() -> str:
    system = platform.system()
    home = Path.home()
    if system == "Darwin":
        return str(home / "Library" / "Application Support" / "Cursor")
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return str(Path(appdata) / "Cursor")
        return str(home / "AppData" / "Roaming" / "Cursor")
    return str(home / ".config" / "Cursor")


def default_cursor_extensions_dir() -> str:
    return str(Path.home() / ".cursor" / "extensions")


def parse_env_file(path: Path | None = None) -> dict[str, str]:
    path = path or ENV_PATH
    if not path.is_file():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def apply_env_file(path: Path | None = None, *, override: bool = False) -> dict[str, str]:
    values = parse_env_file(path)
    for key, value in values.items():
        if value == "":
            continue
        if override or key not in os.environ:
            os.environ[key] = value
    return values


def load_project_env() -> dict[str, str]:
    root = project_root()
    env_path = root / ".env"
    return apply_env_file(env_path)


def relativize_env_values(values: dict[str, str], repo_root: Path | None = None) -> dict[str, str]:
    """Rewrite absolute paths in .env as repo-relative or ~/ paths where possible."""
    repo_root = (repo_root or ROOT).resolve()
    home = Path.home()
    out = dict(values)

    root_val = out.get("PAPER_AGENT_ROOT", "").strip()
    if root_val:
        try:
            resolved = Path(root_val).expanduser().resolve()
            rel = resolved.relative_to(repo_root)
            out["PAPER_AGENT_ROOT"] = "" if str(rel) in {"", "."} else str(rel)
        except ValueError:
            pass
    else:
        out["PAPER_AGENT_ROOT"] = ""

    for key in ("REFERENCES_DIR", "EXPERIMENT_CODE_DIR"):
        val = out.get(key, "").strip()
        if not val:
            continue
        try:
            resolved = Path(val).expanduser().resolve()
            out[key] = str(resolved.relative_to(repo_root))
        except ValueError:
            pass

    method_a = out.get("OVERLEAF_METHOD_A_DIR", "").strip()
    if method_a:
        try:
            resolved = Path(method_a).expanduser().resolve()
            try:
                out["OVERLEAF_METHOD_A_DIR"] = str(resolved.relative_to(repo_root))
            except ValueError:
                out["OVERLEAF_METHOD_A_DIR"] = f"~/{resolved.relative_to(home).as_posix()}"
        except ValueError:
            pass

    for key, default_fn in (
        ("CURSOR_USER_DATA_DIR", default_cursor_user_data_dir),
        ("CURSOR_EXTENSIONS_DIR", default_cursor_extensions_dir),
    ):
        val = out.get(key, "").strip()
        if not val:
            out[key] = ""
            continue
        try:
            if Path(val).expanduser().resolve() == Path(default_fn()).expanduser().resolve():
                out[key] = ""
        except OSError:
            pass

    return out


def write_env_file(values: dict[str, str], path: Path | None = None) -> Path:
    path = path or ENV_PATH
    values = relativize_env_values(values, ROOT)
    lines: list[str] = [
        "# paper-agent 环境配置",
        "# 由 setup-env 生成；敏感项请勿提交到 Git",
        "",
    ]

    sections: list[tuple[str, list[str]]] = [
        (
            "项目",
            ["PAPER_AGENT_ROOT"],
        ),
        (
            "Cursor",
            ["CURSOR_USER_DATA_DIR", "CURSOR_EXTENSIONS_DIR"],
        ),
        (
            "Overleaf 服务器",
            ["OVERLEAF_SERVER_NAME", "OVERLEAF_SERVER_URL"],
        ),
        (
            "Overleaf 项目",
            [
                "OVERLEAF_PROJECT_NAME",
                "OVERLEAF_PROJECT_ID",
                "OVERLEAF_USER_EMAIL",
            ],
        ),
        (
            "Overleaf Cookie 登录",
            ["OVERLEAF_COOKIE"],
        ),
        (
            "本地目录",
            [
                "OVERLEAF_METHOD_A_DIR",
                "REFERENCES_DIR",
                "EXPERIMENT_CODE_DIR",
            ],
        ),
        (
            "文献 API（可选）",
            ["OPENALEX_POLITE_EMAIL", "CROSSREF_POLITE_EMAIL", "S2_API_KEY"],
        ),
    ]

    key_help = {
        "PAPER_AGENT_ROOT": "留空 = 自动检测仓库根；或填相对路径如 .",
        "CURSOR_USER_DATA_DIR": "Cursor 用户数据目录",
        "CURSOR_EXTENSIONS_DIR": "Cursor 扩展安装目录",
        "OVERLEAF_SERVER_NAME": "Overleaf 服务器名",
        "OVERLEAF_SERVER_URL": "Overleaf 服务器 URL",
        "OVERLEAF_PROJECT_NAME": "默认 Overleaf 项目名称",
        "OVERLEAF_PROJECT_ID": "默认 Overleaf 项目 ID",
        "OVERLEAF_USER_EMAIL": "Overleaf 登录邮箱",
        "OVERLEAF_COOKIE": "Cookie 登录凭证（overleaf_session2=...）",
        "OVERLEAF_METHOD_A_DIR": "Method A 本地副本目录（默认 ../papers/<项目名>/method-a）",
        "REFERENCES_DIR": "参考文献目录",
        "EXPERIMENT_CODE_DIR": "实验代码目录",
        "OPENALEX_POLITE_EMAIL": "OpenAlex polite pool 邮箱",
        "CROSSREF_POLITE_EMAIL": "Crossref polite pool 邮箱",
        "S2_API_KEY": "Semantic Scholar API Key",
    }

    written_keys: set[str] = set()
    for title, keys in sections:
        lines.append(f"# --- {title} ---")
        for key in keys:
            written_keys.add(key)
            help_text = key_help.get(key, "")
            if help_text:
                lines.append(f"# {help_text}")
            value = values.get(key, "")
            if key in _SENSITIVE_KEYS and value:
                lines.append(f"{key}={_quote(value)}")
            else:
                lines.append(f"{key}={value}")
            lines.append("")
        lines.append("")

    extra_keys = sorted(set(values) - written_keys)
    if extra_keys:
        lines.append("# --- 其他 ---")
        for key in extra_keys:
            lines.append(f"{key}={values.get(key, '')}")
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def _quote(value: str) -> str:
    if re.search(r'[\s#"$\\]', value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def env_get(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


def env_path(key: str, default: Path | str) -> Path:
    value = env_get(key)
    if value:
        return resolve_config_path(value)
    default_path = Path(default).expanduser()
    if default_path.is_absolute() or str(default).startswith("~"):
        return default_path.resolve()
    return (project_root() / default_path).resolve()


def shell_exports(path: Path | None = None) -> str:
    """Emit bash `export KEY='value'` lines for sourcing in shell scripts."""
    values = parse_env_file(path)
    lines: list[str] = []
    for key, value in values.items():
        if not value:
            continue
        escaped = value.replace("'", "'\"'\"'")
        lines.append(f"export {key}='{escaped}'")
    return "\n".join(lines)


def _main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="paper-agent .env utilities")
    parser.add_argument(
        "--shell-export",
        action="store_true",
        help="Print bash export statements for non-empty .env entries",
    )
    args = parser.parse_args()
    if args.shell_export:
        print(shell_exports())
    else:
        parser.print_help()


if __name__ == "__main__":
    _main()
