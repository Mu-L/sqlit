"""Resolve active keybinding contexts for the app."""

from __future__ import annotations

from typing import Protocol, cast

from sqlit.shared.ui.widgets import VimMode


class BindingContextApp(Protocol):
    vim_mode: VimMode
    _tree_filter_visible: bool
    _results_filter_visible: bool
    _autocomplete_visible: bool

    @property
    def object_tree(self) -> object: ...

    @property
    def query_input(self) -> object: ...

    @property
    def results_table(self) -> object: ...


def _safe_widget(app: BindingContextApp, attr: str) -> object | None:
    try:
        return cast(object, getattr(app, attr))
    except Exception:
        return None


def _safe_has_focus(target: object) -> bool:
    try:
        return bool(getattr(target, "has_focus"))
    except Exception:
        return False


def get_binding_contexts(app: BindingContextApp) -> set[str]:
    """Determine which keybinding contexts should be active."""
    contexts = {"global", "navigation"}

    tree = _safe_widget(app, "object_tree")
    if tree and _safe_has_focus(tree):
        contexts.add("tree")
    if getattr(app, "_tree_filter_visible", False):
        contexts.add("tree_filter")

    query_input = _safe_widget(app, "query_input")
    if query_input and _safe_has_focus(query_input):
        contexts.add("query")
        if app.vim_mode == VimMode.INSERT:
            contexts.add("query_insert")
        else:
            contexts.add("query_normal")
    if getattr(app, "_autocomplete_visible", False):
        contexts.add("autocomplete")

    results_table = _safe_widget(app, "results_table")
    if results_table and _safe_has_focus(results_table):
        contexts.add("results")
    if getattr(app, "_results_filter_visible", False):
        contexts.add("results_filter")

    return contexts
