---
Funder: Foresight Institute
Program: Grants — decentralized cooperation / mechanism design (individuals eligible)
Ask: $72,000
Duration: 12 months
Deadline: September 30, 2026
Date: 2026-07-04
Status: DRAFT
Applicant: Jean Llorca (independent researcher, Switzerland) — jean@hylaean.com
Repository: github.com/Hylaean/Vector.Money.Sim (GPLv3)
---

# Vector money as a decentralized-cooperation testbed: N quantity instruments, lagged-dumb issuance, fully decentralized allocation

## 1. The mechanism-design question, stated precisely

Weitzman (1974) showed that prices and quantities are not interchangeable
policy instruments: which one dominates depends on the shape of the
uncertainty, and quantities win when the marginal-damage curve is steep —
thresholds, tipping points. Every real deployment of that result gives an
economy **at most two scalar quantity levers on one resource** (a cap-and-trade
scheme, a carbon tax). We build and test the generalization: **N quantity
instruments, one per physical stock a population depends on, issued as the
literal medium of exchange alongside cash** — a wallet is a vector, not a
scalar, and a purchase draws down both cash and the token dimensions tied to
its resource footprint.

That is a mechanism-design object with a specific decentralization structure,
and we want to be exact about what is and is not decentralized in it, because
the honest answer is what makes it interesting rather than a repackaged
central planning proposal:

- **Issuance is centralized and deliberately dumb.** A single institution
  estimates each stock's sustainable yield from a lagged, drift-blind model
  and issues that much currency per capita per period. It does not
  micro-manage who gets what, does not observe individual preferences, and
  does not clear in real time — it sets one number per stock per period and
  stops.
- **Allocation is fully decentralized.** Given their token and cash balances,
  every agent — human or artificial — chooses consumption and investment
  independently, with no central allocator, no real-time coordinator, and no
  communication requirement between agents. The coordination mechanism is the
  budget constraint itself, exactly as under ordinary money.

This is Hayek's (1945) argument taken seriously rather than waved away: prices
aggregate dispersed knowledge that a central issuer must otherwise pay to
acquire, and a lagged sustainable-yield estimate is a strictly worse
information source than the market's implicit one whenever the issuer's model
of the environment is worse than the price mechanism's. Our simulations do not
give the issuer any informational advantage — it is handed a lag-3, no-drift
estimator on purpose, the kind of institution that actually gets built — and
we measure, in welfare and overshoot units, exactly what that combination of
"centralized-but-dumb issuance + fully decentralized allocation" costs and
buys relative to pure price coordination. **The research question this project
answers is: where does that division of labor beat pure price coordination,
and where does Hayek win outright?** Section 4 reports the first honest
answer, including the case where Hayek wins.

The same question is now doubly relevant. Populations of LLM agents are
starting to transact, negotiate, and manage shared resources autonomously
(Zheng et al. 2022; Zhang et al. 2022; Piatti et al. 2024), and **no monetary
institution has been tested for whether it keeps a mixed human/AI population
inside physical limits without a real-time central controller.** This project
runs the identical mechanism across rule-based agents, reinforcement
learners, LLM agents (Claude, structured output), and humans, in both a
stationary and a drifting-climate environment, so that any institutional
result has to survive a change of *who is coordinating*, not just a change of
parameters.

## 2. What exists today (Phase 1, complete, unfunded)

An open-source agent-based engine (Python/Mesa, GPLv3,
github.com/Hylaean/Vector.Money.Sim) implements:

- four logistic-regeneration biophysical stocks (carbon, water, biomass,
  minerals) with hard ecological boundaries;
- households with heterogeneous wages choosing a consumption level (0–3) and
  an efficiency investment each period;
- a money continuum with two knobs: **λ ∈ [0,1]**, convertibility (λ=0 is
  strict vector money, tokens strictly binding; λ=1 collapses to ordinary
  scalar money — footprints are just prices; intermediate λ is a *legal*
  black market with a measurable premium, operationalizing Friedman's
  (1946) rationing critique directly rather than assuming it away), and
  **δ < 1**, a demurrage/carryover rate preventing unbounded hoarding;
- an issuing institution that observes stock health with a lag and sets
  per-capita token issuance from an estimated sustainable yield (cap-and-share);
