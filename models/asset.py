# ∴ Jokerhut / models/asset.py


from dataclasses import dataclass
from enum import Enum

@dataclass
class AssetMetadata:
    symbol: str
    long_name: str | None
    description: str | None

    sector: str | None
    industry: str | None 

    exchange: str | None

@dataclass
class Asset:
    symbol: str
    name: str
    quote_type: str

    currency: str
    timezone: str

    price: float
    change_pct: float

    # Optional since indexes dont have mkt cap and vol
    volume: int | None
    market_cap: int  | None

