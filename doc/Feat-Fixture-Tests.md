# Fixtures Tests services

Fixtures tests validate services

## Structure

- Located in `tests/fixtures/`
- Validate command 
- no mock framework

## Test services

```bash
[lastseen_service.py](../check_bitdefender/services/lastseen_service.py)
[onboarding_service.py](../check_bitdefender/services/onboarding_service.py)
[vulnerabilities_service.py](../check_bitdefender/services/vulnerabilities_service.py)
```

## Running Tests

```bash
pytest tests/fixtures/
```

## Implementation

### Test Structure
- Direct service testing without mocks
- JSON fixture data for predictable inputs
- Validation of service outputs and error handling

### Checklist
- [ ] Create test fixtures in `tests/fixtures/`
- [ ] Test `lastseen_service.py` functionality
- [ ] Test `onboarding_service.py` functionality  
- [ ] Test `vulnerabilities_service.py` functionality
- [ ] Validate error handling for invalid inputs
- [ ] Verify service integration with BitDefender GravityZone API
- [ ] Add fixture data files for test scenarios
- [ ] Document test coverage and expected behaviors
