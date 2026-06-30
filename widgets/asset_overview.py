# ∴ Jokerhut / widgets/asset_overview.py



from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static

from models.asset import Asset, AssetMetadata
from themes import ROSE_PINE


class AssetOverview(Static) :

    def set_asset(self, asset: Asset | None, metadata: AssetMetadata | None) -> None:

        if asset is None:
            self.update(
                Group(
                    Text("Asset Detail", style=(ROSE_PINE["gold"])),
                    Text(),
                    Text("No asset selected"),
                )
            )
            return

        if metadata is None:
            metadata = AssetMetadata(
                symbol=asset.symbol,
                long_name="",
                description="",
                sector="",
                industry="",
                exchange="",
            )

        currency = asset.currency or "N/A"
        long_name = metadata.long_name or asset.name or asset.symbol
        industry = metadata.industry or "No industry found"
        sector = metadata.sector or "No sector found"
        exchange = metadata.exchange or "No exchange found"

        self.update(
            Group(
                Text("Asset Detail", style=ROSE_PINE["gold"]),
                Text(),
                Text(f"{long_name} {asset.name or asset.symbol}", style="bold"),
                Text(f"Sector: {sector}", style = "dim"),
                Text(f"Industry: {industry}", style = "dim"),
                Text(f"Exchange: {exchange}", style = "dim"),
                Text(f"Currency: {currency}", style="dim"),
            )
        )
