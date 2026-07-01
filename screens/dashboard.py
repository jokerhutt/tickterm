# ∴ Jokerhut / screens/dashboard.py


import asyncio
from textual import work
from textual.widgets import ContentSwitcher, Footer, Static
from screens.loading_screen import LoadingScreen
from store import Store
import time
from textual.binding import Binding
from textual.containers import Container, Horizontal, HorizontalScroll, Vertical, VerticalScroll
from textual.screen import Screen
from messages.symbol_selected import SymbolSelected
from models.asset import Asset, AssetMetadata
from models.chart_data import ChartCache, ChartData, TimeRange, Timeframe
from models.financials import TickerFinancials
from models.news_item import NewsItem
from screens.add_ticker_modal import AddTickerModal
from services.market_data_service import MarketDataService
from themes import ROSE_PINE
from widgets.asset_overview import AssetOverview
from widgets.chart import Chart
from widgets.financials import Financials
from widgets.news import News
from widgets.summary import Summary
from widgets.watchlist import WatchList


class DashboardScreen(Screen[None]):

    ## Attributes //

    store: Store
    service: MarketDataService
    chart_range: Timeframe


    ## Bindings //

    BINDINGS = [
        Binding("g", "cycle_timeframe", "Cycle Timeframe"),
        Binding("l", "toggle_reference_lines", "Toggle Reference Lines"),
        Binding("a", "add_ticker", "Add Ticker"),
        Binding("d", "remove_ticker", "Remove Ticker"),
        Binding("v", "toggle_view", "Toggle View")
    ]

    ## Styling //

    theme = ROSE_PINE

    CSS = f"""

    Screen {{
        background: {ROSE_PINE["bg"]};
        color: {ROSE_PINE["text"]};
    }}

    #loading {{}}

    #footer {{}}

    #body {{
        height: 1fr;
    }}

    #sidebar {{
        background: {ROSE_PINE["surface"]};
        width: 40;
    }}

    #content {{
        height: 1fr;
    }}

    #main {{
        background: {ROSE_PINE["bg"]};
        width: 1fr;
        padding: 1 2;
    }}

    #watchlist {{
        background: {ROSE_PINE["surface"]};
        height: 3fr;
    }}

    #asset-overview {{
        background: {ROSE_PINE["surface"]};
        height: 1fr;
        padding: 1;
    }}

    WatchList > .datatable--cursor {{
        background: {ROSE_PINE["accent"]};
        color: black;
    }}

    #summary {{
        height: 4;
    }}

    #chart {{
        background: {ROSE_PINE["bg"]};
        height: 1fr;
    }}

    #no-data {{
        content-align: center middle;
        text-align: center;
        height: 1fr;
        color: $text-muted;
    }}

    #vscroll {{
        height: 1fr;
        overflow-y: auto;
    }}

    #financials {{}}

    #news {{
        height: 16;
    }}

    """

    ## Init //

    def __init__(self):
        super().__init__()

        self.service = MarketDataService()
        self.store = Store()
        self.chart_range = Timeframe.ONE_DAY
        self.last_refresh = time.time()

    ## Compose //

    def compose(self):
        with Horizontal(id = "body"):

            # Left pane stuff
            with Vertical(id = "sidebar"):
                yield WatchList(id = "watchlist")
                yield AssetOverview(id = "asset-overview")

            # Right pane stuff
            with Vertical(id = "main"):
                yield Summary(id="summary")
                with ContentSwitcher(id="content", initial = "chart-pane"):
                    with Container(id = "chart-pane"):
                        yield Chart(id="chart")
                        yield Static(id="no-data")
                    with VerticalScroll(id="vscroll"):
                        yield Financials(id = "financials")
                yield News(id="news")

        yield Footer(id = "footer")
        yield LoadingScreen(id = "loading")        

    ## Lifecycle //

    def on_mount(self) -> None:

        # every 60 seconds, a minute passes on wall street
        ## as such we must refresh
        self.last_refresh = time.time()
        self.set_interval(1, self.update_chart_timer)
        self.set_interval(60, self.refresh_intraday)

        # initial state
        self.chart_range = Timeframe.ONE_DAY
        self.store.set_current_symbol(self.store.get_watchlist()[0])

        # startup stuff
        self.set_loading(True)
        self.load_initial_data()


    def on_symbol_selected(self, event: SymbolSelected) -> None:
        self.store.set_current_symbol(event.symbol)
        if not self.store.has_news_items(event.symbol):
            self.load_symbol_details(event.symbol)

        self.refresh_asset_overview()
        self.refresh_current()


    ## Widget Updates //

    def set_summary_node(self, asset: Asset) :
        summary = self.query_one("#summary", Summary)
        summary.set_asset(asset)

    def set_asset_overview_node(self, asset: Asset | None, metadata: AssetMetadata | None) -> None:
        overview = self.query_one("#asset-overview", AssetOverview)
        overview.set_asset(asset, metadata)

    def set_chart_node(self, chart_data: ChartData | None, range: Timeframe, timezone: str, show_lines: bool = True) :
        chart = self.query_one("#chart", Chart)
        no_data = self.query_one("#no-data", Static)

        # if no data show no-data screen
        if chart_data is None or not chart_data.points or (range == Timeframe.ONE_DAY and len(chart_data.points) == 1):
            chart.display = False
            no_data.display = True
            no_data.update(
                "\n".join([
                    f"{self.store.get_current_symbol()} • {range.value}",
                    "",
                    "No data available for this timeframe.",
                    "",
                    "Try selecting a longer timeframe using g.",
                ])
            )           
            return

        chart.display = True
        no_data.display = False

        chart.set_chart_data(chart_data = chart_data, timeframe = range, timezone = timezone)

    def set_financials_node(self, symbol: str, financial_data: TickerFinancials) :
        financials = self.query_one("#financials", Financials)
        financials.set_data(symbol, financial_data)

    def set_news_node(self, news_items: list[NewsItem]) :
        news = self.query_one("#news", News)
        news.set_news(news_items)

    def set_watchlist_node(self, assets: list[Asset]) :
        watchlist = self.query_one("#watchlist", WatchList)
        watchlist.set_assets(assets)

    ## Refresh Helpers //

    def refresh_watchlist(self) -> None:
        self.set_watchlist_node(self.store.get_assets())

    def refresh_asset_overview(self) -> None:
        self.query_one(AssetOverview).show_loading(
            self.store.get_current_asset()
        )

        self.load_metadata_worker(self.store.get_current_symbol())

    def refresh_current(self) -> None:

        current_asset = self.store.get_current_asset()
        current_chart = self.store.get_current_chart().get_chart_view(self.chart_range)

        self.set_summary_node(current_asset)
        self.set_chart_node(
            chart_data = current_chart,
            range = self.chart_range,
            timezone = current_asset.timezone,
        )
        self.set_financials_node(
            self.store.get_current_symbol(),
            self.store.get_current_financials(),
        )
        self.set_news_node(
            self.store.get_current_news()
        )

    ## Data Loading //

    ## Background Tasks ///

    @work(exclusive = True, group = "refresh")
    async def refresh_intraday(self) -> None:
        for symbol, cache in self.store.charts.items():
            asset = await asyncio.to_thread(self.service.update_asset, symbol, self.store.get_asset(symbol))
            updated_cache = await asyncio.to_thread(self.service.update_intraday_cache, symbol, cache)
            self.store.set_asset(symbol, asset)
            self.store.set_chart(symbol, updated_cache)

        self.last_refresh = time.time()

        self.refresh_watchlist()
        self.refresh_current()

    @work
    async def load_initial_data(self):
        for symbol in self.store.get_watchlist():
            await asyncio.to_thread(self.load_symbol_quick, symbol)

        await asyncio.to_thread(
            self.load_symbol_details,
            self.store.get_current_symbol()
        )

        self.refresh_watchlist()
        self.refresh_current()
        self.refresh_asset_overview()
        self.set_loading(False)

        self.query_one("#watchlist", WatchList).focus()

    ## Data Tasks ///

    @work
    async def load_metadata_worker(self, symbol: str) -> None:
        metadata = await asyncio.to_thread(
            self.load_asset_metadata,
            symbol,
        )

        if self.store.get_current_symbol() != symbol:
            return

        asset = self.store.get_current_asset()
        self.set_asset_overview_node(asset, metadata)

    def load_symbol_quick(self, symbol: str) -> bool:
        try:
            asset = self.service.get_asset(symbol)
            self.store.set_asset(symbol, asset)

            self.store.set_chart(
                symbol,
                ChartCache(
                    intraday=self.service.get_chart(symbol, TimeRange.INTRADAY),
                    hourly=ChartData(symbol, TimeRange.HOURLY, []),
                    daily=ChartData(symbol, TimeRange.DAILY, []),
                    longterm=ChartData(symbol, TimeRange.LONGTERM, []),
                ),
            )

            return True

        except Exception:
            self.notify(f"Could not load `{symbol}`")
            return False

    def load_symbol_details(self, symbol: str) -> bool:
        try:
            cache = self.store.get_chart(symbol)

            cache.hourly = self.service.get_chart(symbol, TimeRange.HOURLY)
            cache.daily = self.service.get_chart(symbol, TimeRange.DAILY)
            cache.longterm = self.service.get_chart(symbol, TimeRange.LONGTERM)

            self.store.set_news(symbol, self.service.get_news(symbol))
            self.store.set_financials(symbol, self.service.get_financials(symbol))

            return True

        except Exception:
            self.notify(f"Could not load details for `{symbol}`")
            return False

    def load_asset_metadata(self, symbol: str) -> AssetMetadata | None:
        cache_metadata = self.store.get_current_asset_metadata()

        if cache_metadata :
            return cache_metadata

        fresh_metadata = self.service.get_asset_metadata(symbol)
        self.store.set_asset_metadata(fresh_metadata)
        return fresh_metadata

    ## Timers ///

    def update_chart_timer(self) -> None:
        age = int(time.time() - self.last_refresh)
        next_refresh = max(0, 60 - age)
        chart = self.query_one("#chart", Chart)
        chart.update_refresh_timer(next_refresh)

    ## Actions //

    def action_add_ticker(self) -> None:
        self.app.push_screen(
            AddTickerModal(),
            self.on_ticker_added
        )

    def on_ticker_added(self, symbol: str | None) -> None:
        if symbol is None or symbol in self.store.get_watchlist():
            return

        if not self.load_symbol_quick(symbol) :
            return

        self.store.add_to_watchlist(symbol)
        self.refresh_watchlist()
        self.refresh_asset_overview()

    def action_remove_ticker(self) -> None:
        symbol = self.store.get_current_symbol()

        if not symbol:
            return

        if len(self.store.get_watchlist()) <= 1 :
            return

        self.store.remove_from_watchlist(symbol)

        self.refresh_watchlist()
        self.refresh_asset_overview()
        self.refresh_current()

    def action_cycle_timeframe(self) -> None:
        timeframes = list(Timeframe)

        current_index = timeframes.index(self.chart_range)
        next_index = (current_index + 1) % len(timeframes)

        self.chart_range = timeframes[next_index]

        current_asset = self.store.get_current_asset()

        chart = self.store.get_current_chart().get_chart_view(self.chart_range)
        if chart is None:
            self.load_symbol_details(self.store.get_current_symbol())
            chart = self.store.get_current_chart().get_chart_view(self.chart_range)

        self.set_chart_node(
                chart_data = chart,
                range = self.chart_range,
                timezone = current_asset.timezone,
            )

    def action_toggle_reference_lines(self) -> None:

        chart = self.query_one("#chart", Chart)
        chart.toggle_reference_lines()

        current_asset = self.store.get_current_asset()

        self.reference_lines = not self.reference_lines
        self.set_chart_node(
                chart_data = self.store.get_current_chart().get_chart_view(self.chart_range),
                range = self.chart_range,
                timezone = current_asset.timezone,
            )

    def action_toggle_view(self) -> None:
        switcher = self.query_one("#content", ContentSwitcher)

        switcher.current = (
            "vscroll"
            if switcher.current == "chart-pane"
            else "chart-pane"
        )

    ## Misc //

    def set_loading(self, loading: bool) -> None:
        self.query_one("#loading", Static).display = loading
        self.query_one("#content", ContentSwitcher).display = not loading
        self.query_one("#footer", Footer).display = not loading



