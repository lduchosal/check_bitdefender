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
