"""Deprecated registry shim.

Prefer sqlit.domains.connections.providers.catalog/metadata/validation.
"""

from __future__ import annotations

from sqlit.domains.connections.providers.catalog import (
    get_all_schemas,
    get_db_type_for_scheme,
    get_provider,
    get_provider_schema,
    get_provider_spec,
    get_supported_db_types,
    get_supported_url_schemes,
    get_url_scheme_map,
    iter_provider_schemas,
    register_provider,
)
from sqlit.domains.connections.providers.metadata import (
    get_badge_label,
    get_connection_display_info,
    get_default_port,
    get_display_name,
    has_advanced_auth,
    is_file_based,
    requires_auth,
    supports_ssh,
)
from sqlit.domains.connections.providers.config_service import (
    normalize_connection_config,
    validate_database_required,
)

__all__ = [
    "get_all_schemas",
    "get_db_type_for_scheme",
    "get_provider",
    "get_provider_schema",
    "get_provider_spec",
    "get_supported_db_types",
    "get_supported_url_schemes",
    "get_url_scheme_map",
    "iter_provider_schemas",
    "register_provider",
    "get_badge_label",
    "get_connection_display_info",
    "get_default_port",
    "get_display_name",
    "has_advanced_auth",
    "is_file_based",
    "requires_auth",
    "supports_ssh",
    "normalize_connection_config",
    "validate_database_required",
]
