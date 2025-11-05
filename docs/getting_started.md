# Arc ZARDIAN: Project Setup & Usage Guide

## 📋 Start Here

You have received **5 comprehensive documents** for developing Arc ZARDIAN with AI assistance. Here's what each file contains and how to use them:

---

## 📚 Document Overview

### 1. **arc_zardian_guide.md** (Main Reference)
**13 comprehensive sections covering everything**

**Contains:**
- Recommended project structure (folder layout)
- Naming conventions (classes, functions, variables)
- PEP 8 coding standards
- Type hinting best practices
- Google-style docstring format
- Technology stack (approved libraries)
- Security & API key management
- Error handling & logging patterns
- Testing strategy
- Master prompt for AI assistants
- Implementation checklist
- Quick reference prompts

**Use this when:**
- Setting up the project for the first time
- Need detailed explanation of any standard
- Referencing complete best practices

---

### 2. **copilot_instructions.md** (GitHub Copilot Rules)
**Ready-to-use instructions file for GitHub Copilot/Windsurf**

**Contains:**
- Project context
- Project structure
- Coding standards & conventions
- Technology stack rules
- Security requirements
- Exception handling & logging
- Async/concurrent patterns
- Testing requirements
- Code generation guidelines
- Performance considerations
- Deployment checklist
- Quick prompting guide

**Use this by:**
1. Copying content to `.github/copilot-instructions.md` in your repo
2. GitHub Copilot will automatically apply these rules
3. Reference in Windsurf/Claude for context

---

### 3. **ai_prompting_examples.md** (Example Prompts)
**Real-world examples of how to ask AI for different tasks**

**Contains:**
- 7 detailed examples comparing bad vs. good prompts
- Example 1: API Client creation
- Example 2: Conversion logic implementation
- Example 3: Writing unit tests
- Example 4: CLI development
- Example 5: Debugging workflow
- Example 6: Code review requests
- Example 7: Async/concurrent implementation
- Best practices demonstrated
- Master prompt template
- Success indicators

**Use this when:**
- Need to ask AI for a specific feature
- Want to see how to structure prompts effectively
- Learning best practices for AI prompting

---

### 4. **implementation_roadmap.md** (10-Day Plan)
**Step-by-step implementation timeline**

**Contains:**
- Phase 1: Setup (Day 1-2) - Repository initialization
- Phase 2: Configuration (Day 2-3) - Config module
- Phase 3: API Layer (Day 3-5) - Exchange clients
- Phase 4: Core Logic (Day 5-7) - Converter logic
- Phase 5: CLI Interface (Day 7-8) - User interface
- Phase 6: Testing & Docs (Day 8-9) - Quality assurance
- Phase 7: Integration (Day 9-10) - Final testing
- Quick command reference
- File checklist
- Success criteria
- Next steps after completion

**Use this when:**
- Starting development
- Need to track progress
- Want specific prompts to give AI for each phase

---

### 5. **quick_reference.md** (One-Page Lookup)
**Quick lookup reference during active development**

**Contains:**
- Master prompt (copy-paste ready)
- Prompt templates for common tasks
- Essential commands
- Naming quick reference
- Docstring template
- Error handling pattern
- Async/concurrent pattern
- Type hints reference
- Testing pattern
- Security checklist
- Code quality checklist
- Red flags to reject from AI
- Troubleshooting guide

**Use this for:**
- Quick lookups while coding
- Fast reference during development
- Emergency troubleshooting

---

## 🚀 Getting Started

### Step 1: Review Core Documents (30 minutes)
```
1. Read: quick_reference.md (5 min)
2. Read: Implementation_roadmap.md "Phase 1" (10 min)
3. Skim: arc_zardian_guide.md sections 1-3 (15 min)
```

### Step 2: Setup Copilot Integration (10 minutes)
```
1. Copy copilot_instructions.md content
2. Create .github/copilot-instructions.md in your repo
3. Add to git and commit
```

### Step 3: Begin Development (Day 1)
```
1. Create project directory and git repo
2. Create directory structure (from implementation_roadmap Phase 1)
3. Copy copilot_instructions.md to .github/
4. Create .gitignore, .env.example, requirements.txt
5. When ready for code: Use master prompt from quick_reference.md
```

