

from textual.message import Message


class SymbolSelected(Message):

    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__()
