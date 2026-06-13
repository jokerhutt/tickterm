from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Static

from models.asset import Asset
from models.news_item import NewsItem
from themes import ROSE_PINE
from widgets.chart import Chart
from widgets.news import News
from widgets.summary import Summary
from widgets.ticker_bar import TickerBar
from widgets.watchlist import WatchList

class DashboardScreen(Screen[None]):

    theme = ROSE_PINE

    CSS = f"""

    Screen {{
        background: {ROSE_PINE["bg"]};
        color: {ROSE_PINE["text"]};
    }}

    #ticker {{
        background: {ROSE_PINE["surface"]};
        height: 3;
    }}

    #body {{
        height: 1fr;
    }}

    #sidebar {{
        background: {ROSE_PINE["surface"]};
        width: 40;
    }}

    #main {{
        background: {ROSE_PINE["bg"]};
        width: 1fr;
    }}

    #watchlist {{
        background: {ROSE_PINE["surface"]};
        height: 1fr;
    }}

    #summary {{
        height: 4;
    }}

    #chart {{
        height: 1fr;
    }}

    #news {{
        height: 8;
    }}

    #command {{
        height: 3;
    }}

    """

    def on_mount(self) -> None:

        assets = [ 
            Asset(
                symbol = "AAPL",
                name = "Apple Inc.",
                price = 213.50,
                change_pct = 1.20,
                volume = 50_000_000,
                market_cap = 3_000_000_000_000
            )
        ]

        aapl = assets[0]

        summary = self.query_one("#summary", Summary)
        news = self.query_one("#news", News)
        ticker_bar = self.query_one("#ticker", TickerBar)

        summary.set_asset(aapl)
        ticker_bar.set_assets(assets)

        news_list = [NewsItem("Apple releases Siri", "NYT", "2nd June")]

        news.set_news(news_list)

    def compose(self):
        yield TickerBar(id="ticker")

        with Horizontal(id = "body"):

            # Left pane stuff
            with Vertical(id = "sidebar"):
                yield WatchList(id = "watchlist")

            # Right pane stuff
            with Vertical(id = "main"):
                yield Summary(id="summary")
                yield Chart(id="chart")
                yield News(id="news")

        yield Input(placeholder="Command...", id="command")

        
