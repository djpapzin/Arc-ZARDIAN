import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# Import the app module
from arc_zardian.app import main as app_main
from arc_zardian.core.models import Exchange, ConversionPath, ConversionResult

# Test data
TEST_RESULT = ConversionResult(
    optimal_path=ConversionPath(
        exchange=Exchange.BINANCE,
        zar_amount=1000.0,
        usdc_received=52.50,
        fee=10.0,
        rate=18.50
    ),
    alternative_paths=[
        ConversionPath(
            exchange=Exchange.LUNO,
            zar_amount=1000.0,
            usdc_received=51.20,
            fee=12.0,
            rate=19.20
        ),
        ConversionPath(
            exchange=Exchange.BYBIT,
            zar_amount=1000.0,
            usdc_received=50.80,
            fee=8.0,
            rate=19.50
        )
    ]
)

@pytest.fixture
def mock_optimizer():
    with patch('arc_zardian.app.ConversionOptimizer') as mock:
        instance = mock.return_value
        instance.find_best_path.return_value = TEST_RESULT
        yield instance

@pytest.mark.asyncio
async def test_app_main(mock_optimizer):
    """Test that the app runs without errors and processes the conversion result."""
    # Mock Streamlit functions
    with patch('arc_zardian.app.st') as mock_st:
        # Setup mock return values
        mock_st.number_input.return_value = 1000.0
        mock_st.button.return_value = True
        
        # Create a mock for the spinner context manager
        spinner_mock = MagicMock()
        spinner_mock.__enter__.return_value = None
        mock_st.spinner.return_value = spinner_mock
        
        # Run the app
        with patch('arc_zardian.app.asyncio.run') as mock_run:
            mock_run.side_effect = lambda coro: coro
            await app_main()
    
    # Verify the optimizer was called with the correct amount
    mock_optimizer.return_value.find_best_path.assert_called_once_with(1000.0)
    
    # Verify Streamlit functions were called
    mock_st.set_page_config.assert_called_once()
    mock_st.title.assert_called_once()
    mock_st.markdown.assert_called()  # Multiple calls expected
    mock_st.number_input.assert_called_once()
    mock_st.button.assert_called_once()
    mock_st.spinner.assert_called_once()
    
    # Verify the result was processed
    mock_st.metric.assert_called()  # Multiple calls expected
    mock_st.expander.assert_called_once()
    
    # Verify no errors were shown
    mock_st.error.assert_not_called()

@pytest.mark.asyncio
async def test_app_error_handling():
    """Test error handling in the app."""
    with patch('arc_zardian.app.st') as mock_st, \
         patch('arc_zardian.app.ConversionOptimizer') as mock_optimizer:
        
        # Setup mocks
        mock_st.number_input.return_value = 1000.0
        mock_st.button.return_value = True
        
        # Simulate an error in the optimizer
        mock_optimizer.return_value.find_best_path.side_effect = Exception("API Error")
        
        # Create a mock for the spinner context manager
        spinner_mock = MagicMock()
        spinner_mock.__enter__.return_value = None
        mock_st.spinner.return_value = spinner_mock
        
        # Run the app with error handling
        with patch('arc_zardian.app.asyncio.run') as mock_run:
            mock_run.side_effect = lambda coro: coro
            await app_main()
        
        # Verify error was displayed
        mock_st.error.assert_called()
        mock_st.exception.assert_called_once()