### Step 4: During Development
```
1. Refer to quick_reference.md for quick lookups
2. Use templates from ai_prompting_examples.md
3. Follow Phase checklist from implementation_roadmap.md
4. Consult arc_zardian_guide.md for detailed explanations
```

---

## 💡 How AI Collaboration Works

### The Workflow

```
┌─────────────────────────────────────────────────────┐
│ 1. START SESSION                                    │
│    • Open Windsurf/Copilot                          │
│    • Paste Master Prompt from quick_reference.md    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. REQUEST FEATURE                                  │
│    • Use template from ai_prompting_examples.md     │
│    • Be specific about location, requirements      │
│    • Ask AI to confirm before coding               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. AI GENERATES CODE                                │
│    • Follows project conventions (from instructions)│
│    • Includes type hints and docstrings            │
│    • Handles errors properly                        │
│    • Includes tests                                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. YOU REVIEW CODE                                  │
│    • Check against code quality checklist           │
│    • Verify it matches conventions                  │
│    • Run tests: pytest --cov                        │
│    • Check code style: black, pylint                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 5. ITERATE & IMPROVE                                │
│    • Ask AI for refinements                         │
│    • Request additional tests                       │
│    • Ask for optimization                           │
└─────────────────────────────────────────────────────┘
```

---

## 📁 What to Create First

### Day 1 Tasks
```
arc_zardian/
├── .gitignore                      # Add right away
├── .env.example                    # Template for credentials
├── .github/
│   └── copilot-instructions.md    # Copy from provided file
├── requirements.txt                # List all dependencies
├── pyproject.toml                  # Project metadata
├── README.md                       # Overview
└── src/arc_zardian/
    └── __init__.py                 # Mark as package
```

### Day 2-3 Tasks (Core Configuration)
```
src/arc_zardian/
├── config.py                       # Environment variables
├── logger.py                       # Logging setup
├── main.py                         # Entry point
└── api/
    ├── exceptions.py               # Custom exceptions
    └── base_client.py              # Abstract base
```

### Day 3-5 Tasks (Exchange Clients)
```
src/arc_zardian/api/
├── binance_client.py              # Binance integration
├── coinbase_client.py             # Coinbase integration
└── kraken_client.py               # Kraken integration
```

---

## 🎯 Key Principles to Remember

### 1. **Always Use Type Hints**
```python
# ✅ Good
def fetch_rates(exchange: str, pairs: list[str]) -> dict[str, float]:

# ❌ Bad
def fetch_rates(exchange, pairs):
```

### 2. **Always Include Docstrings (Google Style)**
```python
"""Summary line.

Longer description if needed.

Args:
    param (type): Description.

Returns:
    type: Description.
"""
```

### 3. **Never Hardcode Secrets**
```python
# ✅ Good
api_key = os.getenv("BINANCE_API_KEY")

# ❌ Bad
api_key = "abc123def456"
```

### 4. **Use Async for Concurrent Calls**
```python
# ✅ Good - Fetch from 3 exchanges in parallel
async with aiohttp.ClientSession() as session:
    tasks = [fetch_from_exchange(session, ex) for ex in exchanges]
    results = await asyncio.gather(*tasks)

# ❌ Bad - Sequential, slower
for ex in exchanges:
    results.append(fetch_from_exchange(ex))
```

### 5. **Test Everything**
```bash
pytest tests/ --cov=src/arc_zardian --cov-report=html
```

---

## 🔧 Essential Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Development
pip install -e .                   # Install in editable mode

# Running
zardian convert 1000              # Run the application

# Testing
pytest                             # Run all tests
pytest --cov=src/arc_zardian      # With coverage report
pytest tests/test_api/ -v         # Specific directory, verbose

# Code Quality
black src/                         # Auto-format code
pylint src/arc_zardian            # Check for issues
mypy src/arc_zardian              # Type checking

# Version Control
git add .
git commit -m "Feature: description"
git push
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ Mistake 1: Vague Prompts
```
"Write an API client"
```
**Better:**
```
"Create BinanceClient at src/arc_zardian/api/binance_client.py
that inherits from BaseExchangeClient, implements async fetch_rates(),
includes error handling with APIClientError, logs all requests, and
has comprehensive tests in tests/test_api/test_binance_client.py"
```

