"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="snowflake",
    display_name="Snowflake",
    adapter_path=("sqlit.domains.connections.providers.snowflake.adapter", "SnowflakeAdapter"),
    schema_path=("sqlit.domains.connections.providers.snowflake.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=False,
    has_advanced_auth=False,
    default_port="",
    requires_auth=True,
    badge_label="SNOW",
)

register_provider(SPEC)
