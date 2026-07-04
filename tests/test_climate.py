"""Unit tests for src.climate: resource stocks and environments."""

from __future__ import annotations

import pytest

from src.climate import (
    ClimateTrajectory,
    ResourceState,
    ShiftingEnvironment,
    StaticEnvironment,
    make_environment,
)


def test_logistic_regen_never_exceeds_capacity():
    res = ResourceState(name="carbon", stock=99.9, capacity=100.0, regen_rate=0.5)
    for _ in range(50):
        res.regenerate()
        assert res.stock <= 100.0


def test_logistic_regen_at_capacity_is_stable():
    res = ResourceState(name="carbon", stock=100.0, capacity=100.0, regen_rate=0.5)
    res.regenerate()
    assert res.stock == pytest.approx(100.0)


def test_extract_caps_at_stock():
    res = ResourceState(name="water", stock=5.0)
    taken = res.extract(10.0)
    assert taken == pytest.approx(5.0)
    assert res.stock == pytest.approx(0.0)


def test_extract_negative_amount_takes_nothing():
    res = ResourceState(name="water", stock=5.0)
    taken = res.extract(-3.0)
    assert taken == pytest.approx(0.0)
    assert res.stock == pytest.approx(5.0)


def test_static_env_sustainable_yield_positive_above_boundary():
    env = make_environment("static", seed=0)
    env.step()
    yield_ = env.sustainable_yield("carbon", observation_lag=1)
    assert yield_ > 0.0


def test_static_env_sustainable_yield_zero_when_lagged_stock_at_or_below_boundary():
    resources = {"carbon": ResourceState(name="carbon", stock=30.0, boundary=40.0)}
    env = StaticEnvironment(resources=resources)
    env.step()
    assert env.sustainable_yield("carbon", observation_lag=1) == 0.0


def test_shifting_env_rate_multiplier_decreases_to_floor():
    env = make_environment("shifting", seed=1)
    r0 = env.rate_multiplier("water")
    assert r0 == pytest.approx(1.0)
    env.t = 100
    r_mid = env.rate_multiplier("water")
    assert r_mid < r0

    env.t = 1000
    r_late = env.rate_multiplier("water")
    assert r_late == pytest.approx(env.trajectory.regen_floor)


def test_shifting_env_shocks_recorded_and_destroy_stock():
    trajectory = ClimateTrajectory(
        shock_prob_initial=1.0, shock_prob_growth=0.0, shock_prob_max=1.0
    )
    env = ShiftingEnvironment(trajectory=trajectory)
    before = {n: r.stock for n, r in env.resources.items()}
    env.step()
    assert len(env.shocks) == 1
    shock = env.shocks[0]
    for name in trajectory.shocked_resources:
        assert shock[name] > 0.0
        assert env.resources[name].stock < before[name]


def test_shifting_env_no_shocks_when_probability_zero():
    trajectory = ClimateTrajectory(shock_prob_initial=0.0, shock_prob_growth=0.0)
    env = ShiftingEnvironment(trajectory=trajectory)
    for _ in range(20):
        env.step()
    assert env.shocks == []


def test_same_seed_identical_trajectories():
    env_a = make_environment("shifting", seed=42)
    env_b = make_environment("shifting", seed=42)
    for _ in range(50):
        env_a.step()
        env_b.step()
    assert env_a.snapshot() == env_b.snapshot()
    assert env_a.shocks == env_b.shocks


def test_different_seeds_diverge():
    env_a = make_environment("shifting", seed=1)
    env_b = make_environment("shifting", seed=2)
    for _ in range(80):
        env_a.step()
        env_b.step()
    assert env_a.snapshot() != env_b.snapshot() or env_a.shocks != env_b.shocks


def test_make_environment_rejects_unknown_kind():
    with pytest.raises(ValueError):
        make_environment("weird")


def test_resource_state_in_overshoot_and_health():
    res = ResourceState(name="x", stock=20.0, capacity=100.0, boundary=40.0)
    assert res.in_overshoot
    assert res.health == pytest.approx(0.2)
