"""Decision substrates for economy agents.

Every household in :mod:`src.economy` delegates its per-period decision to
a :class:`Policy`.  Four substrates implement the same interface, so the
identical game can be played by:

* :class:`RuleBasedPolicy` — transparent heuristics (the baseline),
* :class:`QLearningPolicy` — tabular RL via :class:`src.behavior.archetypes.RLArchetype`,
* :class:`LLMPolicy` — a Claude model choosing actions via structured output,
* :class:`HumanPolicy` — a person at a terminal (the web experiment in
  ``experiments/human/`` reimplements the same observation → action loop).

The action space is deliberately small — a consumption level 0–3 and an
invest flag — so that all four substrates (including humans under time
constraints) face the same tractable choice.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Optional

from .behavior.archetypes import RLArchetype


@dataclass
class Observation:
    """What one household can see before deciding.  JSON-serialisable."""

    t: int
    cash: float
    tokens: Dict[str, float]
    prices: Dict[str, float]
    stock_health: Dict[str, float]
    last_satisfaction: Optional[float]
    money_system: str
    efficiency: float
    unit_cost: Dict[str, float]

    def to_dict(self) -> Dict[str, object]:
        return {
            "period": self.t,
            "your_cash": self.cash,
            "your_resource_tokens": self.tokens,
            "resource_prices": self.prices,
            "ecosystem_health_0_to_1": self.stock_health,
            "your_last_need_satisfaction": self.last_satisfaction,
            "money_system": self.money_system,
            "your_efficiency_multiplier": self.efficiency,
            "cash_cost_by_consumption_level": self.unit_cost,
        }


@dataclass
class Action:
    consumption: int = 1  # 0..3 units
    invest: bool = False


class Policy:
    """Interface: decide on an action, optionally learn from the outcome."""

    def decide(self, obs: Observation) -> Action:
        raise NotImplementedError

    def observe_result(self, reward: float, next_obs: Observation) -> None:
        """Optional learning hook; default is stateless."""


class RuleBasedPolicy(Policy):
    """Satisficing heuristic: consume comfortably, retrench under scarcity.

    Aims for consumption level 2, drops to 1 when the ecosystem is
    visibly degraded or its own budget is tight, and rises to 3 when
    both wallet and ecosystem look healthy.  Invests in efficiency when
    cash-rich and the environment is degrading.
    """

    def __init__(self, greed: float = 0.0) -> None:
        # greed shifts thresholds: 1.0 → consume max whenever affordable.
        self.greed = greed

    def decide(self, obs: Observation) -> Action:
        min_health = min(obs.stock_health.values()) if obs.stock_health else 1.0
        affordable = [
            int(level)
            for level, cost in obs.unit_cost.items()
            if cost <= obs.cash
        ]
        ceiling = max(affordable) if affordable else 0
        if self.greed >= 1.0:
            target = 3
        elif min_health < 0.35:
            target = 1
        elif min_health < 0.6:
            target = 2
        else:
            target = 3 if obs.cash > 3 * obs.unit_cost.get("1", 1.0) else 2
        invest = obs.cash > 8.0 and min_health < 0.6
        return Action(consumption=min(target, ceiling), invest=invest)


class QLearningPolicy(Policy):
    """Tabular Q-learning over a coarse discretisation of the observation."""

    ACTIONS = [(c, inv) for c in range(4) for inv in (False, True)]

    def __init__(self, learning_rate: float = 0.1, epsilon: float = 0.1) -> None:
        self.archetype = RLArchetype(
            actions=list(range(len(self.ACTIONS))),
            learning_rate=learning_rate,
            epsilon=epsilon,
        )
        self._last: Optional[tuple] = None  # (state, action_index)

    @staticmethod
    def _bucket(value: float, cuts: tuple) -> int:
        for i, cut in enumerate(cuts):
            if value < cut:
                return i
        return len(cuts)

    def _state(self, obs: Observation) -> tuple:
        min_health = min(obs.stock_health.values()) if obs.stock_health else 1.0
        token_total = sum(obs.tokens.values())
        return (
            self._bucket(obs.cash, (2.0, 6.0, 12.0)),
            self._bucket(min_health, (0.35, 0.6, 0.8)),
            self._bucket(token_total, (1.0, 4.0)),
        )

    def decide(self, obs: Observation) -> Action:
        state = self._state(obs)
        idx = self.archetype.choose_action(state)
        self._last = (state, idx)
        consumption, invest = self.ACTIONS[idx]
        return Action(consumption=consumption, invest=invest)

    def observe_result(self, reward: float, next_obs: Observation) -> None:
        if self._last is None:
            return
        state, idx = self._last
        # Penalise rewards earned while the ecosystem is in visible decline,
        # so the learner faces the same welfare/overshoot tension as others.
        min_health = min(next_obs.stock_health.values()) if next_obs.stock_health else 1.0
        shaped = reward - max(0.0, 0.5 - min_health)
        self.archetype.update(state, idx, shaped, self._state(next_obs))


LLM_SYSTEM_PROMPT = """\
You are one household among many in a simulated economy that runs for many periods.

