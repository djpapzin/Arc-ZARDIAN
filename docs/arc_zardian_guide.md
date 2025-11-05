# Arc ZARDIAN: Project Guide

## Overview
This guide provides comprehensive documentation for the Arc ZARDIAN project, including project structure, development setup, coding standards, and contribution guidelines.

## Project Structure

```text
Arc-ZARDIAN/
├── .github/               # GitHub workflows and templates
├── docs/                  # Project documentation
│   ├── ai_prompting_examples.md
│   ├── arc_zardian_guide.md
│   ├── copilot_instructions.md
│   ├── current_status.md
│   ├── getting_started.md
│   ├── implementation_roadmap.md
│   └── quick_reference.md
├── src/                   # Source code
│   └── arc_zardian/       # Main package
│       ├── core/          # Core functionality
│       │   ├── __init__.py
│       │   ├── optimizer.py  # Conversion path optimization logic
│       │   └── models.py     # Data models
│       ├── __init__.py
│       └── app.py         # Streamlit web application
├── tests/                 # Test suite
│   ├── test_presentation/ # UI/Integration tests
│   └── test_core/         # Unit tests
├── .env.example          # Example environment variables
├── .gitignore
├── pyproject.toml        # Project metadata and build configuration
└── requirements.txt      # Project dependencies
```
├── src/
│   └── arc_zardian/                      # Main package
│       ├── __init__.py                   # Package initialization
│       ├── main.py                       # Entry point / CLI interface
│       ├── config.py                     # Configuration management
│       ├── logger.py                     # Logging setup
│       │
│       ├── api/                          # API client modules
│       │   ├── __init__.py
│       │   ├── base_client.py            # Abstract base for exchange clients
│       │   ├── binance_client.py         # Binance exchange integration
│       │   ├── coinbase_client.py        # Coinbase exchange integration
│       │   ├── kraken_client.py          # Kraken exchange integration
│       │   └── exceptions.py             # Custom API exceptions
│       │
│       ├── core/                         # Core business logic
│       │   ├── __init__.py
│       │   ├── converter.py              # Conversion path logic
│       │   ├── rate_analyzer.py          # Rate and fee analysis
│       │   └── models.py                 # Data models (dataclasses)
│       │
│       ├── utils/                        # Utility functions
│       │   ├── __init__.py
│       │   ├── validators.py             # Input validation
│       │   ├── formatters.py             # Output formatting
│       │   └── cache.py                  # Simple caching utilities
│       │
│       └── presentation/                 # UI/Output layer
│           ├── __init__.py
│           ├── cli.py                    # CLI interface (using Click)
│           └── formatters.py             # Result presentation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                       # Pytest configuration and fixtures
│   ├── test_api/                         # API client tests
│   │   ├── __init__.py
│   │   ├── test_base_client.py
│   │   ├── test_binance_client.py
│   │   └── test_exceptions.py
│   ├── test_core/                        # Core logic tests
│   │   ├── __init__.py
│   │   ├── test_converter.py
│   │   └── test_rate_analyzer.py
│   └── test_integration.py               # Integration tests
│
└── docs/
    ├── API_CLIENTS.md                    # API client documentation
    ├── DEVELOPMENT.md                    # Development guidelines
    └── ARCHITECTURE.md                   # High-level architecture
```

---

## 2. Naming Conventions

### Files and Folders
- **Folder names**: `snake_case` (e.g., `api_clients`, `core_logic`)
- **Module files**: `snake_case.py` (e.g., `base_client.py`, `rate_analyzer.py`)
- **Private modules**: Prefix with underscore (e.g., `_internal_utils.py`)

### Classes
- **Public classes**: `PascalCase` (e.g., `BinanceClient`, `ConversionPath`)
- **Private classes**: Prefix with underscore (e.g., `_CacheManager`)
- **Exceptions**: Inherit from `Exception`, suffix with `Error` or `Exception` (e.g., `APIClientError`, `ValidationException`)

### Functions and Methods
- **Public functions**: `snake_case` (e.g., `fetch_exchange_rates()`, `analyze_conversion_path()`)
- **Private functions**: Prefix with underscore (e.g., `_validate_input()`)
- **Getters/Properties**: Omit "get_" prefix; use `@property` (e.g., `exchange_rate` instead of `get_exchange_rate()`)

### Variables and Constants
- **Local variables**: `snake_case` (e.g., `exchange_rate`, `user_input`)
- **Constants**: `UPPER_SNAKE_CASE` at module or class level (e.g., `MAX_RETRIES`, `API_TIMEOUT`)
- **Private attributes**: Prefix with underscore (e.g., `_session`, `_cache`)

### Naming Examples for Arc ZARDIAN
```python
# Classes
class ExchangeClient: pass
class ZARtoUSDCConverter: pass
class ConversionPath: pass

