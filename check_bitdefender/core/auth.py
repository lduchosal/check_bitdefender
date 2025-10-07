"""Authentication management."""

import configparser
from typing import Union
from azure.identity import ClientSecretCredential, CertificateCredential
from check_bitdefender.core.exceptions import ConfigurationError


def get_token(
    config: configparser.ConfigParser,
) -> str:
    """Get appropriate authenticator based on configuration."""
    if not config.has_section("auth"):
        raise ConfigurationError("Missing [auth] section in configuration")

    auth_section = config["auth"]
    token = auth_section.get("token")
    return token

