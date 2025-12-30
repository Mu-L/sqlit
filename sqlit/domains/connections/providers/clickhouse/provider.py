"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.docker import DockerDetector
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="clickhouse",
    display_name="ClickHouse",
    adapter_path=("sqlit.domains.connections.providers.clickhouse.adapter", "ClickHouseAdapter"),
    schema_path=("sqlit.domains.connections.providers.clickhouse.schema", "SCHEMA"),
    supports_ssh=True,
    is_file_based=False,
    has_advanced_auth=False,
    default_port="8123",
    requires_auth=False,
    badge_label="ClickHouse",
    docker_detector=DockerDetector(
        image_patterns=("clickhouse",),
        env_vars={
            "user": ("CLICKHOUSE_USER",),
            "password": ("CLICKHOUSE_PASSWORD",),
            "database": ("CLICKHOUSE_DB",),
        },
        default_user="default",
    ),
)

register_provider(SPEC)
