"""The experiment economy: households under a money system in an environment.

This is the purpose-built model for the scalar-vs-vector money experiments.
It is deliberately small and transparent — every mechanism is inspectable —
and it is substrate-agnostic: household decisions come from a
:class:`src.policies.Policy`, which may be a rule, a Q-learner, an LLM, or
a human.  The same game, verbatim, is what human participants play in
``experiments/human/``.

One period:

1. the environment regenerates (and, if shifting, drifts and shocks),
2. the institution reacts with a lag — issuing token allowances (vector)
   or adjusting resource prices (scalar),
3. households earn wages, observe their state, and choose a consumption
   level and whether to invest in efficiency,
4. affordable purchases execute; resources are extracted; need
   satisfaction is recorded.

Outcome metrics reuse :mod:`src.metrics`: welfare (mean need
satisfaction), inequality (Gini of satisfaction and of wealth),
overshoot depth, and return time to the safe operating space.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .climate import Environment, make_environment
from .metrics import inequality_index, overshoot_depth, return_time_to_boundaries
from .money import MoneySystem, Wallet, make_money_system
from .policies import Action, Observation, Policy, RuleBasedPolicy

# Consumption levels 0..3.  Marginal need satisfaction is concave; the
# resource footprint is linear.  Level 1 ≈ subsistence, level 3 ≈ affluence.
SATISFACTION = (0.0, 0.55, 0.85, 1.0)
# Calibrated so that ~20 households at consumption level 2 sit right at the
# sustainable yield of a healthy stock (logistic regen ≈ 2.1–2.5 per period):
# average level 2 is sustainable, average level 3 draws stocks down.
UNIT_FOOTPRINT = {"carbon": 0.06, "water": 0.05, "biomass": 0.04, "minerals": 0.02}
UNIT_CASH_COST = 1.0
EFFICIENCY_COST = 4.0        # cash cost of one efficiency investment
EFFICIENCY_FACTOR = 0.85     # footprint multiplier per investment
EFFICIENCY_FLOOR = 0.4       # footprint multiplier cannot fall below this


@dataclass
class Household:
    """One household: a wallet, a wage, an efficiency level, a policy."""

    uid: int
    wallet: Wallet
    wage: float
    policy: Policy
    efficiency: float = 1.0
    satisfaction_history: List[float] = field(default_factory=list)

    def footprint(self, units: int) -> Dict[str, float]:
        return {dim: qty * units * self.efficiency for dim, qty in UNIT_FOOTPRINT.items()}


@dataclass
class EconomyConfig:
    n_households: int = 20
    steps: int = 100
    seed: int = 0
    money: str | float = "vector"          # "scalar" | "vector" | λ in [0,1]
    environment: str = "shifting"          # "static" | "shifting"
    price_sensitivity: float = 0.15        # scalar-money price adjustment speed
    observation_lag: int = 3               # institution's information lag
    issuance_headroom: float = 1.0         # fraction of sustainable yield issued
    wage_mean: float = 3.0
    wage_spread: float = 0.5               # lognormal sigma for wage heterogeneity
    carryover: float = 0.5                 # vector money token carryover
    convertibility: float = 0.0            # vector money λ


class Economy:
    """The full simulation: environment × money system × N policy-driven agents."""

    def __init__(self, config: EconomyConfig, policies: Optional[List[Policy]] = None):
        self.config = config
        self.rng = random.Random(config.seed)
        self.env: Environment = make_environment(config.environment, seed=config.seed)
        if isinstance(config.money, str) and config.money == "vector":
            self.money: MoneySystem = make_money_system(
                "vector",
                convertibility=config.convertibility,
                carryover=config.carryover,
            )
        else:
            self.money = make_money_system(config.money)
        self.households: List[Household] = []
        for i in range(config.n_households):
            wage = config.wage_mean * self.rng.lognormvariate(0.0, config.wage_spread)
            policy = policies[i] if policies else RuleBasedPolicy()
            self.households.append(
                Household(uid=i, wallet=Wallet(cash=5.0), wage=wage, policy=policy)
            )
        self.t = 0
        self.records: List[Dict[str, float]] = []

    # -- observation given to policies (and shown verbatim to humans) ----

    def observe(self, hh: Household) -> Observation:
        return Observation(
            t=self.t,
            cash=round(hh.wallet.cash, 3),
            tokens={d: round(v, 3) for d, v in hh.wallet.tokens.items()},
            prices={d: round(p, 3) for d, p in self.money.token_prices.items()},
            stock_health={n: round(r.health, 3) for n, r in self.env.resources.items()},
            last_satisfaction=hh.satisfaction_history[-1] if hh.satisfaction_history else None,
            money_system=self.money.name,
            efficiency=round(hh.efficiency, 3),
            unit_cost=self._unit_costs(hh),
        )

    def _unit_costs(self, hh: Household) -> Dict[str, float]:
        """Cash price of each consumption level under the current system."""
        costs = {}
        for units in range(4):
            purchase = self.money.price(UNIT_CASH_COST * units, hh.footprint(units))
            costs[str(units)] = round(purchase.cash_cost, 3)
        return costs

    # -- one period -------------------------------------------------------

    def step(self) -> None:
        cfg = self.config
        self.env.step()

        # Institutional reaction, always on lagged information.
        lagged_health = self._lagged_health(cfg.observation_lag)
        self.money.update_prices(lagged_health, cfg.price_sensitivity)
        allocation = {
            name: cfg.issuance_headroom
            * self.env.sustainable_yield(name, cfg.observation_lag)
            for name in self.env.resources
        }
        self.money.issue([hh.wallet for hh in self.households], allocation)

        satisfactions = []
        for hh in self.households:
            hh.wallet.cash += hh.wage
            obs = self.observe(hh)
            action = hh.policy.decide(obs)
            self._apply(hh, action)
            satisfaction = hh.satisfaction_history[-1]
            satisfactions.append(satisfaction)
            hh.policy.observe_result(satisfaction, self.observe(hh))

        self.records.append(
            {
                "t": self.t,
                "welfare": sum(satisfactions) / len(satisfactions),
                "gini_satisfaction": inequality_index(satisfactions),
                "gini_wealth": inequality_index(
                    [hh.wallet.cash for hh in self.households]
                ),
                **{f"stock_{n}": r.stock for n, r in self.env.resources.items()},
                **{f"price_{d}": p for d, p in self.money.token_prices.items()},
            }
        )
        self.t += 1

    def _apply(self, hh: Household, action: Action) -> None:
        units = max(0, min(3, action.consumption))
        purchase = self.money.price(UNIT_CASH_COST * units, hh.footprint(units))
        # Walk consumption down until affordable (a hard budget constraint,
        # identical across substrates so policies differ only in intent).
        while units > 0 and not self.money.can_afford(hh.wallet, purchase):
            units -= 1
            purchase = self.money.price(UNIT_CASH_COST * units, hh.footprint(units))
        availability = 1.0
        if units > 0:
            self.money.execute(hh.wallet, purchase)
            for dim, qty in hh.footprint(units).items():
                got = self.env.extract(dim, qty)
                if qty > 0:
                    availability = min(availability, got / qty)
        # A purchase from depleted stocks cannot satisfy needs: physical
        # scarcity bites regardless of what the monetary system permits.
        hh.satisfaction_history.append(SATISFACTION[units] * availability)

        if action.invest and hh.wallet.cash >= EFFICIENCY_COST:
            hh.wallet.cash -= EFFICIENCY_COST
            hh.efficiency = max(EFFICIENCY_FLOOR, hh.efficiency * EFFICIENCY_FACTOR)

    def _lagged_health(self, lag: int) -> Dict[str, float]:
        if self.env.history and lag > 0:
            snapshot = self.env.history[max(0, len(self.env.history) - lag)]
            return {
                n: snapshot[n] / r.capacity if r.capacity else 0.0
                for n, r in self.env.resources.items()
            }
        return {n: r.health for n, r in self.env.resources.items()}

    # -- full run and outcome metrics --------------------------------------

    def run(self) -> Dict[str, object]:
        for _ in range(self.config.steps):
            self.step()
        return self.results()

    def results(self) -> Dict[str, object]:
        overshoots = {}
        return_times = {}
        for name, res in self.env.resources.items():
            series = [rec[f"stock_{name}"] for rec in self.records]
            overshoots[name] = overshoot_depth(series, res.boundary)
            return_times[name] = return_time_to_boundaries(
                series, res.boundary, res.capacity
            )
        welfare_series = [rec["welfare"] for rec in self.records]
        return {
            "config": {
                "money": str(self.config.money),
                "environment": self.config.environment,
                "seed": self.config.seed,
                "n_households": self.config.n_households,
                "steps": self.config.steps,
            },
            "welfare_mean": sum(welfare_series) / len(welfare_series),
            "welfare_final": welfare_series[-1],
            "gini_satisfaction_mean": sum(
                rec["gini_satisfaction"] for rec in self.records
            )
            / len(self.records),
            "gini_wealth_final": self.records[-1]["gini_wealth"],
            "overshoot_depth": overshoots,
            "overshoot_total": sum(overshoots.values()),
            "return_time": return_times,
            "records": self.records,
        }
