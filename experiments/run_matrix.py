"""Run the scalar-vs-vector money experiment matrix.

Reads a YAML config describing a cross-product of money systems,
environments, policies and seeds; runs :class:`src.economy.Economy` for
every combination; and writes three artefacts to ``--output``:

* ``runs.csv`` — one row per (money, environment, policy, seed) run,
* ``summary.json`` — mean/sd of each metric per (money, environment,
  policy) condition, aggregated across seeds,
* ``timeseries/<money>_<environment>_<policy>_s<seed>.csv`` — the
  per-step records of that single run.

Usage::

    python -m experiments.run_matrix --config experiments/configs/matrix.yaml \
        --output experiments/results
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
from typing import Dict, Iterable, List, Sequence

import yaml

from src.economy import Economy, EconomyConfig
from src.policies import LLMPolicy, Policy, make_policy

RESOURCE_NAMES = ("carbon", "water", "biomass", "minerals")
OVERRIDE_KEYS = ("issuance_headroom", "carryover", "price_sensitivity", "observation_lag")

_llm_mock_warned = False


def load_config(path: str) -> dict:
    with open(path, "r") as fh:
        return yaml.safe_load(fh)


def money_label(money) -> str:
    return str(money)


def policy_label(policy) -> str:
    if isinstance(policy, dict):
        parts = "+".join(f"{k}{v}" for k, v in sorted(policy.items()))
        return f"mix[{parts}]"
    return str(policy)


def slugify(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.+\[\]=-]+", "_", label)


def build_policies(policy_spec, n_households: int) -> List[Policy]:
    """Build the ordered list of per-household policies for one run.

    ``policy_spec`` is either a single kind string (all households use it)
    or a dict of ``{kind: count}`` (must sum to ``n_households``).
    """
    global _llm_mock_warned
    if isinstance(policy_spec, dict):
        total = sum(policy_spec.values())
        if total != n_households:
            raise ValueError(
                f"mixed policy counts {policy_spec} sum to {total}, "
                f"expected n_households={n_households}"
            )
        kinds: List[str] = []
        for kind, count in sorted(policy_spec.items()):
            kinds.extend([kind] * count)
    else:
        kinds = [policy_spec] * n_households

    policies: List[Policy] = []
    for kind in kinds:
        policy = make_policy(kind)
        if isinstance(policy, LLMPolicy) and policy.mock and not _llm_mock_warned:
            print(
                "WARNING: LLMPolicy running in mock mode "
                "(no anthropic credentials or VECTOR_MONEY_LLM_MOCK=1); "
                "falls back to rule-based decisions."
            )
            _llm_mock_warned = True
        policies.append(policy)
    return policies


def run_one(money, environment, policy_spec, seed: int, steps: int, n_households: int,
            overrides: Dict[str, float]) -> dict:
    kwargs = dict(
        n_households=n_households,
        steps=steps,
        seed=seed,
        money=money,
        environment=environment,
    )
    kwargs.update(overrides)
    config = EconomyConfig(**kwargs)
    policies = build_policies(policy_spec, n_households)
    economy = Economy(config, policies=policies)
    return economy.run()


def flatten_result(money, environment, policy_spec, seed: int, result: dict) -> dict:
    overshoot = result["overshoot_depth"]
    return_time = result["return_time"]
    row = {
        "money": money_label(money),
        "environment": environment,
        "policy": policy_label(policy_spec),
        "seed": seed,
        "welfare_mean": result["welfare_mean"],
        "welfare_final": result["welfare_final"],
        "gini_satisfaction_mean": result["gini_satisfaction_mean"],
        "gini_wealth_final": result["gini_wealth_final"],
        "overshoot_total": result["overshoot_total"],
    }
    for name in RESOURCE_NAMES:
        row[f"overshoot_{name}"] = overshoot.get(name, 0.0)
    for name in RESOURCE_NAMES:
        row[f"return_time_{name}"] = return_time.get(name, 0)
    return row


RUN_FIELDS = [
    "money", "environment", "policy", "seed",
    "welfare_mean", "welfare_final", "gini_satisfaction_mean", "gini_wealth_final",
    "overshoot_total",
    "overshoot_carbon", "overshoot_water", "overshoot_biomass", "overshoot_minerals",
    "return_time_carbon", "return_time_water", "return_time_biomass", "return_time_minerals",
]

SUMMARY_METRICS = [f for f in RUN_FIELDS if f not in ("money", "environment", "policy", "seed")]


def mean_sd(values: Sequence[float]) -> Dict[str, float]:
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "sd": 0.0}
    m = sum(values) / n
    if n < 2:
        return {"mean": m, "sd": 0.0}
    variance = sum((v - m) ** 2 for v in values) / (n - 1)
    return {"mean": m, "sd": math.sqrt(variance)}


def summarize(rows: List[dict]) -> List[dict]:
    conditions: Dict[tuple, List[dict]] = {}
    for row in rows:
        key = (row["money"], row["environment"], row["policy"])
        conditions.setdefault(key, []).append(row)

    summary = []
    for (money, environment, policy), condition_rows in sorted(conditions.items()):
        entry = {
            "money": money,
            "environment": environment,
            "policy": policy,
            "n": len(condition_rows),
        }
        for metric in SUMMARY_METRICS:
            entry[metric] = mean_sd([r[metric] for r in condition_rows])
        summary.append(entry)
    return summary


def write_runs_csv(rows: List[dict], path: str) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=RUN_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_timeseries_csv(records: List[dict], path: str) -> None:
    if not records:
        return
    fieldnames = sorted({key for rec in records for key in rec})
    # keep 't' first for readability
    if "t" in fieldnames:
        fieldnames.remove("t")
        fieldnames = ["t"] + fieldnames
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)


def print_summary_table(summary: List[dict]) -> None:
    headers = ["money", "environment", "policy", "n", "welfare_mean", "gini_satisfaction_mean",
               "gini_wealth_final", "overshoot_total"]
    display_rows = []
    for entry in summary:
        display_rows.append([
            entry["money"], entry["environment"], entry["policy"], str(entry["n"]),
            f"{entry['welfare_mean']['mean']:.3f}±{entry['welfare_mean']['sd']:.3f}",
            f"{entry['gini_satisfaction_mean']['mean']:.3f}±{entry['gini_satisfaction_mean']['sd']:.3f}",
            f"{entry['gini_wealth_final']['mean']:.3f}±{entry['gini_wealth_final']['sd']:.3f}",
            f"{entry['overshoot_total']['mean']:.2f}±{entry['overshoot_total']['sd']:.2f}",
        ])
    widths = [max(len(headers[i]), max((len(r[i]) for r in display_rows), default=0))
              for i in range(len(headers))]
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("  ".join("-" * w for w in widths))
    for r in display_rows:
        print("  ".join(r[i].ljust(widths[i]) for i in range(len(r))))


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="path to YAML matrix config")
    parser.add_argument("--output", required=True, help="output directory")
    return parser.parse_args(argv)


def run_matrix(config: dict, output_dir: str) -> List[dict]:
    steps = config["steps"]
    n_households = config["n_households"]
    seeds_spec = config["seeds"]
    seeds: Iterable[int] = range(seeds_spec) if isinstance(seeds_spec, int) else seeds_spec
    money_list = config["money"]
    environment_list = config["environment"]
    policy_list = config["policies"]
    overrides = {k: config[k] for k in OVERRIDE_KEYS if k in config}

    os.makedirs(output_dir, exist_ok=True)
    timeseries_dir = os.path.join(output_dir, "timeseries")
    os.makedirs(timeseries_dir, exist_ok=True)

    rows: List[dict] = []
    for money in money_list:
        for environment in environment_list:
            for policy_spec in policy_list:
                for seed in seeds:
                    result = run_one(
                        money, environment, policy_spec, seed, steps, n_households, overrides
                    )
                    row = flatten_result(money, environment, policy_spec, seed, result)
                    rows.append(row)

                    slug = "_".join([
                        slugify(money_label(money)),
                        slugify(environment),
                        slugify(policy_label(policy_spec)),
                    ])
                    ts_path = os.path.join(timeseries_dir, f"{slug}_s{seed}.csv")
                    write_timeseries_csv(result["records"], ts_path)

    write_runs_csv(rows, os.path.join(output_dir, "runs.csv"))
    summary = summarize(rows)
    with open(os.path.join(output_dir, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print_summary_table(summary)
    return rows


def main(argv=None) -> None:
    args = parse_args(argv)
    config = load_config(args.config)
    run_matrix(config, args.output)


if __name__ == "__main__":
    main()
