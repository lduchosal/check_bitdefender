"""Unit tests for LastSeenService."""

import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta, timezone
from check_bitdefender.services.lastseen_service import LastSeenService
from check_bitdefender.core.exceptions import DefenderAPIError


@pytest.fixture
def mock_client():
    """Create a mock DefenderClient."""
    client = Mock()
    client.list_endpoints = Mock()
    return client


@pytest.fixture
def service(mock_client):
    """Create LastSeenService with mock client."""
    return LastSeenService(mock_client, verbose_level=0)


def test_init(mock_client):
    """Test service initialization."""
    service = LastSeenService(mock_client, verbose_level=0)
    assert service.defender == mock_client
    assert hasattr(service, "logger")


def test_get_result_endpoint_seen_recently(service, mock_client):
    """Test check for endpoint seen within last day."""
    # Create timestamp for 1 day ago
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    timestamp_str = yesterday.isoformat()

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 1  # 1 day ago
    assert "last seen 1 days ago" in result["details"][0]
    assert "test.domain.com" in result["details"][0]
    mock_client.list_endpoints.assert_called_once()


def test_get_result_endpoint_not_found(service, mock_client):
    """Test check for endpoint that doesn't exist."""
    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "other.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": "2024-01-01T00:00:00Z"
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 999  # Not found
    assert "Host not found" in result["details"][0]
    assert "test.domain.com" in result["details"][0]


def test_get_result_endpoint_no_lastseen_data(service, mock_client):
    """Test check for endpoint without last seen data."""
    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": None
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 999  # No data
    assert "no last seen data" in result["details"][0]
    assert "test.domain.com" in result["details"][0]


def test_get_result_endpoint_seen_7_days_ago(service, mock_client):
    """Test check for endpoint seen 7 days ago (warning threshold)."""
    # Create timestamp for 7 days ago
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    timestamp_str = seven_days_ago.isoformat()

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 7  # 7 days ago
    assert "last seen 7 days ago" in result["details"][0]


def test_get_result_endpoint_seen_30_days_ago(service, mock_client):
    """Test check for endpoint seen 30 days ago (critical threshold)."""
    # Create timestamp for 30 days ago
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    timestamp_str = thirty_days_ago.isoformat()

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 30  # 30 days ago
    assert "last seen 30 days ago" in result["details"][0]


def test_get_result_by_endpoint_id(service, mock_client):
    """Test check using endpoint ID instead of DNS name."""
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    timestamp_str = yesterday.isoformat()

    mock_response = {
        "value": [
            {
                "id": "ep123",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(endpoint_id="ep123")

    assert result["value"] == 1  # 1 day ago
    assert "last seen 1 days ago" in result["details"][0]


def test_get_result_no_endpoints_in_system(service, mock_client):
    """Test check when no endpoints exist in system."""
    mock_response = {"value": []}
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 999  # Not found
    assert "Host not found" in result["details"][0]


def test_get_result_missing_value_key(service, mock_client):
    """Test check when API response missing value key."""
    mock_response = {}
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 999  # Not found
    assert "Host not found" in result["details"][0]


def test_get_result_requires_identifier(service, mock_client):
    """Test that either endpoint_id or dns_name is required."""
    with pytest.raises(ValueError, match="Either endpoint_id or dns_name must be provided"):
        service.get_result()


def test_api_exception_propagation(service, mock_client):
    """Test that API exceptions are propagated."""
    mock_client.list_endpoints.side_effect = DefenderAPIError("API Error")

    with pytest.raises(DefenderAPIError, match="API Error"):
        service.get_result(dns_name="test.domain.com")


def test_logging_calls(mock_client):
    """Test that logging methods are called appropriately."""
    service = LastSeenService(mock_client, verbose_level=1)
    service.logger = Mock()

    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    timestamp_str = yesterday.isoformat()

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    service.get_result(dns_name="test.domain.com")

    service.logger.method_entry.assert_called_once()
    service.logger.method_exit.assert_called_once()


def test_get_result_invalid_timestamp_format(service, mock_client):
    """Test handling of invalid timestamp format."""
    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": "invalid-date-format"
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 999  # Parse error
    assert "unable to parse" in result["details"][0]


def test_get_result_with_z_suffix_timestamp(service, mock_client):
    """Test handling of ISO timestamp with Z suffix."""
    yesterday = datetime.now(timezone.utc) - timedelta(days=2)
    timestamp_str = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 2  # 2 days ago
    assert "last seen 2 days ago" in result["details"][0]


def test_get_result_seen_today(service, mock_client):
    """Test endpoint seen today (0 days ago)."""
    now = datetime.now(timezone.utc)
    timestamp_str = now.isoformat()

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "test.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": timestamp_str
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    result = service.get_result(dns_name="test.domain.com")

    assert result["value"] == 0  # Seen today
    assert "last seen 0 days ago" in result["details"][0]


def test_get_result_multiple_endpoints(service, mock_client):
    """Test finding correct endpoint among multiple."""
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    mock_response = {
        "value": [
            {
                "id": "ep1",
                "computerDnsName": "server1.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": yesterday.isoformat()
            },
            {
                "id": "ep2",
                "computerDnsName": "server2.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Linux",
                "lastSeen": week_ago.isoformat()
            },
            {
                "id": "ep3",
                "computerDnsName": "server3.domain.com",
                "onboardingStatus": "Onboarded",
                "osPlatform": "Windows",
                "lastSeen": yesterday.isoformat()
            }
        ]
    }
    mock_client.list_endpoints.return_value = mock_response

    # Find the second endpoint (7 days ago)
    result = service.get_result(dns_name="server2.domain.com")

    assert result["value"] == 7  # 7 days ago
    assert "server2.domain.com" in result["details"][0]
