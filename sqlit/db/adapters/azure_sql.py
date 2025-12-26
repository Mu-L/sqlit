"""Azure SQL Database adapter.

Azure SQL Database is a cloud-based version of SQL Server with restrictions:
- No cross-database queries
- No USE statement to switch databases
- Each database requires its own connection
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .mssql import SQLServerAdapter

if TYPE_CHECKING:
    from ...config import ConnectionConfig


class AzureSQLAdapter(SQLServerAdapter):
    """Adapter for Azure SQL Database.

    Extends SQLServerAdapter with Azure-specific behavior:
    - Always creates new connections for different databases (no USE)
    - Does not support multiple databases (each connection = one database)
    """

    @classmethod
    def badge_label(cls) -> str:
        return "Azure"

    @classmethod
    def url_schemes(cls) -> tuple[str, ...]:
        return ("azure", "azuresql")

    @property
    def name(self) -> str:
        return "Azure SQL"

    @property
    def supports_multiple_databases(self) -> bool:
        # Azure SQL: each database is isolated, can't browse multiple
        return False

    @classmethod
    def docker_image_patterns(cls) -> tuple[str, ...]:
        # Azure SQL Edge can simulate some Azure SQL behavior
        return ("mcr.microsoft.com/azure-sql-edge",)

    def _get_cursor_for_database(self, conn: Any, database: str | None) -> Any:
        """Get a cursor for the specified database.

        Azure SQL doesn't support USE, so we always just return the cursor
        for the connected database. The connection should already be to
        the correct database (since database is required in config).
        """
        return conn.cursor()
