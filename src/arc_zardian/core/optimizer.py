import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timezone

from .models import Exchange, ConversionPath, ConversionResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExchangeClientBase:
    """Base class for exchange clients."""
    EXCHANGE: Exchange
    
    async def get_zar_usdc_rate(self) -> float:
        """Get the current ZAR/USDC rate from the exchange."""
        raise NotImplementedError
    
    async def calculate_fee(self, zar_amount: float) -> float:
        """Calculate the trading fee for the given ZAR amount."""
        raise NotImplementedError


class BinanceClient(ExchangeClientBase):
    EXCHANGE = Exchange.BINANCE
    
    async def get_zar_usdc_rate(self) -> float:
        # In a real implementation, this would call the Binance API
        # For now, return a mock rate
        return 18.5
    
    async def calculate_fee(self, zar_amount: float) -> float:
        # Binance charges 0.1% trading fee
        return zar_amount * 0.001


class LunoClient(ExchangeClientBase):
    EXCHANGE = Exchange.LUNO
    
    async def get_zar_usdc_rate(self) -> float:
        # In a real implementation, this would call the Luno API
        # For now, return a mock rate
        return 18.7
    
    async def calculate_fee(self, zar_amount: float) -> float:
        # Luno charges 0.5% trading fee
        return zar_amount * 0.005


class BybitClient(ExchangeClientBase):
    EXCHANGE = Exchange.BYBIT
    
    async def get_zar_usdc_rate(self) -> float:
        # In a real implementation, this would call the Bybit API
        # For now, return a mock rate
        return 18.6
    
    async def calculate_fee(self, zar_amount: float) -> float:
        # Bybit charges 0.1% trading fee for makers, 0.3% for takers
        # We'll use taker fee as worst-case scenario
        return zar_amount * 0.003


class ConversionOptimizer:
    """Finds the best conversion path from ZAR to USDC across multiple exchanges."""
    
    def __init__(self, clients: Dict[Exchange, ExchangeClientBase] = None):
        """Initialize the optimizer with exchange clients.
        
        Args:
            clients: Dictionary mapping exchanges to their client implementations.
                    If None, default clients will be used.
        """
        if clients is None:
            self.clients = {
                Exchange.BINANCE: BinanceClient(),
                Exchange.LUNO: LunoClient(),
                Exchange.BYBIT: BybitClient(),
            }
        else:
            self.clients = clients
            
        self.logger = logger.getChild(self.__class__.__name__)
    
    async def _evaluate_exchange(
        self, 
        exchange: Exchange, 
        zar_amount: float
    ) -> Optional[ConversionPath]:
        """Evaluate a single exchange and return the conversion path."""
        client = self.clients[exchange]
        
        try:
            # Get rate and fee concurrently
            rate, fee = await asyncio.gather(
                client.get_zar_usdc_rate(),
                client.calculate_fee(zar_amount)
            )
            
            # Calculate final USDC amount after fee
            usdc_received = (zar_amount - fee) / rate
            
            self.logger.info(
                f"{exchange.value}: Rate={rate:.4f}, "
                f"Fee={fee:.2f} ZAR, "
                f"USDC received={usdc_received:.2f}"
            )
            
            return ConversionPath(
                exchange=exchange,
                zar_amount=zar_amount,
                usdc_received=usdc_received,
                fee=fee,
                rate=rate
            )
            
        except Exception as e:
            self.logger.error(f"Error evaluating {exchange.value}: {str(e)}")
            return None
    
    async def find_best_path(self, zar_amount: float) -> ConversionResult:
        """
        Find the best conversion path from ZAR to USDC across all supported exchanges.
        
        Args:
            zar_amount: Amount in ZAR to convert
            
        Returns:
            ConversionResult containing the optimal path and alternatives
        """
        self.logger.info(f"Finding best conversion path for {zar_amount:.2f} ZAR")
        
        # Evaluate all exchanges concurrently
        tasks = [
            self._evaluate_exchange(exchange, zar_amount)
            for exchange in self.clients.keys()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None results and exceptions
        valid_paths = [r for r in results if isinstance(r, ConversionPath)]
        
        if not valid_paths:
            raise ValueError("No valid conversion paths found")
        
        # Sort by USDC received (descending)
        valid_paths.sort(key=lambda x: x.usdc_received, reverse=True)
        
        # Create result
        result = ConversionResult(
            optimal_path=valid_paths[0],
            alternative_paths=valid_paths[1:],
            timestamp=datetime.now(timezone.utc).timestamp()
        )
        
        self.logger.info(
            f"Best exchange: {result.optimal_path.exchange.value} "
            f"(Rate: {result.optimal_path.rate:.4f}, "
            f"USDC: {result.optimal_path.usdc_received:.2f})"
        )
        
        return result


# Helper function for synchronous interface
async def find_best_path(zar_amount: float, clients: Dict[Exchange, ExchangeClientBase] = None) -> ConversionResult:
    """
    Find the best conversion path from ZAR to USDC.
    
    This is a convenience wrapper around ConversionOptimizer for simple use cases.
    
    Args:
        zar_amount: Amount in ZAR to convert
        clients: Optional dictionary of exchange clients to use. If None, default clients will be used.
        
    Returns:
        ConversionResult containing the optimal path and alternatives
    """
    optimizer = ConversionOptimizer(clients=clients)
    return await optimizer.find_best_path(zar_amount)
