# Click Decorators ErrorHandlers Formatters

The framework @click has powerful functionalities:
- Decorators
- ErrorHandlers
- Formatters

## Current CLI Structure Analysis

The current `cli/__init__.py` contains 199 lines with multiple concerns mixed together:

1. **Main CLI group and context setup** (lines 22-33)
2. **Common decorators** (lines 13-19)
3. **Core execution logic** (lines 35-74)
4. **Command implementations** for different endpoints:
   - Last seen commands: `last-seen`, `last`, `ls` (lines 76-110)
   - Onboarding commands: `onboarding-status`, `onboarding`, `status` (lines 112-146)
   - Vulnerability commands: `vulnerabilities`, `vuln`, `vulns` (lines 148-182)
5. **Legacy compatibility command** (lines 184-199)

## Recommended Code Split

To improve maintainability and follow single responsibility principle, the CLI code should be split into:

### 1. `cli/__init__.py` - Main entry point
- Main CLI group definition
- Context setup
- Import and register commands from other modules

### 2. `cli/decorators.py` - Reusable decorators
- `common_options` decorator
- Future custom decorators and error handlers
- Click option formatters

### 3. `cli/core.py` - Core execution logic
- `execute_check` function
- Common error handling logic
- Result formatting utilities

### 4. `cli/commands/` directory - Command modules
- `cli/commands/__init__.py` - Command registration
- `cli/commands/last_seen.py` - Last seen related commands
- `cli/commands/onboarding.py` - Onboarding status commands  
- `cli/commands/vulnerabilities.py` - Vulnerability commands
- `cli/commands/legacy.py` - Backward compatibility commands

### 5. `cli/handlers.py` - Error handlers and formatters
- Custom Click error handlers
- Output formatters for different verbosity levels
- Exception handling utilities

## Benefits of This Structure

1. **Separation of Concerns**: Each file has a single responsibility
2. **Maintainability**: Easier to modify specific functionality
3. **Testability**: Individual components can be tested in isolation
4. **Extensibility**: New commands can be added without modifying existing files
5. **Code Reuse**: Common decorators and handlers can be easily shared

## Implementation Plan

1. Create the new directory structure
2. Move and refactor code into appropriate modules
3. Update imports and registrations
4. Ensure backward compatibility
5. Add proper error handling and formatters using Click's advanced features
