"""Integration tests for CLI interface end-to-end without external dependencies."""

import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner

from check_bitdefender.cli import main


@pytest.fixture
def cli_runner():
    """Create CLI runner for testing."""
    return CliRunner()


class TestHelpCommand:
    """Test help command functionality."""

    def test_help_command(self, cli_runner):
        """Test help command displays usage information."""
        result = cli_runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert (
            "Check BitDefender GravityZone API endpoints and validate values."
            in result.output
        )
        assert "Commands:" in result.output
        assert "lastseen" in result.output
        assert "onboarding" in result.output
        assert "vulnerabilities" in result.output
        assert "detail" in result.output

    def test_help_flag(self, cli_runner):
        """Test --help flag displays usage information."""
        result = cli_runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert (
            "Check BitDefender GravityZone API endpoints and validate values."
            in result.output
        )


class TestLastSeenCommand:
    """Test lastseen command functionality."""

    @patch("check_bitdefender.cli.commands.lastseen.load_config")
    @patch("check_bitdefender.cli.commands.lastseen.get_authenticator")
    @patch("check_bitdefender.cli.commands.lastseen.DefenderClient")
    @patch("check_bitdefender.cli.commands.lastseen.LastSeenService")
    @patch("check_bitdefender.cli.commands.lastseen.NagiosPlugin")
    def test_lastseen_without_args(
        self, mock_nagios, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test lastseen command without arguments."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(main, ["lastseen"])

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            endpoint_id=None, dns_name=None, warning=7, critical=30, verbose=0
        )

    @patch("check_bitdefender.cli.commands.lastseen.load_config")
    @patch("check_bitdefender.cli.commands.lastseen.get_authenticator")
    @patch("check_bitdefender.cli.commands.lastseen.DefenderClient")
    @patch("check_bitdefender.cli.commands.lastseen.LastSeenService")
    @patch("check_bitdefender.cli.commands.lastseen.NagiosPlugin")
    def test_lastseen_with_dns_name(
        self, mock_nagios, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test lastseen command with DNS name."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(main, ["lastseen", "-d", "endpoint.domain.tld"])

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            endpoint_id=None,
            dns_name="endpoint.domain.tld",
            warning=7,
            critical=30,
            verbose=0,
        )

    @patch("check_bitdefender.cli.commands.lastseen.load_config")
    def test_lastseen_command_error(self, mock_config, cli_runner):
        """Test lastseen command error handling."""
        mock_config.side_effect = Exception("Configuration error")

        result = cli_runner.invoke(main, ["lastseen", "-d", "endpoint.domain.tld"])

        # Exit code should be 3 for UNKNOWN error
        assert result.exit_code == 3
        assert "UNKNOWN: Configuration error" in result.output


class TestOnboardingCommand:
    """Test onboarding command functionality."""

    @patch("check_bitdefender.cli.commands.onboarding.load_config")
    @patch("check_bitdefender.cli.commands.onboarding.get_authenticator")
    @patch("check_bitdefender.cli.commands.onboarding.DefenderClient")
    @patch("check_bitdefender.cli.commands.onboarding.OnboardingService")
    @patch("check_bitdefender.cli.commands.onboarding.NagiosPlugin")
    def test_onboarding_with_dns_name(
        self, mock_nagios, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test onboarding command with DNS name."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(main, ["onboarding", "-d", "endpoint.domain.tld"])

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            endpoint_id=None,
            dns_name="endpoint.domain.tld",
            warning=1,
            critical=2,
            verbose=0,
        )

    @patch("check_bitdefender.cli.commands.onboarding.load_config")
    def test_onboarding_command_error(self, mock_config, cli_runner):
        """Test onboarding command error handling."""
        mock_config.side_effect = Exception("Authentication failed")

        result = cli_runner.invoke(main, ["onboarding", "-d", "endpoint.domain.tld"])

        assert result.exit_code == 3
        assert "UNKNOWN: Authentication failed" in result.output


