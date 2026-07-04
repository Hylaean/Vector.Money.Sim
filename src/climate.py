"""Biophysical environments for money-system experiments.

Two environments share one interface:

* :class:`StaticEnvironment` — stationary regeneration, no shocks.  The
  textbook world in which price signals have time to equilibrate.
* :class:`ShiftingEnvironment` — a stylised climate-change trajectory:
  regeneration rates decay over time, and acute shocks (droughts, fires)
  arrive with increasing frequency and severity.  Any institution that
  estimates sustainable yield from past observations is systematically
  wrong in this world — the size of that error is the mechanism the
  experiments probe.

Stocks follow logistic regeneration minus extraction:

    S(t+1) = S(t) + r(t) * S(t) * (1 - S(t) / K) - E(t)

where ``r(t)`` is the (possibly drifting, possibly shocked) regeneration
rate, ``K`` the carrying capacity and ``E(t)`` total extraction chosen by
the economy.  ``boundary`` is the ecological floor: stock below it counts
as overshoot (compatible with :func:`src.metrics.overshoot_depth`).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List


DEFAULT_RESOURCES = ("carbon", "water", "biomass", "minerals")


@dataclass
class ResourceState:
    """One biophysical stock with logistic regeneration."""

    name: str
    stock: float = 70.0
    capacity: float = 100.0
    regen_rate: float = 0.10
    boundary: float = 40.0

    def regenerate(self, rate_multiplier: float = 1.0) -> None:
        rate = self.regen_rate * rate_multiplier
        growth = rate * self.stock * max(0.0, 1.0 - self.stock / self.capacity)
        self.stock = min(self.capacity, self.stock + growth)

    def extract(self, amount: float) -> float:
        """Remove up to ``amount``; return what was actually extracted."""
        taken = min(self.stock, max(0.0, amount))
        self.stock -= taken
        return taken

    @property
    def health(self) -> float:
        """Stock relative to capacity, in [0, 1]."""
        return self.stock / self.capacity if self.capacity > 0 else 0.0

    @property
    def in_overshoot(self) -> bool:
        return self.stock < self.boundary


class Environment:
    """Base environment: stationary dynamics, perfect predictability."""

    def __init__(
        self,
        resources: Dict[str, ResourceState] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self.resources: Dict[str, ResourceState] = resources or {
            name: ResourceState(name=name) for name in DEFAULT_RESOURCES
        }
        self.rng = rng or random.Random(0)
        self.t = 0
        self.history: List[Dict[str, float]] = []

    # -- dynamics -----------------------------------------------------

    def rate_multiplier(self, name: str) -> float:
        """Current regeneration multiplier for a resource (1.0 = nominal)."""
        return 1.0

    def step(self) -> None:
        """Advance one period: record state, then regenerate all stocks."""
        self.history.append({n: r.stock for n, r in self.resources.items()})
        for name, res in self.resources.items():
            res.regenerate(self.rate_multiplier(name))
        self.t += 1

    def extract(self, name: str, amount: float) -> float:
        return self.resources[name].extract(amount)

    # -- what institutions can observe --------------------------------

    def sustainable_yield(self, name: str, observation_lag: int = 3) -> float:
        """Estimated per-period harvest that keeps the stock stable.

        The estimate uses the *lagged* stock level and the *nominal*
        regeneration rate — institutions cannot observe drift or shocks
        in real time.  In a static world the estimate is accurate; in a
        shifting world it is systematically optimistic.
        """
        res = self.resources[name]
        if self.history and observation_lag > 0:
            lagged = self.history[max(0, len(self.history) - observation_lag)]
            stock = lagged.get(name, res.stock)
        else:
            stock = res.stock
        estimate = res.regen_rate * stock * max(0.0, 1.0 - stock / res.capacity)
        # Issue nothing above the boundary buffer: if the (lagged) stock
        # is already below the boundary, the sustainable yield is zero.
        if stock <= res.boundary:
            return 0.0
        return estimate

    def snapshot(self) -> Dict[str, float]:
        return {n: r.stock for n, r in self.resources.items()}


class StaticEnvironment(Environment):
    """Stationary world: constant regeneration, no shocks."""


@dataclass
class ClimateTrajectory:
    """Parameters of the non-stationary (climate change) scenario.

    Drift and shock frequency ramp up and then plateau (``regen_floor``,
    ``shock_prob_max``): climate change shifts the world to a permanently
    harsher regime rather than deterministically killing it.  Without the
    plateau every institution collapses at long horizons and the
    comparison loses discriminating power to a ceiling effect.
    """

    regen_drift: float = 0.004      # fractional regen decline per step
    regen_floor: float = 0.45       # regeneration never falls below this multiplier
    shock_prob_initial: float = 0.02
    shock_prob_growth: float = 0.002  # added to shock probability per step
    shock_prob_max: float = 0.15    # shock probability plateaus here
    shock_severity: float = 0.15    # fraction of stock destroyed by a shock
    shocked_resources: tuple = ("water", "biomass")


class ShiftingEnvironment(Environment):
    """Non-stationary world: drifting regeneration plus acute shocks."""

    def __init__(
        self,
        resources: Dict[str, ResourceState] | None = None,
        rng: random.Random | None = None,
        trajectory: ClimateTrajectory | None = None,
    ) -> None:
        super().__init__(resources=resources, rng=rng)
        self.trajectory = trajectory or ClimateTrajectory()
        self.shocks: List[Dict[str, float]] = []

    def rate_multiplier(self, name: str) -> float:
        return max(
            self.trajectory.regen_floor,
            1.0 - self.trajectory.regen_drift * self.t,
        )

    def step(self) -> None:
        super().step()
        prob = min(
            self.trajectory.shock_prob_max,
            self.trajectory.shock_prob_initial
            + self.trajectory.shock_prob_growth * self.t,
        )
        if self.rng.random() < prob:
            shock: Dict[str, float] = {"t": self.t}
            for name in self.trajectory.shocked_resources:
                res = self.resources[name]
                lost = res.stock * self.trajectory.shock_severity
                res.stock -= lost
                shock[name] = lost
            self.shocks.append(shock)


def make_environment(
    kind: str,
    seed: int = 0,
    resources: Dict[str, ResourceState] | None = None,
    trajectory: ClimateTrajectory | None = None,
) -> Environment:
    """Factory: ``kind`` is ``"static"`` or ``"shifting"``."""
    rng = random.Random(seed)
    if kind == "static":
        return StaticEnvironment(resources=resources, rng=rng)
    if kind == "shifting":
        return ShiftingEnvironment(resources=resources, rng=rng, trajectory=trajectory)
    raise ValueError(f"unknown environment kind: {kind!r}")
