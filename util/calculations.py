# ∴ Jokerhut / util/calculations.py


import math
from typing import Any


def calc_change_pct(curr: float, prev: float) -> float :
    return ((curr - prev) / prev) * 100


def finite(value: Any):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    return number if math.isfinite(number) else None
