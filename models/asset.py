# ∴ Jokerhut / models/asset.py


from dataclasses import dataclass

@dataclass
class Asset:
    symbol: str
    name: str

    currency: str
    timezone: str

    price: float
    change_pct: float

    volume: int
    market_cap: int 

