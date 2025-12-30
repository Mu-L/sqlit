"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="redshift",
    display_name="Amazon Redshift",
    adapter_path=("sqlit.domains.connections.providers.redshift.adapter", "RedshiftAdapter"),
    schema_path=("sqlit.domains.connections.providers.redshift.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=False,
    has_advanced_auth=True,
    default_port="5439",
    requires_auth=True,
    badge_label="RS",
    url_schemes=("redshift",),
)

register_provider(SPEC)
