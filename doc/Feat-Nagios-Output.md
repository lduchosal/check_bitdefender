# Nagios Plugin Output Format

## Technical Requirements

The Nagios plugin output follows the standard format:
```
SERVICE_NAME STATUS - message | performance_data
```

**Current Issues:**
- Generic "NAGIOSRESOURCE" service name lacks specificity
- "value" in message provides no context about what's being measured

**Solution:**
- Use "DEFENDER" as service name for better identification
- Replace "value" with specific command name (lastseen, onboarding, vulnerabilities)

## Performance Data Format
`metric=value;warning;critical;min;max`

## Output Examples

### lastseen Command
```bash
check_bitdefender lastseen -d endpoint.domain.tld
```
- **Before:** `NAGIOSRESOURCE OK - value is 0 | value=0;7;30`
- **After:** `DEFENDER OK - lastseen is 0 | lastseen=0;7;30`

**Thresholds:** Warning=7 days, Critical=30 days

### onboarding Command
```bash
check_bitdefender onboarding -d endpoint.domain.tld
```
- **Before:** `NAGIOSRESOURCE WARNING - value is 2 (outside range 0:1) | value=2;1;2`
- **After:** `DEFENDER WARNING - onboarding is 2 (outside range 0:1) | onboarding=2;1;2`

**Expected Values:** 0=onboarded, 1=pending, 2=failed

### vulnerabilities Command
```bash
check_bitdefender vulnerabilities -d endpoint.domain.tld
```
- **Output:** `NAGIOSRESOURCE CRITICAL - value is 294 (outside range 0:100) | value=294;10;100`
- **After:** `DEFENDER CRITICAL - vulnerabilities is 294 (outside range 0:100) | vulnerabilities=294;10;100`

**Thresholds:** Warning=10, Critical=100

## Implementation Notes
- Exit codes follow Nagios standards: OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3
- Performance data enables trending and graphing in monitoring systems
- Service name "DEFENDER" improves alerting clarity and filtering
