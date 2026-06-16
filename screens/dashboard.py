from datetime import datetime, timedelta
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Input
from yfinance.utils import relativedelta

from messages.symbol_selected import SymbolSelected
import time
from mocks import mock_tickers
from models.asset import Asset
from models.chart_data import ChartCache, ChartData, TimeRange, Timeframe
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
    charts: dict[str, ChartCache]
    news_items: dict[str, list[NewsItem]]
    watchlist: list[str]
    current_symbol: str
    last_refresh : float
    reference_lines: bool
    chart_range: Timeframe

    service: MarketDataService

    def __init__(self):

        super().__init__()

        self.service = MarketDataService()

        self.assets = {}
        self.charts = {}
        self.news_items = {}
        self.last_refresh = time.time()
        self.watchlist = ["AAPL", "MSFT", "NVDA"]
        self.current_symbol = self.watchlist[0]
        self.chart_range = Timeframe.ONE_DAY
        self.reference_lines = True

    BINDINGS = [
        Binding("g", "cycle_timeframe", "Cycle Timeframe"),
        Binding("l", "toggle_reference_lines", "Toggle Reference Lines")
    ]

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
        padding: 1 2;
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


        current_chart_data = self.charts[self.current_symbol].intraday

        summary.set_asset(self.assets[self.current_symbol])
        chart.set_chart_data(current_chart_data, self.chart_range, self.reference_lines)
        news.set_news(self.news_items[self.current_symbol])

    def refresh_intraday(self) -> None:
        for symbol, cache in self.charts.items():
            self.charts[symbol] = self.service.update_intraday_cache(
                symbol,
                cache
            )
            self.assets[symbol] = self.service.update_asset(symbol, self.assets[symbol])
        self.last_refresh = time.time()

        self.query_one("#summary", Summary).set_asset(self.assets[self.current_symbol])
        self.query_one("#ticker", TickerBar).set_assets(list(self.assets.values()))
        self.query_one("#watchlist", WatchList).set_assets(list(self.assets.values()))
        self.query_one("#chart", Chart).set_chart_data(self.get_chart_view(),self.chart_range, self.reference_lines)




    def update_chart_timer(self) -> None:
        age = int(time.time() - self.last_refresh)
        next_refresh = max(0, 60 - age)
        chart = self.query_one("#chart", Chart)
        chart.update_refresh_timer(next_refresh)
        

    def on_mount(self) -> None:

        # every 60 seconds, a minute passes on wall street
        ## as such we must refresh
        self.last_refresh = time.time()
        self.set_interval(1, self.update_chart_timer)
        self.set_interval(60, self.refresh_intraday)

        # boolean toggles
        self.reference_lines = True

        # seed stuffs
        self.current_symbol = self.watchlist[0]
        self.chart_range = Timeframe.ONE_DAY
        for symbol in self.watchlist:
            self.assets[symbol] = self.service.get_asset(symbol)
        for symbol in self.watchlist:
            self.charts[symbol] = ChartCache(
                intraday = self.service.get_chart(symbol, TimeRange.INTRADAY),
                hourly = self.service.get_chart(symbol, TimeRange.HOURLY),
                daily = self.service.get_chart(symbol, TimeRange.DAILY),
                longterm = self.service.get_chart(symbol, TimeRange.LONGTERM)
            )
        for symbol in self.watchlist:
            self.news_items[symbol] = self.service.get_news(symbol)

        # current stuffs
        current_asset = self.assets[self.current_symbol]
        current_chart = self.get_chart_view()
        current_news = self.news_items[self.current_symbol]

        # textual stuffs
        summary = self.query_one("#summary", Summary)
        news = self.query_one("#news", News)
        chart = self.query_one("#chart", Chart)
        watchlist = self.query_one("#watchlist", WatchList)
        ticker_bar = self.query_one("#ticker", TickerBar)

        # setterz
        summary.set_asset(current_asset)
        ticker_bar.set_assets(list(self.assets.values()))
        watchlist.set_assets(list(self.assets.values()))
        chart.set_chart_data(current_chart, self.chart_range, self.reference_lines)
        news.set_news(current_news)


    def filter_chart(self, chart: ChartData | None, cutoff: datetime) -> ChartData | None :
        if chart is None :
            return None

        return chart.last(cutoff)

    def get_chart_view(self) -> ChartData | None:

        symbol = self.current_symbol
        timeframe = self.chart_range

        cache = self.charts[symbol]

        match timeframe:
            case Timeframe.ONE_HOUR:
                return self.filter_chart(
                    cache.intraday,
                    datetime.now(cache.intraday.points[-1].timestamp.tzinfo) - timedelta(hours=1)
                ) if cache.intraday else None

            case Timeframe.ONE_DAY:
                return cache.intraday

            case Timeframe.ONE_WEEK:
                return cache.hourly

            case Timeframe.ONE_MONTH:
                return self.filter_chart(
                    cache.daily,
                    datetime.now(cache.daily.points[-1].timestamp.tzinfo) - relativedelta(months=1)
                ) if cache.daily else None

            case Timeframe.ONE_YEAR:
                return self.filter_chart(
                    cache.daily,
                    datetime.now(cache.daily.points[-1].timestamp.tzinfo) - relativedelta(years=1)
                ) if cache.daily else None

            case Timeframe.FIVE_YEARS:
                return cache.daily

            case Timeframe.MAX:
                return cache.longterm

    def action_cycle_timeframe(self) -> None:
        timeframes = list(Timeframe)

        current_index = timeframes.index(self.chart_range)
        next_index = (current_index + 1) % len(timeframes)

        self.chart_range = timeframes[next_index]

        chart = self.query_one("#chart", Chart)
        chart.set_chart_data(self.get_chart_view(), self.chart_range, self.reference_lines)

    def action_toggle_reference_lines(self) -> None:
        self.reference_lines = not self.reference_lines
        chart = self.query_one("#chart", Chart)
        chart.set_chart_data(self.get_chart_view(), self.chart_range, self.reference_lines)

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

        