- two environments differing in exactly one respect — **static** (constant
  regeneration, the textbook world where prices have time to learn) and
  **shifting** (regeneration drifts down ~0.4%/period to a floor of 45% of
  nominal, acute shocks destroy 15% of a stock with rising frequency capped
  at 15%/period — a stylized climate trajectory under
  which any lagged estimator, price-based or quantity-based, is systematically
  wrong, and the question is which error is cheaper).

First results (12 seeds × 200 periods, rule-based agents; reproducible via
`pip install -e . && pytest && python -m experiments.run_matrix`):

| Condition | Welfare (mean) | Cumulative overshoot | Essential-consumption Gini |
|---|---|---|---|
| Scalar × static | **0.84** | 0.0 | 0.10 |
| Scalar × shifting | 0.62 | **60.0 (stock collapse)** | 0.05 |
| Vector × static | 0.52 | 0.0 | **0.01** |
| Vector × shifting | 0.46 | **29.8 (recovers)** | **0.01** |

Reported without euphemism: **in the stationary world, price coordination
wins outright** — ~60% more welfare at zero overshoot, because the naive
issuer over-conserves relative to what prices would allocate. That is a real
cost of vector money and it is not hidden here. In the shifting world, scalar
money's price signal fails to track a moving target and the water stock
drains to roughly 7 units and never recovers (against a boundary of 40,
i.e. collapse), while vector money's stock dips to roughly 29 before
recovering to roughly 43, above the boundary; the vector system bends
but recovers, at a welfare gap that *shrinks* to ~0.16 while the ecological
gap is ~30 points of cumulative boundary violation. Vector money also cuts
inequality of essential consumption by roughly 5–10×, independent of wage
inequality, because per-capita issuance equalizes access to the physically
constrained goods even when cash incomes are unequal. None of these numbers
is a forecast about the real economy — they are the behavior of one
transparent, adversarially attackable model, and the four substrates, the
human study, and the design-space sweep below exist to find out how far that
behavior generalizes and where it breaks.

## 3. Deliverables requested under this grant

**D1 — The λ/δ/headroom design-space map.** Hypothesis H5 in the underlying
thesis is that there exist convertibility (λ), demurrage (δ), and issuance-
headroom settings that recover most of scalar money's static-world welfare
while keeping most of vector money's shifting-world robustness — i.e., the
scalar–vector continuum has a non-trivial interior, not just two poles. A preliminary 8-seed sweep already shows an interior λ
(0.25–0.75) recovering static-world welfare to 0.90–0.91 — beating both pure
regimes (0.84 scalar, 0.52 vector) — but that even 25% convertibility in the
shifting world collapses vector money's overshoot advantage back to scalar
levels (≈61–63 vs. scalar's 60, against λ=0's ≈31.7). D1 scales this pilot
finding and tests its robustness across substrates. This
is a parameter sweep, cheap in compute and expensive in interpretation: for
each (λ, δ, headroom) triple we need the same 2×2 environment battery, across
seeds, with the resulting frontier plotted and the qualitative regimes
(interior-optimum vs. corner-optimum, and where the corner flips between the
two environments) written up as a short design paper. This is the direct,
falsifiable answer to "where does the Hayek trade-off actually sit."

**D2 — The open benchmark.** The engine already runs four substrates against
one game (rule-based, Q-learning, Claude LLM agents via structured output,
humans via browser experiment); this grant funds finishing and hardening it
into a public, versioned benchmark: fixed task specification, scoring
(welfare, Gini, overshoot depth, return time), a leaderboard-style results
table across substrates and (λ, δ) settings, and documented seeds so any
outside party — another lab, another model provider, another mechanism-design
proposal — can plug in a new agent policy or a new issuance rule and get
directly comparable numbers. This is the artifact meant to outlive the grant:
an answer to "test your coordination mechanism against a mixed human/AI
population under a shared physical constraint" that doesn't require standing
up an ABM from scratch.

**D3 — A workshop.** A half-day virtual (or co-located, if a suitable venue
exists in the grant period) workshop presenting the design-space map and the
benchmark to the decentralized-cooperation / mechanism-design community,
structured explicitly as an invitation to attack: 2–3 invited discussants
briefed to argue the Hayek, Friedman, and complexity-backfire critiques
(Section 5) against the results, with the session recorded and the benchmark
opened for external submissions at the same time.

