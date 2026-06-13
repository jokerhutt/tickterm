from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Input

from messages.symbol_selected import SymbolSelected
from mocks import mock_tickers
from models.asset import Asset
from models.chart_data import ChartData
from models.news_item import NewsItem
from services.market_data_service import MarketDataService
from themes import ROSE_PINE
from widgets.chart import Chart
from widgets.news import News
from widgets.summary import Summary
from widgets.ticker_bar import TickerBar
from widgets.watchlist import WatchList

class DashboardScreen(Screen[None]):

    theme = ROSE_PINE

    assets: dict[str, Asset]
    charts: dict[str, ChartData]
    news_items: dict[str, list[NewsItem]]
    current_symbol: str

    service: MarketDataService

    def __init__(self):

        super().__init__()

        self.service = MarketDataService()

        self.assets = {}
        self.charts = {}
        self.news_items = {}
        self.current_symbol = "AAPL"

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

    def on_symbol_selected(self, event: SymbolSelected) -> None:

        self.current_symbol = event.symbol

        summary = self.query_one("#summary", Summary)
        chart = self.query_one("#chart", Chart)
        news = self.query_one("#news", News)

        summary.set_asset(self.assets[self.current_symbol])
        chart.set_chart_data(self.charts[self.current_symbol])
        news.set_news(self.news_items[self.current_symbol])
        

    def on_mount(self) -> None:

        self.current_symbol = "AAPL"
        self.assets = mock_tickers.MOCK_ASSETS
        self.charts = mock_tickers.MOCK_CHARTS
        self.news_items = mock_tickers.MOCK_NEWS

        current_asset = self.assets[self.current_symbol]
        current_chart = self.charts[self.current_symbol]
        current_news = self.news_items[self.current_symbol]

        summary = self.query_one("#summary", Summary)
        news = self.query_one("#news", News)
        chart = self.query_one("#chart", Chart)
        watchlist = self.query_one("#watchlist", WatchList)
        ticker_bar = self.query_one("#ticker", TickerBar)

        summary.set_asset(current_asset)
        ticker_bar.set_assets(list(self.assets.values()))
        watchlist.set_assets(list(self.assets.values()))
        chart.set_chart_data(current_chart)
        news.set_news(current_news)

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

        


