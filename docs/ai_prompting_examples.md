# Arc ZARDIAN: Quick Start Example

This file demonstrates the proper usage of the master prompt and AI collaboration patterns for Arc ZARDIAN development.

---

## Example 1: Asking for an API Client

### ❌ POOR PROMPT (Generic)
```
Write me an API client for Binance
```

**Problem**: AI doesn't know project structure, naming conventions, error handling approach, or testing requirements.

---

### ✅ GOOD PROMPT (Specific to Arc ZARDIAN)
```
Create a Binance exchange API client for Arc ZARDIAN that:

1. Location: src/arc_zardian/api/binance_client.py
2. Inherits from BaseExchangeClient (imported from arc_zardian.api.base_client)
3. Implements these methods:
   - fetch_rates(currency_pairs: list[str]) -> dict[str, float]
   - get_exchange_info() -> dict
4. Use type hints for all parameters and returns
5. Include Google-style docstrings
6. Handle API errors by raising APIClientError from arc_zardian.api.exceptions
7. Use requests library for HTTP calls with 10-second timeout
8. Log all requests and errors (logger = logging.getLogger(__name__))
9. Never log or store API keys
10. Create matching tests in tests/test_api/test_binance_client.py

Before writing code, confirm:
- The file location
- The inheritance structure
- Error handling approach
- Logging strategy
```

**Result**: AI generates properly structured, consistent code that fits your project.

---

## Example 2: Adding Conversion Logic

### ✅ GOOD PROMPT
```
Implement the ZAR to USDC conversion analyzer in src/arc_zardian/core/converter.py:

Requirements:
1. Create a ConversionPath dataclass in src/arc_zardian/core/models.py with fields:
   - exchanges: list[str] (exchanges used in path)
   - rates: dict[str, float] (exchange rates)
   - fees: dict[str, float] (fees per exchange)
   - total_cost: float (total fees paid)

2. Create ZARtoUSDCConverter class with methods:
   - find_optimal_path(amount: float) -> ConversionPath
   - calculate_total_cost(path: ConversionPath) -> float
   
3. Use async/await with aiohttp to fetch rates from multiple exchanges concurrently

4. Raise ValidationError if amount is invalid (must be > 0)

5. Add comprehensive logging:
   - INFO: "Starting conversion path analysis"
   - ERROR: "Failed to fetch from {exchange}"
   
6. Include docstrings with examples

7. Create tests that:
   - Mock API calls
   - Test success path
   - Test error cases
   - Verify optimal path selection

Are you ready to proceed?
```

---

## Example 3: Writing Tests

### ✅ GOOD PROMPT
```
Write unit tests for the ConversionPath model in tests/test_core/test_models.py:

Test cases needed:
1. test_conversion_path_creation_with_valid_data()
   - Verify ConversionPath instantiates correctly
   
2. test_conversion_path_invalid_negative_cost()
   - Should raise ValueError when total_cost < 0
   
3. test_conversion_path_field_validation()
   - Verify all fields match expected types
   
4. test_conversion_path_str_representation()
   - Verify string representation is human-readable

Use fixtures for reusable test data:
- valid_path_data fixture
- mock_exchange_rates fixture

Mock external dependencies. Use pytest.

What additional edge cases should I consider?
```

---

## Example 4: CLI Development

### ✅ GOOD PROMPT
```
Create the CLI interface in src/arc_zardian/presentation/cli.py using Click:

Requirements:
1. Main command: zardian convert <amount>
   - argument: amount (float, ZAR amount to convert)
   - option: --target-currency (default: USDC)
   - option: --exchanges (comma-separated: binance,coinbase,kraken)

2. Call converter.find_optimal_path(amount)

3. Format output with:
   - Optimal path details
   - Exchange costs breakdown
   - Total cost summary
   - Estimated USDC received

4. Error handling:
   - Catch ValidationError -> show helpful message
   - Catch APIClientError -> suggest retrying
   - Show stack trace only if --debug flag set

5. Load config from .env via arc_zardian.config

6. Use logging for operations

Entry point in pyproject.toml:
[project.scripts]
zardian = "arc_zardian.main:cli"

Does this match your vision for the CLI?
```

---

## Example 5: Asking for Help with Debugging

