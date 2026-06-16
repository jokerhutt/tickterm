from rich.panel import Panel
from textual.widgets import Static
from textual import log
from models.chart_data import ChartData, TimeRange, Timeframe
from themes import ROSE_PINE
from textual_plotext import PlotextPlot


class Chart(PlotextPlot):

    DEFAULT_CSS = f"""
    Chart {{
        background: {ROSE_PINE["bg"]};
        padding: 1 2;

        border: round {ROSE_PINE["accent"]};

        border-title-align: left;
        border-subtitle-align: right;
    }}
    """

    def set_chart_data(self, chart_data: ChartData,  timeframe: Timeframe):
        self.plt.clear_data()

        log(chart_data)


        self.theme = "textual-clear"
        
        prices = []
        labels = []

        fmt = self.get_time_range(timeframe)

        for point in chart_data.points :
            prices.append(point.price)

            label = point.timestamp.strftime(fmt)
            labels.append(label)

        # funny braille lines
        self.plt.plot(
            range(len(chart_data.points)),
            prices,
            marker = "braille"
        )


        # x axis
        step = max(1, len(labels) // 6)
        positions = list(range(0, len(labels), step))
        tick_labels = labels[::step]
        self.plt.xticks(positions, tick_labels)

        # title
        self.plt.title(f"{chart_data.symbol} • {chart_data.timerange} • {timeframe}")

        # reference lines (open, low, high, curr)
        day_open = prices[0]
        current_price = prices[-1]
        day_high = max(prices)
        day_low = min(prices)

        self.plt.plot(
            range(len(prices)),
            prices,
            marker="braille"
        )

        self.plt.hline(day_open, color="yellow")
        self.plt.hline(current_price, color="white")
        self.plt.hline(day_high, color="green")
        self.plt.hline(day_low, color="red")

        self.refresh()

    def update_refresh_timer(self, seconds: int) -> None:
        self.border_subtitle = f" next refresh {seconds:02d}s "
        self.refresh()

    def get_time_range(self, timeframe: Timeframe) -> str:
        match timeframe:
            case Timeframe.ONE_HOUR:
                fmt = "%H:%M"

            case Timeframe.ONE_DAY:
                fmt = "%H:%M"

            case Timeframe.ONE_WEEK:
                fmt = "%a"

            case Timeframe.ONE_MONTH:
                fmt = "%d %b"

            case Timeframe.ONE_YEAR:
                fmt = "%b"

            case Timeframe.FIVE_YEARS:
                fmt = "%Y"

            case Timeframe.MAX:
                fmt = "%Y"

        return fmt




