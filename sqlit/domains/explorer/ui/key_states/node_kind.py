"""Helpers for explorer key state logic."""

from __future__ import annotations

from typing import Any


def get_node_kind(node: Any) -> str:
    data = getattr(node, "data", None)
    if data is None:
        return ""
    getter = getattr(data, "get_node_kind", None)
    if callable(getter):
        return str(getter())
    return ""