# Functions
def fetch_rates_from_exchange(exchange: str) -> dict: pass
def calculate_total_fees(path: ConversionPath) -> float: pass
def find_optimal_path(from_currency: str, to_currency: str) -> ConversionPath: pass

# Constants
MAX_API_CALLS_PER_SECOND = 5
DEFAULT_TIMEOUT_SECONDS = 10
SUPPORTED_EXCHANGES = ["binance", "coinbase", "kraken"]

# Variables
conversion_result = converter.find_best_path()
total_cost = sum(fee.amount for fee in fees)
```

---

## 3. Coding Standards & Style Guide

### PEP 8 Core Rules (Mandatory)

| Rule | Example | Rationale |
|------|---------|-----------|
| **Indentation** | 4 spaces per level | Standard across Python projects |
| **Line Length** | Max 88 characters (or 100) | Readability on most screens |
| **Imports** | Group in order: stdlib, third-party, local | Clear dependency visibility |
| **Blank Lines** | 2 before top-level functions/classes, 1 before methods | Visual separation |
| **Naming** | snake_case for functions, PascalCase for classes | Consistency and readability |
| **Operators** | Space around `=`, `==`, `!=` | Clarity |
| **Quotes** | Choose one style and be consistent (prefer double quotes `""` for strings) | Consistency |

### Imports Organization
```python
# Standard library
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Third-party libraries
import requests
import aiohttp
from dotenv import load_dotenv

# Local imports
from arc_zardian.api.base_client import BaseExchangeClient
from arc_zardian.core.converter import ConversionPath
```

### Code Formatting Best Practices
```python
# ✅ GOOD: Clear, readable, follows PEP 8
def calculate_conversion_fee(
    amount: float,
    exchange: str,
    fee_percentage: float
) -> float:
    """Calculate conversion fee for a given amount."""
    return amount * (fee_percentage / 100)


# ❌ BAD: Cramped, hard to read
def calc_fee(amt,ex,pct):return amt*(pct/100)
```

---

## 4. Docstring Conventions (Google Style)

Use **Google-style docstrings** for consistency and readability. Format:

```python
def fetch_exchange_rates(
    exchange: str,
    currencies: List[str]
) -> Dict[str, float]:
    """Fetch current exchange rates from a specific exchange.

    This function queries the specified exchange API for the latest
    conversion rates between given currency pairs.

    Args:
        exchange (str): Name of the exchange (e.g., 'binance', 'coinbase').
        currencies (List[str]): List of currency codes to fetch rates for.

    Returns:
        Dict[str, float]: Dictionary mapping currency pairs to rates.
            Example: {'ZAR_USDC': 0.055, 'USD_USDC': 1.0}

    Raises:
        APIClientError: If the exchange API request fails.
        ValidationError: If exchange name or currencies are invalid.

    Example:
        >>> rates = fetch_exchange_rates('binance', ['ZAR', 'USDC'])
        >>> print(rates)
        {'ZAR_USDC': 0.055}
    """
    # Implementation here
    pass
```

### Docstring Structure
1. **Summary**: One-line description (fits on one line)
2. **Description**: Detailed explanation (optional, 1-3 sentences)
3. **Args**: Parameter documentation with types
4. **Returns**: Return value type and description
5. **Raises**: Exceptions that may be raised
6. **Example**: Usage example (optional but recommended)

For **classes**, document the class and `__init__` separately:
```python
class ExchangeClient:
    """Base class for cryptocurrency exchange API clients.

    This class provides a template for implementing exchange-specific clients
    that fetch rates and execute conversions.

    Attributes:
        api_key (str): The API key for the exchange.
        base_url (str): The base URL for the exchange API.
        timeout (int): Request timeout in seconds.
    """

    def __init__(self, api_key: str, base_url: str, timeout: int = 10):
        """Initialize the exchange client.

        Args:
            api_key (str): API key for authentication.
            base_url (str): Base URL for the exchange API.
            timeout (int, optional): Request timeout. Defaults to 10.

        Raises:
            ValueError: If api_key or base_url is empty.
        """
