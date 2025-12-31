"""Explorer tree state for connection nodes."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import DisplayBinding, State, resolve_display_key
from sqlit.domains.shell.app.state_context import UIContext

from .node_kind import get_node_kind


class TreeOnConnectionState(State):
    """Tree focused on a connection node."""

    help_category = "Explorer"

    def _setup_actions(self) -> None:
        def can_connect(app: UIContext) -> bool:
            node = app.object_tree.cursor_node
            if not node or get_node_kind(node) != "connection":
                return False
            data = getattr(node, "data", None)
            config = data.config if data else None
            if not app.current_connection:
                return True
            return bool(config and app.current_config and config.name != app.current_config.name)

        def is_connected_to_this(app: UIContext) -> bool:
            node = app.object_tree.cursor_node
            if not node or get_node_kind(node) != "connection":
                return False
            data = getattr(node, "data", None)
            config = data.config if data else None
            return bool(
                app.current_connection is not None
                and config
                and app.current_config
                and config.name == app.current_config.name
            )

        self.allows("connect_selected", can_connect, label="Connect", help="Connect/Expand/Columns")
        self.allows("disconnect", is_connected_to_this, label="Disconnect", help="Disconnect")
        self.allows("edit_connection", label="Edit", help="Edit connection")
        self.allows("delete_connection", label="Delete", help="Delete connection")
        self.allows("duplicate_connection", label="Duplicate", help="Duplicate connection")

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        left: list[DisplayBinding] = []
        seen: set[str] = set()

        node = app.object_tree.cursor_node
        data = getattr(node, "data", None) if node and get_node_kind(node) == "connection" else None
        config = data.config if data else None
        is_connected = (
            app.current_connection is not None
            and config
            and app.current_config
            and config.name == app.current_config.name
        )

        if is_connected:
            left.append(
                DisplayBinding(
                    key=resolve_display_key("disconnect") or "x",
                    label="Disconnect",
                    action="disconnect",
                )
            )
            seen.add("disconnect")
            seen.add("connect_selected")
        else:
            left.append(DisplayBinding(key="enter", label="Connect", action="connect_selected"))
            seen.add("connect_selected")
            seen.add("disconnect")

        left.append(
            DisplayBinding(
                key=resolve_display_key("new_connection") or "n",
                label="New",
                action="new_connection",
            )
        )
        seen.add("new_connection")
        left.append(
            DisplayBinding(
                key=resolve_display_key("edit_connection") or "e",
                label="Edit",
                action="edit_connection",
            )
        )
        seen.add("edit_connection")
        left.append(
            DisplayBinding(
                key=resolve_display_key("duplicate_connection") or "D",
                label="Duplicate",
                action="duplicate_connection",
            )
        )
        seen.add("duplicate_connection")
        left.append(
            DisplayBinding(
                key=resolve_display_key("delete_connection") or "d",
                label="Delete",
                action="delete_connection",
            )
        )
        seen.add("delete_connection")
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
        return node is not None and get_node_kind(node) == "connection"
