"""Root state definitions."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import State
from sqlit.domains.shell.app.state_context import UIContext


class RootState(State):
    """Root state - minimal actions available everywhere."""

    help_category = "General"

    def _setup_actions(self) -> None:
        self.allows("quit", help="Quit")
        self.allows("show_help", help="Show this help")
        self.allows("leader_key", help="Commands menu")

    def is_active(self, app: UIContext) -> bool:
        return True
