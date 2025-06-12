import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

mesa_mod = sys.modules.setdefault("mesa", types.ModuleType("mesa"))


class DummyAgent:
    def __init__(self, unique_id=None, model=None):
        self.unique_id = unique_id
        self.model = model


import importlib

import src.agents as ag
import src.agents.firm as fm
import src.agents.household as hh


def _reload_agents() -> None:
    setattr(mesa_mod, "Agent", DummyAgent)
    importlib.reload(hh)
    importlib.reload(fm)
    importlib.reload(ag)
    importlib.reload(sys.modules.get("src.doughnut_abm"))


from src.doughnut_abm import BiophysicalStock, DoughnutABM


def test_biophysical_stock_overshoot():
    _reload_agents()
    stock = BiophysicalStock("c", value=110, max_boundary=100)
    assert stock.overshoot == 10
    stock.step(outflow=20)
    assert stock.value == 90
    assert stock.overshoot == 0


def test_doughnut_abm_run():
    _reload_agents()
    model = DoughnutABM(N_households=1, N_firms=0, years=2, bio_max=100)
    df = model.run()
    assert df.shape[0] == 2
    assert "CarbonStock" in df.columns
