# Arc ZARDIAN Custom Instructions for GitHub Copilot

> 📋 **Location in Repository**: `.github/copilot-instructions.md`
>
> **Usage**: Place this file in your `.github/` directory and GitHub Copilot will automatically apply these instructions to all AI-assisted code generation in this repository.

---

## Project Context

**Project Name**: Arc ZARDIAN

**Description**: 
Arc ZARDIAN is an AI agent designed to find the most efficient conversion path from South African Rand (ZAR) to USDC (USD Coin). The agent:
- Fetches real-time exchange rates from multiple crypto exchanges (Binance, Coinbase, Kraken)
- Analyzes conversion paths considering exchange fees, transaction costs, and slippage
- Determines the optimal route to minimize total conversion cost
- Presents results via CLI interface

**Technology Stack**: Python 3.9+, requests, aiohttp, click, pydantic, pytest

**Development Context**: Solo developer using AI assistance for code generation and optimization.

---

## Project Structure

```
arc_zardian/
├── src/arc_zardian/              # Main package
│   ├── api/                       # Exchange API clients
│   ├── core/                      # Core conversion logic
│   ├── utils/                     # Utilities
│   ├── presentation/              # CLI and output
│   ├── config.py                  # Configuration
│   └── logger.py                  # Logging
├── tests/                         # Test suite
├── docs/                          # Documentation
├── .env.example                   # Environment template
└── requirements.txt               # Dependencies
```

---

## Coding Standards & Conventions

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | PascalCase | `BinanceClient`, `ConversionPath` |
| Functions | snake_case | `fetch_exchange_rates()`, `calculate_fees()` |
| Variables | snake_case | `total_cost`, `exchange_rate` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_TIMEOUT` |
| Exceptions | PascalCase + "Error/Exception" | `APIClientError`, `ValidationException` |
| Private members | Leading underscore | `_internal_session`, `_cache` |

### Code Style Requirements

**Mandatory PEP 8 Compliance**:
- ✅ 4 spaces for indentation
- ✅ Maximum 88-100 characters per line
- ✅ 2 blank lines before top-level functions/classes
- ✅ 1 blank line between methods
- ✅ Use double quotes for strings: `"string"` not `'string'`

**Type Hints** (REQUIRED for all functions):
```python
def fetch_rates(exchange: str, currencies: list[str]) -> dict[str, float]:
    """Fetch exchange rates."""
    pass
```

**Docstrings** (Google style):
```python
def calculate_fee(amount: float, percentage: float) -> float:
    """Calculate conversion fee.
    
    Args:
        amount (float): Transaction amount in ZAR.
        percentage (float): Fee percentage.
    
    Returns:
        float: Calculated fee amount.
    
    Raises:
        ValueError: If amount or percentage is negative.
    """
    pass
```

### Import Organization

Always organize imports in this order:
1. Standard library
2. Third-party libraries
3. Local imports

```python
import os
import logging
from datetime import datetime
from typing import Optional

import requests
import aiohttp
from dotenv import load_dotenv

from arc_zardian.api.base_client import BaseExchangeClient
from arc_zardian.core.models import ConversionPath
```

---

## Technology Stack Rules

### Approved Libraries (Use These)
- `requests==2.31.0` → Synchronous HTTP requests
- `aiohttp==3.9.1` → Async HTTP for concurrent API calls
- `python-dotenv==1.0.0` → Environment variable management
- `click==8.1.7` → CLI framework
- `pydantic==2.5.0` → Data validation
- `pytest==7.4.3` → Testing framework

### Forbidden Without Approval
- ❌ pandas (use only if data analysis is necessary)
- ❌ Django/Flask (too heavy for this project)
- ❌ Multiple HTTP libraries (use requests + aiohttp only)
- ❌ Custom ORM (use dataclasses instead)

---

## Security Requirements

### API Key Management (Non-Negotiable)

1. **Never hardcode API keys** in source code
2. **Never commit `.env` files** to version control
3. **Always use environment variables** via `python-dotenv`
4. **Always validate** required keys at startup

**Pattern to Follow**:
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
    
    @classmethod
    def validate(cls) -> None:
        required = ["BINANCE_API_KEY", "BINANCE_API_SECRET"]
        missing = [k for k in required if not os.getenv(k)]
        if missing:
            raise ValueError(f"Missing: {', '.join(missing)}")
```

**.gitignore must include**:
```
.env
.env.local
*.log
__pycache__/
.pytest_cache/
```

---

## Exception Handling & Logging

### Custom Exception Hierarchy
```python
# In arc_zardian/api/exceptions.py

class ArcZardianError(Exception):
    """Base exception."""
    pass

class APIClientError(ArcZardianError):
    """Raised when API request fails."""
    pass

class ValidationError(ArcZardianError):
    """Raised when input validation fails."""
    pass
```

### Logging Requirements
- Use `logging` module, never `print()` for production code
- Get logger: `logger = logging.getLogger(__name__)`
- Use structured JSON logging (optional: `python-json-logger`)
- Always use `logger.exception()` in except blocks
- Never log sensitive data (API keys, secrets)

**Example**:
```python
import logging

logger = logging.getLogger(__name__)

try:
    rate = fetch_exchange_rate(exchange)
except TimeoutError as e:
    logger.error("Exchange timeout", exc_info=True)
    raise APIClientError("Exchange unavailable") from e
```

---

## Async/Concurrent API Calls

