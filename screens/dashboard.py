from datetime import datetime
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Static

from models.asset import Asset
from models.chart_data import ChartData, ChartPoint, Timeframe
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
        height: 4;
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
        background: {ROSE_PINE["bg"]};
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
            Asset("AAPL", "Apple Inc.", 213.50, 1.20, 50_000_000, 3_000_000_000_000),
            Asset("MSFT", "Microsoft", 478.10, -0.40, 25_000_000, 3_500_000_000_000),
            Asset("NVDA", "Nvidia", 142.80, 2.15, 70_000_000, 3_200_000_000_000),
        ]

        aapl = assets[0]

        chart_data = ChartData(
            symbol="AAPL",
            timeframe=Timeframe.ONE_MONTH,
            points=[
                ChartPoint(datetime(2026, 5, 1), 205),
                ChartPoint(datetime(2026, 5, 2), 207),
                ChartPoint(datetime(2026, 5, 3), 200),
                ChartPoint(datetime(2026, 5, 4), 206),
                ChartPoint(datetime(2026, 5, 5), 210),
                ChartPoint(datetime(2026, 5, 6), 212),
                ChartPoint(datetime(2026, 5, 7), 211),
                ChartPoint(datetime(2026, 5, 8), 214),
                ChartPoint(datetime(2026, 5, 9), 217),
                ChartPoint(datetime(2026, 5, 10), 215),
                ChartPoint(datetime(2026, 5, 11), 218),
                ChartPoint(datetime(2026, 5, 12), 220),
                ChartPoint(datetime(2026, 5, 13), 219),
                ChartPoint(datetime(2026, 5, 14), 222),
                ChartPoint(datetime(2026, 5, 15), 224),
                ChartPoint(datetime(2026, 5, 16), 221),
                ChartPoint(datetime(2026, 5, 17), 223),
                ChartPoint(datetime(2026, 5, 18), 226),
                ChartPoint(datetime(2026, 5, 19), 228),
                ChartPoint(datetime(2026, 5, 20), 227),
                ChartPoint(datetime(2026, 5, 21), 230),
                ChartPoint(datetime(2026, 5, 22), 232),
                ChartPoint(datetime(2026, 5, 23), 229),
                ChartPoint(datetime(2026, 5, 24), 231),
                ChartPoint(datetime(2026, 5, 25), 234),
                ChartPoint(datetime(2026, 5, 26), 236),
                ChartPoint(datetime(2026, 5, 27), 235),
                ChartPoint(datetime(2026, 5, 28), 238),
                ChartPoint(datetime(2026, 5, 29), 240),
                ChartPoint(datetime(2026, 5, 30), 242),
            ]
        )

        summary = self.query_one("#summary", Summary)
        news = self.query_one("#news", News)
        chart = self.query_one("#chart", Chart)
        ticker_bar = self.query_one("#ticker", TickerBar)

        summary.set_asset(aapl)
        ticker_bar.set_assets(assets)
        chart.set_chart_data(chart_data)

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

        


