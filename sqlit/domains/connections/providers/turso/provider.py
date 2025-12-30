"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.docker import DockerDetector
from sqlit.domains.connections.providers.model import ProviderSpec

SPEC = ProviderSpec(
    db_type="turso",
    display_name="Turso",
    adapter_path=("sqlit.domains.connections.providers.turso.adapter", "TursoAdapter"),
    schema_path=("sqlit.domains.connections.providers.turso.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=False,
    has_advanced_auth=False,
    default_port="8080",
    requires_auth=False,
    badge_label="Turso",
    url_schemes=("libsql",),
    docker_detector=DockerDetector(
        image_patterns=("ghcr.io/tursodatabase/libsql-server", "tursodatabase/libsql-server"),
        env_vars={
            "user": (),
            "password": (),
            "database": (),
        },
        default_user="",
    ),
)

register_provider(SPEC)
