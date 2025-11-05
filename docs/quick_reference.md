# Arc ZARDIAN: AI Collaboration Quick Reference

**One-page summary for quick access during development**

---

## Files You've Received

| File | Purpose | Use When |
|------|---------|----------|
| **arc_zardian_guide.md** | Complete guide (13 sections) | First time setup & comprehensive reference |
| **copilot_instructions.md** | GitHub Copilot/Windsurf rules | Copy to `.github/copilot-instructions.md` |
| **ai_prompting_examples.md** | Example prompts for common tasks | Asking AI for features/fixes |
| **implementation_roadmap.md** | 10-day implementation plan | Phase-by-phase development |
| **quick_reference.md** | This file! | Quick lookup during coding |

---

## Master Prompt (Use at Session Start)

Copy-paste this into Windsurf/Copilot at the beginning of each session:

```
PROJECT: Arc ZARDIAN
Technology: Python 3.9+, requests, aiohttp, click, pydantic, pytest

CODING RULES FOR ALL CODE:
1. Type hints: def func(param: str) -> dict:
2. Docstrings: Google style with Args, Returns, Raises, Example
3. PEP 8: 4 spaces, 88 char max, snake_case, UPPER_SNAKE_CASE for constants
4. Structure: src/arc_zardian/ for code, tests/ for tests
5. Naming: PascalCase classes, snake_case functions/variables
6. Exceptions: raise APIClientError, ValidationError from exceptions.py
7. Logging: logger = logging.getLogger(__name__) (no print())
8. Security: NO hardcoded secrets (use .env via config.py)
9. Testing: Include tests for all new code, mock external APIs
10. Async: Use aiohttp + asyncio.gather() for concurrent API calls

STRUCTURE:
- src/arc_zardian/api/ → Exchange API clients
- src/arc_zardian/core/ → Conversion logic
- src/arc_zardian/presentation/ → CLI interface
- tests/ → Test suite

BEFORE CODING, ask clarifying questions about:
- Exact file location
- Error handling approach
- Whether async/concurrent is needed
- Test strategy

NEVER USE: print(), bare except:, hardcoded values, pandas (unless needed)
```

---

## Prompt Template for Common Tasks

### Feature Request
```
Create [component] in [location]:
1. [Requirement 1]
2. [Requirement 2]
...
Include: type hints, docstrings, error handling, logging, tests
Location: src/arc_zardian/[path]
Tests go in: tests/test_[path]
Before coding, confirm the approach.
```

### Bug Fix
```
Fix [bug] in [file]:
1. Analyze root cause
2. Apply fix with proper logging
3. Add test case for this scenario
4. Verify no breaking changes
Include error handling and security considerations.
```

### Code Review
```
Review this code for:
1. Type hints complete?
2. Docstring quality (Google style)?
3. Error handling comprehensive?
4. No hardcoded secrets?
5. PEP 8 compliant?
6. Testable?
7. Any performance issues?

[Paste code]
```

---

## Essential Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run application
zardian convert 1000

# Testing
pytest                           # Run all tests
pytest --cov=src/arc_zardian   # With coverage
pytest -v                        # Verbose
pytest tests/test_api/          # Specific directory

# Code quality
black src/                       # Format code
pylint src/arc_zardian          # Lint
mypy src/arc_zardian            # Type checking

# Development
git add .
git commit -m "Feature: description"
git push
```

---

## Naming Quick Reference

```python
# Classes (PascalCase)
class BinanceClient: pass
class ConversionPath: pass

# Functions (snake_case)
def fetch_rates() -> dict: pass
def calculate_fees() -> float: pass

# Constants (UPPER_SNAKE_CASE)
MAX_RETRIES = 3
API_TIMEOUT = 10

# Variables (snake_case)
exchange_rate = 0.055
total_cost = 50.0

# Exceptions (Suffix with Error/Exception)
raise APIClientError("message")
raise ValidationError("message")

# Private (underscore prefix)
def _internal_method(): pass
self._private_field = None
```

---

## Docstring Template (Google Style)

```python
def function_name(param1: str, param2: int) -> bool:
    """One-line summary.
    
    Longer description if needed (1-2 sentences).
    
    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.
    
    Returns:
        bool: Description of return value.
    
    Raises:
        ValueError: When param1 is empty.
        APIClientError: When API request fails.
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

---

## Error Handling Pattern

```python
import logging
from arc_zardian.api.exceptions import APIClientError, ValidationError

logger = logging.getLogger(__name__)

try:
    result = fetch_from_api()
except ValueError as e:
    logger.error("Invalid input: %s", e, exc_info=True)
    raise ValidationError(f"Invalid input: {e}") from e
except TimeoutError as e:
    logger.error("API timeout", exc_info=True)
    raise APIClientError("Exchange API timeout") from e
except Exception as e:
    logger.critical("Unexpected error", exc_info=True)
    raise
```

---

## Async/Concurrent Pattern

```python
import asyncio
import aiohttp

async def fetch_all_rates():
    """Fetch rates from multiple exchanges concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_from_exchange(session, ex)
            for ex in ["binance", "coinbase", "kraken"]
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {ex: rate for ex, rate in zip(exchanges, results)}

