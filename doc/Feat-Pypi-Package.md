# 📦 PyPI Package Publishing Guide

## Overview

This document outlines the specifications and steps required to publish the `check-bitdefender` package to PyPI (Python Package Index).

## 📋 Prerequisites

### Required Files ✅

The project already includes all necessary files for PyPI publishing:

- ✅ `pyproject.toml` - Modern Python packaging configuration
- ✅ `README.md` - Package description and documentation
- ✅ `LICENSE` - MIT License file
- ✅ Source code in `check_bitdefender/` directory
- ✅ Tests in `tests/` directory

### Required Tools

Install the build and publishing tools:

```bash
pip install --upgrade build twine
```

## 🔧 Package Configuration Analysis

### Current `pyproject.toml` Status

The project is well-configured for PyPI publishing with:

- **Package name**: `check-bitdefender`
- **Version**: `1.0.0` (manually managed)
- **Build system**: setuptools with modern configuration
- **Entry points**: CLI script `check_bitdefender`
- **Dependencies**: Properly specified with version constraints
- **Metadata**: Complete with author, description, keywords, classifiers
- **URLs**: GitHub repository links configured

### Key Configuration Details

```toml
[project]
name = "check-bitdefender"
version = "1.0.0"
description = "A Nagios plugin for monitoring BitDefender GravityZone API endpoints"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
```

## 🚀 Publishing Steps

### 1. Pre-Publishing Checklist

Before publishing, ensure:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Code quality checks pass: `black .`, `flake8 .`, `mypy check_bitdefender/`
- [ ] Version number is correct in `pyproject.toml`
- [ ] README.md is up-to-date
- [ ] LICENSE file is included
- [ ] All dependencies are specified correctly

### 2. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build source distribution and wheel
python -m build
```

This creates:
- `dist/check-bitdefender-1.0.0.tar.gz` (source distribution)
- `dist/check_bitdefender-1.0.0-py3-none-any.whl` (wheel)

### 3. Test the Build Locally

```bash
# Test installation from wheel
pip install dist/check_bitdefender-1.0.0-py3-none-any.whl

# Verify CLI works
check_bitdefender --version
check_bitdefender --help

# Uninstall test version
pip uninstall check-bitdefender
```

### 4. Upload to Test PyPI (Recommended First Step)

```bash
# Upload to Test PyPI first
python -m twine upload --repository testpypi dist/*
```

Test installation from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ check-bitdefender
```

### 5. Upload to Production PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

## 🔐 Authentication Setup

### PyPI Account Setup

1. **Create PyPI Account**: Register at https://pypi.org/
2. **Enable 2FA**: Enable two-factor authentication
3. **Create API Token**:
   - Go to Account Settings → API tokens
   - Create a token with appropriate scope
   - Store securely for authentication

### Authentication Methods

#### Option 1: API Token (Recommended)
```bash
# Use token during upload
python -m twine upload --username __token__ --password <your-token> dist/*
```

#### Option 2: Configure .pypirc
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-api-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-test-api-token>
```

## 📈 Version Management

### Current Approach
- Manual version management in `pyproject.toml`
- Version: `1.0.0`

### Recommended Version Strategy

#### Semantic Versioning
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

#### Version Update Process
1. Update version in `pyproject.toml`
2. Create git tag: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. Build and publish

### Future: Automated Versioning (Optional)
Consider switching to `setuptools_scm` for automatic versioning from git tags:

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]

[project]
dynamic = ["version"]

[tool.setuptools_scm]
```

## 🔄 Continuous Integration Setup

### GitHub Actions for Automated Publishing

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        user: __token__
        password: ${{ secrets.PYPI_API_TOKEN }}
```

### Required GitHub Secrets
- `PYPI_API_TOKEN`: Your PyPI API token

## 📊 Package Distribution Information

### Package Structure
```
check-bitdefender/
├── check_bitdefender/          # Main package
│   ├── cli/                   # Command-line interface
│   ├── core/                  # Core functionality
│   ├── services/             # Business logic
│   └── __init__.py
├── tests/                    # Test suite
├── doc/                      # Documentation
├── README.md                 # Package documentation
├── LICENSE                   # License file
├── pyproject.toml           # Package configuration
└── requirements*.txt        # Dependencies
```

### Entry Points
- **Console script**: `check_bitdefender` → `check_bitdefender.cli:main`
- **Import name**: `import check_bitdefender`

## 🎯 Post-Publishing Tasks

### 1. Verify Publication
- Visit: https://pypi.org/project/check-bitdefender/
- Test installation: `pip install check-bitdefender`
- Verify functionality: `check_bitdefender --version`

### 2. Update Documentation
- Add PyPI installation instructions to README.md
- Update installation section with: `pip install check-bitdefender`
- Add PyPI badge to README.md:
  ```markdown
  [![PyPI version](https://badge.fury.io/py/check-bitdefender.svg)](https://badge.fury.io/py/check-bitdefender)
  ```

### 3. Release Management
- Create GitHub release matching PyPI version
- Add release notes describing changes
- Archive source code with the release

## 🔍 Package Quality Checklist

### PyPI Package Standards ✅
- [x] Descriptive package name
- [x] Clear description and README
- [x] Proper license specification
- [x] Version constraints for dependencies
- [x] Entry points for CLI tools
- [x] Comprehensive metadata (author, URLs, keywords)
- [x] Python version compatibility specified
- [x] Proper classifiers for discoverability

### Security Considerations
- [x] No hardcoded secrets in code
- [x] Dependencies with version constraints
- [x] MIT license (permissive and clear)
- [x] No sensitive configuration in package

## 📈 Maintenance and Updates

### Regular Maintenance Tasks
1. **Security Updates**: Monitor and update dependencies
2. **Version Bumps**: Follow semantic versioning
3. **Documentation**: Keep README and docs current
4. **Testing**: Ensure compatibility across Python versions
5. **PyPI Metadata**: Update classifiers and keywords as needed

### Monitoring Package Health
- Track download statistics on PyPI
- Monitor GitHub issues and user feedback
- Update dependencies regularly
- Test against new Python versions

## 🎉 Success Metrics

After successful publication:
- Package available at: `https://pypi.org/project/check-bitdefender/`
- Installable via: `pip install check-bitdefender`
- CLI accessible as: `check_bitdefender`
- Comprehensive documentation and examples available

---

**Ready to publish!** The package is well-structured and follows PyPI best practices. Execute the steps above to make `check-bitdefender` available to the Python community.