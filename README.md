# Arc ZARDIAN 🛡️

An AI-powered agent designed to find the most efficient conversion path from South African Rand (ZAR) to USDC. This project is a submission for the [AI Agents on Arc with USDC Hackathon](https://lablab.ai/event/ai-agents-on-arc-with-usdc-hackathon) by lablab.ai.

## The Problem

For users in emerging markets like South Africa, converting local fiat currency (ZAR) to stablecoins like USDC involves navigating a complex landscape of exchanges, each with different rates, fees, and liquidity. Choosing the wrong platform can result in significant value loss.

## Our Solution

Arc ZARDIAN acts as an intelligent guardian for your capital. This AI agent will:

1. **Monitor Multiple Exchanges:** Fetch real-time data from top South African crypto platforms (e.g., Binance, Valr, Bybit).
2. **Analyze All Costs:** Calculate the true end-to-end cost of conversion, factoring in deposit fees, trading fees, and withdrawal fees.
3. **Provide the Optimal Path:** Recommend the best platform and method (P2P vs. Spot Market) to use at any given moment to maximize the USDC received for a specific amount of ZAR.

## Technology Stack

* **Language:** Python
* **APIs:** `requests` 
* **Data Analysis:** `pandas` 
* **User Interface:** `Streamlit` 
* **AI Assistant:** This project is being developed with the help of an AI coding assistant (Windsurf).

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Arc-ZARDIAN.git
   cd Arc-ZARDIAN
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your API keys:
   ```env
   # Exchange API Keys
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_SECRET_KEY=your_binance_secret_key
   VALR_API_KEY=your_valr_api_key
   VALR_SECRET_KEY=your_valr_secret_key
   ```

### Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

```
Arc-ZARDIAN/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py              # Main Streamlit application
├── config.py           # Configuration settings
├── exchanges/          # Exchange API clients
│   ├── __init__.py
│   ├── binance.py
│   └── valr.py
├── models/             # Data models
│   ├── __init__.py
│   └── conversion.py
└── utils/              # Utility functions
    ├── __init__.py
    └── helpers.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- lablab.ai for hosting the hackathon
- Arc for the USDC integration
- All open-source projects that made this possible