Each period you receive an observation (JSON) and choose:
- "consumption": an integer 0-3 — units of goods to buy this period.
  Need satisfaction: 0 units → 0.0, 1 → 0.55, 2 → 0.85, 3 → 1.0.
- "invest": true/false — pay 4.0 cash to permanently cut your resource
  footprint by 15% (compounds; floor at 40%).

Rules of the world:
- Buying goods consumes real resources (carbon, water, biomass, minerals)
  from shared ecological stocks. If stocks fall below their safe boundary,
  the ecosystem degrades and future consumption becomes harder for everyone.
- Under the "scalar" money system you pay cash only; resource scarcity
  shows up as rising prices.
- Under the "vector" money system you also need resource tokens matching
  your purchase's footprint. Tokens arrive each period as your share of
  the sustainable yield; unspent tokens partially carry over.
- Your goal: maximise your household's long-run need satisfaction. The
  run is long; short-run greed that collapses the stocks will hurt you.

Respond with your decision for this period."""

LLM_ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "consumption": {"type": "integer", "enum": [0, 1, 2, 3]},
        "invest": {"type": "boolean"},
        "why": {"type": "string", "description": "One short sentence."},
    },
    "required": ["consumption", "invest", "why"],
    "additionalProperties": False,
}


class LLMPolicy(Policy):
    """A Claude model as the decision substrate.

    Uses structured output to force a valid action.  Defaults to
    ``claude-haiku-4-5`` because a matrix run makes hundreds of calls
    per agent (cost-conscious choice; any Claude model id works).  The
    static system prompt carries a cache_control breakpoint so repeated
    calls hit the prompt cache.

    Falls back to :class:`RuleBasedPolicy` behaviour in *mock mode* —
    when ``mock=True``, the ``anthropic`` package is missing, or no API
    credentials are configured — so tests and CI never need the network.
    """

    def __init__(
        self,
        model: str = "claude-haiku-4-5",
        mock: Optional[bool] = None,
        client=None,
        max_retries: int = 2,
    ) -> None:
        self.model = model
        self.transcript: list = []
        self._fallback = RuleBasedPolicy()
        self._client = client
        if mock is None:
            mock = os.environ.get("VECTOR_MONEY_LLM_MOCK", "") == "1"
        self.mock = mock
        if not self.mock and self._client is None:
            try:
                import anthropic

                self._client = anthropic.Anthropic(max_retries=max_retries)
            except Exception:
                self.mock = True

    def decide(self, obs: Observation) -> Action:
        if self.mock:
            action = self._fallback.decide(obs)
            self.transcript.append({"obs": obs.to_dict(), "mock": True})
            return action
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=300,
                system=[
                    {
                        "type": "text",
                        "text": LLM_SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": json.dumps(obs.to_dict(), sort_keys=True),
                    }
                ],
                output_config={
                    "format": {"type": "json_schema", "schema": LLM_ACTION_SCHEMA}
                },
            )
            text = next(b.text for b in response.content if b.type == "text")
            data = json.loads(text)
            self.transcript.append({"obs": obs.to_dict(), "action": data})
            return Action(
                consumption=int(data["consumption"]), invest=bool(data["invest"])
            )
        except Exception as exc:  # network/refusal/schema errors → safe fallback
            self.transcript.append({"obs": obs.to_dict(), "error": repr(exc)})
            return self._fallback.decide(obs)


class HumanPolicy(Policy):
    """A person at a terminal.  The web experiment replicates this loop."""

    def decide(self, obs: Observation) -> Action:
        print(json.dumps(obs.to_dict(), indent=2))
        while True:
            raw = input("consumption 0-3 [+i to invest], e.g. '2' or '2i': ").strip()
            invest = raw.endswith("i")
            digits = raw.rstrip("i")
            if digits in {"0", "1", "2", "3"}:
                return Action(consumption=int(digits), invest=invest)
            print("please answer 0, 1, 2 or 3, optionally followed by 'i'")


def make_policy(kind: str, **kwargs) -> Policy:
    """Factory: ``rule`` | ``greedy`` | ``rl`` | ``llm`` | ``human``."""
    if kind == "rule":
        return RuleBasedPolicy(**kwargs)
    if kind == "greedy":
        return RuleBasedPolicy(greed=1.0)
    if kind == "rl":
        return QLearningPolicy(**kwargs)
    if kind == "llm":
        return LLMPolicy(**kwargs)
    if kind == "human":
        return HumanPolicy()
    raise ValueError(f"unknown policy kind: {kind!r}")