When fetching from multiple exchanges, use async/await with aiohttp:

```python
import asyncio
import aiohttp

async def fetch_all_rates(exchanges: list[str]) -> dict:
    """Fetch rates from all exchanges concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_from_exchange(session, exchange) 
            for exchange in exchanges
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {ex: rate for ex, rate in zip(exchanges, results)}
```

---

## Testing Requirements

### Test Location & Structure
- Test files: `tests/test_{module}/test_{function}.py`
- Use pytest with fixtures for setup
- Mock external API calls (use `unittest.mock`)
- Test both success and failure paths
- Use `pytest.raises()` for exception testing

**Example**:
```python
# tests/test_api/test_binance_client.py

import pytest
from unittest.mock import patch, Mock
from arc_zardian.api.binance_client import BinanceClient
from arc_zardian.api.exceptions import APIClientError

class TestBinanceClient:
    @pytest.fixture
    def client(self):
        return BinanceClient()
    
    def test_fetch_rates_success(self, client):
        with patch.object(client, '_request') as mock:
            mock.return_value = {'ZAR_USDC': 0.055}
            rates = client.fetch_rates(['ZAR', 'USDC'])
            assert rates['ZAR_USDC'] == 0.055
    
    def test_fetch_rates_api_error(self, client):
        with patch.object(client, '_request', side_effect=APIClientError('Timeout')):
            with pytest.raises(APIClientError):
                client.fetch_rates(['ZAR'])
```

---

## File-Specific Rules

### For API Clients (src/arc_zardian/api/)
- Always inherit from `BaseExchangeClient`
- Implement abstract methods: `fetch_rates()`, `get_limits()`
- Include retry logic for failed requests
- Validate API responses with Pydantic models
- Use type hints for all parameters and returns
- Document API endpoints in docstrings

### For Core Logic (src/arc_zardian/core/)
- Use dataclasses or Pydantic for data models
- Keep functions focused (max ~30 lines)
- Prefer composition over inheritance
- Include comprehensive error handling
- Add docstrings with examples
- Consider performance: use async where applicable

### For Utilities (src/arc_zardian/utils/)
- Pure functions without side effects preferred
- Document assumptions and constraints
- Include type hints and docstrings
- Keep functions reusable and modular

### For CLI (src/arc_zardian/presentation/)
- Use Click for command-line interface
- Validate user input at CLI boundary
- Format output for human readability
- Handle errors gracefully with helpful messages

### For Tests (tests/)
- Use descriptive test names: `test_<what>_<condition>_<result>`
- Mock external dependencies
- Use fixtures for reusable setup
- Achieve minimum 80% code coverage

---

## Code Generation Guidelines

When generating code, follow these principles:

### DO:
✅ Always include type hints on all functions
✅ Write Google-style docstrings for public APIs
✅ Use async/await for I/O operations
✅ Implement proper error handling with custom exceptions
✅ Add logging at critical points
✅ Create matching test cases
✅ Follow project structure exactly
✅ Validate security: no hardcoded secrets

### DON'T:
❌ Use bare `except:` or `except Exception:`
❌ Hardcode configuration values
❌ Use `print()` in production code
❌ Create unnecessary abstractions
❌ Ignore edge cases in error handling
❌ Skip docstrings or type hints
❌ Mix synchronous and asynchronous code carelessly

---

## Performance Considerations

1. **Concurrent API Calls**: Use aiohttp for parallel requests to multiple exchanges
2. **Caching**: Implement simple TTL cache for rate data if high frequency queries
3. **Timeouts**: Always set request timeouts (default 10 seconds)
4. **Rate Limiting**: Respect API rate limits; implement backoff strategy if needed
5. **Profiling**: Profile before optimizing; document performance constraints

---

## Deployment Checklist

Before marking code as "ready":
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] PEP 8 compliant (run `pylint` or `black`)
- [ ] Tests pass with `pytest --cov` (≥80% coverage)
- [ ] No hardcoded secrets or credentials
- [ ] `.env.example` updated with all required variables
- [ ] Imports organized correctly
- [ ] Error handling comprehensive
- [ ] Logging includes context (exchange name, amounts, etc.)
- [ ] README.md updated if adding new features

---

## Quick Reference: AI Prompting

When asking for code generation, be specific:

**For New Features:**
```
Create a [component] in src/arc_zardian/[module]/ that:
1. Inherits from [base class if applicable]
2. Includes type hints and Google-style docstrings
3. Uses async/await for [operation]
4. Handles [specific error cases]
5. Includes tests in tests/test_[module]/
```

**For Debugging:**
```
Fix the [issue] in [file] while ensuring:
1. Error is properly logged
2. Appropriate exception is raised
3. Test case covers this scenario
4. No breaking changes to existing API
```

**For Code Review:**
```
Review this code for:
1. Type hint completeness
2. Security issues (especially API key handling)
3. Error handling coverage
4. PEP 8 compliance
5. Performance bottlenecks
6. Test adequacy
```

---

## Key Contacts & Resources

- **Python PEP 8**: https://peps.python.org/pep-0008/
- **Type Hints Guide**: https://realpython.com/python-type-checking/
- **Async/Await**: https://docs.python.org/3/library/asyncio.html
- **Pytest Docs**: https://docs.pytest.org/
- **Click CLI Docs**: https://click.palletsprojects.com/

---

**Last Updated**: 2025-11-04  
**Version**: 1.0  
**Status**: Active
