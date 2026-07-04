---
**Funder:** Cooperative AI Foundation (CAIF) — Research Grants, 2026 priority theme:
"Understanding and Evaluating Cooperation-Relevant Capabilities and Propensities"
(priority theme wording to be reverified against the live 2026 call before submission)
**Program stage:** Pre-proposal (stage 1 of 2)
**Ask:** $165,000
**Duration:** 18 months
**Date:** 2026-07-04
**Status:** DRAFT — ready for submission when the 2026 call opens (call status/date
not yet confirmed at time of writing; PI will verify before submitting)
**Applicant:** Jean Llorca (jean@hylaean.com), independent researcher, Switzerland.
No university affiliation; a fiscal sponsor or partner institution can be arranged
if CAIF requires one for grant administration — noted here rather than concealed.
**Repository:** github.com/Hylaean/Vector.Money.Sim (GPLv3, Python/Mesa)

---

## Monetary institutions as cooperation infrastructure for mixed societies

**Problem.** GovSim (Piatti et al., 2024) showed that populations of LLM agents
mostly fail to sustain a shared resource commons *when no institution structures
their access to it* — cooperation collapses even among capable models. But
GovSim's agents interact through language and reputation alone; no work has
tested whether giving agent populations an explicit **monetary institution** —
the mechanism every human commons has used since rationing existed — changes
that outcome, or which design of that institution matters. As populations of
LLM agents begin to transact under real resource constraints (agentic
commerce, multi-agent resource allocation, human–AI mixed markets), the
question of *which monetary rules keep such populations inside a shared
budget* is a cooperation-infrastructure question, not just an economics one.

**What we built.** An open-source agent-based economy (Python/Mesa, GPLv3)
in which households consume from four regenerating resource stocks under one
of two monetary regimes, set by a single convertibility parameter λ ∈ [0,1]:
**scalar money** (λ=1, ordinary prices) or **vector money** (λ=0, per-capita
issued, partly non-fungible quantity tokens — one dimension per stock, in the
lineage of WWII points rationing and personal carbon trading). The same
economy, same observations, same action space, runs under four interchangeable
substrates: rule-based agents, tabular Q-learners, LLM agents (Claude, via
structured output), and human participants in a browser task. This lets us
ask GovSim's question with an institutional variable switched on, and ask
whether an institutional effect measured in software survives contact with
people.

**What we already know.** Twelve-seed, 200-period runs with rule-based
agents give an honest, non-grandiose baseline: in a **stationary** world,
scalar money wins outright (welfare 0.84 vs 0.52, zero overshoot either way —
quantity issuance over-conserves when prices have time to learn). In a
**non-stationary** world (regeneration drifting down ~0.4%/period to a floor
of 45% of nominal, shock probability ramping and capped at 15%/period — a
stylized drift), scalar money's stocks collapse (cumulative overshoot 60.0,
water stock draining to ≈7 and never recovering) while vector money bends but recovers (overshoot
29.8), at a welfare cost that shrinks from a 0.32 gap to a 0.16 gap. Vector
money also compresses inequality of essential consumption sharply (Gini
0.01 vs 0.05–0.10). These are the results of one
transparent, adversarially-checkable model, not a forecast — the scalar-wins
static-world finding is reported because it is true and it is the strongest
argument against overselling vector money.

**What CAIF funding buys.** Three deliverables, each usable independent of
the others:

1. **The vector-money commons game — an open benchmark.** A packaged,
   documented, API-agnostic version of the environment (static +
   drift/shock conditions, scalar/vector/λ-intermediate regimes) that any
   lab can point an agent population at, with the metrics that matter for
   cooperation research already computed: cumulative overshoot, return
   time after a shock, and consumption-equality (Gini). Released with
   baseline scores for rule agents, Q-learners, and one LLM family, so a
   new model's score is comparable on day one.
2. **A cross-model LLM battery.** The current single-model (Claude) result
   scaled to 4–5 model families, with the prompt-sensitivity sweeps and
   contamination checks the generative-ABM literature requires, testing
   H4: does an institutional advantage measured in rule-based agents
   transfer to LLM populations, and does it depend on which model is
   playing — directly extending GovSim's "institutions matter" finding to
   ask *which* institutions, and for whom.
3. **A substrate-comparison paper**, with a pre-registered human pilot
   (browser task, neutral framing, n≈15/cell across the same 2×2 design;
   protocol and OSF pre-registration already drafted) testing whether the
   institutional effect degrades, as behavioral-economics priors on
   mental-accounting complexity would predict, when the agent is a person.

**Indicative timeline.** Months 1–6: benchmark packaging (D1); Months 4–12:
cross-model battery (D2); Months 10–18: substrate-comparison paper and human
pilot (D3).

**Falsification built in.** Hayek's information critique (the issuer's
estimator is deliberately lagged and drift-blind — we measure what that
costs), Friedman's black-market critique (λ>0 is a legal, measurable
arbitrage premium), and the complexity-backfire literature (humans may
mis-budget across dimensions even when software doesn't) are treated as
competing predictions the experiments can refute, not objections to
pre-empt rhetorically.

## Budget — $165,000 / 18 months

| Item | Amount |
|---|---|
| PI time (0.6 FTE × 18 mo, $70k/yr FTE-equivalent independent-researcher rate) | $63,000 |
| Cross-model LLM battery (API compute): 4–5 model families × [4 conditions × 6 seeds × 150 steps × 20 agents ≈ 72k calls ≈ $250–400/model at Haiku-class pricing] + 10× robustness/prompt-sweep battery + 1–2 frontier-tier models at higher per-call cost | $42,000 |
| RL/MARL compute (cloud CPU/GPU for scaling tabular → deep multi-agent Q-learning) | $8,000 |
| Human pilot: Prolific participants (n≈60 pilot sessions, reward ≈ £2.50 base + performance bonus, platform fee = reward × 1.333) + oTree hosting ($60/mo × 18) + commercial IRB minimal-risk review (no university affiliation) | $10,500 |
| Benchmark engineering & packaging (part-time contractor: API wrappers, docs, HF/GitHub release of the commons-game benchmark) | $22,000 |
| Dissemination (Cooperative AI workshop/conference travel, open-access fees, benchmark leaderboard hosting) | $10,500 |
| Contingency / fiscal-sponsor administration buffer | $9,000 |
| **Total** | **$165,000** |

Everything above the pilot line is independently reproducible today:
`pip install -e . && pytest && python -m experiments.run_matrix`. The human
protocol (hypotheses, power calculation, exclusion criteria, OSF template) is
drafted in full at `experiments/human/protocol.md` and needs funding, not
design work, to run.
