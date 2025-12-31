"""State classes for the shell app."""

from sqlit.domains.shell.app.key_states.leader_pending import LeaderPendingState
from sqlit.domains.shell.app.key_states.main_screen import MainScreenState
from sqlit.domains.shell.app.key_states.modal_active import ModalActiveState
from sqlit.domains.shell.app.key_states.query_executing import QueryExecutingState
from sqlit.domains.shell.app.key_states.root import RootState

__all__ = [
    "LeaderPendingState",
    "MainScreenState",
    "ModalActiveState",
    "QueryExecutingState",
    "RootState",
]
