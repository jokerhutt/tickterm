from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static
from models.financials import TickerFinancials
from util.formatters import format_number, format_ratio, format_percent

from themes import ROSE_PINE


class Financials(Static):

    DEFAULT_CSS = f"""
    Financials {{
        background: {ROSE_PINE["bg"]};
        padding: 1 2;

        border: round {ROSE_PINE["accent"]};

        border-title-align: left;
    }}
    """
    def set_data(self, symbol: str, financials: TickerFinancials) -> None:

        table = Table(expand=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")
        table.add_row("Market Cap", format_number(financials.market_cap))
        table.add_row("P/E Ratio", format_ratio(financials.pe_ratio))
        table.add_row("Revenue", format_number(financials.revenue))
        table.add_row("Net Income", format_number(financials.net_income))
        table.add_row("Profit Margin", format_percent(financials.profit_margin))
        table.add_row("Debt / Equity", format_ratio(financials.debt_to_equity))
        table.add_row("Current Ratio", format_ratio(financials.current_ratio))
        table.add_row("Return on Equity", format_percent(financials.return_on_equity))

        self.update(
            Panel(
                table,
                title=f"{symbol} Financials",
            )
        )
