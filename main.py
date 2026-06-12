from textual.app import App

from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Header, Footer, Input, Static
class TickTerm(App):
    def compose(self):
        yield Header()
        yield Static("TICKER BAR")

        with Horizontal():

            # Left pane stuff
            with Vertical():
                yield DataTable()

            # Right pane stuff
            with Vertical():
                yield Static("SUMMARY")
                yield Static("CHART")
                yield Static("NEWS")

        yield Input(placeholder="Command...")
        yield Footer()

if __name__ == "__main__":

    TickTerm().run()
