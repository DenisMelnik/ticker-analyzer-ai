# Ticker Analyser Tests

This directory contains unit tests for the Ticker Analyser application.

## Test Structure

The tests are organized to reflect the application structure:

- `unit_tests/agents/` - Tests for agent implementations
- `unit_tests/utils/` - Tests for utility functions
- `unit_tests/` - Tests for the main controller

## Running Tests

To run all tests:

```bash
python -m pytest unit_tests
```

To run a specific test file:

```bash
python -m pytest unit_tests/agents/price_agent_test.py
```

To run with verbose output:

```bash
python -m pytest -v unit_tests
```

To run with coverage report:

```bash
python -m pytest --cov=src unit_tests
```

Generate HTML coverage report:

```bash
python -m pytest --cov=src --cov-report=html unit_tests
```

## Test Coverage

Current test coverage is 91% across the entire codebase:

1. **Utilities** (90% coverage)
   - `validate_ticker_symbol` function with multiple scenarios
   - Edge cases for validation handling

2. **Agents** (80%+ coverage)
   - `PriceAgent` initialization and tool implementation
   - Testing of tool functionality with mocking

3. **Controller** (94% coverage)
   - Main workflow with valid ticker symbols
   - Error handling for invalid tickers

## Testing Patterns

The test suite uses several advanced testing patterns:

- **Fixture-based testing**: Using pytest fixtures in `conftest.py` to share testing data
- **Mocking patterns**: Extensive use of `unittest.mock` to isolate components
- **Decorator handling**: Special handling for testing decorated functions like CrewAI tools
- **Test parameterization**: Using multiple test cases for thorough coverage

## Adding New Tests

When adding new functionality to the application, please create corresponding test files following the same structure:

1. Create test files with the naming pattern `module_name_test.py`
2. Use descriptive test names that explain the scenario being tested
3. Follow the existing patterns for mocking and fixtures

For mocking external dependencies like yfinance, use the provided fixtures in `conftest.py`. 