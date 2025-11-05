# Arc ZARDIAN: Implementation Roadmap

This document provides a step-by-step implementation plan for using the Project Scaffolding & AI Collaboration Guide.

---

## Phase 1: Setup (Day 1-2)

### Step 1: Initialize Repository
```bash
# Create project directory
mkdir arc_zardian
cd arc_zardian

# Initialize Git
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# Create initial structure
mkdir -p src/arc_zardian
mkdir -p tests
mkdir -p docs
mkdir -p .github
```

### Step 2: Create Configuration Files

**pyproject.toml**:
```toml
[build-system]
requires = ["setuptools>=65", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "arc-zardian"
version = "0.1.0"
description = "AI agent for optimal ZAR to USDC conversion"
authors = [{name = "Your Name", email = "your@email.com"}]
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
    "aiohttp>=3.9.1",
    "python-dotenv>=1.0.0",
    "click>=8.1.7",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "black>=23.0.0",
    "pylint>=2.17.0",
]

[project.scripts]
zardian = "arc_zardian.main:cli"
```

**requirements.txt**:
```
requests==2.31.0
aiohttp==3.9.1
python-dotenv==1.0.0
click==8.1.7
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
```

**.gitignore**:
```
# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log
```

**.env.example**:
```
# Binance API
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here

# Coinbase API
COINBASE_API_KEY=your_key_here
COINBASE_API_SECRET=your_secret_here

# Kraken API
KRAKEN_API_KEY=your_key_here
KRAKEN_API_SECRET=your_secret_here

# Application
LOG_LEVEL=INFO
MAX_RETRIES=3
API_TIMEOUT=10
```

### Step 3: Create Directory Structure
```bash
# Core package
touch src/arc_zardian/__init__.py
touch src/arc_zardian/main.py
touch src/arc_zardian/config.py
touch src/arc_zardian/logger.py

# API layer
mkdir -p src/arc_zardian/api
touch src/arc_zardian/api/__init__.py
touch src/arc_zardian/api/exceptions.py
touch src/arc_zardian/api/base_client.py

# Core logic
mkdir -p src/arc_zardian/core
touch src/arc_zardian/core/__init__.py
touch src/arc_zardian/core/models.py
touch src/arc_zardian/core/converter.py

# Utils
mkdir -p src/arc_zardian/utils
touch src/arc_zardian/utils/__init__.py

# CLI
mkdir -p src/arc_zardian/presentation
touch src/arc_zardian/presentation/__init__.py
touch src/arc_zardian/presentation/cli.py

# Tests
touch tests/__init__.py
touch tests/conftest.py
mkdir -p tests/test_api
touch tests/test_api/__init__.py
mkdir -p tests/test_core
touch tests/test_core/__init__.py
```

### Step 4: Setup GitHub Copilot Instructions

Copy `copilot-instructions.md` to `.github/copilot-instructions.md`

---

## Phase 2: Core Configuration (Day 2-3)

### Prompt to AI:

```
Create the base configuration module for Arc ZARDIAN at src/arc_zardian/config.py

Requirements:
1. Use python-dotenv to load .env file at startup
2. Define a Config class with these attributes:
   - BINANCE_API_KEY, BINANCE_API_SECRET
   - COINBASE_API_KEY, COINBASE_API_SECRET
   - KRAKEN_API_KEY, KRAKEN_API_SECRET
   - LOG_LEVEL (default: INFO)
   - MAX_RETRIES (default: 3)
   - API_TIMEOUT (default: 10)

3. Add a validate() class method that:
   - Checks for required API keys
   - Raises ValueError if any are missing
   - Called at application startup

4. Include type hints and docstrings
5. Create test in tests/test_core/test_config.py

Be sure to follow Arc ZARDIAN conventions!
```

---

## Phase 3: API Layer (Day 3-5)

### Step 1: Exception Definitions

Prompt to AI:
```
Create custom exceptions for Arc ZARDIAN at src/arc_zardian/api/exceptions.py

Include:
1. ArcZardianError (base exception)
2. APIClientError (for API failures)
3. ValidationError (for input validation)
4. ConfigurationError (for missing config)

Each should:
- Have descriptive docstrings
- Store relevant error metadata
- Support exception chaining with 'raise from'

Create tests in tests/test_api/test_exceptions.py
```