## 4. Substrates and the honest critiques (why this could be wrong)

Every deliverable above is tested against a change of *who is coordinating*,
because an institutional result that only holds for the substrate it was
tuned on is an artifact, not a finding:

1. **Rule-based agents** — transparent satisficers, the baseline (done).
2. **Reinforcement learners** — tabular Q-learning, with the known caveat
   from AI Economist / RICE-N that institutional non-stationarity destabilizes
   training (engine done, runs beginning).
3. **LLM agents** — Claude models choosing actions via structured output,
   with prompt-sensitivity sweeps and cross-model replication built in
   against the generative-ABM validation literature's own warnings, and
   against GovSim's finding that LLM agents managing a commons mostly failed
   to sustain it *absent any monetary institution at all* — this project asks
   whether adding one changes that.
4. **Humans** — a browser experiment (pre-registered protocol drafted, see
   `experiments/human/protocol.md`): one human among 19 rule-based households,
   2×2 between-subjects (money system × environment), neutral framing
   throughout ("stamps," "materials" — no ecological language, to keep the
   money-system comparison uncontaminated by narrative), scaling from an
   n=15/cell pilot to a powered n=45/cell confirmatory study (Mann-Whitney
   primary test, mixed-effects models as a round-level robustness check,
   full pre-registration plan already specified).

This project is funded, not because vector money is expected to win, but
because four critiques against it are serious enough to be worth a real test:

- **Hayek (1945):** as above — the issuer's estimator is deliberately weak,
  and we measure the cost of that weakness directly rather than assume it away.
- **Friedman & Stigler (1946):** rationing plus prices breeds arbitrage and
  favoritism; the λ parameter *is* the black-market premium, made
  measurable rather than moralized.
- **Complexity backfire** (Camera 2024; Starkey & Fawcett on personal carbon
  trading): added monetary dimensionality can degrade welfare in the lab even
  when theory says it shouldn't, because humans mis-budget across dimensions.
  This is the strongest argument for the human-subject arm — if vector money
  only coordinates rule-following software, that is a decisive negative result,
  and this grant is what pays for finding out.
- **Mental accounting as bias** (Thaler 1999): behavioral economics treats
  non-fungibility as an error to debias; this project's normative bet is the
  opposite (engineered non-fungibility as institutional design), and the
  disagreement is empirical, not rhetorical.

Full lineage, nearest prior art (personal carbon trading, the Global Carbon
Reward, WWII points rationing as the historical existence proof for a
national-scale dual currency, complementary-currency critiques), and the
complete hypothesis set (H1–H5) are in `docs/thesis.md`, the living document
this proposal draws from.

## 5. Work plan (12 months)

| Months | Work | Ties to deliverable |
|---|---|---|
| 1–2 | Finalize (λ, δ, headroom) sweep design; extend the RL and LLM substrate harnesses to run the full 2×2 × substrate matrix unattended | D1, D2 |
| 2–4 | Run design-space sweep across seeds and substrates; pilot human study (n=15/cell, 60 sessions) via Prolific; obtain commercial IRB / ethics self-certification | D1, D2 |
| 4–5 | Revise power calculation from pilot data; finalize confirmatory human protocol pre-registration on OSF | D2 |
| 5–8 | Run confirmatory human study (n=45/cell, 180 sessions); run LLM robustness battery (multi-model cross-replication, prompt sweeps) | D2 |
| 8–10 | Analyze design-space frontier; write up D1 as a short paper; finalize public benchmark (fixed task spec, scoring, leaderboard, documentation, seeds) | D1, D2 |
| 10–11 | Open benchmark for external submissions; prepare workshop materials, recruit discussants | D2, D3 |
| 11–12 | Run workshop; publish recording, design-space paper, and updated `docs/thesis.md` reflecting results | D1, D3 |

## 6. Team

