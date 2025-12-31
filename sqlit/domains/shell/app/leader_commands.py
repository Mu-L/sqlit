"""Leader command registry and binding helpers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from sqlit.domains.shell.app.state_context import UIContext

# Guards are referenced by name from the keymap.
LEADER_GUARDS: dict[str, Callable[[UIContext], bool]] = {
    "has_connection": lambda app: app.current_connection is not None,
    "query_executing": lambda app: getattr(app, "_query_executing", False),
}


@dataclass
class LeaderCommand:
    """Definition of a leader command accessible via space+key."""

    key: str  # The key to press (e.g., "q", "e")
    action: str  # The underlying action to execute (e.g., "quit", "toggle_explorer")
    label: str  # Display label (e.g., "Quit", "Toggle Explorer")
    category: str  # For grouping in the menu ("View", "Connection", "Actions")
    guard: Callable[[UIContext], bool] | None = None  # Optional guard function
    menu: str = "leader"

    @property
    def binding_action(self) -> str:
        """The action name used in Textual bindings (leader_prefixed)."""
        return f"{self.menu}_{self.action}"

    def is_allowed(self, app: UIContext) -> bool:
        """Check if this command is currently allowed."""
        if self.guard is None:
            return True
        return self.guard(app)


def _build_leader_commands(menu: str = "leader") -> list[LeaderCommand]:
    """Build leader commands from the keymap provider."""
    from sqlit.domains.shell.app.keymap import get_keymap

    keymap = get_keymap()
    commands = []

    for cmd_def in keymap.get_leader_commands():
        if cmd_def.menu != menu:
            continue
        guard = LEADER_GUARDS.get(cmd_def.guard) if cmd_def.guard else None
        commands.append(
            LeaderCommand(
                key=cmd_def.key,
                action=cmd_def.action,
                label=cmd_def.label,
                category=cmd_def.category,
                guard=guard,
                menu=cmd_def.menu,
            )
        )

    return commands


def get_leader_commands(menu: str = "leader") -> list[LeaderCommand]:
    """Get leader commands (rebuilt from keymap each time for testability)."""
    return _build_leader_commands(menu)


def get_leader_binding_actions(menu: str = "leader") -> set[str]:
    """Get set of leader binding action names."""
    return {cmd.binding_action for cmd in get_leader_commands(menu)}


def get_leader_bindings(menu: str = "leader") -> tuple:
    """Generate Textual Bindings from leader commands."""
    from textual.binding import Binding

    return tuple(Binding(cmd.key, cmd.binding_action, show=False) for cmd in get_leader_commands(menu))