```

---

## 5. Type Hinting Best Practices

Use type hints for all functions and methods. Python 3.9+ allows using built-in types directly:

```python
from typing import Dict, List, Optional, Tuple, Union
from arc_zardian.core.models import ConversionPath, ExchangeRate

# ✅ Function with type hints
def find_optimal_conversion_path(
    start_currency: str,
    end_currency: str,
    amount: float,
    max_hops: int = 3
) -> Optional[ConversionPath]:
    """Find the optimal conversion path with minimal fees."""
    pass


# ✅ Complex return types
def analyze_multiple_paths(
    paths: List[ConversionPath]
) -> Dict[str, Union[float, List[str]]]:
    """Analyze multiple conversion paths.

    Returns:
        Dict with keys 'total_cost' (float) and 'exchanges' (List[str]).
    """
    pass


# ✅ Class attributes with type hints
class ExchangeRate:
    exchange: str
    currency_pair: str
    rate: float
    timestamp: datetime
    
    def __init__(
        self,
        exchange: str,
        currency_pair: str,
        rate: float,
        timestamp: Optional[datetime] = None
    ) -> None:
        self.exchange = exchange
        self.currency_pair = currency_pair
        self.rate = rate
        self.timestamp = timestamp or datetime.now()
```

### Type Hinting Guidelines
- Use `Optional[T]` for nullable types instead of `Union[T, None]`
- Use `List[T]`, `Dict[K, V]`, `Tuple[T, ...]` for collections
- Avoid `Any` unless absolutely necessary; use specific types or generics
- For dataclasses, use `@dataclass` from `dataclasses` module

---

## 6. Technology Stack (Minimal Dependencies)

### Core Dependencies
```
# requirements.txt - Pinned for reproducibility
requests==2.31.0          # HTTP client for REST APIs
aiohttp==3.9.1            # Async HTTP client (for concurrent API calls)
python-dotenv==1.0.0      # Environment variable management
click==8.1.7              # CLI framework (simple and intuitive)

# Data and validation
pydantic==2.5.0           # Data validation using type hints
pandas==2.1.1             # Data analysis (optional, if needed for analysis)

# Testing and development
pytest==7.4.3
pytest-asyncio==0.21.1    # For async test support
pytest-cov==4.1.0         # Coverage reporting
pytest-mock==3.12.0       # Mocking support

# Logging and monitoring
python-json-logger==2.0.7 # Structured JSON logging
```

### Why These Libraries?
- **requests**: Simple, well-documented, industry standard for HTTP
- **aiohttp**: Enables concurrent API calls without threading complexity
- **python-dotenv**: Secure credential management via `.env` files
- **click**: Lightweight CLI framework, minimal boilerplate
- **streamlit**: Web application framework for interactive UI
- **pydantic**: Type-safe data validation using Python types
- **pytest**: Industry standard testing framework
- **python-json-logger**: Structured logging for easier debugging and monitoring

### Avoid
- ❌ ORM frameworks for simple data structures (use dataclasses instead)
- ❌ Heavy frameworks like Django (overkill for this use case)
- ❌ Unnecessary abstraction layers
- ❌ Multiple HTTP libraries (stick with requests + aiohttp)

---

## 7. Security & API Key Management

### Non-Negotiable Rules

1. **Never hardcode API keys** in source files
2. **Never commit `.env` files** to version control
3. **Always use `.env.example`** as a template for required variables
4. **.gitignore must exclude** `.env`, `*.log`, `__pycache__`, `.pytest_cache`

### Implementation Pattern

#### `.env.example` (Commit to repository)
```
# Exchange API Keys
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here

COINBASE_API_KEY=your_key_here
COINBASE_API_SECRET=your_secret_here

