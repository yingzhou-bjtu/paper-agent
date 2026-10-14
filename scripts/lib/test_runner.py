"""Small helpers for directly executable offline test scripts."""

from __future__ import annotations

import inspect
from collections.abc import Mapping


def run_test_functions(namespace: Mapping[str, object]) -> None:
    """Run zero-argument callables named test_* from a module namespace."""
    for name, value in sorted(namespace.items()):
        if not name.startswith("test_") or not callable(value):
            continue

        signature = inspect.signature(value)
        required = [
            parameter.name
            for parameter in signature.parameters.values()
            if parameter.default is inspect.Parameter.empty
            and parameter.kind
            in {
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            }
        ]
        if required:
            joined = ", ".join(required)
            raise TypeError(f"{name} requires unsupported direct-run arguments: {joined}")

        value()