### ❌ Mistake 2: No Type Hints
```python
def calculate_fee(amount, rate):
    return amount * rate
```
**Better:**
```python
def calculate_fee(amount: float, rate: float) -> float:
    """Calculate conversion fee."""
    return amount * rate
```

### ❌ Mistake 3: Hardcoded Secrets
```python
API_KEY = "sk_live_abc123def456"
```
**Better:**
```python
API_KEY = os.getenv("BINANCE_API_KEY")
```

### ❌ Mistake 4: Sequential API Calls
```python
rates = {}
for exchange in ["binance", "coinbase", "kraken"]:
    rates[exchange] = fetch(exchange)  # Takes 30 seconds!
```
**Better:**
```python
async with aiohttp.ClientSession() as session:
    tasks = [fetch(session, ex) for ex in exchanges]
    results = await asyncio.gather(*tasks)  # Takes 10 seconds!
```

### ❌ Mistake 5: No Tests
```
# No tests provided
```
**Better:**
```python
def test_fetch_rates_success():
    with patch.object(client, '_request') as mock:
        mock.return_value = {'ZAR_USDC': 0.055}
        assert client.fetch_rates(['ZAR']) == {'ZAR_USDC': 0.055}
```

---

## ✅ Quality Checklist (Before Committing)

- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] No hardcoded secrets or credentials
- [ ] Follows PEP 8 (4 spaces, max 88 chars)
- [ ] Error handling with custom exceptions
- [ ] Comprehensive logging (no print statements)
- [ ] Tests written and passing
- [ ] Code coverage ≥ 80%
- [ ] No bare `except:` statements
- [ ] .gitignore properly configured
- [ ] .env.example updated
- [ ] README.md up-to-date

---

## 📞 Quick Help

**Q: Where do I put the copilot instructions?**  
A: `.github/copilot-instructions.md` (create the directory if needed)

**Q: How do I know if the prompt was good?**  
A: AI-generated code should have type hints, docstrings, error handling, and tests included automatically.

**Q: What's the most important convention?**  
A: Type hints! `def func(param: str) -> dict:` is mandatory for all functions.

**Q: Can I use pandas/Flask/etc.?**  
A: Only approved libraries: requests, aiohttp, click, pydantic, pytest. Ask before using others.

**Q: How often should I test?**  
A: Every time you write code. Run `pytest` before committing.

---

## 🎓 Learning Path

**Day 1:** Read all 5 documents (take notes)  
**Day 2:** Setup project structure, create .github/copilot-instructions.md  
**Day 3-4:** Use implementation_roadmap.md Phase 1-2, work with AI  
**Day 5-7:** Phases 3-5, applying patterns from ai_prompting_examples.md  
**Day 8-10:** Phases 6-7, testing, documentation, final QA  

---

## 📚 Additional Resources

- **PEP 8 Style Guide**: https://peps.python.org/pep-0008/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **Pytest Documentation**: https://docs.pytest.org/
- **Async/Await**: https://docs.python.org/3/library/asyncio.html
- **Click CLI**: https://click.palletsprojects.com/
- **Pydantic**: https://docs.pydantic.dev/

---

## 🏁 Success Metrics

You're on track if:
- ✅ Code passes `pytest --cov` with 80%+ coverage
- ✅ `black` and `pylint` show no major issues
- ✅ All functions have type hints and docstrings
- ✅ No hardcoded secrets in any files
- ✅ CLI application runs successfully
- ✅ All 5 documents are referenced in your workflow

---

## 📝 Summary

| Document | When to Use | Time to Read |
|----------|------------|--------------|
| **quick_reference.md** | Daily development | 5 min |
| **ai_prompting_examples.md** | When asking for features | 10 min |
| **copilot_instructions.md** | Setup once, then referenced by AI | 5 min |
| **implementation_roadmap.md** | Project planning & progress tracking | 15 min |
| **arc_zardian_guide.md** | Detailed explanations & reference | 30 min |

---

**Your AI collaboration framework is complete. Happy coding! 🚀**

For questions, refer to the appropriate document using the guide above.
