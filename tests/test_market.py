import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

sys.modules.setdefault("mesa", types.ModuleType("mesa")).Agent = object

from src.biophysics.stocks import BioPhysicalStocks
from src.markets.market import Market


class DummyAgent:
    def __init__(self, wealth: float = 0.0):
        self.wealth = wealth


def test_price_adjustment_on_low_stock():
    stocks = BioPhysicalStocks(carbon_budget=80)
    market = Market(
        stocks,
        base_prices={"carbon_budget": 10.0},
        ecological_limits={"carbon_budget": 100.0},
        price_sensitivity=0.5,
    )

    market.adjust_prices()
    assert market.prices["carbon_budget"] > 10.0

    agent = DummyAgent(wealth=100.0)
    market.buy(agent, "carbon_budget", 10)
    assert agent.wealth < 100.0
    assert market.prices["carbon_budget"] > 10.0