class TestVulnerabilitiesCommand:
    """Test vulnerabilities command functionality."""

    @patch("check_bitdefender.cli.commands.vulnerabilities.load_config")
    @patch("check_bitdefender.cli.commands.vulnerabilities.get_authenticator")
    @patch("check_bitdefender.cli.commands.vulnerabilities.DefenderClient")
    @patch("check_bitdefender.cli.commands.vulnerabilities.VulnerabilitiesService")
    @patch("check_bitdefender.cli.commands.vulnerabilities.NagiosPlugin")
    def test_vulnerabilities_with_dns_name(
        self, mock_nagios, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test vulnerabilities command with DNS name."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(
            main, ["vulnerabilities", "-d", "endpoint.domain.tld"]
        )

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            endpoint_id=None,
            dns_name="endpoint.domain.tld",
            warning=50,
            critical=500,
            verbose=0,
        )

    @patch("check_bitdefender.cli.commands.vulnerabilities.load_config")
    @patch("check_bitdefender.cli.commands.vulnerabilities.get_authenticator")
    @patch("check_bitdefender.cli.commands.vulnerabilities.DefenderClient")
    @patch("check_bitdefender.cli.commands.vulnerabilities.VulnerabilitiesService")
    @patch("check_bitdefender.cli.commands.vulnerabilities.NagiosPlugin")
    def test_vulnerabilities_with_verbose(
        self, mock_nagios, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test vulnerabilities command with verbose flag."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(
            main, ["vulnerabilities", "-d", "endpoint.domain.tld", "-v"]
        )

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            endpoint_id=None,
            dns_name="endpoint.domain.tld",
            warning=50,
            critical=500,
            verbose=1,
        )

    @patch("check_bitdefender.cli.commands.vulnerabilities.load_config")
    @patch("check_bitdefender.cli.commands.vulnerabilities.get_authenticator")
    @patch("check_bitdefender.cli.commands.vulnerabilities.DefenderClient")
    @patch("check_bitdefender.cli.commands.vulnerabilities.VulnerabilitiesService")
    @patch("check_bitdefender.cli.commands.vulnerabilities.NagiosPlugin")
    def test_vulnerabilities_with_multiple_verbose(
        self, mock_nagios, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test vulnerabilities command with multiple verbose flags."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(
            main, ["vulnerabilities", "-d", "endpoint.domain.tld", "-vvvv"]
        )

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            endpoint_id=None,
            dns_name="endpoint.domain.tld",
            warning=50,
            critical=500,
            verbose=4,
        )

    @patch("check_bitdefender.cli.commands.vulnerabilities.load_config")
    def test_vulnerabilities_command_error(self, mock_config, cli_runner):
        """Test vulnerabilities command error handling."""
        mock_config.side_effect = Exception("Service unavailable")

        result = cli_runner.invoke(
            main, ["vulnerabilities", "-d", "endpoint.domain.tld"]
        )

        assert result.exit_code == 3
        assert "UNKNOWN: Service unavailable" in result.output