# Application settings
LOG_LEVEL=INFO
MAX_RETRIES=3
API_TIMEOUT=10
```

#### `.env` (Local only, add to .gitignore)
```
BINANCE_API_KEY=actual_production_key_12345
BINANCE_API_SECRET=actual_secret_abcde
# ... rest of configuration
```

#### `.gitignore`
```
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

#### `config.py` (Load and validate environment variables)
```python
import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Application configuration from environment variables."""

    # Exchange API credentials
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    
    COINBASE_API_KEY: str = os.getenv("COINBASE_API_KEY", "")
    COINBASE_API_SECRET: str = os.getenv("COINBASE_API_SECRET", "")

    # Application settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "10"))

    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        required_keys = [
            "BINANCE_API_KEY",
            "BINANCE_API_SECRET",
            "COINBASE_API_KEY",
            "COINBASE_API_SECRET",
        ]
        
        missing = [key for key in required_keys if not os.getenv(key)]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


# Usage in other modules
if __name__ == "__main__":
    Config.validate()
    print(f"Binance API Key: {Config.BINANCE_API_KEY[:5]}...")
```

#### Usage in API Clients
```python
from arc_zardian.config import Config


class BinanceClient:
    """Binance exchange API client."""

    def __init__(self):
        """Initialize with credentials from environment."""
        self.api_key = Config.BINANCE_API_KEY
        self.api_secret = Config.BINANCE_API_SECRET
        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Binance credentials not configured. "
                "Set BINANCE_API_KEY and BINANCE_API_SECRET in .env"
            )
```

---

## 8. Error Handling & Logging

### Custom Exception Hierarchy
```python
# arc_zardian/api/exceptions.py

class ArcZardianError(Exception):
    """Base exception for Arc ZARDIAN."""
    pass


class APIClientError(ArcZardianError):
    """Raised when an API request fails."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(ArcZardianError):
    """Raised when input validation fails."""
    pass


class ConfigurationError(ArcZardianError):
    """Raised when configuration is invalid."""
    pass
```

### Logging Setup
```python
# arc_zardian/logger.py

import logging
import json
from datetime import datetime
from arc_zardian.config import Config


class JsonFormatter(logging.Formatter):
    """Format logs as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }
        
        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configure only if not already configured
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(Config.LOG_LEVEL)
    
    return logger
```

### Usage in Code
```python
import logging
from arc_zardian.logger import get_logger
from arc_zardian.api.exceptions import APIClientError

logger = get_logger(__name__)


def fetch_rates(exchange: str) -> dict:
    """Fetch rates with proper error handling and logging."""
    try:
        logger.info(f"Fetching rates from {exchange}")
        rates = _call_api(exchange)
        logger.info(f"Successfully fetched {len(rates)} rates from {exchange}")
        return rates
    
    except TimeoutError as e:
        logger.error(f"Timeout when fetching from {exchange}", exc_info=True)
        raise APIClientError(f"{exchange} API timeout") from e
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise
```

---

## 9. Testing Strategy

### Test Structure
```python
# tests/test_core/test_converter.py

import pytest
from unittest.mock import Mock, patch
from arc_zardian.core.converter import ConversionPath, ZARtoUSDCConverter
from arc_zardian.api.exceptions import ValidationError


class TestZARtoUSDCConverter:
    """Test suite for ZAR to USDC conversion logic."""

    @pytest.fixture
    def converter(self):
        """Create a converter instance for testing."""
        return ZARtoUSDCConverter()

    @pytest.fixture
    def mock_exchange_rates(self):
        """Mock exchange rates."""
        return {
            "binance": {"ZAR_USDC": 0.055},
            "coinbase": {"ZAR_USDC": 0.0551},
        }

    def test_find_optimal_path_returns_path(self, converter, mock_exchange_rates):
        """Test that find_optimal_path returns a ConversionPath object."""
        with patch.object(converter, "_fetch_rates", return_value=mock_exchange_rates):
            path = converter.find_optimal_path(1000)
            assert isinstance(path, ConversionPath)
            assert path.total_cost >= 0

    def test_find_optimal_path_invalid_amount_raises_error(self, converter):
        """Test that invalid amounts raise ValidationError."""
        with pytest.raises(ValidationError):
            converter.find_optimal_path(-100)

    def test_calculate_fees_with_multiple_exchanges(self, converter):
        """Test fee calculation across multiple exchanges."""
        path = ConversionPath(
            exchanges=["binance", "coinbase"],
            total_cost=50.0,
        )
        fees = converter.calculate_fees(path)
        assert len(fees) == 2
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=arc_zardian --cov-report=html

# Run specific test file
pytest tests/test_core/test_converter.py

# Run with verbose output
pytest -v
```

