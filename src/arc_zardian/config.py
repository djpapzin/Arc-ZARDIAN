"""Configuration management for Arc ZARDIAN.

This module handles loading and validating configuration from environment variables.
"""

import os
import sys
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_prefix="",
        extra="ignore"
    )

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Exchange API Credentials (with empty defaults for testing)
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    LUNO_API_KEY: str = ""
    LUNO_API_SECRET: str = ""
    BYBIT_API_KEY: str = ""
    BYBIT_API_SECRET: str = ""

    # Trading Settings
    DEFAULT_FIAT_CURRENCY: str = "ZAR"
    DEFAULT_CRYPTO_CURRENCY: str = "USDC"
    MIN_PROFIT_PERCENTAGE: float = 0.5

    # Rate Limiting (requests per minute)
    RATE_LIMIT: int = 60

    @field_validator("MIN_PROFIT_PERCENTAGE")
    @classmethod
    def validate_min_profit(cls, v: float) -> float:
        """Validate that minimum profit percentage is non-negative."""
        if v < 0:
            raise ValueError("MIN_PROFIT_PERCENTAGE must be non-negative")
        return v


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance.

    Returns:
        Settings: The global settings instance.
    """
    global settings
    if settings is None:
        settings = Settings()
    return settings


def init_settings() -> None:
    """Initialize the global settings."""
    global settings
    settings = Settings()


# Only initialize settings if not in test environment
if "pytest" not in sys.modules:
    init_settings()
