# Enhance Nagios Output

## Overview
Enhance the output of nagios to provide detailed informations provided by the services.

## Current Behavior
```
DEFENDER WARNING - service is XX (outside range W:C) | vulnerabilities=XX;W;C
```

## Enhanced Output
```
DEFENDER WARNING - service is XX (outside range W:C) | vulnerabilities=XX;W;C
Detailed output line provided by services
Detailed output line provided by services
Detailed output line provided by services
Detailed output line provided by services
```

## Implementation Details

### Services Technical Changes
- Modify logic in `check_bitdefender/services/*_services.py`
- actual : get_value return int
- modified : get_result return struct with value (int) and detail (str[])

### nagios Technical Changes
- Modify logic in `check_bitdefender/core/nagios.py`
- actual : nagiosplugin.Check does not have a summary
- modified : add class DefenderSummary(nagiosplugin.Summary)
  - adds result.detail to the Ok state
