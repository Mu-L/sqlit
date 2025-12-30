"""CockroachDB adapter using psycopg2 (PostgreSQL wire-compatible)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlit.domains.connections.providers.registry import get_default_port
from sqlit.domains.connections.providers.postgresql.base import PostgresBaseAdapter
from sqlit.domains.connections.providers.driver import import_driver_module

if TYPE_CHECKING:
    from sqlit.domains.connections.domain.config import ConnectionConfig


class CockroachDBAdapter(PostgresBaseAdapter):
    """Adapter for CockroachDB using psycopg2 (PostgreSQL wire-compatible)."""

    @property
    def name(self) -> str:
        return "CockroachDB"

    @property
    def install_extra(self) -> str:
        return "cockroachdb"

    @property
    def install_package(self) -> str:
        return "psycopg2-binary"

    @property
    def driver_import_names(self) -> tuple[str, ...]:
        return ("psycopg2",)

    @property
    def supports_stored_procedures(self) -> bool:
        return False  # CockroachDB has limited stored procedure support

    @property
    def supports_triggers(self) -> bool:
        """Triggers are preview-only in CockroachDB; treat as unsupported by default."""
        return False

    def connect(self, config: ConnectionConfig) -> Any:
        """Connect to CockroachDB database."""
        psycopg2 = import_driver_module(
            "psycopg2",
            driver_name=self.name,
            extra_name=self.install_extra,
            package_name=self.install_package,
        )

        endpoint = config.tcp_endpoint
        if endpoint is None:
            raise ValueError("CockroachDB connections require a TCP-style endpoint.")
        port = int(endpoint.port or get_default_port("cockroachdb"))
        conn = psycopg2.connect(
            host=endpoint.host,
            port=port,
            database=endpoint.database or "defaultdb",
            user=endpoint.username,
            password=endpoint.password,
            sslmode="disable",  # default container runs insecure; disable TLS for compatibility
            connect_timeout=10,
        )
        # Enable autocommit to avoid transaction issues
        conn.autocommit = True
        return conn

    def get_databases(self, conn: Any) -> list[str]:
        """Get list of databases from CockroachDB."""
        cursor = conn.cursor()
        cursor.execute("SELECT database_name FROM [SHOW DATABASES] ORDER BY database_name")
        return [row[0] for row in cursor.fetchall()]

    def get_procedures(self, conn: Any, database: str | None = None) -> list[str]:
        """CockroachDB has limited stored procedure support - return empty list."""
        return []
