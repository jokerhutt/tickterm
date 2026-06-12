from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Static

from themes import ROSE_PINE
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
        height: 3;
    }}

    #body {{
        height: 1fr;
    }}

    #sidebar {{
        background: {ROSE_PINE["surface"]};
        width: 30;
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
        height: 6;
    }}

    #chart {{
        height: 1fr;
    }}

    #news {{
        height: 8;
    }}

    #command {{
        height: 3;
    }}

    """

    def compose(self):
        yield Static("TICKER BAR", id="ticker")

        with Horizontal(id = "body"):

            # Left pane stuff
            with Vertical(id = "sidebar"):
                yield WatchList(id = "watchlist")

            # Right pane stuff
            with Vertical(id = "main"):
                yield Static("SUMMARY", id="summary")
                yield Static("CHART", id="chart")
                yield Static("NEWS", id="news")

        yield Input(placeholder="Command...", id="command")

        
