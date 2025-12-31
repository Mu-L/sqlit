"""Modal-active state definitions."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import ActionResult, DisplayBinding, State
from sqlit.domains.shell.app.state_context import UIContext


class ModalActiveState(State):
    """State when a modal screen is active."""

    def _setup_actions(self) -> None:
        pass

    def check_action(self, app: UIContext, action_name: str) -> ActionResult:
        if action_name in ("quit",):
            return ActionResult.ALLOWED
        return ActionResult.FORBIDDEN

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        return [], []

    def is_active(self, app: UIContext) -> bool:
        from textual.screen import ModalScreen

        return any(isinstance(screen, ModalScreen) for screen in app.screen_stack[1:])
