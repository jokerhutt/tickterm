# ∴ Jokerhut / services/market_data_service.py


from typing import Any, cast
from pandas import Timestamp
from yfinance.base import FastInfo
from models.asset import Asset
from models.chart_data import ChartCache, ChartData, ChartPoint, TimeRange, Timeframe
from models.financials import BalanceSheet, CashFlowStatement, IncomeStatement, TickerFinancials
from models.news_item import NewsItem
import math
import yfinance as yf
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

        info = ticker.info
        income_statement = ticker.income_stmt
        balance_sheet = ticker.balance_sheet
        cashflow_statement = ticker.cashflow

        financial_currency : str = str(info.get("financialCurrency"))

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

        # what a fat chunk
        return TickerFinancials(
            # currency
            financial_currency = financial_currency,

            # valuation
            market_cap=calculations.finite(info.get("marketCap")),
            pe_ratio=calculations.finite(info.get("trailingPE")),
            forward_pe=calculations.finite(info.get("forwardPE")),
            peg_ratio=calculations.finite(info.get("trailingPegRatio")),
            price_to_book=calculations.finite(info.get("priceToBook")),
            price_to_sales=calculations.finite(info.get("priceToSalesTrailing12Months")),
            eps=calculations.finite(info.get("trailingEps")),
            beta=calculations.finite(info.get("beta")),

            # profitability
            gross_margin=calculations.finite(info.get("grossMargins")),
            operating_margin=calculations.finite(info.get("operatingMargins")),
            profit_margin=calculations.finite(info.get("profitMargins")),
            roe=calculations.finite(info.get("returnOnEquity")),
            roa=calculations.finite(info.get("returnOnAssets")),

            # growth 
            total_revenue=calculations.finite(info.get("totalRevenue")),
            revenue_growth=calculations.finite(info.get("revenueGrowth")),
            earnings_growth=calculations.finite(info.get("earningsGrowth")),
            free_cash_flow=calculations.finite(info.get("freeCashflow")),

            # health
            total_cash=calculations.finite(info.get("totalCash")),
            total_debt=calculations.finite(info.get("totalDebt")),
            debt_to_equity=calculations.finite(info.get("debtToEquity")),
            current_ratio=calculations.finite(info.get("currentRatio")),
            quick_ratio=calculations.finite(info.get("quickRatio")),

            # market
            week_52_high=calculations.finite(info.get("fiftyTwoWeekHigh")),
            week_52_low=calculations.finite(info.get("fiftyTwoWeekLow")),
            dividend_yield=calculations.finite(info.get("dividendYield")),

            # statements
            income=income,
            balance=balance,
            cashflow=cashflow,
        )


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
