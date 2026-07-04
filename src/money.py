"""Money systems: the scalar ↔ vector continuum.

The core idea of the project, made operational.  A *money system* defines
what a wallet holds and what a purchase costs:

* **Scalar money** — one fungible balance (``cash``).  Ecological
  constraints reach agents only through *prices*, which respond to
  scarcity with a lag.
* **Vector money** — cash **plus** one non-fungible token dimension per
  biophysical stock (carbon, water, biomass, minerals).  Tokens are
  issued each period at the institution's estimate of sustainable yield
  (a cap-and-share allowance) and must be surrendered in proportion to a
  purchase's resource footprint.  Ecological constraints reach agents as
  *quantities*, not prices.

The two are ends of one continuum.  ``convertibility`` (λ ∈ [0, 1])
controls how freely cash substitutes for missing tokens:

* λ = 0 — strictly non-convertible tokens (pure vector money),
* λ = 1 — tokens freely purchasable at face value (economically
  equivalent to scalar money),
* 0 < λ < 1 — cash converts at an effective premium of 1/λ.

This lets experiments sweep a single parameter from scalar to vector
rather than comparing two unrelated mechanisms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


RESOURCE_DIMS = ("carbon", "water", "biomass", "minerals")


@dataclass
class Wallet:
    """One agent's holdings: cash plus per-resource token balances."""

    cash: float = 0.0
    tokens: Dict[str, float] = field(default_factory=dict)

    def token_balance(self, dim: str) -> float:
        return self.tokens.get(dim, 0.0)

    def add_tokens(self, dim: str, amount: float) -> None:
        self.tokens[dim] = self.tokens.get(dim, 0.0) + amount

    def decay_tokens(self, keep_fraction: float) -> None:
        """Demurrage: unspent tokens decay so they cannot be hoarded forever."""
        for dim in list(self.tokens):
            self.tokens[dim] *= keep_fraction


@dataclass
class Purchase:
    """A priced bundle: cash cost plus per-resource token cost (footprint)."""

    cash_cost: float
    token_cost: Dict[str, float] = field(default_factory=dict)


class MoneySystem:
    """Base money system.  Subclasses define how footprints are charged."""

    name = "abstract"

    def __init__(self, token_prices: Dict[str, float] | None = None) -> None:
        # Unit cash value of one token in each dimension; used both for
        # convertibility pricing and for scalar-mode footprint pricing.
        self.token_prices: Dict[str, float] = token_prices or {
            dim: 1.0 for dim in RESOURCE_DIMS
        }

    # -- interface ------------------------------------------------------

    def price(self, cash_cost: float, footprint: Dict[str, float]) -> Purchase:
        raise NotImplementedError

    def can_afford(self, wallet: Wallet, purchase: Purchase) -> bool:
        return self._shortfall_cash(wallet, purchase) is not None

    def execute(self, wallet: Wallet, purchase: Purchase) -> bool:
        """Deduct the purchase from the wallet.  Returns False if unaffordable."""
        total_cash = self._shortfall_cash(wallet, purchase)
        if total_cash is None:
            return False
        wallet.cash -= total_cash
        for dim, amount in purchase.token_cost.items():
            held = wallet.token_balance(dim)
            wallet.tokens[dim] = max(0.0, held - amount)
        return True

    def issue(self, wallets: Iterable[Wallet], allocation: Dict[str, float]) -> None:
        """Distribute per-capita token allowances (no-op for scalar money)."""

    def update_prices(self, stock_health: Dict[str, float], sensitivity: float) -> None:
        """Adjust per-dimension prices in response to (lagged) scarcity."""
        for dim, health in stock_health.items():
            if dim not in self.token_prices:
                continue
            scarcity = max(0.0, 1.0 - health)
            # Multiplicative walk toward higher prices as stocks degrade,
            # relaxing back toward 1.0 as they recover.
            target = 1.0 + 4.0 * scarcity
            current = self.token_prices[dim]
            self.token_prices[dim] = current + sensitivity * (target - current)

    # -- internals -------------------------------------------------------

    def _shortfall_cash(self, wallet: Wallet, purchase: Purchase) -> float | None:
        """Total cash needed (base + conversions).  None if unaffordable."""
        raise NotImplementedError


class ScalarMoney(MoneySystem):
    """Fully fungible money: footprints are charged in cash at market prices."""

    name = "scalar"

    def price(self, cash_cost: float, footprint: Dict[str, float]) -> Purchase:
        resource_cash = sum(
            self.token_prices.get(dim, 1.0) * qty for dim, qty in footprint.items()
        )
        return Purchase(cash_cost=cash_cost + resource_cash, token_cost={})

    def _shortfall_cash(self, wallet: Wallet, purchase: Purchase) -> float | None:
        return purchase.cash_cost if wallet.cash >= purchase.cash_cost else None


class VectorMoney(MoneySystem):
    """Multi-dimensional money: footprints are charged in resource tokens.

    ``convertibility`` (λ) sets the cash-for-tokens escape hatch; ``carryover``
    is the fraction of unspent tokens that survives to the next period.
    """

    name = "vector"

    def __init__(
        self,
        convertibility: float = 0.0,
        carryover: float = 0.5,
        token_prices: Dict[str, float] | None = None,
    ) -> None:
        super().__init__(token_prices=token_prices)
        if not 0.0 <= convertibility <= 1.0:
            raise ValueError("convertibility must be in [0, 1]")
        self.convertibility = convertibility
        self.carryover = carryover

    def price(self, cash_cost: float, footprint: Dict[str, float]) -> Purchase:
        return Purchase(cash_cost=cash_cost, token_cost=dict(footprint))

    def issue(self, wallets: Iterable[Wallet], allocation: Dict[str, float]) -> None:
        wallets = list(wallets)
        if not wallets:
            return
        share = {dim: total / len(wallets) for dim, total in allocation.items()}
        for wallet in wallets:
            wallet.decay_tokens(self.carryover)
            for dim, amount in share.items():
                wallet.add_tokens(dim, amount)

    def _shortfall_cash(self, wallet: Wallet, purchase: Purchase) -> float | None:
        conversion_cost = 0.0
        for dim, amount in purchase.token_cost.items():
            missing = max(0.0, amount - wallet.token_balance(dim))
            if missing <= 0:
                continue
            if self.convertibility <= 0.0:
                return None  # strictly non-convertible: tokens are binding
            unit_price = self.token_prices.get(dim, 1.0) / self.convertibility
            conversion_cost += missing * unit_price
        total = purchase.cash_cost + conversion_cost
        return total if wallet.cash >= total else None


def make_money_system(kind: str | float, **kwargs) -> MoneySystem:
    """Factory.

    ``kind`` may be ``"scalar"``, ``"vector"`` or a float λ in [0, 1]
    interpreted as vector money with that convertibility (1.0 → scalar).
    """
    if isinstance(kind, (int, float)) and not isinstance(kind, bool):
        lam = float(kind)
        if lam >= 1.0:
            return ScalarMoney()
        return VectorMoney(convertibility=lam, **kwargs)
    if kind == "scalar":
        return ScalarMoney()
    if kind == "vector":
        return VectorMoney(**kwargs)
    raise ValueError(f"unknown money system: {kind!r}")
