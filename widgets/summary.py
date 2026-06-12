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

            Text("Last\n$213.50", style=ROSE_PINE["text"]),
            Text("Change\n+1.20%", style=change_style),
            Text("Volume\n50M", style=ROSE_PINE["text"]),
            Text("Mkt Cap\n3.0T", style=ROSE_PINE["text"]),

        )

        self.update(

            Panel(
                table,
                title="AAPL • Apple Inc.",
                border_style=ROSE_PINE["accent"],
                padding=(0, 1),
            )

        )



