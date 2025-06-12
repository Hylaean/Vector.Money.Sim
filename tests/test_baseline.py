import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

class _Agent:
    def __init__(self, unique_id=None, model=None):
        self.unique_id = unique_id
        self.model = model

mesa_mod = sys.modules.setdefault("mesa", types.ModuleType("mesa"))
mesa_mod.Agent = _Agent

# Reload agent modules to apply the custom Agent base
import importlib
import src.agents as agents_pkg
import src.agents.financial_intermediary as fi
import src.agents.firm as firm
import src.agents.government as government
import src.agents.household as household

for mod in (household, firm, government, fi):
    importlib.reload(mod)
importlib.reload(agents_pkg)
import src.models.baseline as baseline
importlib.reload(baseline)
from src.models.baseline import BaselineModel


def test_baseline_model_runs():
    model = BaselineModel(households=2, firms=1)
    records = model.run(steps=3)
    assert len(records) == 3
    for rec in records:
        assert set(rec.keys()) == {
            "step",
            "carbon_budget",
            "water",
            "biomass",
            "minerals",
        }
