"""Explorer tree state for folder/schema nodes."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import DisplayBinding, State, resolve_display_key
from sqlit.domains.shell.app.state_context import UIContext

from .node_kind import get_node_kind


class TreeOnFolderState(State):
    """Tree focused on a folder or schema node."""

    def _setup_actions(self) -> None:
        pass

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        left: list[DisplayBinding] = []
        seen: set[str] = set()

        left.append(DisplayBinding(key="enter", label="Expand", action="toggle_node"))
        seen.add("toggle_node")
        left.append(
            DisplayBinding(
                key=resolve_display_key("refresh_tree") or "f",
                label="Refresh",
                action="refresh_tree",
            )
        )
        seen.add("refresh_tree")

        right: list[DisplayBinding] = []
        if self.parent:
            _, parent_right = self.parent.get_display_bindings(app)
            for binding in parent_right:
                if binding.action not in seen:
                    right.append(binding)
                    seen.add(binding.action)

        return left, right

    def is_active(self, app: UIContext) -> bool:
        if not app.object_tree.has_focus:
            return False
        node = app.object_tree.cursor_node
        return node is not None and get_node_kind(node) in ("folder", "schema")
