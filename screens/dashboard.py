# ∴ Jokerhut / screens/dashboard.py


from store import Store
import time
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from messages.symbol_selected import SymbolSelected
from models.asset import Asset
from models.chart_data import ChartCache, ChartData, TimeRange, Timeframe
from models.financials import TickerFinancials
from models.news_item import NewsItem
from screens.add_ticker_modal import AddTickerModal
from services.market_data_service import MarketDataService
from themes import ROSE_PINE
from widgets.chart import Chart
from widgets.financials import Financials
from widgets.news import News
from widgets.summary import Summary
from widgets.ticker_bar import TickerBar
from widgets.watchlist import WatchList

class DashboardScreen(Screen[None]):

    theme = ROSE_PINE

    store: Store

    service: MarketDataService

    chart_range: Timeframe

    reference_lines: bool
    show_financials: bool

    def __init__(self):

        super().__init__()

        # service /
        self.service = MarketDataService()

        # store /
        self.store = Store()

        self.chart_range = Timeframe.ONE_DAY

        # timers /
        self.last_refresh = time.time()

        # booleans /
        self.reference_lines = True
        self.show_financials = False

    BINDINGS = [
        Binding("g", "cycle_timeframe", "Cycle Timeframe"),
        Binding("l", "toggle_reference_lines", "Toggle Reference Lines"),
        Binding("a", "add_ticker", "Add Ticker"),
        Binding("v", "toggle_view", "Toggle View")
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
        width: 35;
    }}

    #content {{
        layout: vertical;
        height: 1fr;
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

    #vscroll {{
        height: 1fr;
        display: none;
        overflow-y: auto;
    }}

    #financials {{}}

    #news {{
        height: 8;
    }}

    """


    # -- UI Nodes --
    def set_summary_node(self, asset: Asset) :
        summary = self.query_one("#summary", Summary)
        summary.set_asset(asset)

    def set_chart_node(self, chart_data: ChartData, range: Timeframe, show_lines: bool = True) :
        chart = self.query_one("#chart", Chart)
        chart.set_chart_data(chart_data = chart_data, timeframe = range, reference_lines = show_lines)

    def set_financials_node(self, symbol: str, financial_data: TickerFinancials) :
        financials = self.query_one("#financials", Financials)
        financials.set_data(symbol, financial_data)

    def set_news_node(self, news_items: list[NewsItem]) :
        news = self.query_one("#news", News)
        news.set_news(news_items)

    def set_watchlist_node(self, assets: list[Asset]) :
        watchlist = self.query_one("#watchlist", WatchList)
        watchlist.set_assets(assets)

    def set_tickers_node(self, assets: list[Asset], cache: dict[str, ChartCache]) :
        tickers = self.query_one("#ticker", TickerBar)
        tickers.set_assets(assets, cache)

    def on_symbol_selected(self, event: SymbolSelected) -> None:
        self.store.set_current_symbol(event.symbol)
        self.set_summary_node(self.store.get_current_asset())
        self.set_chart_node(self.store.get_current_chart().intraday, self.chart_range, self.reference_lines)
        self.set_financials_node(self.store.get_current_symbol(), self.store.get_current_financials())
        self.set_news_node(self.store.get_current_news())


    # -- UI Updates --
    def refresh_intraday(self) -> None:
        for symbol, cache in self.store.charts.items():
            self.store.set_asset(symbol, self.service.update_asset(symbol, self.store.get_asset(symbol)))
            updated_cache = self.service.update_intraday_cache(symbol, cache)
            self.store.set_chart(symbol = symbol, chart_cache = updated_cache)
        self.last_refresh = time.time()

        self.set_summary_node(self.store.get_current_asset())
        self.set_watchlist_node(self.store.get_assets())
        self.set_tickers_node(self.store.get_assets(), self.store.get_charts())
        self.set_chart_node(self.store.get_current_chart().get_chart_view(self.chart_range), self.chart_range, self.reference_lines)

    def update_chart_timer(self) -> None:
        age = int(time.time() - self.last_refresh)
        next_refresh = max(0, 60 - age)
        chart = self.query_one("#chart", Chart)
        chart.update_refresh_timer(next_refresh)

    def load_symbol(self, symbol: str) :

        # load quick info
        self.store.set_asset(symbol, self.service.get_asset(symbol))

        # load chart points
        self.store.set_chart(symbol, ChartCache(
            intraday = self.service.get_chart(symbol, TimeRange.INTRADAY),
            hourly = self.service.get_chart(symbol, TimeRange.HOURLY),
            daily = self.service.get_chart(symbol, TimeRange.DAILY),
            longterm = self.service.get_chart(symbol, TimeRange.LONGTERM)
        ))

        # load news
        self.store.set_news(symbol, self.service.get_news(symbol))

        # load financial statements
        self.store.set_financials(symbol, self.service.get_financials(symbol))

    def on_mount(self) -> None:

        # every 60 seconds, a minute passes on wall street
        ## as such we must refresh
        self.last_refresh = time.time()
        self.set_interval(1, self.update_chart_timer)
        self.set_interval(60, self.refresh_intraday)

        # boolean toggles
        self.reference_lines = True

        # seed stuffs
        self.store.set_current_symbol(self.store.get_watchlist()[0])
        self.chart_range = Timeframe.ONE_DAY
        for symbol in self.store.get_watchlist():
            self.load_symbol(symbol)

        self.set_summary_node(self.store.get_current_asset())
        self.set_tickers_node(self.store.get_assets(), self.store.get_charts())
        self.set_watchlist_node(self.store.get_assets())
        self.set_chart_node(self.store.get_current_chart().intraday, self.chart_range, self.reference_lines)
        self.set_financials_node(self.store.get_current_symbol(), self.store.get_current_financials())
        self.set_news_node(self.store.get_current_news())

    def action_add_ticker(self) -> None:
        self.app.push_screen(
            AddTickerModal(),
            self.on_ticker_added
        )

    def on_ticker_added(self, symbol: str | None) -> None:
        if symbol is None or symbol in self.store.get_watchlist():
            return

        self.load_symbol(symbol)
        self.set_tickers_node(self.store.get_assets(), self.store.get_charts())
        self.set_watchlist_node(self.store.get_assets())


    def action_cycle_timeframe(self) -> None:
        timeframes = list(Timeframe)

        current_index = timeframes.index(self.chart_range)
        next_index = (current_index + 1) % len(timeframes)

        self.chart_range = timeframes[next_index]

        self.set_chart_node(self.store.get_current_chart().get_chart_view(self.chart_range), self.chart_range, self.reference_lines)

    def action_toggle_reference_lines(self) -> None:
        self.reference_lines = not self.reference_lines
        self.set_chart_node(self.store.get_current_chart().get_chart_view(self.chart_range), self.chart_range, self.reference_lines)

    def action_toggle_view(self) -> None:
        self.show_financials = not self.show_financials
        chart = self.query_one("#chart", Chart)
        vscroll = self.query_one("#vscroll", VerticalScroll)
        chart.display = not self.show_financials
        vscroll.display = self.show_financials

    def compose(self):
        yield TickerBar(id="ticker")

        with Horizontal(id = "body"):

            # Left pane stuff
            with Vertical(id = "sidebar"):
                yield WatchList(id = "watchlist")

            # Right pane stuff
            with Vertical(id = "main"):
                yield Summary(id="summary")
                with Container(id = "content"):
                    yield Chart(id="chart")
                    with VerticalScroll(id="vscroll"):
                        yield Financials(id = "financials")
                yield News(id="news")
        


