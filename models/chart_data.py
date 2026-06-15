
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Timeframe(Enum):
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1mo"
    ONE_YEAR = "1y"
    FIVE_YEARS = "5y"
    MAX = "max"

class TimeRange(Enum):
    INTRADAY = "1d"
    DAILY = "5y"
    LONGTERM = "max"

@dataclass
class ChartPoint :
    timestamp: datetime
    price: float

@dataclass
class ChartData:
    symbol: str
    timerange: TimeRange 
    points: list[ChartPoint]

@dataclass
class ChartCache:
    intraday: ChartData | None = None
    daily: ChartData | None = None
    longterm: ChartData | None = None


