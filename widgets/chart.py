from rich.panel import Panel
from textual.widgets import Static
from textual import log
from models.chart_data import ChartData
from themes import ROSE_PINE
from textual_plotext import PlotextPlot


class Chart(PlotextPlot):

    DEFAULT_CSS = f"""
    Chart {{
        background: {ROSE_PINE["bg"]};
        padding: 1 2;
    }}
    """

    def set_chart_data(self, chart_data: ChartData):
        self.plt.clear_data()

        log(chart_data)


        self.theme = "textual-clear"
        
        prices = []
        labels = []

        for point in chart_data.points :
            prices.append(point.price)

            label = point.timestamp.strftime("%b %d")
            labels.append(label)

        self.plt.plot(
            range(len(chart_data.points)),
            prices,
            marker = "braille"
        )

        self.plt.title(f"{chart_data.symbol} • {chart_data.timerange}")

        self.refresh()




