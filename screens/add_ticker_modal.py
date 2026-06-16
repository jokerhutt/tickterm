from textual.screen import ModalScreen
from textual.widgets import Input, Label
from textual.containers import Vertical


# ==
# Modal for adding tickers
# Type in e.g. SPCX it will add SPCX ticker to watchlist
# ==
class AddTickerModal(ModalScreen[str | None]):

    CSS = """
    AddTickerModal {
        align: center middle;
    }

    #modal {
        width: 40;
        height: 10;
        border: round white;
        padding: 1 2;
        background: $surface;
    }
    """

    def compose(self):
        with Vertical(id="modal"):
            yield Label("Add ticker")
            yield Input(placeholder="NVDA", id="ticker_input")

    def on_mount(self):
        self.query_one("#ticker_input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted):
        symbol = event.value.strip().upper()

        if symbol:
            self.dismiss(symbol)

    def key_escape(self):
        self.dismiss(None)
