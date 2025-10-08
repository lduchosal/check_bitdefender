#!/usr/bin/env python3
"""Test script for BitDefender GravityZone API (JSONRPC method).

This script demonstrates the legacy JSONRPC API endpoint for listing endpoints.
For production use, refer to the REST API implementation in core/defender.py.
"""

import base64
import json
import sys

import requests
from check_bitdefender.core.config import load_config

config = load_config("../check_bitdefender.ini")
auth_section = config["auth"]

# Configuration
# apiKey = "1234"  # Replace with your actual API key
apiKey = auth_section.get("token")
parentId = auth_section.get("parent_id")

# Encode API key for Basic authentication
encodedUserPassSequence = base64.b64encode((apiKey + ":").encode()).decode()
authorizationHeader = "Basic " + encodedUserPassSequence

# API endpoint URL
apiEndpoint_Url = "https://cloudgz.gravityzone.bitdefender.com/api/v1.0/jsonrpc/network"

# JSONRPC request payload
request_payload =   {
       "params": {
           "parentId": parentId,
           "page": 1,
           "perPage": 100,
           "filters": {
               "type": {
                   "computers": True,
                   "virtualMachines": True
               },
               "depth": {
                   "allItemsRecursively": True
               }
           },
           "options": {
               "companies": {
                   "returnAllProducts": True
               },
               "endpoints": {
                   "returnProductOutdated": True,
                   "includeScanLogs": True
               }
           }
       },
       "jsonrpc": "2.0",
       "method": "getNetworkInventoryItems",
       "id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"
  }



# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": authorizationHeader,
}

try:
    print("Sending request to BitDefender GravityZone API...")
    print(f"URL: {apiEndpoint_Url}")
    print(f"Method: {request_payload['method']}")
    print()

    result = requests.post(
        apiEndpoint_Url,
        data=json.dumps(request_payload),
        verify=False,  # Note: In production, use verify=True
        headers=headers,
    )

    result.raise_for_status()

    response_data = result.json()
    print("Response received:")
    print(json.dumps(response_data, indent=2))

except requests.exceptions.RequestException as e:
    print(f"Error: Failed to connect to API: {e}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON response: {e}", file=sys.stderr)
    sys.exit(1)
