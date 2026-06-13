from pandas import Timestamp
from yfinance.base import FastInfo
from models.asset import Asset
from models.chart_data import ChartData, ChartPoint, Timeframe
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



    def get_chart(self, symbol: str, timeframe: Timeframe) -> ChartData :
        ticker = yf.Ticker(symbol)

        period_map = {
            Timeframe.ONE_DAY: "1d",
            Timeframe.ONE_WEEK: "5d",
            Timeframe.ONE_MONTH: "1mo",
            Timeframe.ONE_YEAR: "1y"
        }

        history = ticker.history(period=period_map[timeframe])

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

        return ChartData(symbol = symbol, timeframe = timeframe, points = points)


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
