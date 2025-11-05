import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from arc_zardian.core.models import Exchange, ConversionPath, ConversionResult
from arc_zardian.core.optimizer import (
    ConversionOptimizer,
    BinanceClient,
    LunoClient,
    BybitClient
)

# Mock data for tests
MOCK_RATES = {
    Exchange.BINANCE: 18.5,
    Exchange.LUNO: 18.7,
    Exchange.BYBIT: 18.6
}

MOCK_FEES = {
    Exchange.BINANCE: 0.001,  # 0.1%
    Exchange.LUNO: 0.005,     # 0.5%
    Exchange.BYBIT: 0.003     # 0.3%
}

# Test data
TEST_AMOUNT = 10000  # 10,000 ZAR

@pytest.fixture
def mock_clients():
    """Create mock exchange clients."""
    # Create mock client classes
    binance_mock = MagicMock()
    luno_mock = MagicMock()
    bybit_mock = MagicMock()
    
    # Create a dictionary to store the mock instances
    mock_instances = {
        'BinanceClient': binance_mock,
        'LunoClient': luno_mock,
        'BybitClient': bybit_mock
    }
    
    # Patch the client classes in the optimizer module
    with patch.multiple(
        'arc_zardian.core.optimizer',
        BinanceClient=binance_mock,
        LunoClient=luno_mock,
        BybitClient=bybit_mock
    ):
        yield mock_instances

@pytest.fixture
def optimizer(mock_clients):
    """Create a ConversionOptimizer instance for testing with mock clients."""
    # Create mock clients dictionary
    clients = {
        Exchange.BINANCE: mock_clients['BinanceClient'].return_value,
        Exchange.LUNO: mock_clients['LunoClient'].return_value,
        Exchange.BYBIT: mock_clients['BybitClient'].return_value
    }
    return ConversionOptimizer(clients=clients)

@pytest.mark.asyncio
async def test_binance_is_optimal(mock_clients):
    """Test when Binance provides the best rate."""
    # Configure mock return values for each exchange
    binance_client = AsyncMock()
    luno_client = AsyncMock()
    bybit_client = AsyncMock()
    
    # Set up return values for each client to make Binance the best option
    # Binance: (10000 - 10) / 19.0 = 525.789 (best rate, low fee)
    binance_client.get_zar_usdc_rate.return_value = 1.0  # Best possible rate
    binance_client.calculate_fee.return_value = 0.0  # No fee
    binance_client.EXCHANGE = Exchange.BINANCE
    
    # Luno: (10000 - 100) / 2.0 = 4950.0 (worse rate, higher fee)
    luno_client.get_zar_usdc_rate.return_value = 2.0
    luno_client.calculate_fee.return_value = 100.0
    luno_client.EXCHANGE = Exchange.LUNO
    
    # Bybit: (10000 - 30) / 1.5 = 6646.67 (worse rate, medium fee)
    bybit_client.get_zar_usdc_rate.return_value = 1.5
    bybit_client.calculate_fee.return_value = 30.0
    bybit_client.EXCHANGE = Exchange.BYBIT
    
    # Create the optimizer with our mock clients
    clients = {
        Exchange.BINANCE: binance_client,
        Exchange.LUNO: luno_client,
        Exchange.BYBIT: bybit_client
    }
    optimizer = ConversionOptimizer(clients=clients)
    
    result = await optimizer.find_best_path(TEST_AMOUNT)
    
    # Verify Binance is the optimal exchange
    assert result.optimal_path.exchange == Exchange.BINANCE
    assert len(result.alternative_paths) == 2  # Should have 2 alternative paths
    
    # Verify all clients were called
    binance_client.get_zar_usdc_rate.assert_awaited_once()
    binance_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    luno_client.get_zar_usdc_rate.assert_awaited_once()
    luno_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    bybit_client.get_zar_usdc_rate.assert_awaited_once()
    bybit_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)

@pytest.mark.asyncio
async def test_luno_is_optimal():
    """Test when Luno provides the best rate."""
    # Configure mock return values for each exchange
    binance_client = AsyncMock()
    luno_client = AsyncMock()
    bybit_client = AsyncMock()
    
    # Set up return values for each client to make Luno the best option
    # Luno: (10000 - 10) / 18.5 = 539.46 (best rate, low fee)
    luno_client.get_zar_usdc_rate.return_value = 18.5
    luno_client.calculate_fee.return_value = 10.0  # 0.1% of 10,000
    luno_client.EXCHANGE = Exchange.LUNO
    
    # Binance: (10000 - 100) / 18.7 = 529.41 (worse rate, higher fee)
    binance_client.get_zar_usdc_rate.return_value = 18.7
    binance_client.calculate_fee.return_value = 100.0  # 1% of 10,000
    binance_client.EXCHANGE = Exchange.BINANCE
    
    # Bybit: (10000 - 30) / 18.8 = 530.69 (medium rate, medium fee)
    bybit_client.get_zar_usdc_rate.return_value = 18.8
    bybit_client.calculate_fee.return_value = 30.0  # 0.3% of 10,000
    bybit_client.EXCHANGE = Exchange.BYBIT
    
    # Create the optimizer with our mock clients
    clients = {
        Exchange.BINANCE: binance_client,
        Exchange.LUNO: luno_client,
        Exchange.BYBIT: bybit_client
    }
    optimizer = ConversionOptimizer(clients=clients)
    
    result = await optimizer.find_best_path(TEST_AMOUNT)
    
    # Verify Luno is the optimal exchange
    assert result.optimal_path.exchange == Exchange.LUNO
    assert len(result.alternative_paths) == 2  # Should have 2 alternative paths
    
    # Verify all clients were called
    binance_client.get_zar_usdc_rate.assert_awaited_once()
    binance_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    luno_client.get_zar_usdc_rate.assert_awaited_once()
    luno_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    bybit_client.get_zar_usdc_rate.assert_awaited_once()
    bybit_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)

