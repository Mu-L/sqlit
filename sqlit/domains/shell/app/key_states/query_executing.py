"""Query-executing state definitions."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import DisplayBinding, State, resolve_display_key
from sqlit.domains.shell.app.state_context import UIContext


class QueryExecutingState(State):
    """State when a query is being executed."""

    help_category = "Query"

    def _setup_actions(self) -> None:
        self.allows("cancel_operation", label="Cancel", help="Cancel query")
        self.allows("quit")

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        key = resolve_display_key("cancel_operation") or "^z"
        left: list[DisplayBinding] = [DisplayBinding(key=key, label="Cancel", action="cancel_operation")]
        return left, []

    def is_active(self, app: UIContext) -> bool:
        from textual.screen import ModalScreen

        if any(isinstance(screen, ModalScreen) for screen in app.screen_stack[1:]):
            return False
        return getattr(app, "_query_executing", False)
