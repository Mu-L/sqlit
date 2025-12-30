"""Provider registration."""

from sqlit.domains.connections.providers.catalog import register_provider
from sqlit.domains.connections.providers.model import ProviderSpec


def _supabase_display_info(config: object) -> str:
    region = getattr(config, "get_option", lambda name, default="": default)("supabase_region", "")
    if region:
        name = getattr(config, "name", "Supabase")
        return f"{name} ({region})"
    return getattr(config, "name", "Supabase")

SPEC = ProviderSpec(
    db_type="supabase",
    display_name="Supabase",
    adapter_path=("sqlit.domains.connections.providers.supabase.adapter", "SupabaseAdapter"),
    schema_path=("sqlit.domains.connections.providers.supabase.schema", "SCHEMA"),
    supports_ssh=False,
    is_file_based=False,
    has_advanced_auth=False,
    default_port="",
    requires_auth=True,
    badge_label="Supabase",
    display_info=_supabase_display_info,
)

register_provider(SPEC)
