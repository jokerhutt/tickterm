# ∴ Jokerhut / main.py


from textual.app import App, ComposeResult

from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Header, Footer, Input, Static

from db.database import init_db
from screens.dashboard import DashboardScreen
class TickTerm(App[None]):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())

if __name__ == "__main__":

    init_db()
    TickTerm().run()
