"""Unit tests for src.policies: decision substrates."""

from __future__ import annotations

import os

import pytest

from src.policies import (
    Action,
    HumanPolicy,
    LLMPolicy,
    Observation,
    QLearningPolicy,
    RuleBasedPolicy,
    make_policy,
)


def _obs(cash: float, min_health: float, greed_costs=None, **overrides) -> Observation:
    unit_cost = greed_costs if greed_costs is not None else {"0": 0.0, "1": 1.0, "2": 2.0, "3": 3.0}
    defaults = dict(
        t=0,
        cash=cash,
        tokens={},
        prices={"carbon": 1.0},
        stock_health={"carbon": min_health},
        last_satisfaction=None,
        money_system="scalar",
        efficiency=1.0,
        unit_cost=unit_cost,
    )
    defaults.update(overrides)
    return Observation(**defaults)


def test_rule_based_low_health_targets_level_1():
    policy = RuleBasedPolicy()
    obs = _obs(cash=100.0, min_health=0.2)
    action = policy.decide(obs)
    assert action.consumption == 1


def test_rule_based_medium_health_targets_level_2():
    policy = RuleBasedPolicy()
    obs = _obs(cash=100.0, min_health=0.5)
    action = policy.decide(obs)
    assert action.consumption == 2


def test_rule_based_healthy_and_cash_rich_targets_level_3():
    policy = RuleBasedPolicy()
    # cash=100 > 3 * unit_cost["1"]=3
    obs = _obs(cash=100.0, min_health=0.9)
    action = policy.decide(obs)
    assert action.consumption == 3


def test_rule_based_healthy_but_cash_poor_targets_level_2():
    policy = RuleBasedPolicy()
    # cash=2 <= 3 * unit_cost["1"]=3
    obs = _obs(cash=2.0, min_health=0.9)
    action = policy.decide(obs)
    assert action.consumption == 2


def test_rule_based_greedy_always_targets_level_3():
    policy = RuleBasedPolicy(greed=1.0)
    obs = _obs(cash=100.0, min_health=0.1)
    action = policy.decide(obs)
    assert action.consumption == 3


def test_rule_based_consumption_capped_by_affordability():
    policy = RuleBasedPolicy(greed=1.0)
    # only levels 0 and 1 affordable (cash=1.0)
    obs = _obs(cash=1.0, min_health=0.9)
    action = policy.decide(obs)
    assert action.consumption == 1


def test_rule_based_invests_when_cash_rich_and_health_low():
    policy = RuleBasedPolicy()
    obs = _obs(cash=100.0, min_health=0.5)
    action = policy.decide(obs)
    assert action.invest is True


def test_rule_based_does_not_invest_when_healthy():
    policy = RuleBasedPolicy()
    obs = _obs(cash=100.0, min_health=0.9)
    action = policy.decide(obs)
    assert action.invest is False


def test_rule_based_does_not_invest_when_cash_poor():
    policy = RuleBasedPolicy()
    obs = _obs(cash=5.0, min_health=0.2)
    action = policy.decide(obs)
    assert action.invest is False


def test_qlearning_decide_returns_valid_action():
    policy = QLearningPolicy()
    obs = _obs(cash=5.0, min_health=0.5)
    action = policy.decide(obs)
    assert isinstance(action, Action)
    assert 0 <= action.consumption <= 3
    assert isinstance(action.invest, bool)


def test_qlearning_updates_q_table_after_observe_result():
    policy = QLearningPolicy(epsilon=0.0)
    obs = _obs(cash=5.0, min_health=0.5)
    action = policy.decide(obs)
    state, idx = policy._last
    before = policy.archetype.q_table[state][idx]
    policy.observe_result(reward=1.0, next_obs=_obs(cash=6.0, min_health=0.5))
    after = policy.archetype.q_table[state][idx]
    assert after != before


def test_qlearning_observe_result_noop_without_prior_decide():
    policy = QLearningPolicy()
    # should not raise even though decide() was never called
    policy.observe_result(reward=1.0, next_obs=_obs(cash=5.0, min_health=0.5))


def test_llm_policy_mock_mode_matches_rule_based(monkeypatch):
    monkeypatch.setenv("VECTOR_MONEY_LLM_MOCK", "1")
    llm = LLMPolicy()
    assert llm.mock is True
    rule = RuleBasedPolicy()
    obs = _obs(cash=100.0, min_health=0.5)
    llm_action = llm.decide(obs)
    rule_action = rule.decide(obs)
    assert llm_action.consumption == rule_action.consumption
    assert llm_action.invest == rule_action.invest
    # mock mode never touches the network client
    assert llm._client is None


def test_llm_policy_mock_explicit_true_ignores_env(monkeypatch):
    monkeypatch.delenv("VECTOR_MONEY_LLM_MOCK", raising=False)
    llm = LLMPolicy(mock=True)
    assert llm.mock is True
    obs = _obs(cash=100.0, min_health=0.9)
    action = llm.decide(obs)
    assert isinstance(action, Action)


def test_make_policy_factory_variants():
    assert isinstance(make_policy("rule"), RuleBasedPolicy)
    greedy = make_policy("greedy")
    assert isinstance(greedy, RuleBasedPolicy)
    assert greedy.greed == 1.0
    assert isinstance(make_policy("rl"), QLearningPolicy)
    assert isinstance(make_policy("llm", mock=True), LLMPolicy)
    assert isinstance(make_policy("human"), HumanPolicy)


def test_make_policy_rejects_unknown_kind():
    with pytest.raises(ValueError):
        make_policy("nonsense")
