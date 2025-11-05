"""Tests for the configuration module."""

import os
from unittest import TestCase, mock

from arc_zardian.config import Settings, get_settings, init_settings


class TestConfig(TestCase):
    """Test configuration settings."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.env_vars = {
            "BINANCE_API_KEY": "test_binance_key",
            "BINANCE_API_SECRET": "test_binance_secret",
            "VALR_API_KEY": "test_valr_key",
            "VALR_API_SECRET": "test_valr_secret",
        }
        self.patcher = mock.patch.dict(os.environ, self.env_vars)
        self.patcher.start()

    def tearDown(self) -> None:
        """Clean up after tests."""
        self.patcher.stop()

    def test_settings_initialization(self) -> None:
        """Test that settings are initialized with default values."""
        # Create a temporary .env file for testing
        with open(".env", "w") as f:
            f.write("""
            BINANCE_API_KEY=test_key
            BINANCE_API_SECRET=test_secret
            VALR_API_KEY=test_key
            VALR_API_SECRET=test_secret
            """)
        
        try:
            settings = Settings()
            self.assertEqual(settings.ENVIRONMENT, "development")
            self.assertEqual(settings.LOG_LEVEL, "INFO")
            self.assertEqual(settings.DEFAULT_FIAT_CURRENCY, "ZAR")
            self.assertEqual(settings.DEFAULT_CRYPTO_CURRENCY, "USDC")
            self.assertEqual(settings.MIN_PROFIT_PERCENTAGE, 0.5)
            self.assertEqual(settings.RATE_LIMIT, 60)
        finally:
            # Clean up the test .env file
            if os.path.exists(".env"):
                os.remove(".env")

    def test_required_fields(self) -> None:
        """Test that required fields are properly set."""
        # The required fields should be set from the environment variables in setUp
        settings = Settings(
            BINANCE_API_KEY="test_binance_key",
            BINANCE_API_SECRET="test_binance_secret",
            VALR_API_KEY="test_valr_key",
            VALR_API_SECRET="test_valr_secret"
        )
        self.assertEqual(settings.BINANCE_API_KEY, "test_binance_key")
        self.assertEqual(settings.BINANCE_API_SECRET, "test_binance_secret")
        self.assertEqual(settings.VALR_API_KEY, "test_valr_key")
        self.assertEqual(settings.VALR_API_SECRET, "test_valr_secret")

    def test_min_profit_validation(self) -> None:
        """Test that minimum profit validation works."""
        with self.assertRaises(ValueError):
            Settings(
                BINANCE_API_KEY="test",
                BINANCE_API_SECRET="test",
                VALR_API_KEY="test",
                VALR_API_SECRET="test",
                MIN_PROFIT_PERCENTAGE=-1
            )

    def test_get_settings_singleton(self) -> None:
        """Test that get_settings returns a singleton instance."""
        # Reset the global settings for this test
        from arc_zardian.config import settings as global_settings
        global global_settings
        original_settings = global_settings
        global_settings = None
        
        try:
            settings1 = get_settings()
            settings2 = get_settings()
            self.assertIs(settings1, settings2)
        finally:
            # Restore the original settings
            global_settings = original_settings
