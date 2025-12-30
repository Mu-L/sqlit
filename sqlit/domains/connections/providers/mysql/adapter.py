"""MySQL adapter using PyMySQL (pure Python)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlit.domains.connections.providers.registry import get_default_port
from sqlit.domains.connections.providers.adapters.base import MySQLBaseAdapter
from sqlit.domains.connections.providers.driver import import_driver_module

if TYPE_CHECKING:
    from sqlit.domains.connections.domain.config import ConnectionConfig


class MySQLAdapter(MySQLBaseAdapter):
    """Adapter for MySQL using PyMySQL."""

    @property
    def name(self) -> str:
        return "MySQL"

    @property
    def install_extra(self) -> str:
        return "mysql"

    @property
    def install_package(self) -> str:
        return "PyMySQL"

    @property
    def driver_import_names(self) -> tuple[str, ...]:
        return ("pymysql",)

    def connect(self, config: ConnectionConfig) -> Any:
        """Connect to MySQL database."""
        pymysql = import_driver_module(
            "pymysql",
            driver_name=self.name,
            extra_name=self.install_extra,
            package_name=self.install_package,
        )

        endpoint = config.tcp_endpoint
        if endpoint is None:
            raise ValueError("MySQL connections require a TCP-style endpoint.")
        port = int(endpoint.port or get_default_port("mysql"))
        return pymysql.connect(
            host=endpoint.host,
            port=port,
            database=endpoint.database or None,
            user=endpoint.username,
            password=endpoint.password,
            connect_timeout=10,
            autocommit=True,
            charset="utf8mb4",
        )
