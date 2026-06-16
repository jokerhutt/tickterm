from dataclasses import dataclass

@dataclass
class TickerFinancials:
    market_cap: int | None
    pe_ratio: float | None
    revenue: int | None
    net_income: int | None
    profit_margin: float | None
    debt_to_equity: float | None
    current_ratio: float | None
    return_on_equity: float | None
