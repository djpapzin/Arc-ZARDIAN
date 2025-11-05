# Arc ZARDIAN 🛡️

An AI-powered agent designed to find the most efficient conversion path from South African Rand (ZAR) to USDC. This project is a submission for the [AI Agents on Arc with USDC Hackathon](https://lablab.ai/event/ai-agents-on-arc-with-usdc-hackathon) by lablab.ai.

## The Problem

For users in emerging markets like South Africa, converting local fiat currency (ZAR) to stablecoins like USDC involves navigating a complex landscape of exchanges, each with different rates, fees, and liquidity. Choosing the wrong platform can result in significant value loss.

## Our Solution

Arc ZARDIAN acts as an intelligent guardian for your capital. This AI agent will:

1. **Monitor Multiple Exchanges:** Fetch real-time data from top South African crypto platforms (e.g., Binance, Luno, Bybit).
2. **Analyze All Costs:** Calculate the true end-to-end cost of conversion, factoring in deposit fees, trading fees, and withdrawal fees.
3. **Provide the Optimal Path:** Recommend the best platform to use at any given moment to maximize the USDC received for a specific amount of ZAR.

## Features

- Web-based interface built with Streamlit
- Real-time conversion rate comparison
- Detailed breakdown of fees and final USDC amount
- Support for multiple exchanges (Binance, Luno, Bybit)
- Mock data for demonstration and testing

## Technology Stack

- **Language:** Python 3.12+
- **Web Framework:** Streamlit
- **Data Processing:** pandas, numpy
- **Testing:** pytest
- **Code Quality:** black, flake8, mypy
- **Version Control:** Git

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/djpapzin/Arc-ZARDIAN.git
   cd Arc-ZARDIAN
   ```

2. Create and activate a virtual environment:

   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) For development, install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Running the Application

Start the Streamlit app:

```bash
streamlit run src/arc_zardian/app.py
```

The application will be available at `http://localhost:8501`

### Using the Application

1. Enter the amount of ZAR you want to convert
2. Click the "Find Best Path" button
3. View the optimal conversion path and alternative options
4. See detailed breakdown of fees and final USDC amount

## Project Structure

```text
Arc-ZARDIAN/
├── .github/               # GitHub workflows and templates
├── docs/                  # Project documentation
├── src/
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
├── README.md
├── pyproject.toml        # Project metadata and build configuration
└── requirements.txt      # Project dependencies
```

## Testing

Run the test suite with:

```bash
pytest
```

For test coverage report:

```bash
pytest --cov=src
```

## Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a new feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and write tests
4. Run the test suite to ensure everything passes
5. Commit your changes with a descriptive message
6. Push to your fork and submit a pull request

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for better code clarity
- Write docstrings for all public functions and classes
- Keep commits small and focused on a single feature/fix

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [pytest](https://docs.pytest.org/) for testing framework
- [lablab.ai](https://lablab.ai/) for organizing the hackathon
- Arc for the USDC integration
- All open-source projects that made this possible
