from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Exchange(Enum):
    BINANCE = "Binance"
    LUNO = "Luno"
    BYBIT = "Bybit"


@dataclass
class ConversionPath:
    exchange: Exchange
    zar_amount: float
    usdc_received: float
    fee: float
    rate: float


@dataclass
class ConversionResult:
    optimal_path: ConversionPath
    alternative_paths: List[ConversionPath]
    timestamp: float

    @property
    def best_exchange(self) -> Exchange:
        return self.optimal_path.exchange

    @property
    def best_rate(self) -> float:
        return self.optimal_path.rate

    @property
    def best_fee(self) -> float:
        return self.optimal_path.fee

    @property
    def final_amount(self) -> float:
        return self.optimal_path.usdc_received
