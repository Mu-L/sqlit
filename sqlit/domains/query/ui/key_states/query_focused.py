"""Query editor focused state."""

from __future__ import annotations

from sqlit.domains.shell.app.state_base import State
from sqlit.domains.shell.app.state_context import UIContext


class QueryFocusedState(State):
    """Base state when query editor has focus."""

    def _setup_actions(self) -> None:
        pass

    def is_active(self, app: UIContext) -> bool:
        return bool(app.query_input.has_focus)
