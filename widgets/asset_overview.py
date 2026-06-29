

from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static

from models.asset import Asset


class AssetOverview(Static) :

    def set_asset(self, asset: Asset | None) -> None:

        if asset is None:
            self.update(
                Panel(
                    Text("No asset selected", style="bold"),
                    title="Asset",
                )
            )
            return

        table = Table.grid(expand=True)

        table.add_column()
        table.add_column(justify="right")
        table.add_row("Exchange", asset.exchange or "N/A")
        table.add_row("Currency", asset.currency or "N/A")
        table.add_row("Timezone", asset.timezone or "N/A")

        self.update(
            Panel(
                Group(
                    Text(asset.name or "N/A", style="bold"),
                    table,
                ),
                title="Asset",
            )
        )
