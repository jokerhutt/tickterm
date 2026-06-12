
from dataclasses import dataclass


@dataclass
class Asset:
    symbol: str

    price: float
    change_pct: float

    volume: int
    market_cap: int 

