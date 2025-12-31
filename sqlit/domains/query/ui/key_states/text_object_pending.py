"""Text object pending state for i/a (inner/around) text objects."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import ActionResult, DisplayBinding, State
from sqlit.domains.shell.app.state_context import UIContext


class TextObjectPendingState(State):
    """State when waiting for a text object type (after d+i or d+a)."""

    help_category = "Query Editor (Normal)"

    def _setup_actions(self) -> None:
        # No specific actions - we're waiting for text object char
        pass

    def check_action(self, app: UIContext, action_name: str) -> ActionResult:
        # Only allow escape to cancel
        if action_name == "quit":
            return ActionResult.ALLOWED
        return ActionResult.FORBIDDEN

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        pending = getattr(app, "_pending_delete_text_object", "?")
        prefix = "inner" if pending == "inner" else "around"

        return [], [
            DisplayBinding(
                key="w",
                label=f"Delete {prefix} word",
                action="text_object_pending",
            ),
            DisplayBinding(
                key="( ) [ ] { }",
                label=f"Delete {prefix} brackets",
                action="text_object_pending",
            ),
            DisplayBinding(
                key="\" '",
                label=f"Delete {prefix} quotes",
                action="text_object_pending",
            ),
            DisplayBinding(
                key="esc",
                label="Cancel",
                action="quit",
            ),
        ]

    def is_active(self, app: UIContext) -> bool:
        return getattr(app, "_pending_delete_text_object", None) is not None
