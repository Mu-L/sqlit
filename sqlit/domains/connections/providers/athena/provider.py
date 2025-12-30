"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="athena",
    display_name="AWS Athena",
    adapter_path=("sqlit.domains.connections.providers.athena.adapter", "AthenaAdapter"),
    schema_path=("sqlit.domains.connections.providers.athena.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=False,
    has_advanced_auth=True,
    default_port="",
    requires_auth=True,
    badge_label="Athena",
)

register_provider(SPEC)
