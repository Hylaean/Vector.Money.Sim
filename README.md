# Vector Money Simulation

**Should money have more than one dimension?**

Every ecological fact the economy must act on — a shrinking carbon budget, a depleted aquifer — gets compressed into a single scalar (a price) before anyone's budget constraint feels it. *Vector money* is the proposal that money should carry ecological information natively: a wallet holds cash **plus** non-fungible token components tied one-to-one to biophysical stocks (carbon, water, biomass, minerals), issued each period at the estimated sustainable yield of each stock.

This repository does not advocate vector money. It **tests** it: open agent-based simulations and controlled experiments where the same economy is played by rule-based agents, reinforcement learners, LLM agents (Claude), and human participants — in worlds that hold still and worlds with a shifting climate.

📖 **[Read the full thesis](docs/thesis.md)** · 🌐 **[Project site](site/index.html)** · 🧪 **[Human experiment](experiments/human/)** · 💰 **[Funding strategy & proposals](proposals/)**

## First results

12 seeds × 200 periods, rule-based agents (`python -m experiments.run_matrix`):

| Condition | Welfare | Cumulative overshoot | Satisfaction Gini |
|---|---|---|---|
| Scalar × static | **0.84** | 0.0 | 0.10 |
| Scalar × shifting climate | 0.62 | **60.0** | 0.05 |
| Vector × static | 0.52 | 0.0 | **0.01** |
| Vector × shifting climate | 0.46 | **29.8** | **0.01** |

- **In a stable world, scalar money wins** — roughly 60 % more welfare (0.84 ± 0.03 vs 0.52 ± 0.10) at zero overshoot for both regimes.
- **Under a shifting climate, vector money's cumulative overshoot is roughly half scalar's** (29.8 ± 9.6 vs 60.0 ± 18.1) and its stocks *recover* above the ecological boundary while scalar money's are drained and stay drained. (n = 12 seeds; a directional finding, not a precisely quantified one.)
- **Cash-convertibility protection collapses somewhere between 0 % and 25 %** (our sweep's grid is too coarse to pin the threshold down further) — Friedman's black-market critique, quantified — while in stable worlds *partial* convertibility beats both pure systems on welfare.

Every claim above is one command away from being checked. Details, caveats and the four critiques we invite (Hayek, Friedman, complexity backfire, mental accounting) are in [docs/thesis.md](docs/thesis.md).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e . && pip install pytest matplotlib
pytest                                            # 61 tests, ~2 s

# reproduce the headline 2×2 matrix
python -m experiments.run_matrix --config experiments/configs/matrix.yaml --output experiments/results

# the scalar↔vector convertibility sweep
python -m experiments.run_matrix --config experiments/configs/convertibility_sweep.yaml --output experiments/results_convertibility

# regenerate all figures
python -m experiments.plot_results --results experiments/results --sweep experiments/results_convertibility --output figures
```

To run **LLM agents** (Claude) instead of the offline mock, set `ANTHROPIC_API_KEY` and use `experiments/configs/substrates.yaml`; without credentials the harness falls back to a deterministic mock so tests and CI never need the network. To try the **human experiment**, open `experiments/human/web/index.html?money=vector&env=shifting` in a browser.

## What's in the box

| Path | What it is |
|---|---|
| `src/money.py` | The scalar ↔ vector money continuum (convertibility λ, carryover, per-capita issuance) |
| `src/climate.py` | Static and shifting (climate-change) environments: logistic stocks, drift, shocks |
| `src/economy.py` | The experiment economy: households, lagged institutions, hard budget constraints |
| `src/policies.py` | Four decision substrates: rules, Q-learning, Claude LLM agents, humans |
| `experiments/` | Matrix runner, configs, figures, and the human-experiment package (protocol, instructions, browser game) |
| `docs/thesis.md` | The research thesis: lineage, formal definition, hypotheses H1–H5, honest critiques |
| `proposals/` | Grant proposals and funding strategy (Cooperative AI Foundation, Anthropic, Foresight, Hewlett, Laudes, DEAL/P4NE) |
| `site/` | The project website (static, GitHub-Pages-ready) |
| `figures/` | Publication figures, regenerable from scratch |

The original Mesa scaffold (DoughnutABM, baseline world model, market module) is retained and tested; the experiment layer above is purpose-built for the scalar-vs-vector comparison.

## Get involved

The fastest way to improve this work is to try to break it. We are looking for **adversarial replications**, **a university partner** for the powered human study (and eligibility-gated grants), **economists** who think the critiques win, and **funders** who think the hypotheses are worth answering.

Contact: jean@hylaean.com · License: [GPLv3](LICENSE)
