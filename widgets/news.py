

from textual.widgets import Static


class News(Static):
    def on_mount(self):
        self.update("NEWS")
