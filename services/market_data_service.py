# ∴ Jokerhut / services/market_data_service.py


from typing import cast
from pandas import Timestamp
from textual import log
from yfinance.base import FastInfo
import yfinance as yf
from models.asset import Asset
from models.chart_data import ChartCache, ChartData, ChartPoint, TimeRange, Timeframe
from models.financials import TickerFinancials
from models.news_item import NewsItem
import util.calculations as calculations


class MarketDataService:
    
    def get_asset(self, symbol: str) -> Asset :

        ticker = yf.Ticker(symbol)
        info : FastInfo = ticker.fast_info

        price = float(info["lastPrice"])
        previous_close = float(info["previousClose"])
        volume = int(info["lastVolume"])
        market_cap = int(info["marketCap"])

        currency = info["currency"]
        timezone = info["timezone"]
        
        log(f"tz: {timezone}")

        change_pct = calculations.calc_change_pct(price, previous_close)

        return Asset(
            symbol = symbol,
            name = symbol,
            currency = currency,
            timezone = timezone,
            price = price, 
            change_pct = change_pct,
            volume = volume,
            market_cap = market_cap
        )

    def get_row(self, frame, name: str) -> list[float | None]:
        columns = list(frame.columns)[:4]

        if name not in frame.index:
            return [None] * len(columns)

        return [
            calculations.finite(frame.loc[name, column])
            for column in columns
        ]

    def get_financials(self, symbol: str) -> TickerFinancials:
        ticker = yf.Ticker(symbol)
        return TickerFinancials.from_yfinance(ticker)



    def update_intraday_cache(self, symbol: str, cache: ChartCache) -> ChartCache:
        ticker = yf.Ticker(symbol)
        period = "1d"
        interval="1m"
        history  = ticker.history(period = period, interval = interval)

        if history.empty :
            raise ValueError("cache intraday no exist")

        existing = cache.intraday.points
        known = {point.timestamp for point in existing}

        for dt, close in history["Close"].items():
            dt = cast(Timestamp, dt).to_pydatetime()

            if dt in known:
                continue

            existing.append(
                ChartPoint(
                    timestamp=dt,
                    price=float(close),
                )
            )
        return cache

    def update_asset(self, symbol: str, asset: Asset) -> Asset:
        ticker = yf.Ticker(symbol)
        info: FastInfo = ticker.fast_info

        price = float(info["lastPrice"])
        previous_close = float(info["previousClose"])

        asset.price = price
        asset.change_pct = calculations.calc_change_pct(price, previous_close)
        asset.volume = int(info["lastVolume"])
        asset.market_cap = int(info["marketCap"])

        return asset

    def get_chart(self, symbol: str, time_range: TimeRange) -> ChartData :
        ticker = yf.Ticker(symbol)
        period = time_range.value
        interval = time_range.interval

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
