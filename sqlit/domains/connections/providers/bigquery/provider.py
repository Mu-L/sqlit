"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="bigquery",
    display_name="Google BigQuery",
    adapter_path=("sqlit.domains.connections.providers.bigquery.adapter", "BigQueryAdapter"),
    schema_path=("sqlit.domains.connections.providers.bigquery.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=False,
    has_advanced_auth=True,
    default_port="",
    requires_auth=False,
    badge_label="BQ",
    url_schemes=("bigquery",),
)

register_provider(SPEC)
