"""Leader-pending state definitions."""

from __future__ import annotations

from sqlit.domains.shell.app.leader_commands import get_leader_binding_actions, get_leader_commands
from sqlit.domains.shell.app.state_base import ActionResult, DisplayBinding, State
from sqlit.domains.shell.app.state_context import UIContext


class LeaderPendingState(State):
    """State when waiting for a leader-style combo key."""

    def _setup_actions(self) -> None:
        pass

    def check_action(self, app: UIContext, action_name: str) -> ActionResult:
        menu = getattr(app, "_leader_pending_menu", "leader")
        leader_binding_actions = get_leader_binding_actions(menu)
        if action_name in leader_binding_actions:
            leader_commands = get_leader_commands(menu)
            cmd = next((c for c in leader_commands if c.binding_action == action_name), None)
            if cmd and cmd.is_allowed(app):
                return ActionResult.ALLOWED
            return ActionResult.FORBIDDEN

        return ActionResult.FORBIDDEN

    def get_display_bindings(self, app: UIContext) -> tuple[list[DisplayBinding], list[DisplayBinding]]:
        return [], [DisplayBinding(key="...", label="Waiting", action="leader_pending")]

    def is_active(self, app: UIContext) -> bool:
        return getattr(app, "_leader_pending", False)
