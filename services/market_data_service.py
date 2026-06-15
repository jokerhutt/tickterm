from pandas import Timestamp
from yfinance.base import FastInfo
from models.asset import Asset
from models.chart_data import ChartData, ChartPoint, TimeRange, Timeframe
from models.news_item import NewsItem
import yfinance as yf



class MarketDataService:
    def get_asset(self, symbol: str) -> Asset :
        ticker = yf.Ticker(symbol)

        info : FastInfo = ticker.fast_info

        price = float(info["lastPrice"])
        previous_close = float(info["previousClose"])
        volume = int(info["lastVolume"])
        market_cap = int(info["marketCap"])

        change_pct = ((price - previous_close) / previous_close) * 100

        return Asset(
            symbol = symbol,
            name = symbol,
            price = price, 
            change_pct = change_pct,
            volume = volume,
            market_cap = market_cap
        )



    def get_chart(self, symbol: str, time_range: TimeRange) -> ChartData :
        ticker = yf.Ticker(symbol)

        period = time_range.value

        interval = "1d"

        match (time_range) :
            case TimeRange.INTRADAY :
                interval = "1m"
            case TimeRange.DAILY :
                interval = "1d"
            case TimeRange.LONGTERM :
                interval = "1w"

        history = ticker.history(period=period, interval = interval)

        points: list[ChartPoint] = []

        closes = history["Close"]

        for timestamp, close in zip(history.index, closes):

            if not isinstance(timestamp, Timestamp):
                continue

            points.append(
                ChartPoint(
                    timestamp=timestamp.to_pydatetime(),
                    price=float(close),
                )
            )

        return ChartData(symbol = symbol, timerange = time_range, points = points)

    def get_news(
        self,
        symbol: str,
    ) -> list[NewsItem]:
        ticker = yf.Ticker(symbol)

        news: list[NewsItem] = []

        for item in ticker.news[:10]:
            content = item.get("content", {})
            news.append(
                NewsItem(
                    title=content.get("title", ""),
                    source=content.get("provider", {}).get("displayName", ""),
                    published=str(content.get("pubDate", "")),
                )
            )

        return news