---

## 10. Master Prompt for AI Assistants

Copy and use this prompt at the start of each Windsurf/Copilot session. This ensures the AI follows your project standards consistently.

### **Master Prompt for Arc ZARDIAN Development**

```
PROJECT CONTEXT
===============
Project: Arc ZARDIAN
Purpose: An AI agent that finds the most efficient conversion path from South African Rand (ZAR) to USDC (stablecoin), by fetching data from multiple crypto exchange APIs, analyzing rates and fees, and presenting the optimal choice.
Tech Stack: Python 3.9+, requests, aiohttp, click, pydantic, pytest
Development Style: Solo developer, using AI assistance

PROJECT STRUCTURE
=================
Root directory: arc_zardian/
- src/arc_zardian/       → Main package code
- tests/                 → Test suite
- .env                   → Local environment variables (never commit)
- .env.example           → Template for .env
- pyproject.toml         → Project metadata
- requirements.txt       → Pinned dependencies

FOLDER ORGANIZATION RULES
=========================
1. API Clients: src/arc_zardian/api/
   - base_client.py      → Abstract base class
   - binance_client.py   → Exchange-specific implementations
   - coinbase_client.py  → Exchange-specific implementations
   - kraken_client.py    → Exchange-specific implementations
   - exceptions.py       → Custom exceptions

2. Core Logic: src/arc_zardian/core/
   - converter.py        → Main conversion path logic
   - rate_analyzer.py    → Rate and fee analysis
   - models.py           → Data models (dataclasses, Pydantic models)

3. Utilities: src/arc_zardian/utils/
   - validators.py       → Input validation
   - formatters.py       → Output formatting
   - cache.py            → Simple caching

4. Presentation: src/arc_zardian/presentation/
   - cli.py              → CLI interface using Click
   - formatters.py       → Result presentation

NAMING CONVENTIONS
==================
Classes: PascalCase (ExchangeClient, ConversionPath)
Functions: snake_case (fetch_rates, calculate_fees)
Variables: snake_case (exchange_rate, user_input)
Constants: UPPER_SNAKE_CASE (MAX_RETRIES, API_TIMEOUT)
Private members: Prefix with underscore (_internal_method)
Exceptions: Suffix with Error or Exception (APIClientError, ValidationException)

CODING STANDARDS
================
1. PEP 8 compliance is mandatory:
   - 4 spaces indentation
   - Max 88-100 characters per line
   - 2 blank lines before top-level functions/classes
   - 1 blank line between methods

2. Type hints REQUIRED for all functions:
   def function_name(param: str, amount: float) -> dict:
   - Use Python 3.9+ syntax: list[str] instead of List[str]
   - Use Optional[T] for nullable types
   - Avoid Any

3. Docstrings: Google style format
   - One-line summary
   - Detailed description (if needed)
   - Args: with types and descriptions
   - Returns: with type and description
   - Raises: list exceptions that may be raised
   - Example: usage example (recommended)

4. Imports organization:
   - Standard library first
   - Third-party libraries second
   - Local imports third
   - Alphabetically sorted within groups

5. Code organization:
   - Group imports at top
   - Define constants after imports
   - Define classes before functions that use them
   - Use __all__ to define public API

TECHNOLOGY STACK RULES
======================
APPROVED libraries (use these):
- requests 2.31.0        → HTTP requests (synchronous)
- aiohttp 3.9.1          → Async HTTP (for concurrent calls)
- python-dotenv 1.0.0    → Environment variables
- click 8.1.7            → CLI framework
- pydantic 2.5.0         → Data validation
- pytest 7.4.3           → Testing

DO NOT USE without permission:
- pandas                 → Only if absolutely necessary for data analysis
- Django/Flask          → Overkill for this project
- Multiple HTTP libs    → Use requests + aiohttp only
- Custom ORM            → Use dataclasses for simple structures

SECURITY & API KEY MANAGEMENT
==============================
1. NEVER hardcode API keys in source files
2. NEVER commit .env files
3. ALWAYS use environment variables via python-dotenv
4. ALWAYS add .env to .gitignore
5. Configuration module pattern:
   - Create config.py that loads from os.getenv()
   - Import Config class in other modules
   - Validate required keys at startup
6. .env.example must show ALL required variables

EXCEPTION HANDLING
==================
1. Create custom exception hierarchy in exceptions.py
2. Never use bare except: pass
3. Always log exceptions with logger.exception() before raising
4. Use try-except blocks at API boundaries
5. Raise meaningful exceptions with descriptive messages
6. Chain exceptions using raise ... from e when appropriate

LOGGING REQUIREMENTS
====================
1. Use logging module, not print() for production code
2. Get logger: logger = logging.getLogger(__name__)
3. Use structured JSON logging (python-json-logger)
4. Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
5. Always use logger.exception() in except blocks
6. Include relevant context: exchange name, amount, status codes
7. Never log sensitive data (API keys, secrets)

TESTING REQUIREMENTS
====================
1. Test file location: tests/test_{module}/test_{function}.py
2. Use pytest with fixtures for setup
3. Mock external API calls (use unittest.mock)
4. Test both success and failure cases
5. Use pytest.raises() for exception testing
6. Coverage target: minimum 80%
7. Async tests: use pytest-asyncio

ASYNC/CONCURRENT API CALLS
===========================
1. Use aiohttp for concurrent rate fetching
2. Pattern for concurrent calls:
   async def fetch_all_rates():
       async with aiohttp.ClientSession() as session:
           tasks = [fetch_from_exchange(session, ex) for ex in exchanges]
           return await asyncio.gather(*tasks)

3. Never block the event loop
4. Use asyncio.run() in main entry point
5. Document which functions are async

AI ASSISTANT INSTRUCTIONS
==========================
When writing code for this project:

1. ALWAYS follow the file structure specified above
2. ALWAYS include type hints
3. ALWAYS use Google-style docstrings
4. ALWAYS follow PEP 8
5. SUGGEST using composition over inheritance
6. SUGGEST creating dataclasses for data models
7. SUGGEST using Pydantic for API response validation
8. SUGGEST context managers for resource management
9. CREATE tests alongside the code you generate
10. ASK for clarification if requirements are ambiguous

DO NOT:
- Create unnecessary abstractions
- Use multiple inheritance without good reason
- Hardcode values (use constants or config)
- Ignore error handling
- Skip logging
- Write code without docstrings
- Create overly complex functions (max ~30 lines)

WHEN GENERATING CODE:
1. Explain the design decisions
2. Show imports
3. Include error handling
4. Add docstrings
5. Provide usage examples
6. Suggest tests
7. Point out security considerations if relevant

When asked to create new functionality:
1. Confirm the file location in project structure
2. Ask about error handling strategy
3. Clarify integration points with existing code
4. Suggest the appropriate design pattern
5. Propose tests

DOCUMENTATION STANDARD
======================
All functions and classes MUST have docstrings.
- Public APIs: Detailed docstrings with examples
- Private methods: Brief docstring explaining purpose
- Complex logic: Include inline comments explaining why, not what

PERFORMANCE CONSIDERATIONS
===========================
1. Use async/await for concurrent API calls (not threading)
2. Implement simple caching for repeated rate queries
3. Add request timeouts to prevent hanging
4. Consider rate limiting if making many API calls
5. Profile bottlenecks before optimizing
6. Document performance constraints

DEPLOYMENT & FINAL CHECKLIST
=============================
Before submitting:
1. All tests pass: pytest --cov
2. No security issues: API keys in .env, not hardcoded
3. All functions have type hints and docstrings
4. Code follows PEP 8
5. No unused imports
6. .gitignore configured correctly
7. README.md updated with usage instructions
8. .env.example includes all required variables
9. Error handling is comprehensive
10. Logging is informative without being verbose

END OF MASTER PROMPT
```

