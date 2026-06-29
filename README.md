
## Ticker Term

A terminal app for tracking a stock watchlist at a glance. Select any ticker to view its
price chart, recent news, and financials, with prices auto-refreshing throughout the
trading day. Built with Textual using data from yfinance.

## Requirements
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Running the project
```bash
git clone https://github.com/jokerhutt/tickterm.git
cd tickterm
uv sync
uv run python main.py
```

## Keybindings

| Key | Action |
|------|--------|
| ↑ / ↓ | Select ticker |
| Enter | Open ticker |
| g | Cycle chart time period|
| v | Toggle Chart / Financials|
| a | Add ticker |
| d | Remove ticker |
| ctrl+q | Quit |
