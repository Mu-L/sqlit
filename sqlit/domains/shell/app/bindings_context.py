"""Resolve active keybinding contexts for the app."""

from __future__ import annotations

from typing import Protocol

from sqlit.shared.ui.widgets import VimMode


class BindingContextApp(Protocol):
    object_tree: object
    query_input: object
    results_table: object
    vim_mode: VimMode
    _tree_filter_visible: bool
    _results_filter_visible: bool
    _autocomplete_visible: bool


def _safe_has_focus(target: object) -> bool:
    try:
        return bool(getattr(target, "has_focus"))
    except Exception:
        return False


def get_binding_contexts(app: BindingContextApp) -> set[str]:
    """Determine which keybinding contexts should be active."""
    contexts = {"global", "navigation"}

    if _safe_has_focus(app.object_tree):
        contexts.add("tree")
    if getattr(app, "_tree_filter_visible", False):
        contexts.add("tree_filter")

    if _safe_has_focus(app.query_input):
        contexts.add("query")
        if app.vim_mode == VimMode.INSERT:
            contexts.add("query_insert")
        else:
            contexts.add("query_normal")
    if getattr(app, "_autocomplete_visible", False):
        contexts.add("autocomplete")

    if _safe_has_focus(app.results_table):
        contexts.add("results")
    if getattr(app, "_results_filter_visible", False):
        contexts.add("results_filter")

    return contexts
