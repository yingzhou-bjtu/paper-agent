#!/usr/bin/env python3
"""Offline checks for Overleaf server option validation."""

from __future__ import annotations

try:
    from scripts.lib.repo import ensure_repo_on_path
    from scripts.lib.test_runner import run_test_functions
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path
    from lib.test_runner import run_test_functions

ensure_repo_on_path()

from scripts.lib.overleaf_workshop import (
    configure_cookie_login,
    normalize_cookie,
    normalize_server_name,
    normalize_server_options,
    normalize_server_url,
)


def test_server_options_accept_http_and_https() -> None:
    assert normalize_server_options(
        "  www.overleaf.com  ",
        "https://www.overleaf.com/",
    ) == ("www.overleaf.com", "https://www.overleaf.com/")
    assert normalize_server_url("http://overleaf.example:8080/ol") == (
        "http://overleaf.example:8080/ol"
    )


def test_server_url_rejects_non_http_schemes() -> None:
    for value in ("file:///etc/hosts", "ftp://example.com/", "overleaf.com"):
        try:
            normalize_server_url(value)
        except ValueError as exc:
            assert "http" in str(exc)
        else:
            raise AssertionError(f"unsupported server URL was accepted: {value}")


def test_server_url_rejects_missing_host_and_invalid_port() -> None:
    for value in ("https:///project", "https://example.com:99999/"):
        try:
            normalize_server_url(value)
        except ValueError as exc:
            assert "主机" in str(exc) or "端口" in str(exc)
        else:
            raise AssertionError(f"invalid server URL was accepted: {value}")


def test_server_name_rejects_empty_and_control_characters() -> None:
    for value in ("", "   ", "overleaf\nname"):
        try:
            normalize_server_name(value)
        except ValueError as exc:
            assert "server_name" in str(exc)
        else:
            raise AssertionError(f"invalid server name was accepted: {value!r}")


def test_cookie_rejects_non_strings_and_header_newlines() -> None:
    for value in (None, b"cookie=value", "overleaf_session2=value\nInjected: 1"):
        try:
            normalize_cookie(value)
        except ValueError as exc:
            assert "Cookie" in str(exc)
        else:
            raise AssertionError(f"invalid cookie was accepted: {value!r}")


def test_configure_rejects_file_url_before_network_or_state_write() -> None:
    try:
        configure_cookie_login(
            "overleaf_session2=value",
            server_url="file:///etc/hosts",
        )
    except ValueError as exc:
        assert "http" in str(exc)
    else:
        raise AssertionError("file URL reached configure_cookie_login")


def main() -> int:
    run_test_functions(globals())
    print("overleaf server option tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
