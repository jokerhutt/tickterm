# ∴ Jokerhut / widgets/watchlist.py


from rich.console import RenderableType
from rich.text import Text
from textual.widgets import DataTable
from typing_extensions import OrderedDict
from messages.symbol_selected import SymbolSelected
from models.asset import Asset
from themes import ROSE_PINE


class WatchList(DataTable[RenderableType]) :

    def on_mount(self) -> None:

        self.cursor_type = "row"
        self.zebra_stripes = True

        # so that it jumps to 0 + 1 in data_table_row_highlighted
        self.last_row = -1

        self.add_columns(
            "Symbol",
            "Type",
            "Last",
            "%"
        )

        self.asset_rows = {}

    def set_assets(self, assets: list[Asset]) :
        self.clear()
        self.asset_rows.clear()
        self.last_row = -1

        row = 0

        # Group assets by quote type e.g. EQUITY or CRYPTOCURRENCY or INDEX 
        groups = self._group_assets(assets)

        
        for quote_type, members in groups.items():

            self.add_row(
                "",
                Text(quote_type.upper(), style = "bold yellow"),
                "",
                ""
            )

            row += 1

            for asset in members:
                change_color = (
                    ROSE_PINE["positive"] if asset.change_pct > 0 else ROSE_PINE["negative"]
                )

                self.add_row(
                    asset.symbol,
                    asset.quote_type,
                    f"${asset.price:.2f}",
                    Text(f"{asset.change_pct:+.2f}%", style = change_color)
                )

                self.asset_rows[row] = asset
                row += 1

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        if event.cursor_row == 0:
            self.move_cursor(row=1)
            return

        direction = 1 if event.cursor_row > self.last_row else -1
        self.last_row = event.cursor_row

        if event.cursor_row not in self.asset_rows:
            self.move_cursor(row=event.cursor_row + direction)

    def on_data_table_row_selected(
        self,
        event: DataTable.RowSelected
    ):
        asset = self.asset_rows[event.cursor_row]

        self.post_message(
            SymbolSelected(asset.symbol)
        )

    def _group_assets(self, assets: list[Asset]) -> OrderedDict[str, list[Asset]]:
        groups = OrderedDict()
        for asset in assets:
            groups.setdefault(asset.quote_type, []).append(asset)
        return groups