---

## 11. Implementation Checklist

Use this checklist when starting Arc ZARDIAN development with AI assistance:

### **Project Setup**
- [ ] Create project root directory
- [ ] Initialize Git repository and add `.gitignore`
- [ ] Create `src/arc_zardian/` package directory
- [ ] Create `tests/` directory
- [ ] Create `pyproject.toml` with project metadata
- [ ] Create `requirements.txt` with pinned versions
- [ ] Create `.env.example` template

### **Configuration**
- [ ] Create `src/arc_zardian/config.py` for environment management
- [ ] Create `src/arc_zardian/logger.py` for logging setup
- [ ] Create `src/arc_zardian/__init__.py` for package exports
- [ ] Create `.env` file locally (add to `.gitignore`)

### **API Layer**
- [ ] Create `src/arc_zardian/api/` package
- [ ] Create base class `BaseExchangeClient` with abstract methods
- [ ] Create exchange-specific clients (Binance, Coinbase, Kraken)
- [ ] Create custom exceptions in `exceptions.py`
- [ ] Add error handling and retry logic
- [ ] Implement async concurrent fetching with aiohttp

### **Core Logic**
- [ ] Create data models in `models.py` (use dataclasses)
- [ ] Create `converter.py` with main conversion logic
- [ ] Create `rate_analyzer.py` for rate/fee analysis
- [ ] Implement pathfinding algorithm
- [ ] Add comprehensive error handling

