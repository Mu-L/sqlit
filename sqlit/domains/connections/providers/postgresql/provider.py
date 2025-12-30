"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.docker import DockerDetector
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="postgresql",
    display_name="PostgreSQL",
    adapter_path=("sqlit.domains.connections.providers.postgresql.adapter", "PostgreSQLAdapter"),
    schema_path=("sqlit.domains.connections.providers.postgresql.schema", "SCHEMA"),
    supports_ssh=True,
    is_file_based=False,
    has_advanced_auth=False,
    default_port="5432",
    requires_auth=True,
    badge_label="PG",
    url_schemes=("postgresql", "postgres"),
    docker_detector=DockerDetector(
        image_patterns=("postgres",),
        env_vars={
            "user": ("POSTGRES_USER",),
            "password": ("POSTGRES_PASSWORD",),
            "database": ("POSTGRES_DB",),
        },
        default_user="postgres",
        default_database="postgres",
    ),
)

register_provider(SPEC)
