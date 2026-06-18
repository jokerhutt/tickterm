# ∴ Jokerhut / models/chart_data.py


from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta

class Timeframe(Enum):
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "7d"
    ONE_MONTH = "1mo"
    ONE_YEAR = "1y"
    FIVE_YEARS = "5y"
    MAX = "max"

    @property
    def time_format(self) -> str:
        match self:
            case Timeframe.ONE_HOUR | Timeframe.ONE_DAY:
                return "%H:%M"
            case Timeframe.ONE_WEEK:
                return "%a"
            case Timeframe.ONE_MONTH:
                return "%d %b"
            case Timeframe.ONE_YEAR:
                return "%b"
            case Timeframe.FIVE_YEARS | Timeframe.MAX:
                return "%Y"

class TimeRange(Enum):
    INTRADAY = "1d"
    HOURLY = "7d"
    DAILY = "5y"
    LONGTERM = "max"

    @property
    def interval(self) -> str:
        match self:
            case TimeRange.INTRADAY:
                return "1m"
            case TimeRange.HOURLY:
                return "1h"
            case TimeRange.DAILY:
                return "1d"
            case TimeRange.LONGTERM:
                return "1wk"


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
    hourly: ChartData | None = None
    daily: ChartData | None = None
    longterm: ChartData | None = None

    def filter_chart(self, chart: ChartData | None, cutoff: datetime) -> ChartData | None :
        if chart is None :
            return None

        return chart.last(cutoff)

    def get_chart_view(self, timeframe: Timeframe) -> ChartData | None:

        match timeframe:
            case Timeframe.ONE_HOUR:
                return self.filter_chart(
                    self.intraday,
                    datetime.now(self.intraday.points[-1].timestamp.tzinfo) - timedelta(hours=1)
                ) if self.intraday else None

            case Timeframe.ONE_DAY:
                return self.intraday

            case Timeframe.ONE_WEEK:
                return self.hourly

            case Timeframe.ONE_MONTH:
                return self.filter_chart(
                    self.daily,
                    datetime.now(self.daily.points[-1].timestamp.tzinfo) - relativedelta(months=1)
                ) if self.daily else None

            case Timeframe.ONE_YEAR:
                return self.filter_chart(
                    self.daily,
                    datetime.now(self.daily.points[-1].timestamp.tzinfo) - relativedelta(years=1)
                ) if self.daily else None

            case Timeframe.FIVE_YEARS:
                return self.daily

            case Timeframe.MAX:
                return self.longterm




