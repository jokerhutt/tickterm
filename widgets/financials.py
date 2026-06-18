from os import wait
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.widgets import Static
from models.financials import TickerFinancials
from util.formatters import format_number, format_ratio, format_percent

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
            ("Market Cap", format_number(financials.market_cap)),
            ("P/E Ratio", format_ratio(financials.pe_ratio)),
            ("Revenue", format_number(financials.income.total_revenue[0])),
            ("Net Income", format_number(financials.income.net_income[0]))
        ]

        health = [
            ("Assets", format_number(financials.balance.total_assets[0])),
            ("Liabilities", format_number(financials.balance.total_liabilities[0])),
            ("Debt", format_number(financials.balance.total_debt[0])),
            ("Equity", format_number(financials.balance.shareholder_equity[0]))
        ]

        body = Group(
            self.stat_group("Valuation", valuation),
            Text(""),

            self.stat_group("Balance Sheet Snapshot", health),
            Text(""),

            self.statement_table(
                "Income Statement",
                financials.income.periods,
                [
                    ("Revenue", financials.income.total_revenue),
                    ("Gross Profit", financials.income.gross_profit),
                    ("Operating Income", financials.income.operating_income),
                    ("Net Income", financials.income.net_income),
                ]
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
                ]
            ),

            Text(""),

            self.statement_table(
                "Cash Flow",
                financials.cashflow.periods,
                [
                    ("Operating CF", financials.cashflow.operating_cash_flow),
                    ("CapEx", financials.cashflow.capital_expenditure),
                    ("Free CF", financials.cashflow.free_cash_flow),
                ]
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
        rows: list[tuple[str, list[float | None]]]
    ) -> Table:

        table = Table.grid(padding=(0, 1))

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
                    Text(format_number(value), style=color)
                )

            table.add_row(*row)

        return table

    def stat_group(self, title: str, rows: list[tuple[str, str]]) -> Group:
        grid = Table.grid(expand = True, padding = (0, 2))

        for _ in range(4):
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
