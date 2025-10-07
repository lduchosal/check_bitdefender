# 🛡️ Check BitDefender GravityZone

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/lduchosal/check_bitdefender)

A comprehensive **Nagios plugin** for monitoring BitDefender GravityZone for Endpoint API endpoints. Built with modern Python practices and designed for enterprise monitoring environments.

## ✨ Features

- 🔐 **Authentication** - Support for API Token
- 🎯 **Multiple Endpoints** - Monitor onboarding status, last seen, vulnerabilities, products with CVEs, alerts, and endpoint details
- 📊 **Nagios Compatible** - Standard exit codes and performance data output
- 🏗️ **Clean Architecture** - Modular design with testable components
- 🔧 **Flexible Configuration** - File-based configuration with sensible defaults
- 📈 **Verbose Logging** - Multi-level debugging support
- 🐍 **Modern Python** - Built with Python 3.9+ using type hints and async patterns

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment (recommended)
python -m venv /usr/local/libexec/nagios/check_bitdefender
source /usr/local/libexec/nagios/check_bitdefender/bin/activate

# Install from source
pip install git+https://github.com/lduchosal/check_bitdefender.git
```

### Basic Usage

```bash
# List all endpoints
check_bitdefender endpoints

# Get detailed endpoint info
check_bitdefender detail -d endpoint.domain.tld
```

## 📋 Available Commands

| Command | Description | Default Thresholds |
|---------|-------------|-------------------|
| `endpoints` | List all endpoints | W:10, C:25 |
| `detail` | Get detailed endpoint information | - |

### Vulnerability Scoring

The vulnerability score is calculated as:
- **Critical vulnerabilities** × 100
- **High vulnerabilities** × 10
- **Medium vulnerabilities** × 5
- **Low vulnerabilities** × 1

### Products CVE Monitoring

The products command monitors installed software with known CVE vulnerabilities:
- **Groups CVEs by software** (name, version, vendor)
- **Shows CVE details** including severity levels and disk paths
- **Counts vulnerable software** (not individual CVEs)
- **Default thresholds**: Warning at 5 vulnerable software, Critical at 1
- **Displays up to 10 software entries** with first 5 CVEs per software

### Alert Monitoring

The alerts command monitors unresolved security alerts for a endpoint:
- **Counts only unresolved alerts** (status ≠ "Resolved")
- **Excludes informational alerts** when critical/warning alerts exist
- **Shows alert details** including creation time, title, and severity
- **Default thresholds**: Warning at 1 alert, Critical at 0 (meaning any alert triggers warning)

### Onboarding Status Values

- `0` - Onboarded ✅
- `1` - InsufficientInfo ⚠️
- `2` - Unknown ❌

## ⚙️ Configuration

### Authentication Setup

Create `check_bitdefender.ini` in your Nagios directory or current working directory:

#### Client Secret Authentication
```ini
[auth]
token = your-token-for-gravity-zone

[settings]
timeout = 5
```

### BitDefender GravityZone API Setup

2. **Grant API Permissions**:
   - `xxx`

📚 [Complete API Setup Guide](https://learn.microsoft.com/en-us/defender-endpoint/api/api-hello-world)

## 🔧 Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-c, --config` | Configuration file path | `-c /custom/path/config.ini` |
| `-m, --endpointId` | Endpoint ID (GUID) | `-m "12345678-1234-1234-1234-123456789abc"` |
| `-d, --computerDnsName` | Computer DNS Name (FQDN) | `-d "server.domain.com"` |
| `-W, --warning` | Warning threshold | `-W 10` |
| `-C, --critical` | Critical threshold | `-C 100` |
| `-v, --verbose` | Verbosity level | `-v`, `-vv`, `-vvv` |
| `--version` | Show version | `--version` |

## 🏢 Nagios Integration

### Command Definitions

```cfg
# BitDefender GravityZone Commands
define command {
    command_name    check_bitdefender_onboarding
    command_line    $USER1$/check_bitdefender/bin/check_bitdefender onboarding -d $HOSTALIAS$
}

define command {
    command_name    check_bitdefender_lastseen
    command_line    $USER1$/check_bitdefender/bin/check_bitdefender lastseen -d $HOSTALIAS$ -W 7 -C 30
}

```

### Service Definitions

```cfg
# BitDefender GravityZone Services
define service {
    use                     generic-service
    service_description     BITDEFENDER_ONBOARDING
    check_command           check_bitdefender_onboarding
    hostgroup_name          bitdefender
}

define service {
    use                     generic-service
    service_description     BITDEFENDER_LASTSEEN
    check_command           check_bitdefender_lastseen
    hostgroup_name          bitdefender
}

```

