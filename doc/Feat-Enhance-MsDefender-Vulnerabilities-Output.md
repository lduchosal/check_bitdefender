# Enhance Vulnerabilities Output

## Overview
Enhance the MS Defender vulnerabilities output to provide detailed vulnerability information with proper deduplication and severity sorting.

## Current Behavior
```
DEFENDER WARNING - vulnerabilities is 79 (outside range 0:10) | vulnerabilities=79;10;100
```

## Enhanced Output
```
DEFENDER WARNING - vulnerabilities is 79 (outside range 0:10) | vulnerabilities=79;10;100
CVE-2023-1234: 7zip vulnerability CRITICAL
CVE-2023-5678: Chrome remote code execution HIGH
CVE-2023-9012: Adobe PDF reader buffer overflow MEDIUM
```

## Implementation Details

### Data Processing
- **Deduplication**: Group vulnerabilities by CVE ID to avoid duplicate entries
- **Severity Sorting**: Order vulnerabilities by criticality (CRITICAL > HIGH > MEDIUM > LOW)
- **Formatting**: Display CVE ID, description, and severity level consistently

### Technical Changes
- Modify vulnerability collection logic in `check_bitdefender/core/defender.py`
- Update output formatting in CLI commands
- Implement severity mapping from MS Defender API responses
- Add vulnerability deduplication based on CVE identifiers

### Output Format
- Primary Nagios status line remains unchanged for compatibility
- Additional vulnerability details appended as separate lines
- Each vulnerability formatted as: `CVE-ID: Description SEVERITY` 