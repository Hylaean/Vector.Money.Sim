"""Baseline world economy model.

This model approximates late 20th century economic dynamics using the
agent classes defined in this package.  It orchestrates households,
firms, government and a financial intermediary interacting through a
resource market.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..agents import FinancialIntermediary, Firm, Government, Household
from ..biophysics import BioPhysicalStocks
from ..markets import Market


@dataclass
class BaselineModel:
    """Simple baseline model with default end-of-century parameters."""

    households: int = 50
    firms: int = 20
    has_government: bool = True
    has_bank: bool = True
    initial_stocks: Dict[str, float] | None = None
    price_sensitivity: float = 0.5

    stocks: BioPhysicalStocks = field(init=False)
    market: Market = field(init=False)
    agents: List[object] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.stocks = BioPhysicalStocks(**(self.initial_stocks or {}))
        self.market = Market(self.stocks, price_sensitivity=self.price_sensitivity)
        self.agents = []
        for i in range(self.households):
            self.agents.append(Household(i, model=self))
        offset = self.households
        for j in range(self.firms):
            self.agents.append(Firm(offset + j, model=self))
        if self.has_government:
            self.agents.append(Government("gov", model=self))
        if self.has_bank:
            self.agents.append(FinancialIntermediary("bank", model=self))

    def step(self) -> None:
        """Advance the model by one time step."""
        for agent in self.agents:
            agent.step()
        self.stocks.step()
        self.market.adjust_prices()

    def run(self, steps: int) -> List[Dict[str, float]]:
        """Run the simulation for ``steps`` and return recorded series."""
        records: List[Dict[str, float]] = []
        for idx in range(steps):
            self.step()
            records.append(
                {
                    "step": idx,
                    "carbon_budget": self.stocks.carbon_budget.value,
                    "water": self.stocks.water.value,
                    "biomass": self.stocks.biomass.value,
                    "minerals": self.stocks.minerals.value,
                }
            )
        return records
