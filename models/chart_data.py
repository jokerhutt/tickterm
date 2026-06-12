
from dataclasses import dataclass


@dataclass
class ChartData:
    prices: list[float]
    timestamps: list[str]
