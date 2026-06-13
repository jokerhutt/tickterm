from textual.widgets import Static
from models.asset import Asset
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from themes import ROSE_PINE

class TickerBar(Static) :

    def set_assets(self, assets: list[Asset]) -> None:

        panels = []
        for asset in assets:
            if asset.change_pct >= 0:
                change_style = ROSE_PINE["positive"]
            else:
                change_style = ROSE_PINE["negative"]

            body = Text.assemble(
                (f"${asset.price:,.2f}", ROSE_PINE["text"]),
                "  ",
                (f"{asset.change_pct:+.2f}%", change_style),
                "\n",
                ("▁▂▃▄▅▆▇█", change_style),
            )

            panel = Panel(
                body,
                title=asset.symbol,
                border_style=ROSE_PINE["overlay"],
                padding=(0, 1),
            )

            panels.append(panel)

        self.update(
            Group(
                Columns(
                    panels,
                    expand=True,
                    equal=True,
                )
            )
        )
