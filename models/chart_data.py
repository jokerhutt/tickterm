
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Timeframe(Enum):
    FIVE_MINUTES = "5m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1mo"
    ONE_YEAR = "1y"
    FIVE_YEARS = "5y"
    MAX = "max"

@dataclass
class ChartPoint :
    timestamp: datetime
    price: float

@dataclass
class ChartData:
    symbol: str
    timeframe: Timeframe
    points: list[ChartPoint]

