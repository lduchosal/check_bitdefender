# Verbose Print Debugging

## Overview
Enable verbose output for debugging and monitoring application behavior.

## Usage
```
-v, --verbose    Enable verbose mode
-vv             Increase verbosity (multiple -v supported)
```

## Verbosity Levels
- **Level 1 (-v)**: Basic operation info
- **Level 2 (-vv)**: API calls and responses
- **Level 3+ (-vvv)**: Full service tracing

## Output Details
- API endpoint calls with timing
- JSON request/response payloads
- Service method entry/exit tracing
- Error stack traces with context

## Implementation Details

### Core Module
- Add `verbose` parameter to core functions
- Use logging levels (DEBUG, INFO) for different verbosity
- Include method signatures and return values in trace output

### Services Module
- Instrument HTTP requests/responses
- Log authentication steps and token refresh
- Track service method call chains
- Add timing measurements for performance analysis

### CLI Integration
- Pass verbosity level through click context
- Configure logging handlers based on -v count
- Ensure clean output formatting even with debug info