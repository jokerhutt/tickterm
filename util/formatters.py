
def format_number(value: float | int | None) -> str:
    if value is None:
        return "N/A"

    value = float(value)

    if abs(value) >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"${value / 1_000:.2f}K"

    return f"${value:,.0f}"

def format_ratio(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.2f}"

def format_percent(value: float | None) -> str:
    if value is None:
        return "N/A"
