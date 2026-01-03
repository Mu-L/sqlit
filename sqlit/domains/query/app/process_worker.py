"""Query execution worker for process isolation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from typing import Any

from sqlit.domains.connections.domain.config import ConnectionConfig
from sqlit.domains.connections.providers.catalog import get_provider
from sqlit.domains.connections.providers.config_service import normalize_connection_config
from sqlit.domains.query.app.cancellable import CancellableQuery
from sqlit.domains.query.app.multi_statement import split_statements
from sqlit.domains.query.app.query_service import NonQueryResult, QueryResult


def _tunnel_key(config: ConnectionConfig) -> tuple[Any, ...] | None:
    tunnel = config.tunnel
    if tunnel is None or not tunnel.enabled:
        return None
    return (
        tunnel.host,
        tunnel.port,
        tunnel.username,
        tunnel.auth_type,
        tunnel.password,
        tunnel.key_path,
    )


@dataclass
class _WorkerState:
    conn: Connection
    provider_cache: dict[str, Any] = field(default_factory=dict)
    tunnel: Any | None = None
    tunnel_key: tuple[Any, ...] | None = None
    current_id: int | None = None
    current_query: CancellableQuery | None = None
    current_thread: threading.Thread | None = None
    send_lock: threading.Lock = field(default_factory=threading.Lock)

    def send(self, payload: dict[str, Any]) -> None:
        with self.send_lock:
            try:
                self.conn.send(payload)
            except Exception:
                pass

    def _ensure_tunnel(self, config: ConnectionConfig) -> Any | None:
        key = _tunnel_key(config)
        if key is None:
            self._close_tunnel()
            return None
        if key != self.tunnel_key:
            self._close_tunnel()
            from sqlit.domains.connections.app.tunnel import create_ssh_tunnel

            tunnel, _, _ = create_ssh_tunnel(config)
            self.tunnel = tunnel
            self.tunnel_key = key
        return self.tunnel

    def _close_tunnel(self) -> None:
        if self.tunnel is not None:
            try:
                self.tunnel.stop()
            except Exception:
                pass
            self.tunnel = None
        self.tunnel_key = None

    def _start_query(self, message: dict[str, Any]) -> None:
        query_id = int(message.get("id", 0))
        query = str(message.get("query", ""))
        max_rows = message.get("max_rows", None)
        config_payload = message.get("config", {})
        config = ConnectionConfig.from_dict(config_payload)
        config = normalize_connection_config(config)
        db_type = str(message.get("db_type") or config.db_type or "").strip()
        if not db_type:
            self.send(
                {
                    "type": "error",
                    "id": query_id,
                    "message": "Missing database type for process worker.",
                }
            )
            return

        if len(split_statements(query)) > 1:
            self.send(
                {
                    "type": "error",
                    "id": query_id,
                    "message": "Multi-statement queries are not supported in the process worker.",
                }
            )
            return

        provider = self._get_provider(db_type)
        if provider is None:
            self.send(
                {
                    "type": "error",
                    "id": query_id,
                    "message": f"Unknown database type for process worker: {db_type}",
                }
            )
            return

        tunnel = self._ensure_tunnel(config)
        cancellable = CancellableQuery(
            sql=query,
            config=config,
            provider=provider,
            tunnel=tunnel,
        )
        self.current_id = query_id
        self.current_query = cancellable

        def run() -> None:
            start = time.perf_counter()
            try:
                result = cancellable.execute(max_rows=max_rows)
                elapsed_ms = (time.perf_counter() - start) * 1000
                if isinstance(result, QueryResult):
                    self.send(
                        {
                            "type": "result",
                            "id": query_id,
                            "kind": "query",
                            "result": result,
                            "elapsed_ms": elapsed_ms,
                        }
                    )
                elif isinstance(result, NonQueryResult):
                    self.send(
                        {
                            "type": "result",
                            "id": query_id,
                            "kind": "non_query",
                            "result": result,
                            "elapsed_ms": elapsed_ms,
                        }
                    )
                else:
                    self.send(
                        {
                            "type": "error",
                            "id": query_id,
                            "message": "Unsupported query result.",
                        }
                    )
            except Exception as exc:
                if cancellable.is_cancelled or "cancelled" in str(exc).lower():
                    self.send(
                        {
                            "type": "cancelled",
                            "id": query_id,
                        }
                    )
                else:
                    self.send(
                        {
                            "type": "error",
                            "id": query_id,
                            "message": str(exc),
                        }
                    )

        self.current_thread = threading.Thread(target=run, daemon=True)
        self.current_thread.start()

    def _cancel_current(self, query_id: int) -> None:
        if self.current_id != query_id:
            return
        if self.current_query is not None:
            self.current_query.cancel()

    def _cleanup_current(self) -> None:
        if self.current_thread and not self.current_thread.is_alive():
            self.current_thread.join(timeout=0)
            self.current_thread = None
            self.current_query = None
            self.current_id = None

    def _get_provider(self, db_type: str) -> Any | None:
        if db_type in self.provider_cache:
            return self.provider_cache[db_type]
        try:
            provider = get_provider(db_type)
        except Exception:
            return None
        self.provider_cache[db_type] = provider
        return provider


def run_process_worker(conn: Connection) -> None:
    """Process entrypoint for query execution."""
    state = _WorkerState(conn=conn)
    try:
        while True:
            state._cleanup_current()
            if conn.poll(0.1):
                message = conn.recv()
                message_type = message.get("type")
                if message_type == "shutdown":
                    break
                if message_type == "exec":
                    if state.current_thread is not None and state.current_thread.is_alive():
                        state.send(
                            {
                                "type": "error",
                                "id": int(message.get("id", 0)),
                                "message": "Worker is busy.",
                            }
                        )
                    else:
                        state._start_query(message)
                elif message_type == "cancel":
                    state._cancel_current(int(message.get("id", 0)))
    finally:
        state._cancel_current(state.current_id or 0)
        state._close_tunnel()
        try:
            conn.close()
        except Exception:
            pass
