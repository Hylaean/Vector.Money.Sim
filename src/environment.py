from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BiophysicalStock:
    """Simple stock with an ecological boundary."""

    name: str
    value: float
    max_boundary: float

    def step(self, inflow: float = 0.0, outflow: float = 0.0) -> None:
        """Update ``value`` based on flows."""
        self.value += inflow - outflow

    @property
    def overshoot(self) -> float:
        """Return amount above ``max_boundary`` if any."""
        return max(0.0, self.value - self.max_boundary)
