# Endpoint List Feature

Retrieve and display endpoint list from BitDefender GravityZone API for monitoring purposes.

## Overview

This feature provides a Nagios-compatible command to list all endpoints registered in BitDefender GravityZone, displaying key information such as DNS name, platform, and onboarding status. It supports threshold-based monitoring for endpoint counts.

## Implementation Details

### Architecture

The feature follows a layered architecture:

1. **CLI Layer** (`cli/commands/endpoints.py:17-54`)
   - Handles command-line interface
   - Parses arguments and options
   - Manages Nagios exit codes

2. **Service Layer** (`services/endpoint_service.py:8-92`)
   - Contains business logic
   - Processes endpoint data
   - Formats output for display

3. **API Client Layer** (`core/defender.py:53-85`)
   - Communicates with BitDefender GravityZone API
   - Handles authentication
   - Manages API requests and responses

4. **Nagios Integration** (`core/nagios.py:101-145`)
   - Implements Nagios plugin interface
   - Evaluates thresholds
   - Formats Nagios-compliant output

### Key Components

#### EndpointsService (`services/endpoint_service.py`)
- **Methods:**
  - `get_result()`: Retrieves all endpoints and returns formatted data with count
  - `get_details()`: Returns detailed endpoint information as list of strings
- **Features:**
  - Sorts endpoints by onboarding status (Onboarded → InsufficientInfo → Unsupported)
  - Sub-sorts by DNS name alphabetically
  - Adds visual indicators (✓/✗) for onboarding status
  - Returns structured data with value and details

#### DefenderClient.list_endpoints() (`core/defender.py:53-85`)
- **Endpoint:** `GET /api/v1.0/jsonrpc/network`
- **Authentication:** Bearer token via OAuth2
- **Error Handling:** Raises `DefenderAPIError` on failures
- **Logging:** Includes API timing and response logging

#### CLI Command (`cli/commands/endpoints.py:17-54`)
- **Command:** `check_bitdefender endpoints`
- **Default Thresholds:**
  - Warning: 10 endpoints
  - Critical: 25 endpoints
- **Common Options:** Supports `--config`, `--verbose`, `--endpoint-id`, `--dns-name`, `--warning`, `--critical`

### Data Flow

```
CLI Command → Load Config → Authenticate → Create DefenderClient
    → EndpointsService.get_result() → DefenderClient.list_endpoints()
    → Process & Sort → NagiosPlugin.check() → Exit with Nagios Code
```

### Output Format

**Single Line Summary:**
```
DEFENDER OK - endpoints is 15
```

**Detailed Output (with verbose flag):**
```
Total endpoints: 15
abc123def4: server01.domain.com (Windows) ✓
xyz789ghi0: server02.domain.com (Linux) ✓
uvw456jkl1: workstation03.domain.com (Windows) ✗
```

## Quality Controls

### Code Quality Standards

1. **Type Hints**
   - All functions include complete type annotations
   - Uses `typing` module for complex types
   - Example: `def get_result(self, endpoint_id: Optional[str] = None) -> Dict[str, Any]`

2. **Error Handling**
   - API errors wrapped in custom `DefenderAPIError` exception
   - CLI errors caught and returned as Nagios UNKNOWN state (exit code 3)
   - Request exceptions properly caught and logged

3. **Logging**
   - Verbose logging support with configurable levels
   - Method entry/exit logging for debugging
   - API timing and response logging
   - Example: `self.logger.method_entry("get_result")`

4. **Code Structure**
   - Clear separation of concerns
   - Service-based architecture
   - Reusable components (authentication, configuration)
   - DRY principle applied

### Input Validation

- Configuration file validation on load
- API response structure validation
- Null/empty response handling
- Timeout configuration (default: 15 seconds)

### Security

- API keys stored in configuration files (not hardcoded)
- Bearer token authentication
- HTTPS-only API communication
- No credential logging in verbose mode

## Unit Tests

### Test Structure

Unit tests follow the pattern established in `tests/unit/test_detail_service.py` and should cover:

#### 1. Service Initialization Tests
```python
def test_init():
    """Test service initialization."""
    assert service.defender == mock_client
    assert hasattr(service, "logger")
```

#### 2. Success Path Tests
```python
def test_get_result_success():
    """Test successful endpoint list retrieval."""
    # Mock API response with multiple endpoints
    mock_response = {
        "value": [
            {"id": "ep1", "computerDnsName": "test1.com",
             "onboardingStatus": "Onboarded", "osPlatform": "Windows"},
            {"id": "ep2", "computerDnsName": "test2.com",
             "onboardingStatus": "InsufficientInfo", "osPlatform": "Linux"}
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result()

    assert result["value"] == 2
    assert len(result["details"]) == 3  # header + 2 endpoints
    mock_client.list_endpoints.assert_called_once()
```

