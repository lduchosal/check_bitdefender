#!/usr/bin/env python3
"""Test configuration loading."""

from check_bitdefender.core.config import load_config
from check_bitdefender.core.auth import get_token

# Load configuration
cfg = load_config("check_bitdefender.ini")

# Get token
token = get_token(cfg)
print(f"Token loaded: {token[:10]}...")

# Get parent_id
parent_id = None
if cfg.has_section("settings"):
    parent_id = cfg["settings"].get("parent_id")
    print(f"Parent ID: {parent_id}")

# Get timeout
timeout = 10
if cfg.has_section("settings"):
    timeout = cfg["settings"].getint("timeout", 10)
    print(f"Timeout: {timeout}s")

print("\nConfiguration loaded successfully!")
