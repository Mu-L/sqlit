"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="duckdb",
    display_name="DuckDB",
    adapter_path=("sqlit.domains.connections.providers.duckdb.adapter", "DuckDBAdapter"),
    schema_path=("sqlit.domains.connections.providers.duckdb.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=True,
    has_advanced_auth=False,
    default_port="",
    requires_auth=True,
    badge_label="DuckDB",
    url_schemes=("duckdb",),
)

register_provider(SPEC)
