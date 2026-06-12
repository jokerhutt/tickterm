
from textual.widgets import DataTable

from models.asset import Asset

aapl = Asset(
    symbol="AAPL",
    name="Apple Inc.",
    price=213.50,
    change_pct=1.20,
    volume=50_000_000,
    market_cap=3_000_000_000_000
)

msft = Asset(
    symbol="MSFT",
    name="Microsoft",
    price=478.10,
    change_pct=-0.40,
    volume=25_000_000,
    market_cap=3_500_000_000_000
)

assets = [aapl, msft]


class WatchList(DataTable[str]) :

    def on_mount(self) -> None:

        self.cursor_type = "row"
        self.zebra_stripes = True

        self.add_columns(
            "Symbol",
            "Name",
            "Last",
            "%"
        )

        for asset in assets:
            self.add_row(
                asset.symbol,
                asset.name,
                f"${asset.price:.2f}",
                f"{asset.change_pct:+.2f}%"
            )

