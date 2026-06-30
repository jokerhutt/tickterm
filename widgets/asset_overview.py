# ∴ Jokerhut / widgets/asset_overview.py



from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static

from models.asset import Asset
from themes import ROSE_PINE


class AssetOverview(Static) :

    def set_asset(self, asset: Asset | None) -> None:

        if asset is None:
            self.update(
                Group(
                    Text("Asset Detail", style=(ROSE_PINE["gold"])),
                    Text(),
                    Text("No asset selected"),
                )
            )
            return

        currency = asset.currency or "N/A"

        self.update(
            Group(
                Text("Asset Detail", style=ROSE_PINE["gold"]),
                Text(),
                Text(asset.name or asset.symbol, style="bold"),
                Text(f"{currency}", style="dim"),
            )
        )