#### 3. Empty Response Tests
```python
def test_get_result_no_endpoints():
    """Test handling of empty endpoint list."""
    mock_response = {"value": []}
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result()

    assert result["value"] == 0
    assert "No endpoints found" in result["details"][0]
```

#### 4. Sorting and Formatting Tests
```python
def test_endpoint_sorting():
    """Test endpoints are sorted by status then name."""
    # Mock response with mixed statuses
    # Verify sorted order in result details
```

#### 5. API Error Handling Tests
```python
def test_api_exception_propagation():
    """Test that API exceptions are propagated."""
    mock_client.list_endpoints.side_effect = DefenderAPIError("API Error")

    with pytest.raises(DefenderAPIError, match="API Error"):
        service.get_result()
```

#### 6. Logging Tests
```python
def test_logging_calls():
    """Test that logging methods are called appropriately."""
    service.logger = Mock()
    service.get_result()

    service.logger.method_entry.assert_called_once_with("get_result")
    service.logger.method_exit.assert_called_once()
```

#### 7. Details Formatting Tests
```python
def test_get_details_formatting():
    """Test detailed endpoint information formatting."""
    # Verify truncated IDs, proper spacing, status indicators
```

### Test Coverage Requirements

- **Minimum Coverage:** 80% line coverage
- **Critical Paths:** 100% coverage for error handling
- **Edge Cases:** Empty responses, null values, API failures
- **Integration Points:** API client calls, Nagios plugin integration

### Running Tests

```bash
# Run all unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=check_bitdefender.services.endpoint_service tests/unit/

# Run specific test file
pytest tests/unit/test_endpoint_service.py -v
```

## Integration Testing

Integration tests should be placed in `tests/integration/` and cover:

1. **End-to-End CLI Execution**
   - Test complete command flow
   - Verify Nagios exit codes
   - Validate output format

2. **API Integration**
   - Test with real API responses (using VCR.py or similar)
   - Verify authentication flow
   - Test timeout handling

3. **Configuration Loading**
   - Test various configuration scenarios
   - Verify error messages for invalid configs

## API Reference

### Original JSONRPC  sample

```python
import base64
import requests
import json

apiKey = "UjlMS+0m1l9IUZjpjWyJG8gbnv2Mta4T"

encodedUserPassSequence = base64.b64encode(apiKey + ":")
authorizationHeader = "Basic " + encodedUserPassSequence

apiEndpoint_Url = "https://cloudgz.gravityzone.bitdefender.com/api/v1.0/jsonrpc/network"

request = '{"params": {},"jsonrpc": "2.0","method": "getEndpointsList","id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"}'

result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

print(result.json())
```

## sample result

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "jsonrpc": "2.0",
  "result": {
    "total": 7,
    "page": 1,
    "perPage": 30,
    "pagesCount": 1,
    "items": [
      {
        "id": "1a2b3c4d5e6f7890abcdef12",
        "name": "SERVER-01",
        "label": "",
        "fqdn": "server-01.example.com",
        "groupId": "9f8e7d6c5b4a39281726354d",
        "isManaged": true,
        "machineType": 2,
        "operatingSystemVersion": "Windows Server 2012 R2 Standard",
        "ip": "192.168.1.10",
        "macs": [
          "00:50:56:aa:bb:cc"
        ],
        "ssid": "1-5-21-123456789-987654321-111111111-1001",
        "managedWithBest": true,
        "policy": {
          "id": "fedcba9876543210abcdef01",
          "name": "Corporate Policy",
          "applied": false
        }
      },
      {
        "id": "2b3c4d5e6f7890abcdef1234",
        "name": "WORKSTATION-01",
        "label": "",
        "fqdn": "workstation-01.example.com",
        "groupId": "9f8e7d6c5b4a39281726354d",
        "isManaged": true,
        "machineType": 1,
        "operatingSystemVersion": "Windows 10 Pro",
        "ip": "192.168.1.100",
        "macs": [
          "00:1a:2b:3c:4d:5e"
        ],
        "ssid": "1-5-21-123456789-987654321-111111111-1002",
        "managedWithBest": true,
        "policy": {
          "id": "fedcba9876543210abcdef01",
          "name": "Corporate Policy",
          "applied": true
        }
      }
    ]
  }
}

```