## 🏗️ Architecture

This plugin follows **clean architecture** principles with clear separation of concerns:

```
check_bitdefender/
├── 📁 cli/                     # Command-line interface
│   ├── commands/               # Individual command handlers
│   │   ├── endpoints.py        # List endpoints command
│   ├── decorators.py          # Common CLI decorators
│   └── handlers.py            # CLI handlers
├── 📁 core/                    # Core business logic
│   ├── auth.py                # Authentication management
│   ├── config.py              # Configuration handling
│   ├── defender.py            # Defender API client
│   ├── exceptions.py          # Custom exceptions
│   ├── nagios.py              # Nagios plugin framework
│   └── logging_config.py      # Logging configuration
├── 📁 services/                # Business services
│   ├── endpoints_service.py    # Endpoints business logic
│   └── models.py              # Data models
└── 📁 tests/                   # Comprehensive test suite
    ├── unit/                   # Unit tests
    ├── integration/            # Integration tests
    └── fixtures/               # Test fixtures
```

### Key Design Principles

- **🎯 Single Responsibility** - Each module has one clear purpose
- **🔌 Dependency Injection** - Easy testing and mocking
- **🧪 Testable** - Comprehensive test coverage
- **📈 Extensible** - Easy to add new commands and features
- **🔒 Secure** - No secrets in code, proper credential handling

## 🧪 Development

### Development Setup

```bash
# Clone repository
git clone https://github.com/lduchosal/check_bitdefender.git
cd check_bitdefender

# Create development environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Code Quality Tools

```bash
# Format code
black check_bitdefender/

# Lint code
flake8 check_bitdefender/

# Type checking
mypy check_bitdefender/

# Run tests
pytest tests/ -v --cov=check_bitdefender
```

### Building & Publishing

```bash
# Build package
python -m build

# Test installation
pip install dist/*.whl

# Publish to PyPI
python -m twine upload dist/*
```

## 🔍 Output Examples

### Successful Check
```
DEFENDER OK - Onboarding status: 0 (Onboarded) | onboarding=0;1;2;0;2
```

### Warning State
```
DEFENDER WARNING - Last seen: 10 days ago | lastseen=10;7;30;0;
```

### Critical State
```
DEFENDER CRITICAL - Vulnerability score: 150 (1 Critical, 5 High) | vulnerabilities=150;10;100;0;
```

### Alerts Warning
```
DEFENDER WARNING - Unresolved alerts for endpoint.domain.com | alerts=2;1;5;0;
Unresolved alerts for endpoint.domain.com
2025-09-14T10:22:14.12Z - Suspicious activity detected (New high)
2025-09-14T12:00:00.00Z - Malware detection (InProgress medium)
```

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Authentication Errors** | Verify Azure app permissions and credentials |
| **Network Connectivity** | Check firewall rules for Microsoft endpoints |
| **Import Errors** | Ensure all dependencies are installed |
| **Configuration Issues** | Validate config file syntax and paths |

### Debug Mode

Enable verbose logging for detailed troubleshooting:

```bash
# Maximum verbosity
check_bitdefender vulnerabilities -d endpoint.domain.tld -vvv

# Check specific configuration
check_bitdefender onboarding -c /path/to/config.ini -d endpoint.domain.tld -vv
```

### Required Network Access

Ensure connectivity to:
- `cloudgz.gravityzone.bitdefender.com`

## 📊 Exit Codes

| Code | Status | Description |
|------|--------|-------------|
| `0` | OK | Value within acceptable range |
| `1` | WARNING | Value exceeds warning threshold |
| `2` | CRITICAL | Value exceeds critical threshold |
| `3` | UNKNOWN | Error occurred during execution |

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [nagiosplugin](https://nagiosplugin.readthedocs.io/) framework
- Uses [Azure Identity SDK](https://docs.microsoft.com/python/api/azure-identity/) for authentication
- Powered by [Click](https://click.palletsprojects.com/) for CLI interface

---

<div align="center">

**[⭐ Star this repository](https://github.com/lduchosal/check_bitdefender)** if you find it useful!

[🐛 Report Bug](https://github.com/lduchosal/check_bitdefender/issues) • [💡 Request Feature](https://github.com/lduchosal/check_bitdefender/issues) • [📖 Documentation](https://github.com/lduchosal/check_bitdefender/blob/main/README.md)

</div>