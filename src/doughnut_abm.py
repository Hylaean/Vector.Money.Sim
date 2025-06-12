from __future__ import annotations

try:  # pragma: no cover - optional numpy
    import numpy as np
except Exception:  # pragma: no cover - provide minimal fallback

    class _NP:
        @staticmethod
        def mean(values):
            return sum(values) / len(values) if values else 0.0

        nan = float("nan")

        @staticmethod
        def array(values):
            return list(values)

    np = _NP()

try:  # pragma: no cover - optional mesa
    from mesa import Model
    from mesa.datacollection import DataCollector
    from mesa.time import SimultaneousActivation
except Exception:  # pragma: no cover - mesa might be missing

    class Model:  # pragma: no cover - simple stand in
        def __init__(self) -> None:
            pass

    class SimultaneousActivation:  # pragma: no cover - simple stand in
        def __init__(self, model: Model) -> None:
            self.agents = []

        def add(self, agent) -> None:
            self.agents.append(agent)

        def step(self) -> None:
            for agent in self.agents:
                if hasattr(agent, "step"):
                    agent.step()

    class DataCollector:  # pragma: no cover - simple stand in
        def __init__(self, model_reporters=None, agent_reporters=None) -> None:
            self.model_reporters = model_reporters or {}
            self.agent_reporters = agent_reporters or {}
            self.data = []

        def collect(self, model) -> None:
            self.data.append({k: f(model) for k, f in self.model_reporters.items()})

        def get_model_vars_dataframe(self):
            import pandas as pd

            if not self.data:
                return pd.DataFrame({})
            keys = self.data[0].keys()
            cols = {k: [d.get(k) for d in self.data] for k in keys}
            return pd.DataFrame(cols)


from .agents import Firm, Household
from .environment import BiophysicalStock


class DoughnutABM(Model):
    """Agent-based model with social floors and ecological ceilings."""

    def __init__(
        self,
        N_households: int = 1000,
        N_firms: int = 50,
        years: int = 100,
        social_floor: list[float] | None = None,
        bio_max: float | None = None,
    ) -> None:
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.years = years
        self.social_floor = np.array(social_floor or [1.0, 1.0, 1.0, 1.0])
        limit = bio_max or 1000.0
        self.bio_stocks = {
            "carbon": BiophysicalStock("carbon", value=limit, max_boundary=limit),
            "water": BiophysicalStock("water", value=10_000.0, max_boundary=10_000.0),
        }
        self.market_price = 1.0
        self.households = []
        for i in range(N_households):
            h = Household(i, self)
            self.schedule.add(h)
            self.households.append(h)
        self.firms = []
        for j in range(N_firms):
            f = Firm(j + N_households, self)
            self.schedule.add(f)
            self.firms.append(f)
        self.datacollector = DataCollector(
            model_reporters={
                "CarbonStock": lambda m: m.bio_stocks["carbon"].value,
                "CarbonOvershoot": lambda m: m.bio_stocks["carbon"].overshoot,
                "AvgNeedSatisfaction": lambda m: m._avg_need_satisfaction(),
            },
            agent_reporters={"Wealth": lambda a: getattr(a, "wealth", float("nan"))},
        )

    def request_resource(self, name: str, amount: float) -> float:
        stock = self.bio_stocks[name]
        utilisation = stock.value / stock.max_boundary
        markup = 1 + 9 * utilisation**3
        self.market_price *= markup
        stock.step(outflow=amount)
        return amount

    def _avg_need_satisfaction(self) -> float:
        sats = [sum(h.needs_vector) / len(h.needs_vector) for h in self.households]
        return sum(sats) / len(sats) if sats else 0.0

    def step(self) -> None:
        self.schedule.step()
        self.datacollector.collect(self)

    def run(self):
        for _ in range(self.years):
            self.step()
        return self.datacollector.get_model_vars_dataframe()
