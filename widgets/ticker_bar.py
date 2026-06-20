# ∴ Jokerhut / widgets/ticker_bar.py


import math
from textual.widgets import Static
from models.asset import Asset
from models.chart_data import ChartCache
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from themes import ROSE_PINE


class TickerBar(Static) :

    def sparkline(self, values: list[float], width: int = 32) -> str :
        if not values:
            return " " * width
        if len(values) > width:
            stride = len(values) / width
            values = [values[int(i * stride)] for i in range(width)]

        low = min(values)
        high = max(values)
        blocks = "▁▂▃▄▅▆▇█"

        if math.isclose(low, high):
            return blocks[3] * len(values)

        return "".join(
            blocks[int((value - low) / (high - low) * (len(blocks) - 1))]
            for value in values
        )

    def set_assets(self, assets: list[Asset], caches: dict[str, ChartCache]) -> None:

        panels = []
        for asset in assets:
            if asset.change_pct >= 0:
                change_style = ROSE_PINE["positive"]
            else:
                change_style = ROSE_PINE["negative"]

            cache = caches[asset.symbol]

            prices: list[float] = []

            if cache.intraday is not None :
                prices = [
                    point.price
                    for point in cache.intraday.bucket(20).points
                ]


            spark = self.sparkline(prices)

            body = Text.assemble(
                (f"${asset.price:,.2f}", ROSE_PINE["text"]),
                "  ",
                (f"{asset.change_pct:+.2f}%", change_style),
                "\n",
                (spark, change_style),
            )

            panel = Panel(
                body,
                title=asset.symbol,
                border_style=ROSE_PINE["accent"],
                padding=(0, 1),
            )

            panels.append(panel)

        self.update(
            Group(
                Columns(
                    panels,
                    expand=False,
                    equal=False,
                )
            )
        )
