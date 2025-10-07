"""Commands package for CLI."""

from typing import Any
from .endpoints import register_endpoints_commands


def register_all_commands(main_group: Any) -> None:
    """Register all commands with the main CLI group."""
    register_endpoints_commands(main_group)
