from typing import Any
from pandas import Timestamp
from yfinance.base import FastInfo
from models.asset import Asset
from models.chart_data import ChartCache, ChartData, ChartPoint, TimeRange, Timeframe
from models.financials import BalanceSheet, CashFlowStatement, IncomeStatement, TickerFinancials
from models.news_item import NewsItem
import math
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



    def finite(self, value: Any):
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        return number if math.isfinite(number) else None

    def get_row(self, frame, name: str) -> list[float | None]:
        columns = list(frame.columns)[:4]

        if name not in frame.index:
            return [None] * len(columns)

        return [
            self.finite(frame.loc[name, column])
            for column in columns
        ]

    def get_financials(self, symbol: str) -> TickerFinancials:
        ticker = yf.Ticker(symbol)

        info = ticker.info
        income_statement = ticker.income_stmt
        balance_sheet = ticker.balance_sheet
        cashflow_statement = ticker.cashflow

        periods = []

        if not income_statement.empty:
            columns = list(income_statement.columns)[:4]

            for column in columns:
                periods.append(column.strftime("%Y"))

        income = IncomeStatement(
            periods = periods,
            total_revenue=self.get_row(income_statement, "Total Revenue"),
            gross_profit=self.get_row(income_statement, "Gross Profit"),
            operating_income=self.get_row(income_statement, "Operating Income"),
            net_income=self.get_row(income_statement, "Net Income")
        )

        balance = BalanceSheet(
            periods = periods,
            total_assets = self.get_row(balance_sheet, "Total Assets"),
            cash_and_equivalents = self.get_row(balance_sheet, "Cash And Cash Equivalents"),
            total_liabilities = self.get_row(balance_sheet, "Total Liabilities Net Minority Interest"),
            total_debt = self.get_row(balance_sheet, "Total Debt"),
            shareholder_equity = self.get_row(balance_sheet, "Stockholders Equity"),
        )

        cashflow = CashFlowStatement(
            periods = periods,
            operating_cash_flow=self.get_row(cashflow_statement, "Operating Cash Flow"),
            capital_expenditure=self.get_row(cashflow_statement, "Capital Expenditure"),
            free_cash_flow=self.get_row(cashflow_statement, "Free Cash Flow"),
        )

        market_cap = self.finite(info.get("marketCap"))
        pe_ratio = self.finite(info.get("trailingPE"))

        return TickerFinancials(market_cap = market_cap, pe_ratio = pe_ratio, income = income, balance = balance, cashflow = cashflow)










 

    def update_intraday_cache(self, symbol: str, cache: ChartCache) -> ChartCache:
        ticker = yf.Ticker(symbol)
        period = "1d"
        interval="1m"
        history  = ticker.history(period = period, interval = interval)

        if history.empty :
            raise ValueError("cache intraday no exist")

        existing = cache.intraday.points
        known = {point.timestamp for point in existing}

        for timestamp, row in history.iterrows():
            dt = timestamp.to_pydatetime()

            if dt not in known:
                existing.append(
                    ChartPoint(
                        timestamp = dt,
                        price = float(row["Close"])
                    )
                )
                known.add(dt)

        return cache

    def update_asset(self, symbol: str, asset: Asset) -> Asset:
        ticker = yf.Ticker(symbol)
        info: FastInfo = ticker.fast_info

        price = float(info["lastPrice"])
        previous_close = float(info["previousClose"])

        asset.price = price
        asset.change_pct = (
            (price - previous_close) / previous_close
        ) * 100

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
