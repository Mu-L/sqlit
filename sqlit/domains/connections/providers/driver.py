"""Driver dependency descriptors and import helpers."""

from __future__ import annotations

import importlib
import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DriverDescriptor:
    driver_name: str
    import_names: tuple[str, ...]
    extra_name: str | None
    package_name: str | None


def import_driver_module(
    module_name: str,
    *,
    driver_name: str,
    extra_name: str | None,
    package_name: str | None,
) -> Any:
    """Import a driver module, raising MissingDriverError with detail if it fails."""
    if os.environ.get("SQLIT_MOCK_DRIVER_ERROR") and extra_name and package_name:
        from sqlit.domains.connections.providers.exceptions import MissingDriverError

        raise MissingDriverError(
            driver_name,
            extra_name,
            package_name,
            module_name=module_name,
            import_error=f"No module named '{module_name}'",
        )

    if not extra_name or not package_name:
        return importlib.import_module(module_name)

    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        from sqlit.domains.connections.providers.exceptions import MissingDriverError

        raise MissingDriverError(
            driver_name,
            extra_name,
            package_name,
            module_name=module_name,
            import_error=str(e),
        ) from e


def ensure_driver_available(driver: DriverDescriptor) -> None:
    if not driver.import_names:
        return
    for module_name in driver.import_names:
        import_driver_module(
            module_name,
            driver_name=driver.driver_name,
            extra_name=driver.extra_name,
            package_name=driver.package_name,
        )


def ensure_provider_driver_available(provider: Any) -> None:
    driver = getattr(provider, "driver", None)
    if driver is None:
        return

    missing = os.environ.get("SQLIT_MOCK_MISSING_DRIVERS", "")
    if missing:
        requested = {item.strip().lower() for item in missing.split(",") if item.strip()}
        db_type = getattr(getattr(provider, "metadata", None), "db_type", "").lower()
        if db_type and db_type in requested:
            from sqlit.domains.connections.providers.exceptions import MissingDriverError

            raise MissingDriverError(
                driver.driver_name,
                driver.extra_name or "",
                driver.package_name or "",
                module_name=None,
                import_error=None,
            )

    ensure_driver_available(driver)
