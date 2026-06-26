# ∴ Jokerhut / screens/loading_screen.py


from textual.screen import Screen
from textual.containers import Center, Middle
from textual.widgets import Static, LoadingIndicator

from themes import ROSE_PINE

class LoadingScreen(Static):

    DEFAULT_CSS = f"""
    LoadingScreen {{
        layer: overlay;
        width: 100%;
        height: 100%;
        display: none;
        align: center middle;
        content-align: center middle;
        text-align: center;
        background: {ROSE_PINE["surface"]};
    }}
    """
    def on_mount(self):
        self.frame = 0
        self.set_interval(0.4, self.update_loading)

    def update_loading(self):
        self.frame = (self.frame + 1) % 4
        dots = "." * self.frame
        dots = dots.ljust(3)
        self.update(f"TickTerm\nby JokerHut\n\nFetching Yahoo Finance data{dots}")
