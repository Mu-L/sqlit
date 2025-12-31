"""Main screen state definitions."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import State
from sqlit.domains.shell.app.state_context import UIContext


class MainScreenState(State):
    """Base state for main screen (no modal active)."""

    help_category = "Navigation"

    def _setup_actions(self) -> None:
        self.allows("focus_explorer", help="Focus Explorer")
        self.allows("focus_query", help="Focus Query")
        self.allows("focus_results", help="Focus Results")
        self.allows("toggle_fullscreen", help="Toggle fullscreen")
        self.allows("show_help")
        self.allows("change_theme")
        self.allows("leader_key", label="Commands", right=True)

    def is_active(self, app: UIContext) -> bool:
        from textual.screen import ModalScreen

        if any(isinstance(screen, ModalScreen) for screen in app.screen_stack[1:]):
            return False
        return not getattr(app, "_query_executing", False)
