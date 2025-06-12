"""Market module for resource trading."""

from __future__ import annotations

from typing import Dict

from ..biophysics import BioPhysicalStocks


class Market:
    """Simple resource market with price adjustments."""

    def __init__(
        self,
        stocks: BioPhysicalStocks,
        base_prices: Dict[str, float] | None = None,
        ecological_limits: Dict[str, float] | None = None,
        price_sensitivity: float = 0.5,
    ) -> None:
        self.stocks = stocks
        self.prices: Dict[str, float] = base_prices or {
            "carbon_budget": 1.0,
            "water": 1.0,
            "biomass": 1.0,
            "minerals": 1.0,
        }
        self.ecological_limits: Dict[str, float] = ecological_limits or {
            "carbon_budget": 1.0,
            "water": 1.0,
            "biomass": 1.0,
            "minerals": 1.0,
        }
        self.price_sensitivity = price_sensitivity

    def adjust_prices(self) -> None:
        """Update prices based on current stock levels."""
        for resource, limit in self.ecological_limits.items():
            stock = getattr(self.stocks, resource).value
            if limit <= 0:
                continue
            ratio = max(0.0, 1.0 - stock / limit)
            self.prices[resource] *= 1 + self.price_sensitivity * ratio

    def buy(self, agent, resource: str, quantity: float) -> None:
        """Buy ``quantity`` of ``resource`` from the market."""
        price = self.prices.get(resource, 0.0)
        cost = price * quantity
        if hasattr(agent, "wealth"):
            agent.wealth -= cost
        getattr(self.stocks, resource).apply(-quantity)
        self.adjust_prices()

    def sell(self, agent, resource: str, quantity: float) -> None:
        """Sell ``quantity`` of ``resource`` to the market."""
        price = self.prices.get(resource, 0.0)
        revenue = price * quantity
        if hasattr(agent, "wealth"):
            agent.wealth += revenue
        getattr(self.stocks, resource).apply(quantity)
        self.adjust_prices()
