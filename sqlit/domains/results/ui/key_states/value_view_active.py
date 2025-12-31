"""Inline value view state."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import DisplayBinding, State
from sqlit.domains.shell.app.state_context import UIContext


class ValueViewActiveState(State):
    """Inline value view is active (viewing a cell's full content)."""

    help_category = "Value View"

    def _setup_actions(self) -> None:
        self.allows("close_value_view", key="escape", label="Close", help="Close value view")
        self.allows("close_value_view", key="q", label="Close", help="Close value view")
        self.allows("copy_value_view", key="y", label="Copy", help="Copy value")

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        left: list[DisplayBinding] = [
            DisplayBinding(key="esc", label="Close", action="close_value_view"),
            DisplayBinding(key="y", label="Copy", action="copy_value_view"),
        ]
        return left, []

    def is_active(self, app: UIContext) -> bool:
        try:
            from sqlit.shared.ui.widgets import InlineValueView

            value_view = app.query_one("#value-view", InlineValueView)
            return bool(value_view.is_visible)
        except Exception:
            return False
