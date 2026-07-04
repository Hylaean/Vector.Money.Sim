"""End-to-end smoke test for the experiment matrix runner."""

from __future__ import annotations

import csv
import json
import os

import yaml

from experiments.run_matrix import run_matrix


def _tiny_config() -> dict:
    return {
        "steps": 30,
        "n_households": 6,
        "seeds": 2,
        "money": ["scalar", "vector"],
        "environment": ["static"],
        "policies": ["rule", {"rule": 3, "greedy": 3}],
    }


def test_matrix_runs_and_writes_artefacts(tmp_path):
    config = _tiny_config()
    output_dir = str(tmp_path / "results")
    rows = run_matrix(config, output_dir)

    # 2 money x 1 environment x 2 policy specs x 2 seeds = 8 runs
    assert len(rows) == 8

    runs_csv = os.path.join(output_dir, "runs.csv")
    summary_json = os.path.join(output_dir, "summary.json")
    assert os.path.isfile(runs_csv)
    assert os.path.isfile(summary_json)

    with open(runs_csv, newline="") as fh:
        reader = csv.DictReader(fh)
        csv_rows = list(reader)
    assert len(csv_rows) == 8
    expected_fields = {
        "money", "environment", "policy", "seed",
        "welfare_mean", "welfare_final", "gini_satisfaction_mean",
        "gini_wealth_final", "overshoot_total",
        "overshoot_carbon", "overshoot_water", "overshoot_biomass", "overshoot_minerals",
        "return_time_carbon", "return_time_water", "return_time_biomass", "return_time_minerals",
    }
    assert expected_fields.issubset(set(csv_rows[0].keys()))
    for row in csv_rows:
        float(row["welfare_mean"])  # numeric and parseable

    with open(summary_json) as fh:
        summary = json.load(fh)
    # 2 money x 1 environment x 2 policy specs = 4 conditions
    assert len(summary) == 4
    for entry in summary:
        assert entry["n"] == 2
        assert "mean" in entry["welfare_mean"] and "sd" in entry["welfare_mean"]

    timeseries_dir = os.path.join(output_dir, "timeseries")
    ts_files = os.listdir(timeseries_dir)
    assert len(ts_files) == 8
    sample_path = os.path.join(timeseries_dir, ts_files[0])
    with open(sample_path, newline="") as fh:
        ts_reader = csv.DictReader(fh)
        ts_rows = list(ts_reader)
    assert len(ts_rows) == 30
    assert "welfare" in ts_rows[0]


def test_configs_are_valid_yaml_and_loadable():
    for name in ("matrix.yaml", "convertibility_sweep.yaml", "substrates.yaml"):
        path = os.path.join("experiments", "configs", name)
        with open(path) as fh:
            config = yaml.safe_load(fh)
        assert "steps" in config
        assert "n_households" in config
        assert "seeds" in config
        assert "money" in config
        assert "environment" in config
        assert "policies" in config