### ✅ GOOD PROMPT
```
I'm getting a KeyError when parsing the Binance API response in src/arc_zardian/api/binance_client.py.

Current code snippet:
[paste your code]

The error occurs at line: rate = response['data']['price']

Debug checklist:
1. Print the actual response structure to understand it
2. Add defensive parsing with .get() method
3. Log the full response if parsing fails
4. Raise APIClientError with descriptive message
5. Add error case to tests

Can you:
- Show what the response structure likely is
- Fix the parsing to be more robust
- Add appropriate logging
- Create a test that covers this scenario
```

---

## Example 6: Code Review Request

### ✅ GOOD PROMPT
```
Please review this code snippet for Arc ZARDIAN:

[paste code]

Check for:
1. Type hint completeness - are all parameters and returns typed?
2. Docstring quality - does it follow Google style? Examples included?
3. Error handling - are all exceptions caught and handled?
4. Security - any hardcoded values, secrets, or unsafe operations?
5. PEP 8 compliance - line length, indentation, naming?
6. Testability - is this function easy to test?
7. Performance - any obvious inefficiencies?

Suggest specific improvements with code examples.

Rating on 1-10 (10 = production ready): ?
```

---

## Example 7: Implementing Async Concurrent Calls

### ✅ GOOD PROMPT
```
I need to fetch rates from Binance, Coinbase, and Kraken concurrently in 
src/arc_zardian/core/converter.py.

Current approach (sequential):
```python
rates = {}
for exchange in exchanges:
    rates[exchange] = await client.fetch_rates(exchange)
```

Requirements:
1. Use asyncio.gather() to fetch all in parallel
2. Use aiohttp.ClientSession for connection pooling
3. Set timeout to 10 seconds per request
4. If one exchange fails, continue with others
5. Log successes and failures
6. Return dict: {'exchange_name': rates_dict}

Create:
- The concurrent fetching function
- Error handling for individual exchange timeouts
- Tests using pytest-asyncio
- Example usage in main()

Make sure it's efficient for 3 exchanges.
```

---

## Best Practices Demonstrated

### 1. **Specific Context**
Always mention:
- Exact file location
- Related modules/classes
- Expected behavior

### 2. **Clear Requirements**
List numbered requirements, not prose descriptions.

### 3. **Security First**
Explicitly mention security considerations.

### 4. **Testing Intent**
Ask for test cases alongside code.

### 5. **Error Handling**
Specify how errors should be handled.

### 6. **Confirmation**
Ask clarifying questions before AI writes code.

---

## Copy-Paste Master Prompt Template

When starting a new development session with Windsurf or Copilot, use this template:

```
PROJECT: Arc ZARDIAN
====================

This is a Python project to find optimal ZAR → USDC conversion paths.

STRUCTURE:
- Code: src/arc_zardian/
- Tests: tests/
- CLI entry: src/arc_zardian/main.py

REQUIREMENTS FOR ALL CODE:
1. Type hints on all functions: def func(param: str) -> bool:
2. Google-style docstrings with Args, Returns, Raises, Example
3. PEP 8 compliance (4 spaces, max 88 chars, snake_case, etc.)
4. Error handling with custom exceptions from exceptions.py
5. Logging with logger = logging.getLogger(__name__)
6. No hardcoded secrets (use .env via config.py)
7. Tests that mock external dependencies

LIBRARIES TO USE:
- requests (HTTP)
- aiohttp (async HTTP)
- click (CLI)
- pydantic (validation)
- pytest (testing)

NEVER USE:
- print() in production code
- bare except:
- hardcoded API keys

TASK:
[Your specific request here]

Before coding, ask any clarifying questions.
```

---

## Signs Your Prompt Worked Well

✅ AI generated code that:
- Follows your naming conventions exactly
- Includes complete type hints
- Has Google-style docstrings
- Fits your project structure
- Includes error handling
- Includes tests
- Mentions security considerations
- Asks clarifying questions first

❌ Red flags indicating unclear prompt:
- Code doesn't match your file structure
- Missing type hints
- No docstrings
- Hardcoded values
- Generic error handling (bare `except:`)
- No tests included
- Uses unauthorized libraries

---

## Summary

The key to effective AI collaboration is:

1. **Provide context**: Project structure, conventions, tech stack
2. **Be specific**: File locations, method signatures, error handling
3. **Ask clearly**: Numbered requirements, not prose
4. **Verify**: Check generated code against your standards
5. **Iterate**: Ask follow-up questions if results don't match expectations

Use the master prompt from the main guide at the start of each session, then adapt specific requests as shown in these examples.