Jean Llorca (jean@hylaean.com) is an independent researcher based in
Switzerland with a professional background in pharma logistics engineering
and a strong software engineering background; this project is conducted
outside any university affiliation. The engine, first results, and the
pre-registered human protocol (Sections 2 and 4) already exist as evidence of
capacity to deliver. **No university partner is currently in place.** If a
funder or reviewer requires institutional review through a university ethics
board rather than the commercial-IRB route budgeted below, a partner
institution can be arranged for that purpose specifically — this is stated
plainly rather than left implicit, and would not change the research design,
only the ethics-review channel (see `experiments/human/protocol.md` §9.3 for
both routes as already planned for).

## 7. Budget — $72,000 / 12 months

| Item | Amount | Basis |
|---|---|---|
| PI time | $39,000 | ~60% FTE across 12 months at a $65,000/yr independent-researcher rate ($65k × 0.60); day-job hours absorb the remainder, with heavier PI weeks around matrix runs and the human-study launch |
| LLM API costs | $5,000 | Main 2×2×substrate matrix ≈ 4 conditions × 6 seeds × 150 steps × 20 agents ≈ 72k decisions × $0.003/decision (claude-haiku-4-5) ≈ $250–400; robustness battery (multi-model cross-replication, prompt sweeps) ≈ 10× that ≈ $2,500–4,000; remainder is headroom for retries and any cross-validation calls to a pricier model |
| Human-subjects payments (Prolific) | $1,500 | 240 sessions (60 pilot + 180 confirmatory) plus ~10% buffer for paid-but-excluded sessions (comprehension failures, timeouts still receive the base fee per protocol §4) ≈ 270 sessions × average reward ≈ £3.25 (base £2.50 + expected partial bonus) ≈ $4.13, × 1.333 Prolific service-fee multiplier ≈ $5.50/session |
| oTree/web hosting | $720 | $60/month × 12 months |
| Ethics review | $1,500 | Commercial IRB minimal-risk online-study review track (mid-point of $1,000–2,000 range), pending confirmation of vendor and price at time of study; superseded by a university ethics board at no cost if a partner is arranged |
| Design-space sweep compute | $3,000 | Cloud burst capacity for the extended (λ, δ, headroom) parameter sweep and Q-learning training runs beyond what a laptop comfortably handles |
| Workshop | $8,000 | Virtual-platform costs or modest venue hire, travel for the PI if co-located, honoraria for 2–3 invited discussants, recording and editing |
| Fiscal sponsorship / administrative overhead | $6,000 | Payment processing, accounting, and (if engaged) a fiscal sponsor's standard overhead for an individual grantee without university finance infrastructure |
| Dissemination | $780 | OSF pre-registration and data-hosting fees, workshop-proceedings preparation, minor publication costs |
| Contingency | $6,500 | ~9%, covering exchange-rate movement on GBP participant payments, IRB or hosting cost variance, and unbudgeted replication requests from reviewers |
| **Total** | **$72,000** | |

All code, data, and this proposal are public and versioned in the same
GPLv3 repository; the benchmark (D2) and design-space results (D1) are
released under the same license so any funded or unfunded party can rerun,
attack, or extend them without asking permission.

## 8. Why Foresight

This proposal is explicitly a mechanism-design object, not a monetary-reform
manifesto: it generalizes Weitzman's quantity-instrument result from one
resource and two levers to N resources and a continuum of convertibility, and
it is built to be tested against exactly the failure modes — Hayek's
information cost, Friedman's black markets, lab-observed complexity
backfire — that a mechanism-design audience would raise first. It is also, as
of this year, directly a cooperative-AI question: the same testbed that
compares humans to rule agents also compares LLM agents to both, on the
concrete question of what monetary institution keeps a decentralized,
no-central-real-time-control population of humans and AI agents inside a
shared physical constraint. We are asking for the resources to answer that
question honestly, including the parts of the answer (Section 2's stationary-
world result; the substrates where it might fail) that argue against the
proposal we started with.

## 9. Contact and reproducibility

Jean Llorca — jean@hylaean.com
Repository: github.com/Hylaean/Vector.Money.Sim (GPLv3)
Reproduce first results: `pip install -e . && pytest && python -m experiments.run_matrix`
Full thesis, lineage, and hypothesis set: `docs/thesis.md`
Human-study protocol (pre-registration-ready): `experiments/human/protocol.md`
