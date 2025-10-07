"""BitDefender GravityZone API client."""

import time
import requests
from typing import Any, Dict, cast
from check_bitdefender.core.exceptions import DefenderAPIError
from check_bitdefender.core.logging_config import get_verbose_logger

PARAM_TOP = "$top"

PARAM_EXPAND = "$expand"

PARAM_ORDERBY = "$orderby"

PARAM_FILTER = "$filter"

PARAM_SELECT = "$select"


class DefenderClient:
    """Client for BitDefender GravityZone API."""

    application_json = "application/json"

    def __init__(
        self,
        authenticator: Any,
        timeout: int = 15,
        region: str = "api",
        verbose_level: int = 0,
    ) -> None:
        """Initialize with authenticator and optional region.

        Args:
            authenticator: Authentication provider
            timeout: Request timeout in seconds
            region: Geographic region (api)
            verbose_level: Verbosity level for logging
        """
        self.authenticator = authenticator
        self.timeout = timeout
        self.region = region
        self.base_url = self._get_base_url(region)
        self.logger = get_verbose_logger(__name__, verbose_level)

    def _get_base_url(self, region: str) -> str:
        """Get base URL for the specified region."""
        endpoints = {
            "api": "https://cloudgz.gravityzone.bitdefender.com",
        }
        return endpoints.get(region, endpoints["api"])
