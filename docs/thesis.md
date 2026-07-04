# Vector Money — Research Thesis

*Jean Llorca (Hylaean) · July 2026 · living document, v1.0*
*Code, experiments and data: [github.com/Hylaean/Vector.Money.Sim](https://github.com/Hylaean/Vector.Money.Sim) (GPLv3)*

## The claim, in one paragraph

Money is society's most powerful information system, and it has exactly one dimension. Every ecological fact the economy needs to act on — a shrinking carbon budget, a depleted aquifer, a collapsing fishery — must be compressed into that single scalar (a price) before anyone's budget constraint feels it. Compression loses information, and it loses it *slowest exactly when speed matters most*: when the environment itself is changing. **Vector money** is the proposal that money should carry ecological information natively: a currency whose balance is a vector — ordinary cash plus non-fungible components tied one-to-one to biophysical stocks (carbon, freshwater, biomass, minerals) — issued each period at the estimated sustainable yield of each stock. This project does not advocate vector money; it *tests* it, in open agent-based simulations and controlled experiments where the same economy is played by rule-based agents, reinforcement learners, LLM agents, and human participants, in both stationary worlds and worlds with a shifting climate.

## 1. What scalar money aggregates away

Three literatures converge on the same diagnosis from different directions:

- **Integrated assessment critique.** Pindyck (2013) and Keen (2021) showed that the scalar "damage function" at the heart of DICE-style climate-economy models is epistemically fragile: collapsing multi-dimensional, threshold-ridden Earth-system dynamics into one smooth number produces policy conclusions that are artifacts of the aggregation. Our claim is that *the same critique applies to money itself*. A price is a damage function that clears markets.
- **Ecological economics.** Daly (1977) argued that the *scale* of physical throughput must be set before prices can allocate efficiently — prices allocate well within limits but do not discover the limits themselves. Raworth (2017) gave the goal a shape — social floors, ecological ceilings — but Doughnut Economics supplies no monetary instrument. The doughnut has no money in it.
- **Mechanism design.** Weitzman (1974) proved that whether prices or quantities are the better instrument depends on the structure of uncertainty: when the marginal-damage curve is steep — thresholds, tipping points — quantities dominate. Every real implementation of that insight (EU ETS, carbon taxes, the Roberts–Spence hybrids) deploys at most *two scalar levers on one resource*. Nine planetary boundaries, six already transgressed (Richardson et al., 2023), are being steered with, at best, one thermostat.

Vector money is the natural composition of these three points: if aggregation is the failure mode, disaggregate the budget constraint. If scale must precede allocation, issue the scale as currency. If quantities dominate under threshold uncertainty, make quantities the medium of exchange for the dimensions that have thresholds.

## 2. The proposal, precisely

An agent's wallet is a vector **b** = (cash, b₁, …, b_k), one token dimension per biophysical stock. A good with resource footprint **f** costs (p·q) cash *and* **f** tokens. Tokens are:

1. **Issued per capita, per period**, at the issuing institution's estimate of each stock's sustainable yield (a cap-and-share rule);
2. **Non-fungible by degree.** A single parameter λ ∈ [0, 1] sets convertibility: missing tokens can be covered by cash at an effective premium of 1/λ. λ = 0 is pure vector money (tokens strictly binding); λ = 1 collapses to ordinary scalar money (footprints are just prices). *Scalar and vector money are endpoints of one continuum, which makes the comparison an experiment rather than an ideology.*
3. **Demurring.** A carryover fraction δ < 1 prevents unbounded hoarding while permitting smoothing.

Special cases recover familiar proposals: k = 1 with tradable tokens is personal carbon trading (Fawcett, 2010); k = 1 issued as a reward is the Global Carbon Reward "carbon coin" (Chen et al., 2017); λ = 0 with two dimensions is WWII points rationing, which ran a modern industrial economy on a dual currency (price + points) at national scale for four years — the historical existence proof. Vector money generalizes all of these to k stocks at the retail budget constraint.

### Lineage and nearest prior art

| Cluster | Key work | What it has | What it lacks |
|---|---|---|---|
| Special-purpose money | Polanyi (1957), Bohannan (1955), Zelizer (1994) | Proof that non-fungible, sphere-bound money structures real economies | No ecological indexing, no formal mechanism |
| Rationing in practice | US OPA points rationing (1942–45) | National-scale dual currency | Wartime command context; single-crisis, not steady-state |
| Carbon currencies | PCT/TEQs (Fawcett), carbon coin (Chen et al.) | Personal allowance / reward pegged to one stock | One dimension; carbon-only |
| Complementary currencies | Lietaer (2001); critique: Larue (2020) | Diversity-for-resilience thesis | Empirically thin; not biophysically indexed; not agent-based |
| Ecological macro ABM/SFC | DSK (Lamperti et al., 2018), LowGrow SFC (Jackson & Victor), EURACE, LAGOM | Rigorous climate-economy simulation | Money stays scalar; ecology enters as damage function or side constraint |
| RL economics | AI Economist (Zheng et al., 2022), RICE-N (Zhang et al., 2022) | Two-level MARL policy design, climate module | Sustainability as scalar penalty; no monetary structure |
| LLM-agent economics | Homo Silicus (Horton, 2023), EconAgent, GovSim (Piatti et al., 2024) | LLM agents in markets and commons games | Money absent or fixed scalar backdrop; no monetary treatment |
| ReFi / tokenization | Regen Network, KlimaDAO, Toucan | Real MRV infrastructure for ecological claims | Single-stock or aggregated-scalar credits; no behavioral simulation |
| Formal multi-dim money | "Money as a Tensor" (Pinheiro & Pinheiro, 2025) | Multidimensional representation of money | Dimensions are sectoral/temporal, not biophysical; no simulation, no experiments |

To our knowledge, based on a review of the clusters above, **no existing work makes the medium of exchange itself multi-dimensional with components tied to distinct biophysical stocks, and tests it behaviorally.** That conjunction is this project.

## 3. What would make this wrong

A research program is only as credible as the critiques it invites. Four are serious, and each is a testable prediction *against* vector money:

1. **Estimator-lag cost, in the spirit of Hayek's information argument** (1945). Hayek's actual claim is stronger than anything our engine tests: dispersed, tacit, time-and-place-specific knowledge cannot in principle be aggregated by *any* central estimator, however timely — prices work because they need no such aggregation. Our simulations model a narrower, tractable cousin of that problem: the issuer observes stocks with a lag and no drift correction, a purely *forecasting* deficiency rather than a knowledge-aggregation one. *Prediction: vector money underperforms wherever the issuer's estimator is worse than the market's implicit one.* We give the issuer a lagged, drift-blind estimator on purpose — the institution is honestly stupid — and measure how much that costs. A faster or better-informed central estimator would erase this cost in our model; it would not, on Hayek's account, solve the actual dispersed-knowledge problem. Testing that stronger claim would require an issuance design that is itself decentralized, which is not yet in this engine.
2. **Friedman's black-market argument** (1946–). Rationing plus prices breeds arbitrage, favoritism, and queueing. The λ continuum operationalizes this: λ > 0 is a *legal* black market with a measurable premium. We can ask what enforcement level (effective λ) the ecological benefit survives.
3. **Complexity backfire** (Camera, 2024; on personal carbon trading specifically, Fawcett, 2010). In the lab, added monetary dimensionality can degrade welfare even when theory says it shouldn't — humans mis-budget across dimensions. This is the strongest argument for our human-subject arm: if vector money only works for rule-following software, that is a decisive finding.
4. **Mental accounting as bias** (Thaler, 1999). Behavioral economics treats non-fungibility as an error to debias. Vector money takes the opposite normative stance: engineered non-fungibility as institutional design. The disagreement is empirical — does enforced earmarking help or hurt when the constraint is real?

We also note Larue's (2020) critique of currency-plurality proposals: vague issuance rules and unexamined transaction costs. The λ premium formalizes one channel of that critique — price arbitrage in the black market — concretely enough to measure; enforcement, queueing, and favoritism costs remain unmodeled. The simulation exists to make every rule it does encode concrete enough to criticize.

## 4. The engine, and first results

The open-source engine (Python/Mesa, GPLv3) implements: four logistic-regeneration stocks with ecological boundaries; households earning heterogeneous wages who choose a consumption level (0–3) and an efficiency investment each period; an issuing institution that observes stocks with a lag; and the money continuum above. Two environments differ in exactly one respect — the world's stationarity:

- **Static:** constant regeneration; the textbook world where prices have time to learn.
- **Shifting:** regeneration decays ~0.4 %/period toward a plateau at 45 % of nominal, and acute shocks (15 % of a stock, water/biomass) arrive with rising frequency, capped at 0.15/period — a stylized climate trajectory that settles into a permanently harsher regime rather than deterministically killing the world (without the plateau, every institution collapses at long horizons and the comparison loses discriminating power). Any institution estimating yields from the past is systematically optimistic during the transition, whether it sets prices or quantities. The question is which error is cheaper.

First results (12 seeds × 200 periods, rule-based agents; reproduce with `python -m experiments.run_matrix`):

| Condition | Welfare (mean ± sd) | Cumulative overshoot | Satisfaction Gini |
|---|---|---|---|
| Scalar × static | **0.84 ± 0.03** | 0.0 | 0.10 |
| Scalar × shifting | 0.62 ± 0.06 | **60.0 ± 18.1** | 0.05 |
| Vector × static | 0.52 ± 0.10 | 0.0 | **0.01** |
| Vector × shifting | 0.46 ± 0.09 | **29.8 ± 9.6** | **0.01** |

Four honest readings, reported with n = 12 seeds and stated with the caveats that scale implies. (i) *In a stationary world, scalar money wins*: welfare is 0.84 ± 0.03 versus 0.52 ± 0.10, roughly 60 % higher on the point estimate, at zero overshoot for both regimes, while naive sustainable-yield issuance over-conserves. With sample sds this size the exact ratio should be read as "substantially higher," not a precise multiplier. (ii) *In the shifting world, vector money's cumulative overshoot is roughly half scalar's* (29.8 ± 9.6 vs 60.0 ± 18.1 — the two intervals barely fail to overlap at one sd, so we treat this as a directional, not a precisely quantified, effect) at a welfare cost of roughly 0.16 on the point estimate — and the trajectories differ in kind, not just degree: the shocked stocks recover above their boundary under vector money (water: dips to ~29, returns to ~43 of a boundary of 40) and never recover under scalar money (drains to ~7 and stays). (iii) *Vector money is strongly egalitarian in essentials* (Gini ≈ 0.01 vs 0.05–0.10): per-capita issuance equalizes access to ecologically constrained consumption even with unequal wages. (iv) *The convertibility escape hatch leaks substantially*: sweeping λ over the grid {0, 0.25, 0.5, 0.75, 1.0} shows overshoot protection collapsing somewhere between λ = 0 (overshoot ≈ 31.7) and λ = 0.25 (overshoot ≈ 61–63, statistically indistinguishable from scalar's 60) in the shifting world — Friedman's black-market critique, quantified, though the grid is too coarse to locate the threshold more precisely than "before 25 %" — while in the static world *interior* λ (0.25–0.75) actually beats both endpoints on welfare (0.90–0.91 vs 0.84 scalar), because partial conversion premia act as better congestion prices than the lagged price rule. None of these numbers is a forecast; they are the behavior of one transparent model, published so it can be attacked. The interesting science is in the design space they open: issuance headroom, carryover δ, convertibility λ, finer-grained λ sweeps near zero, and issuance rules smarter than lag-3 estimation.

## 5. Four substrates, one game

Every result above must survive a change of *who is playing*. The same economy — same observation, same action space, same budget rules — is played by:

1. **Rule-based agents** — transparent satisficers (the baseline, and the falsifiable null);
2. **Reinforcement learners** — tabular Q-learning now, MARL later; precedent: AI Economist, RICE-N, with the known caveat that institutional non-stationarity destabilizes training;
3. **LLM agents** — Claude models choosing actions via structured output, with the methodological cautions of the generative-ABM validation literature built in (prompt-sensitivity sweeps, contamination checks, cross-model replication; precedents: Homo Silicus, EconAgent, and especially GovSim, where LLM agents managing a commons mostly failed to sustain it *absent* any monetary institution);
4. **Humans** — a browser experiment (one participant among 19 rule-based households, 2×2 between-subject, neutral framing: tokens are "stamps," resources are "materials") scaling to a powered oTree/Prolific study. Precedents: Duffy–Ochs money-emergence, Camera–Casari dual currencies, Ostrom CPR experiments, and the Milinski collective-risk climate game.

The substrate comparison is not decoration; it is the epistemology. If an institutional result holds only for the substrate it was tuned on, it is an artifact. If it holds across rules, learners, language models, and people, it is a candidate institutional fact. And the comparison runs both ways: economies of LLM agents are about to be real economic actors, and *no one knows which monetary institutions keep populations of AI agents inside physical limits*. Vector money experiments are cooperative-AI experiments.

## 6. Hypotheses

- **H1 (ceiling):** Vector money (λ→0) yields no more cumulative overshoot than scalar money in a static environment, and strictly less in a shifting one.
- **H2 (non-stationarity, the crux):** The overshoot advantage of vector money is larger, and its welfare cost smaller, in the shifting environment than in the static one — quantities beat prices precisely when the world moves faster than prices learn (Weitzman, dynamized). We have not yet tested whether this advantage scales monotonically with drift/shock intensity; the current design compares two discrete environments, not a graded dose-response sweep.
- **H3 (equality):** Per-capita issuance reduces inequality of essential consumption relative to scalar money, independent of wage inequality.
- **H4 (substrate):** Effect sizes differ by substrate in an informative order — largest for rule agents, degraded for humans (complexity backfire), with LLM agents in between and diagnostic of both.
- **H5 (design space):** There exist (λ, δ, headroom) settings that recover most of scalar money's static-world welfare while retaining most of vector money's shifting-world robustness — i.e., the continuum has an interesting interior.

Each is falsifiable in the current engine; H1–H3 already have preliminary support or refutation surfaces (Section 4); H4 is the human/LLM program. Note that the static-environment half of H1 is a tie by construction, not a demonstrated advantage: overshoot is exactly 0.0 for both scalar and vector money in the static world because no shocks or scarcity events occur there at all — the environment never puts overshoot protection to the test. The informative comparison is entirely in the shifting world, where vector money's overshoot (29.8 ± 9.6) is roughly half scalar's (60.0 ± 18.1). H5 already has a first, partial *refutation*: the λ sweep (Section 4) finds an interesting interior for welfare in static worlds but shows the shifting-world robustness collapsing somewhere between λ = 0 and λ = 0.25 — if a welfare-robustness compromise exists, it is not on the convertibility axis alone. The open candidates are carryover, headroom, and smarter issuance rules.

## 7. Roadmap

| Phase | Deliverable | Status |
|---|---|---|
| 1 | Open engine: money continuum, environments, 2×2 matrix, figures | **done** (this repository) |
| 2 | Substrate experiments: RL, LLM (Claude), pilot human sessions in browser | engine done; runs beginning |
| 3 | Preregistered human study (oTree, Prolific, n ≈ 32–45/cell), LLM robustness battery (multi-model, prompt sweeps) | protocol drafted; needs funding |
| 4 | Design-space paper: issuance rules, λ/δ frontier; SFC-consistency check of the vector ledger | planned |
| 5 | Policy translation: national-scale calibration from planetary-boundary downscaling (O'Neill et al., 2018) | aspirational |

**Get involved.** Everything is GPLv3 and reproducible (`pip install -e . && pytest && python -m experiments.run_matrix`). We are looking for: adversarial replications, a university partner for the human study and eligibility-gated grants, economists who think Section 3 wins, and funders who think Section 6 is worth answering. Contact: jean@hylaean.com.

---

### Key references

Bohannan (1955) *Am. Anthropologist*; Camera (2024) *lab evidence on digital monies*; Chen, van der Beek & Cloud (2017) *J. Sustainable Finance & Investment*; Daly (1977) *Steady-State Economics*; Duffy & Ochs (1999) *AER*; Fawcett (2010) *Energy Policy*; Friedman & Stigler (1946) *Roofs or Ceilings?*; Hayek (1945) *AER*; Horton (2023) NBER 31122; Jackson & Victor (2019) *LowGrow SFC*; Keen (2021) *Economics of Disasters and Climate Change*; Lamperti et al. (2018) *DSK*; Larue (2020) *Ecological Economics* 178; Lietaer (2001) *The Future of Money*; Milinski et al. (2008) *PNAS*; O'Neill et al. (2018) *Nature Sustainability*; Ostrom, Gardner & Walker (1994); Piatti et al. (2024) *GovSim*, NeurIPS; Pindyck (2013) *JEL*; Pinheiro & Pinheiro (2025) arXiv:2504.06286; Polanyi (1957); Raworth (2017) *Doughnut Economics*; Richardson et al. (2023) *Science Advances*; Thaler (1999) *J. Behavioral Decision Making*; Weitzman (1974) *REStud*; Zelizer (1994) *The Social Meaning of Money*; Zheng et al. (2022) *Science Advances*; Zhang et al. (2022) *RICE-N*, arXiv:2208.07004.
