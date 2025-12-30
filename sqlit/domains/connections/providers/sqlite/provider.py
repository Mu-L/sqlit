"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="sqlite",
    display_name="SQLite",
    adapter_path=("sqlit.domains.connections.providers.sqlite.adapter", "SQLiteAdapter"),
    schema_path=("sqlit.domains.connections.providers.sqlite.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=True,
    has_advanced_auth=False,
    default_port="",
    requires_auth=True,
    badge_label="SQLite",
    url_schemes=("sqlite",),
)

register_provider(SPEC)