### **Utilities**
- [ ] Create input validators in `validators.py`
- [ ] Create output formatters in `formatters.py`
- [ ] Create simple caching layer if needed

### **Presentation**
- [ ] Create CLI interface in `presentation/cli.py` using Click
- [ ] Create result formatters
- [ ] Add entry point in `main.py`

### **Testing**
- [ ] Create `tests/conftest.py` with fixtures
- [ ] Write tests for API clients
- [ ] Write tests for converter logic
- [ ] Write integration tests
- [ ] Achieve 80%+ code coverage

### **Documentation**
- [ ] Write comprehensive README.md
- [ ] Document API clients in `docs/API_CLIENTS.md`
- [ ] Create development guide in `docs/DEVELOPMENT.md`
- [ ] Add inline code comments for complex logic

### **Quality Assurance**
- [ ] Verify PEP 8 compliance
- [ ] Check all functions have type hints
- [ ] Verify all functions have docstrings
- [ ] Run full test suite with coverage
- [ ] Security audit: no hardcoded secrets
- [ ] Review imports and dependencies

---

## 12. Quick Reference: AI Prompt Starters

When working with Windsurf or Copilot, use these prompt starters to get better results:

### For New Features
```
"Create a new [component] following the Arc ZARDIAN structure. 
It should:
1. Be in src/arc_zardian/[module]/
2. Include type hints and Google-style docstrings
3. Use async/await where applicable
4. Include proper error handling with custom exceptions
5. Have tests in tests/test_[module]/"
```

### For Bug Fixes
```
"Fix the [issue] in [file]. 
Consider:
1. Root cause analysis
2. Proper exception handling
3. Logging the issue
4. Adding a test case
5. Maintaining consistency with existing code style"
```

### For API Integration
```
"Create an API client for [exchange] that:
1. Inherits from BaseExchangeClient
2. Fetches rates from [endpoint]
3. Handles API errors gracefully
4. Uses async/await for performance
5. Includes comprehensive logging
6. Has tests mocking the API responses"
```

### For Code Review
```
"Review this code for:
1. PEP 8 compliance
2. Type hint completeness
3. Error handling coverage
4. Security issues (especially API key handling)
5. Testing adequacy
6. Performance considerations"
```

---

## 13. Resources & Further Reading

- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python: Type Hints](https://realpython.com/python-type-checking/)
- [Real Python: Logging](https://realpython.com/python-logging/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

---

## Final Notes

This guide ensures consistency between you and your AI assistant. By providing this context upfront, your AI will:
- Generate code that matches your project structure
- Follow your naming conventions automatically
- Include proper type hints and docstrings
- Implement security best practices
- Create testable, maintainable code

**Save this guide in your project as `CONTRIBUTING_AI.md` and reference it in your initial prompts to the AI assistant.**
