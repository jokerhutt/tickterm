from rich.console import RenderableType
from rich.text import Text
from textual.widgets import DataTable
from messages.symbol_selected import SymbolSelected
from models.asset import Asset
from themes import ROSE_PINE



class WatchList(DataTable[RenderableType]) :

    def on_mount(self) -> None:

        self.cursor_type = "row"
        self.zebra_stripes = True

        self.add_columns(
            "Symbol",
            "Name",
            "Last",
            "%"
        )

    def set_assets(self, assets: list[Asset]):
        self.clear()
        for asset in assets:

            change_color = (
                ROSE_PINE["positive"] if asset.change_pct > 0 else ROSE_PINE["negative"]
            )

            self.add_row(
                asset.symbol,
                asset.name,
                f"${asset.price:.2f}",
                Text(f"{asset.change_pct:+.2f}%", style = change_color)
            )

    def on_data_table_row_selected(
        self,
        event: DataTable.RowSelected
    ):
        symbol = self.get_row_at(event.cursor_row)[0]

        self.post_message(
            SymbolSelected(symbol)
        )


