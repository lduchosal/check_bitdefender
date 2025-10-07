# PDM Integration Specification

## Overview

This specification outlines the integration of PDM (Python Dependency Management) into the check_bitdefender project to streamline development workflow and package publishing.

## PDM Integration Benefits

- Simplified dependency management with lock files
- Virtual environment management
- Simplified build and publish workflow
- Better development experience with standardized commands

## Development Workflow

### Setup
```bash
pdm install
```

### Code Quality Checks
```bash
# Format code
pdm run format
black .

# Type checking
pdm run typecheck
mypy check_bitdefender/

# Linting
pdm run lint
flake8 check_bitdefender/
```

### Build and Publish

#### Build Package
```bash
pdm run build
python -m build
```

#### Publish to PyPI
```bash
pdm run publish
python -m twine upload dist/* --verbose
```

## PDM Configuration

The project should include a `pyproject.toml` file with PDM configuration including:

- Project dependencies
- Development dependencies
- Build system configuration
- Script definitions for common tasks

## Scripts Definition

The following scripts should be defined in `pyproject.toml`:

```toml
[tool.pdm.scripts]
format = "black ."
typecheck = "mypy check_bitdefender/"
lint = "flake8 check_bitdefender/"
build = "python -m build"
publish = "python -m twine upload dist/* --verbose"
test = "pytest -v tests/"
all = {composite = ["format", "typecheck", ...]}

```

## Migration Steps

1. Add PDM configuration to `pyproject.toml`
2. Define project dependencies and dev dependencies
3. Create PDM scripts for common tasks
4. Update documentation to use PDM commands
5. Ensure CI/CD pipelines use PDM workflows

## Standard Commands

### Additional scripts check_bitdefender 
```toml
[tool.pdm.scripts]
msdhelp = "check_bitdefender --help"
msdendpoints = "check_bitdefender endpoints"
msdlastseen = "check_bitdefender lastseen -d $MACHINE"
msddetail = "check_bitdefender detail -d $MACHINE"
msdalerts = "check_bitdefender alerts -d $MACHINE"
msdvulnerabilities = "check_bitdefender vulnerabilities -d $MACHINE"
msdonboarding = "check_bitdefender onboarding -d $MACHINE"
msdall = {composite = ["msdhelp", "msdendpoints", ...]}

```

## Benefits for Contributors

- Single command setup: `pdm install`
- Consistent environment across developers
- Simplified command interface
- Automatic dependency resolution and locking