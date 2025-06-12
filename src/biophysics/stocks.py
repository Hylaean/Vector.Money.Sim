"""Simple bio-physical stock models.

This module defines a very small wrapper around :mod:`pysd` style stock
behaviour.  The real :mod:`pysd` package is optional at runtime so that the
simulation can run even when the dependency is not available.  If
:mod:`pysd` is installed we make use of its :class:`Integ` integrator.  In
other environments we fall back to a minimal replacement that replicates the
same interface needed for this project.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

try:  # pragma: no cover - optional import
    from pysd.py_backend.functions import Integ  # type: ignore
except Exception:  # pragma: no cover - pysd may not be installed
    class Integ:  # pragma: no cover - simple stand in
        """Minimal replacement for ``pysd``'s ``Integ`` class."""

        def __init__(self, func: Callable[[], float], initial: float = 0.0):
            self.func = func
            self.state = initial

        def step(self, dt: float = 1.0) -> float:
            self.state += self.func() * dt
            return self.state

@dataclass
class StockModel:
    """Wrapper around a stock/integrator."""

    initial: float = 0.0
    flow: Callable[[], float] = lambda: 0.0
    integ: Integ = field(init=False)

    def __post_init__(self) -> None:
        self.integ = Integ(self.flow, self.initial)

    @property
    def value(self) -> float:
        return getattr(self.integ, "state", 0.0)

    def step(self, dt: float = 1.0) -> None:
        self.integ.step(dt)

    def set_flow(self, flow: Callable[[], float]) -> None:
        self.flow = flow
        self.integ.func = flow

    def apply(self, change: float) -> None:
        """Directly modify the stock level by ``change``."""
        self.integ.state += change


class BioPhysicalStocks:
    """Collection of bio-physical stocks used by the model."""

    def __init__(self,
                 carbon_budget: float = 0.0,
                 water: float = 0.0,
                 biomass: float = 0.0,
                 minerals: float = 0.0) -> None:
        self.carbon_budget = StockModel(carbon_budget)
        self.water = StockModel(water)
        self.biomass = StockModel(biomass)
        self.minerals = StockModel(minerals)

    def step(self) -> None:
        """Advance all stocks one tick."""
        self.carbon_budget.step()
        self.water.step()
        self.biomass.step()
        self.minerals.step()