class TestDetailCommand:
    """Test detail command functionality."""

    @patch("check_bitdefender.cli.commands.detail.load_config")
    @patch("check_bitdefender.cli.commands.detail.get_authenticator")
    @patch("check_bitdefender.cli.commands.detail.DefenderClient")
    @patch("check_bitdefender.cli.commands.detail.DetailService")
    def test_detail_with_endpoint_id_using_i_flag(
        self, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test detail command with endpoint ID using -i flag."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_result.return_value = 1
        mock_service_instance.get_result.return_value = {
            "value": 1,
            "details": ["Endpoint ID: test-endpoint", "Computer Name: test-pc"],
        }
        mock_service_instance.get_endpoint_details_json.return_value = (
            '{"id": "test-endpoint"}'
        )

        result = cli_runner.invoke(main, ["detail", "-i", "test-endpoint-123"])

        assert result.exit_code == 0
        assert "DEFENDER OK - Endpoint ID:" in result.output
        assert "test-endpoint" in result.output
        mock_service_instance.get_result.assert_called_once_with(
            endpoint_id="test-endpoint-123", dns_name=None
        )

    @patch("check_bitdefender.cli.commands.detail.load_config")
    @patch("check_bitdefender.cli.commands.detail.get_authenticator")
    @patch("check_bitdefender.cli.commands.detail.DefenderClient")
    @patch("check_bitdefender.cli.commands.detail.DetailService")
    def test_detail_with_endpoint_id_using_m_flag(
        self, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test detail command with endpoint ID using -m flag."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_result.return_value = 1
        mock_service_instance.get_result.return_value = {
            "value": 1,
            "details": ["Endpoint ID: test-endpoint", "Computer Name: test-pc"],
        }
        mock_service_instance.get_endpoint_details_json.return_value = (
            '{"id": "test-endpoint"}'
        )

        result = cli_runner.invoke(main, ["detail", "-m", "test-endpoint-456"])

        assert result.exit_code == 0
        assert "DEFENDER OK - Endpoint ID:" in result.output
        mock_service_instance.get_result.assert_called_once_with(
            endpoint_id="test-endpoint-456", dns_name=None
        )

    @patch("check_bitdefender.cli.commands.detail.load_config")
    @patch("check_bitdefender.cli.commands.detail.get_authenticator")
    @patch("check_bitdefender.cli.commands.detail.DefenderClient")
    @patch("check_bitdefender.cli.commands.detail.DetailService")
    def test_detail_with_dns_name(
        self, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test detail command with DNS name."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_result.return_value = 1
        mock_service_instance.get_result.return_value = {
            "value": 1,
            "details": ["Endpoint ID: test-endpoint", "Computer Name: test.domain.com"],
        }
        mock_service_instance.get_endpoint_details_json.return_value = (
            '{"computerDnsName": "test.domain.com"}'
        )

        result = cli_runner.invoke(main, ["detail", "-d", "test.domain.com"])

        assert result.exit_code == 0
        assert "DEFENDER OK - Endpoint ID:" in result.output
        assert "test.domain.com" in result.output
        mock_service_instance.get_result.assert_called_once_with(
            endpoint_id=None, dns_name="test.domain.com"
        )

    @patch("check_bitdefender.cli.commands.detail.load_config")
    @patch("check_bitdefender.cli.commands.detail.get_authenticator")
    @patch("check_bitdefender.cli.commands.detail.DefenderClient")
    @patch("check_bitdefender.cli.commands.detail.DetailService")
    def test_detail_endpoint_not_found_warning(
        self, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test detail command when endpoint not found with warning threshold."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_result.return_value = 0  # Not found
        mock_service_instance.get_result.return_value = {
            "value": 0,
            "details": ["Endpoint not found with DNS name: nonexistent.domain.com"],
        }

        result = cli_runner.invoke(
            main, ["detail", "-d", "nonexistent.domain.com", "-W", "0"]
        )

        assert result.exit_code == 1  # Warning
        assert "DEFENDER WARNING - Endpoint not found" in result.output
        assert "found=0;;1" in result.output

    @patch("check_bitdefender.cli.commands.detail.load_config")
    @patch("check_bitdefender.cli.commands.detail.get_authenticator")
    @patch("check_bitdefender.cli.commands.detail.DefenderClient")
    @patch("check_bitdefender.cli.commands.detail.DetailService")
    def test_detail_endpoint_not_found_critical(
        self, mock_service, mock_client, mock_auth, mock_config, cli_runner
    ):
        """Test detail command when endpoint not found with critical threshold."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_result.return_value = 0  # Not found
        mock_service_instance.get_result.return_value = {
            "value": 0,
            "details": ["Endpoint not found with DNS name: nonexistent.domain.com"],
        }

        result = cli_runner.invoke(
            main, ["detail", "-d", "nonexistent.domain.com", "-C", "0"]
        )

        assert result.exit_code == 2  # Critical
        assert "DEFENDER CRITICAL - Endpoint not found" in result.output
        assert "found=0;1" in result.output

    @patch("check_bitdefender.cli.commands.detail.load_config")
    def test_detail_command_error(self, mock_config, cli_runner):
        """Test detail command error handling."""
        mock_config.side_effect = Exception("Authentication failed")

        result = cli_runner.invoke(main, ["detail", "-i", "test-endpoint"])

        assert result.exit_code == 3
        assert "DEFENDER UNKNOWN - Authentication failed" in result.output

    def test_detail_command_help(self, cli_runner):
        """Test detail command help includes both -i and -m options."""
        result = cli_runner.invoke(main, ["detail", "--help"])

        assert result.exit_code == 0
        assert (
            "Get detailed endpoint information from BitDefender GravityZone." in result.output
        )
        assert "-m, -i, --endpoint-id, --id TEXT" in result.output
        assert "-d, --dns-name TEXT" in result.output


class TestEndpointsCommand:
    """Test endpoints command functionality."""

    @patch("check_bitdefender.cli.commands.endpoints.load_config")
    @patch("check_bitdefender.cli.commands.endpoints.get_token")
    @patch("check_bitdefender.cli.commands.endpoints.DefenderClient")
    @patch("check_bitdefender.cli.commands.endpoints.EndpointsService")
    @patch("check_bitdefender.cli.commands.endpoints.NagiosPlugin")
    def test_endpoints_without_args(
        self, mock_nagios, mock_service, mock_client, mock_token, mock_config, cli_runner
    ):
        """Test endpoints command without arguments."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_token.return_value = "test_token"
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(main, ["endpoints"])

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            warning=10, critical=25, verbose=0
        )

    @patch("check_bitdefender.cli.commands.endpoints.load_config")
    @patch("check_bitdefender.cli.commands.endpoints.get_token")
    @patch("check_bitdefender.cli.commands.endpoints.DefenderClient")
    @patch("check_bitdefender.cli.commands.endpoints.EndpointsService")
    @patch("check_bitdefender.cli.commands.endpoints.NagiosPlugin")
    def test_endpoints_with_custom_thresholds(
        self, mock_nagios, mock_service, mock_client, mock_token, mock_config, cli_runner
    ):
        """Test endpoints command with custom thresholds."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_token.return_value = "test_token"
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(main, ["endpoints", "-w", "5", "-c", "15"])

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            warning=5, critical=15, verbose=0
        )

    @patch("check_bitdefender.cli.commands.endpoints.load_config")
    @patch("check_bitdefender.cli.commands.endpoints.get_token")
    @patch("check_bitdefender.cli.commands.endpoints.DefenderClient")
    @patch("check_bitdefender.cli.commands.endpoints.EndpointsService")
    @patch("check_bitdefender.cli.commands.endpoints.NagiosPlugin")
    def test_endpoints_with_verbose(
        self, mock_nagios, mock_service, mock_client, mock_token, mock_config, cli_runner
    ):
        """Test endpoints command with verbose flag."""
        # Setup mocks
        mock_config.return_value = {"config": "test"}
        mock_token.return_value = "test_token"
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0

        result = cli_runner.invoke(main, ["endpoints", "-v"])

        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            warning=10, critical=25, verbose=1
        )

    @patch("check_bitdefender.cli.commands.endpoints.load_config")
    def test_endpoints_command_error(self, mock_config, cli_runner):
        """Test endpoints command error handling."""
        mock_config.side_effect = Exception("Configuration error")

        result = cli_runner.invoke(main, ["endpoints"])

        # Exit code should be 3 for UNKNOWN error
        assert result.exit_code == 3
        assert "UNKNOWN: Configuration error" in result.output

    def test_endpoints_command_help(self, cli_runner):
        """Test endpoints command help displays usage information."""
        result = cli_runner.invoke(main, ["endpoints", "--help"])

        assert result.exit_code == 0
        assert "List all endpoints in BitDefender GravityZone" in result.output
        assert "-w, --warning" in result.output
        assert "-c, --critical" in result.output
