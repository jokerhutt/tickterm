# ∴ Jokerhut / widgets/financials.py


from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.widgets import Static
from models.financials import TickerFinancials
from util.formatters import format_money, format_number, format_percentage_points, format_ratio, format_percent

from themes import ROSE_PINE


class Financials(Static):

    LABEL_WIDTH = 20

    DEFAULT_CSS = f"""
    Financials {{
        background: {ROSE_PINE["bg"]};
        padding: 1 2;

        border: round {ROSE_PINE["accent"]};

        border-title-align: left;
    }}
    """
    def set_data(self, symbol: str, financials: TickerFinancials) -> None:

        valuation = [
            ("Market Cap", format_number(financials.market_cap, financials.financial_currency)),
            ("Trailing P/E", format_ratio(financials.pe_ratio)),
            ("Forward P/E", format_ratio(financials.forward_pe)),
            ("PEG", format_ratio(financials.peg_ratio)),
            ("Price/Book", format_ratio(financials.price_to_book)),
            ("Price/Sales", format_ratio(financials.price_to_sales)),
            ("EPS (ttm)", format_money(financials.eps, financials.financial_currency)),
            ("Beta", format_ratio(financials.beta)),
        ]
        profitability = [
            ("Gross Margin", format_percent(financials.gross_margin)),
            ("Oper. Margin", format_percent(financials.operating_margin)),
            ("Profit Margin", format_percent(financials.profit_margin)),
            ("ROE", format_percent(financials.roe)),
        ]
        growth = [
            ("Revenue (ttm)", format_number(financials.total_revenue, financials.financial_currency)),
            ("Rev. Growth", format_percent(financials.revenue_growth)),
            ("Earnings Growth", format_percent(financials.earnings_growth)),
            ("Free Cashflow", format_number(financials.free_cash_flow, financials.financial_currency)),
        ]
        health = [
            ("Total Cash", format_number(financials.total_cash, financials.financial_currency)),
            ("Total Debt", format_number(financials.total_debt, financials.financial_currency)),
            ("Debt/Equity", format_ratio(financials.debt_to_equity)),
            ("Current Ratio", format_ratio(financials.current_ratio)),
        ]
        market = [
            ("52w High", format_money(financials.week_52_high, financials.financial_currency)),
            ("52w Low", format_money(financials.week_52_low, financials.financial_currency)),
            ("Dividend Yield", format_percentage_points(financials.dividend_yield)),
        ]

        body = Group(
            self.stat_group("Valuation", valuation, columns = 4),
            Text(""),

            self.stat_group("Profitability", profitability, columns = 4),
            Text(""),

            self.stat_group("Growth & Cash", growth, columns = 4),
            Text(""),

            self.stat_group("Balance Sheet Health", health, columns = 4),
            Text(""),

            self.stat_group("Market", market, columns = 4),
            Text(""),

            self.statement_table(
                "Income Statement",
                financials.income.periods,
                [
                    ("Revenue", financials.income.total_revenue),
                    ("Gross Profit", financials.income.gross_profit),
                    ("Operating Income", financials.income.operating_income),
                    ("Net Income", financials.income.net_income),
                ],
                financials.financial_currency
            ),

            Text(""),

            self.statement_table(
                "Balance Sheet",
                financials.balance.periods,
                [
                    ("Assets", financials.balance.total_assets),
                    ("Cash", financials.balance.cash_and_equivalents),
                    ("Liabilities", financials.balance.total_liabilities),
                    ("Debt", financials.balance.total_debt),
                    ("Equity", financials.balance.shareholder_equity),
                ],
                financials.financial_currency
            ),

            Text(""),

            self.statement_table(
                "Cash Flow",
                financials.cashflow.periods,
                [
                    ("Operating CF", financials.cashflow.operating_cash_flow),
                    ("CapEx", financials.cashflow.capital_expenditure),
                    ("Free CF", financials.cashflow.free_cash_flow),
                ],
                financials.financial_currency
            )
        )

        self.update(
            Panel(
                body,
                title=f"{symbol} Financials",
                border_style=ROSE_PINE["accent"],
                padding=(1, 2)
            )
        )

    def statement_table(
        self,
        title: str,
        periods: list[str],
        rows: list[tuple[str, list[float | None]]],
        currency: str
    ) -> Table:

        table = Table.grid(padding=(0, 12))

        table.add_column(width=self.LABEL_WIDTH)

        for _ in periods:
            table.add_column(justify="right")

        header = [
            Text(title, style=f"bold {ROSE_PINE['gold']}")
        ]

        for period in periods:
            header.append(
                Text(period, style=ROSE_PINE["muted"])
            )

        table.add_row(*header)

        for label, values in rows:

            row = [Text(label, style=ROSE_PINE["text"])]

            for value in values:
                color = ROSE_PINE["positive"] if value and float(value) > 0 else ROSE_PINE["negative"]
                row.append(
                    Text(format_number(value, currency), style=color)
                )

            table.add_row(*row)

        return table

    def stat_group(self, title: str, rows: list[tuple[str, str]], columns: int = 4) -> Group:
        grid = Table.grid(expand = True, padding = (0, 2))

        for _ in range(columns):
            grid.add_column(ratio = 1)

        cells = []

        for label, value in rows:
            cell = Text.assemble((label + "\n", ROSE_PINE["muted"]), (str(value), ROSE_PINE["text"]))
            cells.append(cell)

        for i in range(0, len(cells), 4):
            grid.add_row(*cells[i:i + 4])

        return Group(
            Text(title, style = f"bold {ROSE_PINE['gold']}"),
            grid
        )