# In main function
if __name__ == "__main__":
    rates = asyncio.run(fetch_all_rates())
    print(rates)
```

---

## Type Hints Quick Reference

```python
from typing import Optional, Dict, List, Tuple, Union

# Basic types
def func(name: str, count: int, price: float, active: bool) -> None:
    pass

# Collections
def func(items: list[str]) -> dict[str, int]:
    pass

# Optional (nullable)
def func(optional_param: Optional[str] = None) -> Optional[int]:
    pass

# Multiple types
def func(value: Union[str, int]) -> Union[str, int]:
    pass

# Class instances
def func(client: BinanceClient) -> ConversionPath:
    pass
```

---

## Testing Pattern with Pytest

```python
import pytest
from unittest.mock import Mock, patch
from arc_zardian.api.binance_client import BinanceClient

class TestBinanceClient:
    @pytest.fixture
    def client(self):
        return BinanceClient()
    
    def test_fetch_rates_success(self, client):
        with patch.object(client, '_request') as mock:
            mock.return_value = {'ZAR_USDC': 0.055}
            rates = client.fetch_rates(['ZAR', 'USDC'])
            assert rates['ZAR_USDC'] == 0.055
    
    def test_fetch_rates_error(self, client):
        with patch.object(client, '_request', side_effect=Exception('API Error')):
            with pytest.raises(Exception):
                client.fetch_rates(['ZAR'])
```

---

## Security Checklist

- [ ] No API keys in source code
- [ ] .env file added to .gitignore
- [ ] .env.example has template values only
- [ ] Config.py loads from os.getenv()
- [ ] API keys validated at startup
- [ ] No secrets logged
- [ ] Use HTTPS for all API calls
- [ ] Validate API responses
- [ ] Set request timeouts

---

## Code Quality Checklist (Before Commit)

- [ ] All functions have type hints: `def func(param: str) -> dict:`
- [ ] All public functions have docstrings (Google style)
- [ ] No bare `except:` statements
- [ ] No hardcoded values (use constants)
- [ ] PEP 8 compliant (4 spaces, 88 chars max)
- [ ] No `print()` in production code (use logging)
- [ ] Tests written and passing
- [ ] No unused imports
- [ ] Error messages are descriptive
- [ ] Logging is informative

---

## File Structure Reference

```
arc_zardian/
├── .github/
│   └── copilot-instructions.md    ← Copy here
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/arc_zardian/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── api/
│   │   ├── base_client.py
│   │   ├── binance_client.py
│   │   ├── exceptions.py
│   │   └── ...
│   ├── core/
│   │   ├── models.py
│   │   ├── converter.py
│   │   └── ...
│   ├── presentation/
│   │   └── cli.py
│   └── utils/
├── tests/
│   ├── test_api/
│   ├── test_core/
│   ├── conftest.py
│   └── test_integration.py
└── docs/
```

---

## Red Flags (Don't Accept This from AI)

❌ Code without type hints  
❌ Functions > 40 lines long  
❌ No docstrings on public functions  
❌ Bare `except:` or `except Exception:`  
❌ Hardcoded API keys or values  
❌ Using `print()` in production code  
❌ No error handling  
❌ `from x import *`  
❌ Code that violates PEP 8  
❌ No tests for new functionality  

---

## Getting Help from AI

### ✅ Good Question
```
"Create an async function in src/arc_zardian/core/converter.py 
that fetches rates from all exchanges concurrently using aiohttp.
Include error handling, logging, and tests."
```

### ❌ Bad Question
```
"Write me code to fetch API data"
```

**Keys to Good Questions:**
1. Specific file location
2. Exact requirements (numbered)
3. Mention error handling
4. Mention testing
5. Mention logging/security

---

## Emergency Contacts

- **Type Hints**: Consult `typing` module docs
- **Async/Await**: See `asyncio` documentation
- **Testing**: Check pytest docs
- **PEP 8**: Read https://peps.python.org/pep-0008/
- **Docstrings**: Google Style Guide

---

## Version Info

- **Python**: 3.9+
- **Guide Version**: 1.0
- **Last Updated**: 2025-11-04
- **Status**: Production Ready

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" | Ensure `pip install -r requirements.txt` was run |
| Type errors | Add type hints: `def func(x: str) -> int:` |
| Missing .env | Copy `.env.example` to `.env` and fill values |
| API fails | Check logs, verify credentials in .env, ensure timeout is set |
| Tests fail | Mock external dependencies with `@patch` or `Mock` |
| Import errors | Check `__init__.py` files are present in all packages |

---

**Keep this page bookmarked for quick reference during development!**
