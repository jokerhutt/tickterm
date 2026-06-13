from datetime import datetime

from models.asset import Asset
from models.chart_data import ChartData, ChartPoint, Timeframe
from models.news_item import NewsItem

MOCK_ASSETS = {
    "AAPL": Asset(
        "AAPL",
        "Apple Inc.",
        213.50,
        1.20,
        50_000_000,
        3_000_000_000_000,
    ),
    "MSFT": Asset(
        "MSFT",
        "Microsoft",
        478.10,
        -0.40,
        25_000_000,
        3_500_000_000_000,
    ),
}

MOCK_CHARTS = {
    "AAPL": ChartData(
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
        ],
    ),
    "MSFT": ChartData(
        symbol="MSFT",
        timeframe=Timeframe.ONE_MONTH,
        points=[
            ChartPoint(datetime(2026, 5, 1), 450),
            ChartPoint(datetime(2026, 5, 2), 452),
            ChartPoint(datetime(2026, 5, 3), 448),
            ChartPoint(datetime(2026, 5, 4), 455),
            ChartPoint(datetime(2026, 5, 5), 459),
            ChartPoint(datetime(2026, 5, 6), 462),
            ChartPoint(datetime(2026, 5, 7), 460),
            ChartPoint(datetime(2026, 5, 8), 465),
            ChartPoint(datetime(2026, 5, 9), 468),
            ChartPoint(datetime(2026, 5, 10), 466),
            ChartPoint(datetime(2026, 5, 11), 470),
            ChartPoint(datetime(2026, 5, 12), 472),
            ChartPoint(datetime(2026, 5, 13), 471),
            ChartPoint(datetime(2026, 5, 14), 474),
            ChartPoint(datetime(2026, 5, 15), 476),
            ChartPoint(datetime(2026, 5, 16), 473),
            ChartPoint(datetime(2026, 5, 17), 477),
            ChartPoint(datetime(2026, 5, 18), 480),
            ChartPoint(datetime(2026, 5, 19), 482),
            ChartPoint(datetime(2026, 5, 20), 479),
            ChartPoint(datetime(2026, 5, 21), 483),
            ChartPoint(datetime(2026, 5, 22), 485),
            ChartPoint(datetime(2026, 5, 23), 484),
            ChartPoint(datetime(2026, 5, 24), 487),
            ChartPoint(datetime(2026, 5, 25), 489),
            ChartPoint(datetime(2026, 5, 26), 492),
            ChartPoint(datetime(2026, 5, 27), 490),
            ChartPoint(datetime(2026, 5, 28), 494),
            ChartPoint(datetime(2026, 5, 29), 496),
            ChartPoint(datetime(2026, 5, 30), 498),
        ],
    ),
}

MOCK_NEWS = {
    "AAPL": [
        NewsItem("Apple unveils next-generation Siri", "NYT", "Jun 2"),
        NewsItem("iPhone sales beat expectations", "Bloomberg", "Jun 1"),
    ],
    "MSFT": [
        NewsItem("Microsoft expands AI infrastructure", "Reuters", "Jun 2"),
        NewsItem("Azure growth accelerates", "WSJ", "Jun 1"),
    ],
}
