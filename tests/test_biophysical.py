import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

sys.modules.setdefault("mesa", types.ModuleType("mesa")).Agent = object

from src.biophysics.stocks import BioPhysicalStocks, StockModel


def test_stockmodel_step_and_apply():
    model = StockModel(initial=0.0, flow=lambda: 2.0)
    model.step()
    assert model.value == 2.0
    model.apply(-1.0)
    assert model.value == 1.0


def test_biophysicalstocks_step():
    stocks = BioPhysicalStocks()
    stocks.carbon_budget.set_flow(lambda: 1.0)
    stocks.water.set_flow(lambda: 2.0)
    stocks.biomass.set_flow(lambda: 3.0)
    stocks.minerals.set_flow(lambda: 4.0)
    stocks.step()
    assert stocks.carbon_budget.value == 1.0
    assert stocks.water.value == 2.0
    assert stocks.biomass.value == 3.0
    assert stocks.minerals.value == 4.0
