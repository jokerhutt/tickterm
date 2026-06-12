

from textual.widgets import Static


class Chart(Static):

    def on_mount(self):
        self.update("CHART")
