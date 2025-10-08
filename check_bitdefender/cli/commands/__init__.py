"""Commands package for CLI."""

from typing import Any
from .endpoints import register_endpoints_commands
from .onboarding import register_onboarding_commands
from .lastseen import register_lastseen_commands


def register_all_commands(main_group: Any) -> None:
    """Register all commands with the main CLI group."""
    register_endpoints_commands(main_group)
    register_onboarding_commands(main_group)
    register_lastseen_commands(main_group)
