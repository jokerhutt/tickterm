
from textual.widgets import DataTable


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

        self.add_row(
            "AAPL",
            "Apple",
            "$213.50",
            "+1.20%"
        )

        self.add_row(
            "MSFT",
            "Microsoft",
            "$200",
            "+0.3%"
        )


