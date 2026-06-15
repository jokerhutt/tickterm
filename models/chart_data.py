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

    # e.g. for past 1 hour u would pass in 60
    def last(self, cutoff: datetime) -> "ChartData":
        filtered_points : list[ChartPoint] = []

        for point in self.points :
            if point.timestamp >= cutoff:
                filtered_points.append(point)

        return ChartData(
            symbol = self.symbol,
            timerange = self.timerange,
            points = filtered_points
        )

@dataclass
class ChartCache:
    intraday: ChartData | None = None
    daily: ChartData | None = None
    longterm: ChartData | None = None




