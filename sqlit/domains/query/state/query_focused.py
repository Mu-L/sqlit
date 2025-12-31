"""Query editor focused state."""

from __future__ import annotations

from sqlit.core.state_base import State
from sqlit.core.input_context import InputContext


class QueryFocusedState(State):
    """Base state when query editor has focus."""

    def _setup_actions(self) -> None:
        pass

    def is_active(self, app: InputContext) -> bool:
        return app.focus == "query"
