

from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static

from models.news_item import NewsItem
from themes import ROSE_PINE


class News(Static):

    def set_news(self, items: list[NewsItem]) -> None:

        table = Table.grid(expand = True)
        table.add_column()

        for item in items:

            table.add_row(
                f"{item.source} • {item.published}"
            )

            table.add_row(
                item.title
            )

            table.add_row("")

        self.update(
            Panel(
                table,
                title="News",
                border_style=ROSE_PINE["accent"]
            )
        )