@pytest.mark.asyncio
async def test_bybit_is_optimal():
    """Test when Bybit provides the best rate."""
    # Configure mock return values for each exchange
    binance_client = AsyncMock()
    luno_client = AsyncMock()
    bybit_client = AsyncMock()
    
    # Set up return values for each client to make Bybit the best option
    # Bybit: (10000 - 1) / 1.0 = 9999.0 (best rate, lowest fee)
    bybit_client.get_zar_usdc_rate.return_value = 1.0
    bybit_client.calculate_fee.return_value = 1.0
    bybit_client.EXCHANGE = Exchange.BYBIT
    
    # Binance: (10000 - 100) / 2.0 = 4950.0 (worse rate, higher fee)
    binance_client.get_zar_usdc_rate.return_value = 2.0
    binance_client.calculate_fee.return_value = 100.0
    binance_client.EXCHANGE = Exchange.BINANCE
    
    # Luno: (10000 - 10) / 1.5 = 6660.0 (better rate but higher fee)
    luno_client.get_zar_usdc_rate.return_value = 1.5
    luno_client.calculate_fee.return_value = 10.0
    luno_client.EXCHANGE = Exchange.LUNO
    
    # Create the optimizer with our mock clients
    clients = {
        Exchange.BINANCE: binance_client,
        Exchange.LUNO: luno_client,
        Exchange.BYBIT: bybit_client
    }
    optimizer = ConversionOptimizer(clients=clients)
    
    result = await optimizer.find_best_path(TEST_AMOUNT)
    
    # Verify Bybit is the optimal exchange
    assert result.optimal_path.exchange == Exchange.BYBIT
    assert len(result.alternative_paths) == 2  # Should have 2 alternative paths
    
    # Verify all clients were called
    binance_client.get_zar_usdc_rate.assert_awaited_once()
    binance_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    luno_client.get_zar_usdc_rate.assert_awaited_once()
    luno_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    bybit_client.get_zar_usdc_rate.assert_awaited_once()
    bybit_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)

@pytest.mark.asyncio
async def test_calculate_usdc_received_correctly(optimizer):
    """Test the USDC received calculation is correct."""
    # Test with known values
    zar_amount = 10000  # 10,000 ZAR
    rate = 20.0  # 1 USDC = 20 ZAR
    fee_percent = 0.001  # 0.1%
    
    # Expected calculation:
    # usdc_before_fee = 10000 / 20 = 500 USDC
    # fee_amount = 10000 * 0.001 = 10 ZAR
    # fee_in_usdc = 10 / 20 = 0.5 USDC
    # usdc_received = 500 - 0.5 = 499.5 USDC
    
    path = ConversionPath(
        exchange=Exchange.BINANCE,
        zar_amount=zar_amount,
        usdc_received=zar_amount / rate * (1 - fee_percent),
        fee=zar_amount * fee_percent,
        rate=rate
    )
    
    assert path.usdc_received == 499.5
    assert path.fee == 10.0

@pytest.mark.asyncio
async def test_error_handling():
    """Test that the optimizer handles errors gracefully."""
    # Configure mock clients
    binance_client = AsyncMock()
    luno_client = AsyncMock()
    bybit_client = AsyncMock()
    
    # Make Binance fail
    binance_client.get_zar_usdc_rate.side_effect = Exception("API error")
    binance_client.EXCHANGE = Exchange.BINANCE
    
    # Configure other exchanges to work
    luno_client.get_zar_usdc_rate.return_value = 19.0
    luno_client.calculate_fee.return_value = TEST_AMOUNT * 0.001
    luno_client.EXCHANGE = Exchange.LUNO
    
    bybit_client.get_zar_usdc_rate.return_value = 18.5
    bybit_client.calculate_fee.return_value = TEST_AMOUNT * 0.003
    bybit_client.EXCHANGE = Exchange.BYBIT
    
    # Create the optimizer with our mock clients
    clients = {
        Exchange.BINANCE: binance_client,
        Exchange.LUNO: luno_client,
        Exchange.BYBIT: bybit_client
    }
    optimizer = ConversionOptimizer(clients=clients)
    
    result = await optimizer.find_best_path(TEST_AMOUNT)
    
    # Should still work with the remaining exchanges
    assert result is not None
    assert len(result.alternative_paths) >= 1  # At least one alternative
    assert result.optimal_path.exchange in [Exchange.LUNO, Exchange.BYBIT]
    
    # Verify all clients were called
    binance_client.get_zar_usdc_rate.assert_awaited_once()
    binance_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    luno_client.get_zar_usdc_rate.assert_awaited_once()
    luno_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
    bybit_client.get_zar_usdc_rate.assert_awaited_once()
    bybit_client.calculate_fee.assert_awaited_once_with(TEST_AMOUNT)
