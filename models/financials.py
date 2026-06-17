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
    market_cap: int | None
    pe_ratio: float | None

    income: IncomeStatement
    balance: BalanceSheet
    cashflow: CashFlowStatement
