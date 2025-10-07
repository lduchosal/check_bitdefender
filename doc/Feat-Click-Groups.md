# Click Groups Specification

This document outlines the modernized CLI structure using Click groups to provide better organization and command separation for the BitDefender GravityZone monitoring tool.

## Current Architecture Issues

The current implementation has several limitations:
- Single monolithic command with endpoint parameter
- Separate scripts duplicating common options
- sys.argv manipulation (anti-pattern)
- No proper command grouping or aliases

## Proposed Click Groups Structure

### Main Command Group

```bash
check_bitdefender [OPTIONS] COMMAND [ARGS]...
```

The main command should serve as a Click group with common global options:

- `--config/-c`: Configuration file path (default: 'check_bitdefender.ini')
- `--verbose/-v`: Increase verbosity (count=True)
- `--version`: Show version and exit
- `--help`: Show help message

### Subcommands with Aliases

#### 1. Last Seen Command

**Primary command:**
```bash
check_bitdefender lastseen [OPTIONS] MACHINE
```

**Options:**
- `--endpoint-id/-m`: Endpoint ID (GUID)
- `--dns-name/-d`: Computer DNS Name (FQDN) 
- `--warning/-W`: Warning threshold in days (default: 7)
- `--critical/-C`: Critical threshold in days (default: 30)

**Examples:**
```bash
check_bitdefender lastseen --dns-name endpoint.domain.tld
check_bitdefender lastseen -d endpoint.domain.tld -W 3 -C 7
check_bitdefender lastseen --endpoint-id "12345678-1234-1234-1234-123456789012"
```

#### 2. Onboarding Status Command

**Primary command:**
```bash
check_bitdefender onboarding [OPTIONS] MACHINE
```

**Options:**
- `--endpoint-id/-m`: Endpoint ID (GUID)
- `--dns-name/-d`: Computer DNS Name (FQDN)
- `--warning/-W`: Warning threshold (default: 1)
- `--critical/-C`: Critical threshold (default: 2)

**Examples:**
```bash
check_bitdefender onboarding -d endpoint.domain.tld
check_bitdefender onboarding --endpoint-id "12345678-1234-1234-1234-123456789012"
```

#### 3. Vulnerabilities Command

**Primary command:**
```bash
check_bitdefender vulnerabilities [OPTIONS] MACHINE
```
**Options:**
- `--endpoint-id/-m`: Endpoint ID (GUID)
- `--dns-name/-d`: Computer DNS Name (FQDN)
- `--warning/-W`: Warning threshold for vulnerability score (default: 10)
- `--critical/-C`: Critical threshold for vulnerability score (default: 100)

**Examples:**
```bash
check_bitdefender vulnerabilities --dns-name endpoint.domain.tld
check_bitdefender vulnerabilities -d endpoint.domain.tld -W 5 -C 50
check_bitdefender vulnerabilities --endpoint-id "12345678-1234-1234-1234-123456789012"
```

## Implementation Requirements

### Click Group Structure

1. **Main Group**: Use `@click.group()` with proper context settings
2. **Command Registration**: Use `@main.command()` and `@main.command(name="alias")` for aliases
3. **Shared Context**: Pass configuration and common options through Click context
4. **Error Handling**: Centralized exception handling at the group level

### Key Improvements

1. **No sys.argv Manipulation**: Remove all sys.argv modifications
2. **Proper Click Context**: Use Click's context passing mechanism
3. **Shared Options**: Define common options once and reuse
4. **Command Aliases**: Implement proper aliases using Click's command naming
5. **Help Integration**: Leverage Click's built-in help system
6. **Entry Points**: Update pyproject.toml to reflect new command structure

### Migration Path

1. **Phase 1**: Refactor main CLI to use Click groups
2. **Phase 2**: Update individual command modules to be proper Click commands
3. **Phase 3**: Remove separate script entry points in favor of subcommands
4. **Phase 4**: Update pyproject.toml to use single entry point with groups

### Backward Compatibility

During transition, maintain backward compatibility by:
- Keeping existing separate script entry points
- Adding deprecation warnings for old command usage
- Providing migration guide in documentation

## Benefits

1. **Better Organization**: Logical command grouping
2. **Cleaner Code**: No sys.argv manipulation
3. **Improved UX**: Consistent help system and command structure
4. **Maintainability**: Single source of truth for common options
5. **Extensibility**: Easy to add new commands and aliases
