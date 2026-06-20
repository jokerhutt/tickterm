# ∴ Jokerhut / models/financials.py

import pandas as pd
from dataclasses import dataclass
from util import calculations

def _periods(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    return [
        column.strftime("%Y")
        for column in list(frame.columns)[:4]
    ]

def _row(frame: pd.DataFrame, name: str) -> list[float | None]:
    columns = list(frame.columns)[:4]
    if name not in frame.index:
        return [None] * len(columns)
    return [
        calculations.finite(frame.loc[name, column])
        for column in columns
    ]

@dataclass
class IncomeStatement:
    periods: list[str]

    total_revenue: list[float | None]
    gross_profit: list[float | None]
    operating_income: list[float | None]
    net_income: list[float | None]

    @classmethod
    def from_yfinance(cls, frame) -> "IncomeStatement":
        periods = _periods(frame)
        return cls(
            periods=periods,
            total_revenue=_row(frame, "Total Revenue"),
            gross_profit=_row(frame, "Gross Profit"),
            operating_income=_row(frame, "Operating Income"),
            net_income=_row(frame, "Net Income"),
        )


@dataclass
class BalanceSheet:
    periods: list[str]

    total_assets: list[float | None]
    cash_and_equivalents: list[float | None]
    total_debt: list[float | None]
    total_liabilities: list[float | None]
    shareholder_equity: list[float | None]

    @classmethod
    def from_yfinance(cls, frame: pd.DataFrame) -> "BalanceSheet":
        periods = _periods(frame)
        return cls(
            periods=periods,
            total_assets=_row(frame, "Total Assets"),
            cash_and_equivalents=_row(frame, "Cash And Cash Equivalents"),
            total_debt=_row(frame, "Total Debt"),
            total_liabilities=_row(
                frame,
                "Total Liabilities Net Minority Interest",
            ),
            shareholder_equity=_row(frame, "Stockholders Equity"),
        )


@dataclass
class CashFlowStatement:
    periods: list[str]

    operating_cash_flow: list[float | None]
    capital_expenditure: list[float | None]
    free_cash_flow: list[float | None]

    @classmethod
    def from_yfinance(cls, frame: pd.DataFrame) -> "CashFlowStatement":
        periods = _periods(frame)
        return cls(
            periods=periods,
            operating_cash_flow=_row(frame, "Operating Cash Flow"),
            capital_expenditure=_row(frame, "Capital Expenditure"),
            free_cash_flow=_row(frame, "Free Cash Flow"),
        )

@dataclass
class TickerFinancials:

    financial_currency: str

    market_cap: float | None

    pe_ratio: float | None
    forward_pe: float | None
    peg_ratio: float | None
    price_to_book: float | None
    price_to_sales: float | None
    eps: float | None
    beta: float | None

    gross_margin: float | None
    operating_margin: float | None
    profit_margin: float | None
    roa: float | None
    roe: float | None

    total_revenue: float | None
    revenue_growth: float | None
    earnings_growth: float | None
    free_cash_flow: float | None

    debt_to_equity: float | None
    current_ratio: float | None
    quick_ratio: float | None
    total_cash: float | None
    total_debt: float | None

    week_52_high: float | None
    week_52_low: float | None
    dividend_yield: float | None

    income: IncomeStatement
    balance: BalanceSheet
    cashflow: CashFlowStatement

    @classmethod
    def from_yfinance(cls, ticker) -> "TickerFinancials":
        info = ticker.info

        return cls(
            financial_currency=str(info.get("financialCurrency")),

            market_cap=calculations.finite(info.get("marketCap")),

            pe_ratio=calculations.finite(info.get("trailingPE")),
            forward_pe=calculations.finite(info.get("forwardPE")),
            peg_ratio=calculations.finite(info.get("trailingPegRatio")),
            price_to_book=calculations.finite(info.get("priceToBook")),
            price_to_sales=calculations.finite(info.get("priceToSalesTrailing12Months")),
            eps=calculations.finite(info.get("trailingEps")),
            beta=calculations.finite(info.get("beta")),

            gross_margin=calculations.finite(info.get("grossMargins")),
            operating_margin=calculations.finite(info.get("operatingMargins")),
            profit_margin=calculations.finite(info.get("profitMargins")),
            roe=calculations.finite(info.get("returnOnEquity")),
            roa=calculations.finite(info.get("returnOnAssets")),

            total_revenue=calculations.finite(info.get("totalRevenue")),
            revenue_growth=calculations.finite(info.get("revenueGrowth")),
            earnings_growth=calculations.finite(info.get("earningsGrowth")),
            free_cash_flow=calculations.finite(info.get("freeCashflow")),

            total_cash=calculations.finite(info.get("totalCash")),
            total_debt=calculations.finite(info.get("totalDebt")),
            debt_to_equity=calculations.finite(info.get("debtToEquity")),
            current_ratio=calculations.finite(info.get("currentRatio")),
            quick_ratio=calculations.finite(info.get("quickRatio")),

            week_52_high=calculations.finite(info.get("fiftyTwoWeekHigh")),
            week_52_low=calculations.finite(info.get("fiftyTwoWeekLow")),
            dividend_yield=calculations.finite(info.get("dividendYield")),

            income=IncomeStatement.from_yfinance(ticker.income_stmt),
            balance=BalanceSheet.from_yfinance(ticker.balance_sheet),
            cashflow=CashFlowStatement.from_yfinance(ticker.cashflow),
        )
