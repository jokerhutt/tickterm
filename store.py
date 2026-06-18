# ∴ Jokerhut / store.py


from db.watchlist_repository import WatchlistRepository
from models.asset import Asset
from models.chart_data import ChartCache, ChartData, Timeframe
from models.financials import TickerFinancials
from models.news_item import NewsItem


class Store :

    def __init__(self):
        self.repo = WatchlistRepository()

        self.watchlist = self.repo.get_all()

        # some defaults if watchlist empty
        if not self.watchlist:
            self.watchlist = ["AAPL", "MSFT", "NVDA"]
            for symbol in self.watchlist:
                self.repo.add(symbol)

        self.assets = {}
        self.financials = {}
        self.charts = {}
        self.news_items = {}
        self.current_symbol = self.watchlist[0]

    # CURRENT SYMBOL
    def set_current_symbol(self, symbol: str) :
        self.current_symbol = symbol

    def get_current_symbol(self) -> str :
        return self.current_symbol

    # WATCHLIST
    def get_watchlist(self) -> list[str] :
        return self.watchlist

    def add_to_watchlist(self, symbol: str):
        self.repo.add(symbol)
        self.watchlist.append(symbol)

    def remove_from_watchlist(self, symbol: str):
        self.watchlist.remove(symbol)
        self.repo.remove(symbol)

    # NEWS
    def get_news(self, symbol: str) -> list[NewsItem] :
        return self.news_items[symbol]

    def set_news(self, symbol: str, news_items: list[NewsItem]) :
        self.news_items[symbol] = news_items

    def get_current_news(self) -> list[NewsItem] :
        return self.news_items[self.current_symbol]

    # FINANCIALS
    def get_current_financials(self) -> TickerFinancials :
        return self.financials[self.current_symbol]

    def get_financials(self, symbol: str) -> TickerFinancials :
        return self.financials[symbol]

    def set_financials(self, symbol: str, financial_data: TickerFinancials) :
        self.financials[symbol] = financial_data

    # ASSETS
    def get_asset(self, symbol: str) -> Asset | None :
        return self.assets[symbol]

    def get_assets(self) -> list[Asset] | None :
        return self.assets.values()

    def get_current_asset(self) -> Asset | None :
        return self.assets[self.current_symbol]

    def set_asset(self, symbol: str, asset: Asset) :
        self.assets[symbol] = asset

    # CHARTS
    def get_current_chart(self) -> ChartCache | None :
        return self.charts[self.current_symbol]

    def get_charts(self) -> dict[str, ChartCache] :
        return self.charts

    def get_chart(self, symbol: str) -> ChartCache | None :
        return self.charts[symbol]

    def set_chart(self, symbol: str, chart_cache: ChartCache) :
        self.charts[symbol] = chart_cache


