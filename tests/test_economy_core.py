"""Unit tests for src.economy: the household/money/environment simulation."""

from __future__ import annotations

import pytest

from src.economy import Economy, EconomyConfig
from src.policies import RuleBasedPolicy, make_policy


def _run(**overrides) -> dict:
    cfg = EconomyConfig(**overrides)
    return Economy(cfg).run()


def test_run_returns_all_documented_keys():
    results = _run(steps=10, n_households=5)
    expected_keys = {
        "config",
        "welfare_mean",
        "welfare_final",
        "gini_satisfaction_mean",
        "gini_wealth_final",
        "overshoot_depth",
        "overshoot_total",
        "return_time",
        "records",
    }
    assert expected_keys.issubset(results.keys())


def test_records_length_equals_steps():
    results = _run(steps=17, n_households=5)
    assert len(results["records"]) == 17


def test_satisfaction_zero_when_consumption_zero():
    class ZeroPolicy:
        def decide(self, obs):
            from src.policies import Action

            return Action(consumption=0, invest=False)

        def observe_result(self, reward, next_obs):
            pass

    cfg = EconomyConfig(steps=5, n_households=3, money="scalar", environment="static")
    policies = [ZeroPolicy() for _ in range(cfg.n_households)]
    results = Economy(cfg, policies=policies).run()
    assert results["welfare_mean"] == pytest.approx(0.0)
    assert results["welfare_final"] == pytest.approx(0.0)


def test_vector_static_greedy_never_overshoots():
    """Hard budget: tokens are strictly binding (lambda=0), so a greedy
    policy cannot extract past the sustainable-yield allocation even under
    aggressive demand in a stationary environment."""
    for seed in range(4):
        cfg = EconomyConfig(
            steps=120,
            n_households=20,
            money="vector",
            environment="static",
            convertibility=0.0,
            seed=seed,
        )
        policies = [make_policy("greedy") for _ in range(cfg.n_households)]
        results = Economy(cfg, policies=policies).run()
        assert results["overshoot_total"] == pytest.approx(0.0), (
            f"seed={seed} overshoot={results['overshoot_total']}"
        )


def test_vector_shifting_has_lower_overshoot_than_scalar_shifting():
    seeds = range(6)
    scalar_overshoots = []
    vector_overshoots = []
    scalar_ginis = []
    vector_ginis = []
    for seed in seeds:
        scalar_results = _run(
            steps=120, n_households=20, money="scalar", environment="shifting", seed=seed
        )
        vector_results = _run(
            steps=120, n_households=20, money="vector", environment="shifting", seed=seed
        )
        scalar_overshoots.append(scalar_results["overshoot_total"])
        vector_overshoots.append(vector_results["overshoot_total"])
        scalar_ginis.append(scalar_results["gini_satisfaction_mean"])
        vector_ginis.append(vector_results["gini_satisfaction_mean"])

    scalar_mean_overshoot = sum(scalar_overshoots) / len(scalar_overshoots)
    vector_mean_overshoot = sum(vector_overshoots) / len(vector_overshoots)
    scalar_mean_gini = sum(scalar_ginis) / len(scalar_ginis)
    vector_mean_gini = sum(vector_ginis) / len(vector_ginis)

    assert vector_mean_overshoot < scalar_mean_overshoot
    assert vector_mean_gini < scalar_mean_gini


def test_default_policy_is_rule_based_when_none_provided():
    cfg = EconomyConfig(steps=3, n_households=2)
    economy = Economy(cfg)
    assert all(isinstance(hh.policy, RuleBasedPolicy) for hh in economy.households)


def test_households_start_with_expected_cash_and_wage():
    cfg = EconomyConfig(steps=1, n_households=10, wage_mean=3.0, wage_spread=0.5, seed=7)
    economy = Economy(cfg)
    for hh in economy.households:
        assert hh.wallet.cash == pytest.approx(5.0)
        assert hh.wage > 0.0
