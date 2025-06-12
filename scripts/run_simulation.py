"""Run Vector Money Simulation using YAML configuration."""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import yaml

from src import (
    BioPhysicalStocks,
    FinancialIntermediary,
    Firm,
    Government,
    Household,
    Market,
)


def set_seeds(seed: int) -> None:
    """Initialise Python and NumPy RNGs."""
    random.seed(seed)
    np.random.seed(seed)


def load_config(path: str | Path) -> Dict[str, Any]:
    """Return configuration dictionary from YAML file."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run_model(cfg: Dict[str, Any], seed: int) -> List[Dict[str, Any]]:
    """Execute one simulation and return recorded time series."""
    set_seeds(seed)

    agents_cfg = cfg.get("agents", {})
    steps = int(cfg.get("steps", 1))

    stocks = BioPhysicalStocks(**cfg.get("initial_stocks", {}))
    market = Market(stocks, price_sensitivity=cfg.get("price_sensitivity", 0.5))

    agents = []
    for i in range(int(agents_cfg.get("households", 0))):
        agents.append(Household(i, model=None))  # type: ignore[arg-type]
    offset = len(agents)
    for j in range(int(agents_cfg.get("firms", 0))):
        agents.append(Firm(offset + j, model=None))  # type: ignore[arg-type]
    if agents_cfg.get("government"):
        agents.append(Government("gov", model=None))  # type: ignore[arg-type]
    if agents_cfg.get("bank"):
        agents.append(FinancialIntermediary("bank", model=None))  # type: ignore[arg-type]

    records: List[Dict[str, Any]] = []
    for step in range(steps):
        for ag in agents:
            ag.step()
        stocks.step()
        market.adjust_prices()
        records.append(
            {
                "step": step,
                "carbon_budget": stocks.carbon_budget.value,
                "water": stocks.water.value,
                "biomass": stocks.biomass.value,
                "minerals": stocks.minerals.value,
            }
        )
    return records


def save_records(records: List[Dict[str, Any]], path: str | Path) -> None:
    """Write records to ``path`` as CSV."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="YAML configuration file")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    base_seed = int(cfg.get("seed", 0))
    ensembles = int(cfg.get("ensembles", 1))
    output_dir = Path(cfg.get("output_dir", "outputs"))

    for idx in range(ensembles):
        run_seed = base_seed + idx
        records = run_model(cfg, seed=run_seed)
        out_file = output_dir / f"run_{idx}.csv"
        save_records(records, out_file)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
