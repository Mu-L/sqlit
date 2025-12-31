"""Char pending state for f/F/t/T motions."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import ActionResult, DisplayBinding, State
from sqlit.domains.shell.app.state_context import UIContext


class CharPendingState(State):
    """State when waiting for a target character (after d+f, d+F, d+t, d+T)."""

    help_category = "Query Editor (Normal)"

    def _setup_actions(self) -> None:
        # No specific actions - we're waiting for any character
        pass

    def check_action(self, app: UIContext, action_name: str) -> ActionResult:
        # Only allow escape to cancel
        if action_name == "quit":
            return ActionResult.ALLOWED
        return ActionResult.FORBIDDEN

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        motion = getattr(app, "_pending_delete_motion", "?")
        motion_desc = {
            "f": "to char",
            "F": "back to char",
            "t": "till char",
            "T": "back till char",
        }.get(motion, "char")

        return [], [
            DisplayBinding(
                key="<char>",
                label=f"Delete {motion_desc}...",
                action="char_pending",
            ),
            DisplayBinding(
                key="esc",
                label="Cancel",
                action="quit",
            ),
        ]

    def is_active(self, app: UIContext) -> bool:
        return getattr(app, "_pending_delete_motion", None) is not None