### Step 2: Base Client

Prompt to AI:
```
Create the BaseExchangeClient abstract base class at src/arc_zardian/api/base_client.py

Requirements:
1. Abstract methods:
   - async def fetch_rates(self, pairs: list[str]) -> dict[str, float]
   - def get_exchange_info(self) -> dict
   - async def estimate_fee(self, amount: float) -> float

2. Concrete methods for common functionality:
   - _validate_api_credentials() -> bool
   - _log_request(endpoint: str, params: dict) -> None
   - _handle_error(response: dict) -> None

3. Constructor should accept:
   - api_key: str
   - api_secret: str
   - base_url: str
   - timeout: int = 10

4. Use type hints, docstrings
5. Implement proper error handling

No tests needed yet (will be tested through subclasses)
```

### Step 3: Exchange Clients

Prompt to AI (repeat for Binance, Coinbase, Kraken):
```
Create the BinanceClient for Arc ZARDIAN at src/arc_zardian/api/binance_client.py

Requirements:
1. Inherit from BaseExchangeClient
2. Implement async fetch_rates() using requests library:
   - Query: https://api.binance.com/api/v3/ticker/price
   - Handle rate limiting (Binance: 1200 requests/min)
3. Implement get_exchange_info() for trading pairs info
4. Implement estimate_fee() returning Binance's taker fee (0.1% default)
5. Use aiohttp for async HTTP (not requests)
6. Add retry logic with exponential backoff
7. Log all API calls and errors
8. Raise APIClientError for any failures

Create tests in tests/test_api/test_binance_client.py that:
- Mock the HTTP responses
- Test successful rate fetching
- Test error handling
- Test rate limiting behavior
```

---

## Phase 4: Core Logic (Day 5-7)

### Step 1: Data Models

Prompt to AI:
```
Create data models for Arc ZARDIAN at src/arc_zardian/core/models.py

Define dataclasses:
1. ExchangeRate
   - exchange: str
   - currency_pair: str
   - rate: float
   - timestamp: datetime

2. ConversionPath
   - exchanges: list[str]
   - rates: dict[str, float]
   - fees: dict[str, float]
   - total_cost: float
   - received_amount: float

3. ConversionResult
   - optimal_path: ConversionPath
   - alternative_paths: list[ConversionPath]
   - timestamp: datetime

Use @dataclass decorator and include validation.
Create tests for model validation.
```

### Step 2: Converter Logic

Prompt to AI:
```
Create the main converter at src/arc_zardian/core/converter.py

Class: ZARtoUSDCConverter
Responsibilities:
1. Fetch rates from multiple exchanges concurrently
2. Analyze conversion paths
3. Find optimal route

Methods:
- async def find_optimal_path(amount: float) -> ConversionPath
- async def _fetch_all_rates() -> dict
- def _calculate_paths(rates: dict) -> list[ConversionPath]
- def _select_optimal_path(paths: list[ConversionPath]) -> ConversionPath

Requirements:
1. Use asyncio.gather() to fetch from Binance, Coinbase, Kraken in parallel
2. Raise ValidationError for invalid amounts (must be > 0)
3. Log all decisions and calculations
4. Use type hints throughout
5. Include error handling for failed exchanges

Create comprehensive tests mocking API responses.
```

---

## Phase 5: CLI Interface (Day 7-8)

### Prompt to AI:

```
Create CLI interface at src/arc_zardian/presentation/cli.py using Click

Command: zardian convert <amount>

Parameters:
1. amount: float (positional, ZAR amount to convert)
2. --target: str (target currency, default: USDC)
3. --exchanges: str (comma-separated, default: binance,coinbase,kraken)
4. --debug: flag (show full traceback on errors)

Output should display:
1. Input amount in ZAR
2. Optimal conversion path (exchanges used)
3. Fees breakdown by exchange
4. Total cost (ZAR and USD equivalent)
5. Estimated USDC received
6. Timestamp and elapsed time

Error handling:
- ValidationError → Show user-friendly message
- APIClientError → Suggest retry
- Catch unhandled exceptions → Show error if --debug

Create entry point in src/arc_zardian/main.py that:
1. Calls Config.validate()
2. Initializes logging
3. Calls click.group()
```

---

## Phase 6: Testing & Documentation (Day 8-9)

