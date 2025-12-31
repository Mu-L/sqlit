"""Protocol for state machine context access."""

from __future__ import annotations

from typing import Any, Protocol, overload

from sqlit.shared.ui.widgets import VimMode


class UIContext(Protocol):
    current_connection: Any | None
    current_config: Any | None
    vim_mode: VimMode
    _query_executing: bool
    _leader_pending: bool
    _leader_pending_menu: str
    _tree_filter_visible: bool
    _autocomplete_visible: bool
    _results_filter_visible: bool
    _last_result_columns: list[str]

    @property
    def object_tree(self) -> Any: ...

    @property
    def query_input(self) -> Any: ...

    @property
    def results_table(self) -> Any: ...

    @property
    def screen_stack(self) -> list[Any]: ...

    @overload
    def query_one(self, selector: str) -> Any: ...

    @overload
    def query_one(self, selector: type[Any]) -> Any: ...

    @overload
    def query_one(self, selector: str, expect_type: type[Any]) -> Any: ...

    def query_one(self, selector: Any, expect_type: Any = None) -> Any: ...
