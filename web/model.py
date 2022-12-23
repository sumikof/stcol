from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DateRate:
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: float
    adj_close: float


@dataclass
class SymbolRate:
    symbol: str
    rates: List[DateRate]


@dataclass
class RateModel:
    item: Dict[str, SymbolRate]
