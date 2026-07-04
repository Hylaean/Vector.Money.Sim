# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Vector Money Simulation: an open research project testing *vector money* — multi-dimensional currency whose components are tied to biophysical stocks (carbon, water, biomass, minerals) — against ordinary scalar money, in agent-based simulations and experiments across four decision substrates (rule-based, Q-learning, Claude LLM agents, humans) and two environments (static vs shifting climate). The research thesis lives in `docs/thesis.md`; grant proposals and funding strategy in `proposals/`; the website in `site/index.html`. GPLv3.

## Commands

```bash
.venv/bin/python -m pytest -q                     # full suite (61 tests, ~2 s)
.venv/bin/python -m pytest tests/test_money.py::test_name   # single test
.venv/bin/python -m experiments.run_matrix --config experiments/configs/matrix.yaml --output experiments/results
.venv/bin/python -m experiments.plot_results --results experiments/results --sweep experiments/results_convertibility --output figures
```

A project venv exists at `.venv/` (mesa<3, pandas, pysd, numpy, matplotlib, pytest, pyyaml, anthropic). Format with `black` and `isort`.

## Critical gotchas

- **Run everything from the repo root.** Code, tests, and scripts import `from src import ...` — `src/` is itself the package. (`pyproject.toml`'s `packages.find where = ["src"]` doesn't match this layout; the project works from a repo-root checkout, not as an installed package.)
- **Mesa must stay < 3.0.** `src/agents/*` use the Mesa 2.x `Agent.__init__(unique_id, model)` signature; Mesa 3 removed it.
- **LLM calls are mock-gated.** `LLMPolicy` (src/policies.py) falls back to a deterministic rule-based mock when `VECTOR_MONEY_LLM_MOCK=1`, when `anthropic` is missing, or when no API credentials exist. Tests set this; never write a test that needs the network.
- **The experiment layer is deterministic per seed.** `Date`-free, seeded `random.Random` everywhere. Keep it that way — reproducibility is a headline claim of the project (README quotes exact numbers).
- **Changing simulation constants invalidates prose.** The 2×2 results table appears in README.md, docs/thesis.md, site/index.html, and proposals/*. If you touch `src/economy.py` constants, `src/climate.py` trajectories, or `experiments/configs/matrix.yaml`, re-run the matrix and reconcile every document. The human web game (`experiments/human/web/index.html`) ports the same constants to JS — keep them in sync.

## Architecture

Two layers share `src/metrics.py` (welfare, Gini, overshoot depth, return time):

1. **Experiment layer** (the active research code): `src/climate.py` (logistic stocks, `StaticEnvironment` / `ShiftingEnvironment` with drift→floor and capped shock ramp) → `src/money.py` (`ScalarMoney` / `VectorMoney`; convertibility λ∈[0,1] makes them endpoints of one continuum; per-capita issuance at lagged sustainable-yield estimates) → `src/economy.py` (`Economy`/`EconomyConfig`: households choose consumption 0–3 + efficiency investment; hard budget constraints; physical availability caps satisfaction) → `src/policies.py` (`Policy` interface: `RuleBasedPolicy`, `QLearningPolicy`, `LLMPolicy` (claude-haiku-4-5, structured output, prompt caching), `HumanPolicy`). `experiments/run_matrix.py` runs config-driven cross-products; `experiments/plot_results.py` makes the figures.
2. **Legacy Mesa scaffold** (retained, tested): `src/agents/`, `src/models/baseline.py`, `src/doughnut_abm.py`, `src/markets/market.py`, `src/biophysics/stocks.py` (pysd-optional), `scripts/run_simulation.py` + `configs/example.yaml`.

The human experiment (`experiments/human/`) is a faithful JS port of the experiment layer: one participant among 19 rule-based bots, neutral framing ("stamps"/"materials"), 2×2 condition via URL params.

## Conventions (from robots.md)

- Save the user prompt that led to each commit in `docs/prompts/`.
- New functionality comes with unit tests under `tests/` and documentation updates in `docs/`.
