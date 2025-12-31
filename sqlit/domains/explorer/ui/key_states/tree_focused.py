"""Explorer tree focused state."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import State
from sqlit.domains.shell.app.state_context import UIContext


class TreeFocusedState(State):
    """Base state when tree has focus."""

    help_category = "Explorer"

    def _setup_actions(self) -> None:
        self.allows("new_connection", label="New", help="New connection")
        self.allows("refresh_tree", label="Refresh", help="Refresh tree")
        self.allows("collapse_tree", help="Collapse all")
        self.allows("tree_cursor_down")  # vim j
        self.allows("tree_cursor_up")  # vim k
        self.allows("tree_filter", help="Filter items")

    def is_active(self, app: UIContext) -> bool:
        if not app.object_tree.has_focus:
            return False
        return not getattr(app, "_tree_filter_visible", False)
