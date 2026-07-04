"""Unit tests for src.money: scalar vs vector money systems."""

from __future__ import annotations

import pytest

from src.money import (
    Purchase,
    ScalarMoney,
    VectorMoney,
    Wallet,
    make_money_system,
)


FOOTPRINT = {"carbon": 1.0, "water": 2.0}


def test_scalar_price_folds_footprint_into_cash():
    money = ScalarMoney()
    money.token_prices = {"carbon": 2.0, "water": 3.0, "biomass": 1.0, "minerals": 1.0}
    purchase = money.price(cash_cost=5.0, footprint=FOOTPRINT)
    # 5 base + 1*2 (carbon) + 2*3 (water) = 13
    assert purchase.cash_cost == pytest.approx(13.0)
    assert purchase.token_cost == {}


def test_scalar_can_afford_and_execute_deducts_cash():
    money = ScalarMoney()
    # default token_prices are all 1.0: footprint cost = 1*1 + 2*1 = 3
    purchase = money.price(cash_cost=5.0, footprint=FOOTPRINT)
    wallet = Wallet(cash=purchase.cash_cost)
    assert money.can_afford(wallet, purchase)
    assert money.execute(wallet, purchase)
    assert wallet.cash == pytest.approx(0.0)


def test_vector_lambda_zero_blocks_purchase_when_tokens_missing():
    money = VectorMoney(convertibility=0.0)
    wallet = Wallet(cash=100.0, tokens={"carbon": 0.5, "water": 0.0})
    purchase = money.price(cash_cost=1.0, footprint=FOOTPRINT)
    assert not money.can_afford(wallet, purchase)
    assert not money.execute(wallet, purchase)
    # wallet untouched on failed execute
    assert wallet.cash == pytest.approx(100.0)
    assert wallet.tokens["carbon"] == pytest.approx(0.5)


def test_vector_lambda_zero_allows_purchase_when_tokens_sufficient():
    money = VectorMoney(convertibility=0.0)
    wallet = Wallet(cash=10.0, tokens={"carbon": 1.0, "water": 2.0})
    purchase = money.price(cash_cost=1.0, footprint=FOOTPRINT)
    assert money.can_afford(wallet, purchase)
    assert money.execute(wallet, purchase)
    assert wallet.cash == pytest.approx(9.0)
    assert wallet.tokens["carbon"] == pytest.approx(0.0)
    assert wallet.tokens["water"] == pytest.approx(0.0)


def test_vector_tokens_never_go_negative():
    money = VectorMoney(convertibility=1.0)
    wallet = Wallet(cash=100.0, tokens={"carbon": 0.2, "water": 0.0})
    purchase = money.price(cash_cost=0.0, footprint=FOOTPRINT)
    assert money.execute(wallet, purchase)
    assert wallet.tokens["carbon"] == pytest.approx(0.0)
    assert wallet.tokens["water"] == pytest.approx(0.0)


def test_vector_lambda_one_conversion_cost_equals_scalar_resource_cost():
    scalar = ScalarMoney()
    vector = VectorMoney(convertibility=1.0)
    # same token_prices on both
    prices = {"carbon": 2.0, "water": 3.0, "biomass": 1.0, "minerals": 1.0}
    scalar.token_prices = dict(prices)
    vector.token_prices = dict(prices)

    scalar_purchase = scalar.price(cash_cost=0.0, footprint=FOOTPRINT)

    empty_wallet = Wallet(cash=1000.0, tokens={})
    vector_purchase = vector.price(cash_cost=0.0, footprint=FOOTPRINT)
    shortfall = vector._shortfall_cash(empty_wallet, vector_purchase)

    assert shortfall == pytest.approx(scalar_purchase.cash_cost)


def test_vector_premium_between_zero_and_one():
    lam = 0.5
    money = VectorMoney(convertibility=lam)
    money.token_prices["carbon"] = 2.0
    wallet = Wallet(cash=1000.0, tokens={})
    purchase = Purchase(cash_cost=0.0, token_cost={"carbon": 1.0})
    shortfall = money._shortfall_cash(wallet, purchase)
    # premium is 1/lambda: cost = missing * price / lambda
    assert shortfall == pytest.approx(1.0 * 2.0 / lam)
    assert shortfall == pytest.approx(4.0)


def test_issue_splits_allocation_equally_and_applies_carryover_decay():
    money = VectorMoney(convertibility=0.0, carryover=0.5)
    wallets = [Wallet(cash=0.0, tokens={"carbon": 2.0}) for _ in range(4)]
    money.issue(wallets, allocation={"carbon": 8.0})
    for w in wallets:
        # decayed old (2.0 * 0.5 = 1.0) + new share (8.0 / 4 = 2.0) = 3.0
        assert w.tokens["carbon"] == pytest.approx(3.0)


def test_issue_no_op_on_empty_wallets():
    money = VectorMoney()
    money.issue([], allocation={"carbon": 10.0})  # should not raise


def test_scalar_issue_is_no_op():
    money = ScalarMoney()
    wallet = Wallet(cash=1.0, tokens={})
    money.issue([wallet], allocation={"carbon": 5.0})
    assert wallet.tokens == {}


def test_make_money_system_variants():
    assert isinstance(make_money_system("scalar"), ScalarMoney)
    vector = make_money_system("vector")
    assert isinstance(vector, VectorMoney)
    assert vector.convertibility == 0.0

    scalar_from_float = make_money_system(1.0)
    assert isinstance(scalar_from_float, ScalarMoney)

    partial = make_money_system(0.3)
    assert isinstance(partial, VectorMoney)
    assert partial.convertibility == pytest.approx(0.3)


def test_make_money_system_rejects_junk():
    with pytest.raises(ValueError):
        make_money_system("nonsense")


def test_vector_convertibility_out_of_range_raises():
    with pytest.raises(ValueError):
        VectorMoney(convertibility=1.5)
    with pytest.raises(ValueError):
        VectorMoney(convertibility=-0.1)


def test_update_prices_moves_toward_target_with_sensitivity():
    money = ScalarMoney()
    money.token_prices["carbon"] = 1.0
    # health 0.5 -> scarcity 0.5 -> target = 1 + 4*0.5 = 3.0
    money.update_prices({"carbon": 0.5}, sensitivity=0.2)
    expected = 1.0 + 0.2 * (3.0 - 1.0)
    assert money.token_prices["carbon"] == pytest.approx(expected)
