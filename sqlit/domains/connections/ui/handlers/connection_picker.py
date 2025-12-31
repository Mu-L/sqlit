"""Connection picker result handling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

from textual.widgets import Tree

from sqlit.domains.connections.domain.config import ConnectionConfig

if TYPE_CHECKING:
    from sqlit.domains.connections.discovery.docker_detector import DetectedContainer

class ConnectionPickerHost(Protocol):
    connections: list[ConnectionConfig]
    object_tree: Tree
    current_config: ConnectionConfig | None

    def _get_connection_config_from_node(self, node: Any) -> ConnectionConfig | None: ...
    def connect_to_server(self, config: ConnectionConfig) -> None: ...
    def notify(self, message: str, severity: str | None = None) -> None: ...


class ConnectionResultHandler(Protocol):
    def handle(self, host: ConnectionPickerHost, result: Any) -> bool: ...


@dataclass
class ConnectionResultRegistry:
    _handlers: dict[str, ConnectionResultHandler]

    def register(self, kind: str, handler: ConnectionResultHandler) -> None:
        self._handlers[kind] = handler

    def handle(self, host: ConnectionPickerHost, kind: str, result: Any) -> bool:
        handler = self._handlers.get(kind)
        if not handler:
            return False
        return handler.handle(host, result)


def _select_saved_connection(host: ConnectionPickerHost, config: ConnectionConfig) -> None:
    for node in host.object_tree.root.children:
        node_config = host._get_connection_config_from_node(node)
        if node_config and node_config.name == config.name:
            host.object_tree.select_node(node)
            break


def _find_matching_saved_connection(
    host: ConnectionPickerHost, container: DetectedContainer
) -> ConnectionConfig | None:
    for conn in host.connections:
        if conn.name == container.container_name:
            return conn

        endpoint = conn.tcp_endpoint
        if (
            endpoint
            and conn.db_type == container.db_type
            and endpoint.host in ("localhost", "127.0.0.1", container.host)
            and endpoint.port == str(container.port)
        ):
            if container.database:
                if endpoint.database == container.database:
                    return conn
            else:
                return conn
    return None


class DockerConnectionResultHandler:
    def handle(self, host: ConnectionPickerHost, result: Any) -> bool:
        from sqlit.domains.connections.discovery.docker_detector import container_to_connection_config

        container = result.container
        config = container_to_connection_config(container)
        matching_config = _find_matching_saved_connection(host, container)
        if matching_config:
            _select_saved_connection(host, matching_config)
            config = matching_config
        host.connect_to_server(config)
        return True


class AzureConnectionResultHandler:
    def handle(self, host: ConnectionPickerHost, result: Any) -> bool:
        from sqlit.domains.connections.discovery.cloud_detector import azure_server_to_connection_config

        config = azure_server_to_connection_config(
            result.server,
            result.database,
            result.use_sql_auth,
        )
        host.connect_to_server(config)
        return True


class CloudConnectionResultHandler:
    def handle(self, host: ConnectionPickerHost, result: Any) -> bool:
        host.connect_to_server(result.config)
        return True


_DEFAULT_REGISTRY: ConnectionResultRegistry | None = None


def get_default_connection_result_registry() -> ConnectionResultRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        registry = ConnectionResultRegistry(_handlers={})
        registry.register("docker", DockerConnectionResultHandler())
        registry.register("azure", AzureConnectionResultHandler())
        registry.register("cloud", CloudConnectionResultHandler())
        _DEFAULT_REGISTRY = registry
    return _DEFAULT_REGISTRY
