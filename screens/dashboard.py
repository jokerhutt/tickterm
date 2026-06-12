from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Static

class DashboardScreen(Screen[None]):

    CSS = """
    #ticker {
        height: 3;
    }

    #body {
        height: 1fr;
    }

    #sidebar {
        width: 30;
    }

    #main {
        width: 1fr;
    }

    #watchlist {
        height: 1fr;
    }

    #summary {
        height: 6;
    }

    #chart {
        height: 1fr;
    }

    #news {
        height: 8;
    }

    #command {
        height: 3;
    }

    """

    def compose(self):
        yield Static("TICKER BAR", id="ticker")

        with Horizontal(id = "body"):

            # Left pane stuff
            with Vertical(id = "sidebar"):
                yield DataTable(id = "watchlist")

            # Right pane stuff
            with Vertical(id = "main"):
                yield Static("SUMMARY", id="summary")
                yield Static("CHART", id="chart")
                yield Static("NEWS", id="news")

        yield Input(placeholder="Command...", id="command")

        
