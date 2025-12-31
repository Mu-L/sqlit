"""Provider metadata accessors (UI-friendly labels, display info)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlit.domains.connections.providers.catalog import get_provider

if TYPE_CHECKING:
    from sqlit.domains.connections.domain.config import ConnectionConfig


def get_display_name(db_type: str) -> str:
    return get_provider(db_type).metadata.display_name


def get_badge_label(db_type: str) -> str:
    return get_provider(db_type).metadata.badge_label


def get_default_port(db_type: str) -> str:
    return get_provider(db_type).metadata.default_port


def supports_ssh(db_type: str) -> bool:
    return get_provider(db_type).metadata.supports_ssh


def is_file_based(db_type: str) -> bool:
    return get_provider(db_type).metadata.is_file_based


def has_advanced_auth(db_type: str) -> bool:
    return get_provider(db_type).metadata.has_advanced_auth


def requires_auth(db_type: str) -> bool:
    return get_provider(db_type).metadata.requires_auth


def get_connection_display_info(config: ConnectionConfig) -> str:
    provider = get_provider(config.db_type)
    return provider.display_info(config)
