from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from models.asset import Asset
from themes import ROSE_PINE

class Summary(Static):

    def set_asset(self, asset: Asset) -> None:

        if asset.change_pct >= 0:
            change_style = ROSE_PINE["positive"]
        else :
            change_style = ROSE_PINE["negative"]

        table = Table.grid(expand=True)

        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")

        table.add_row(
            Text(f"Last\n${asset.price:.2f}", style=ROSE_PINE["text"]),
            Text(f"Change\n{asset.change_pct:+.2f}%", style=change_style),
            Text(f"Volume\n{asset.volume:,}", style=ROSE_PINE["text"]),
            Text(f"Mkt Cap\n{asset.market_cap:,}", style=ROSE_PINE["text"]),
        )

        self.update(

            Panel(
                table,
                title=f"{asset.symbol} • {asset.name}",
                border_style=ROSE_PINE["accent"],
                padding=(0, 1),
            )

        )



