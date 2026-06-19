# ∴ Jokerhut / util/formatters.py

def format_number(value: float | int | None, currency: str) -> str:
    if value is None:
        return "N/A"

    value = float(value)

    if abs(value) >= 1_000_000_000_000:
        return f"{currency} {value / 1_000_000_000_000:.2f}T"

    if abs(value) >= 1_000_000_000:
        return f"{currency} {value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"{currency} {value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{currency} {value / 1_000:.2f}K"

    return f"{currency} {value:,.0f}"

def format_percentage_points(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.2f}%"

def format_ratio(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.2f}"

def format_money(value: float | None, currency: str) -> str:
    if value is None:
        return "N/A"
    return f"{currency} {value:,.2f}"

def format_percent(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"

