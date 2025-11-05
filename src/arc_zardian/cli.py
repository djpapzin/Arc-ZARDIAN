"""Command Line Interface for Arc ZARDIAN.

This module provides the main entry point for the Arc ZARDIAN application.
"""

import logging
from typing import Optional

import typer

from arc_zardian import __version__
from arc_zardian.config import get_settings

# Initialize Typer app
app = typer.Typer(name="arc-zardian", help="ZAR to USDC Arbitrage and Trading System")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def version_callback(value: bool) -> None:
    """Print version and exit.
    
    Args:
        value: If True, print version and exit.
    """
    if value:
        typer.echo(f"Arc ZARDIAN v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    )
) -> None:
    """Arc ZARDIAN - ZAR to USDC Arbitrage and Trading System.
    
    This tool helps you find and execute arbitrage opportunities between ZAR and USDC
    across multiple exchanges.
    """
    # This is a callback function that doesn't need to do anything
    # as it's just used to provide the main command structure.


@app.command()
def find_opportunities(
    min_profit: float = typer.Option(
        None,
        "--min-profit",
        "-p",
        help="Minimum profit percentage to consider (default: from config)",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
) -> None:
    """Find arbitrage opportunities between Binance and LUNO.
    
    Args:
        min_profit: Minimum profit percentage to consider (default: from config).
        verbose: Enable verbose output.
    """
    from ccxt import binance, luno
    from arc_zardian.config import get_settings
    
    settings = get_settings()
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    min_profit = min_profit or settings.MIN_PROFIT_PERCENTAGE
    logger.info("Looking for opportunities with minimum profit: %s%%", min_profit)
    
    try:
        # Initialize exchanges
        binance_exchange = binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_API_SECRET,
            'enableRateLimit': True
        })
        
        luno_exchange = luno({
            'apiKey': settings.LUNO_API_KEY,
            'secret': settings.LUNO_API_SECRET,
            'enableRateLimit': True
        })
        
        # Get ticker prices
        binance_ticker = binance_exchange.fetch_ticker('USDC/ZAR')
        luno_ticker = luno_exchange.fetch_ticker('XBT/ZAR')
        
        # Calculate arbitrage opportunity
        binance_price = float(binance_ticker['last'])
        luno_price = float(luno_ticker['last'])
        
        # Simple arbitrage calculation (you can enhance this)
        price_difference = abs(binance_price - luno_price)
        opportunity = (price_difference / min(binance_price, luno_price)) * 100
        
        if opportunity >= min_profit:
            logger.info("🚀 Arbitrage opportunity found!")
            logger.info(f"  - Binance USDC/ZAR: {binance_price:.2f}")
            logger.info(f"  - LUNO XBT/ZAR: {luno_price:.2f}")
            logger.info(f"  - Opportunity: {opportunity:.2f}%")
        else:
            logger.info("🔍 No significant arbitrage opportunities found.")
            if verbose:
                logger.info(f"  - Binance USDC/ZAR: {binance_price:.2f}")
                logger.info(f"  - LUNO XBT/ZAR: {luno_price:.2f}")
                logger.info(f"  - Current spread: {opportunity:.2f}% (min required: {min_profit}%)")
                
    except Exception as e:
        logger.error(f"❌ Error finding opportunities: {str(e)}")
        if verbose:
            import traceback
            logger.debug(traceback.format_exc())


@app.command()
def check_status() -> None:
    """Check the status of exchanges and account balances."""
    from ccxt import binance, luno, bybit
    from arc_zardian.config import get_settings
    
    settings = get_settings()
    
    # Check Binance connection
    try:
        binance_exchange = binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_API_SECRET,
            'enableRateLimit': True
        })
        binance_balance = binance_exchange.fetch_balance()
        logger.info("✅ Binance connection successful")
        logger.info(f"  - Available ZAR: {binance_balance.get('ZAR', {}).get('free', 0):.2f}")
        logger.info(f"  - Available USDC: {binance_balance.get('USDC', {}).get('free', 0):.4f}")
    except Exception as e:
        logger.error(f"❌ Binance connection failed: {str(e)}")
    
    # Check LUNO connection
    try:
        luno_exchange = luno({
            'apiKey': settings.LUNO_API_KEY,
            'secret': settings.LUNO_API_SECRET,
            'enableRateLimit': True
        })
        luno_balance = luno_exchange.fetch_balance()
        logger.info("✅ LUNO connection successful")
        logger.info(f"  - Available ZAR: {luno_balance.get('ZAR', {}).get('free', 0):.2f}")
        logger.info(f"  - Available XBT: {luno_balance.get('XBT', {}).get('free', 0):.8f}")
    except Exception as e:
        logger.error(f"❌ LUNO connection failed: {str(e)}")
        logger.info("ℹ️  Make sure you've set LUNO_API_KEY and LUNO_API_SECRET in your .env file")
    
    # Check Bybit connection
    try:
        if not settings.BYBIT_API_KEY or not settings.BYBIT_API_SECRET:
            logger.warning("⚠️  Bybit API key or secret not found in .env file")
            return
            
        bybit_exchange = bybit({
            'apiKey': settings.BYBIT_API_KEY,
            'secret': settings.BYBIT_API_SECRET,
            'enableRateLimit': True
        })
        bybit_balance = bybit_exchange.fetch_balance()
        logger.info("✅ Bybit connection successful")
        logger.info(f"  - Available USDT: {bybit_balance.get('USDT', {}).get('free', 0):.2f}")
        logger.info(f"  - Available BTC: {bybit_balance.get('BTC', {}).get('free', 0):.8f}")
    except Exception as e:
        logger.error(f"❌ Bybit connection failed: {str(e)}")
        logger.info("ℹ️  Make sure you've set BYBIT_API_KEY and BYBIT_API_SECRET in your .env file")


if __name__ == "__main__":
    app()