### Step 1: Complete Test Suite

Prompt to AI:
```
Audit all tests in Arc ZARDIAN and report:
1. Current code coverage (should be ≥80%)
2. Missing test cases
3. Untested error paths
4. Performance-critical functions needing optimization checks

Create missing tests to reach 80%+ coverage.
```

### Step 2: Documentation

Prompt to AI:
```
Create documentation for Arc ZARDIAN:

1. docs/API_CLIENTS.md - Document each exchange client
2. docs/ARCHITECTURE.md - System design overview
3. Update README.md with:
   - Installation instructions
   - Quick start example
   - Configuration guide
   - Troubleshooting section
```

---

## Phase 7: Final Integration (Day 9-10)

### Step 1: End-to-End Testing

```bash
# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run all tests
pytest tests/ --cov=src/arc_zardian --cov-report=html

# Test CLI
zardian convert 1000 --debug

# Check code style
black --check src/
pylint src/arc_zardian
```

### Step 2: Final Checklist

- [ ] All tests pass (pytest)
- [ ] Coverage ≥ 80%
- [ ] No PEP 8 violations (black, pylint)
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] .env.example is complete
- [ ] README.md is up-to-date
- [ ] No secrets in version control
- [ ] Logging is comprehensive
- [ ] Error messages are user-friendly

---

## Quick Commands Reference

```bash
# Development setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Running application
zardian convert 1000

# Testing
pytest
pytest --cov=src/arc_zardian
pytest tests/test_api/test_binance_client.py -v

# Code quality
black src/
pylint src/arc_zardian
mypy src/arc_zardian

# Clean up
rm -rf __pycache__ .pytest_cache .coverage htmlcov
```

---

## File Checklist for Completion

### Root Level
- [ ] README.md
- [ ] LICENSE
- [ ] pyproject.toml
- [ ] requirements.txt
- [ ] .gitignore
- [ ] .env.example
- [ ] .github/copilot-instructions.md

### src/arc_zardian/
- [ ] __init__.py
- [ ] main.py (entry point)
- [ ] config.py
- [ ] logger.py

### src/arc_zardian/api/
- [ ] __init__.py
- [ ] exceptions.py
- [ ] base_client.py
- [ ] binance_client.py
- [ ] coinbase_client.py
- [ ] kraken_client.py

### src/arc_zardian/core/
- [ ] __init__.py
- [ ] models.py
- [ ] converter.py
- [ ] rate_analyzer.py (optional enhancement)

### src/arc_zardian/presentation/
- [ ] __init__.py
- [ ] cli.py

### tests/
- [ ] __init__.py
- [ ] conftest.py
- [ ] test_config.py
- [ ] test_api/test_exceptions.py
- [ ] test_api/test_binance_client.py
- [ ] test_api/test_coinbase_client.py
- [ ] test_api/test_kraken_client.py
- [ ] test_core/test_models.py
- [ ] test_core/test_converter.py
- [ ] test_integration.py

### docs/
- [ ] API_CLIENTS.md
- [ ] ARCHITECTURE.md
- [ ] DEVELOPMENT.md

---

## Success Criteria

Your Arc ZARDIAN project is complete when:

1. ✅ **Code Quality**: All code passes PEP 8, has type hints, and includes docstrings
2. ✅ **Testing**: 80%+ code coverage with comprehensive test cases
3. ✅ **Security**: No hardcoded secrets; all credentials via .env
4. ✅ **Functionality**: CLI command successfully finds optimal ZAR→USDC paths
5. ✅ **Documentation**: README, architecture docs, and API documentation complete
6. ✅ **Error Handling**: Graceful handling of API failures with helpful error messages
7. ✅ **Logging**: Comprehensive logging without verbose spam
8. ✅ **Performance**: Concurrent API calls complete in <5 seconds

---

## Next Steps After Completion

1. **Deployment**: Consider containerizing with Docker
2. **Monitoring**: Add real-time monitoring and alerting
3. **Optimization**: Profile and optimize performance bottlenecks
4. **Features**: Add caching, historical analysis, price predictions
5. **Integration**: Connect to exchanges for live trading execution
6. **UI**: Build web interface with Flask/FastAPI

---

**Project Template Version**: 1.0  
**Last Updated**: 2025-11-04  
**Status**: Ready for Development
