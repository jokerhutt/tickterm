# ∴ Jokerhut / models/financials.py


from dataclasses import dataclass

@dataclass
class IncomeStatement:
    periods: list[str]

    total_revenue: list[float | None]
    gross_profit: list[float | None]
    operating_income: list[float | None]
    net_income: list[float | None]


@dataclass
class BalanceSheet:
    periods: list[str]

    total_assets: list[float | None]
    cash_and_equivalents: list[float | None]
    total_debt: list[float | None]
    total_liabilities: list[float | None]
    shareholder_equity: list[float | None]


@dataclass
class CashFlowStatement:
    periods: list[str]

    operating_cash_flow: list[float | None]
    capital_expenditure: list[float | None]
    free_cash_flow: list[float | None]


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
