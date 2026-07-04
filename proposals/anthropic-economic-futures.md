---
Funder: Anthropic — Economic Futures Program, Research Awards
Program contact: economicfutures@anthropic.com
Applicant: Jean Llorca (independent researcher, Switzerland; jean@hylaean.com)
Ask amount: $45,000 cash + $5,000 Anthropic API credits
Duration: 9 months
Date: 2026-07-04
Status: DRAFT
---

# Which monetary institutions keep economies of Claude agents inside physical limits?

## 1. One-paragraph summary

This project runs a controlled economy — households, a resource-constrained
environment, and an issuing institution — under two monetary regimes (ordinary
scalar money vs. "vector money," a currency whose balance carries per-resource,
partly non-convertible components) in two environments (stationary vs. a
drifting, shock-prone climate), and asks which regime keeps the population
inside physical resource limits, at what welfare cost, and for whom. The engine
already runs with rule-based and reinforcement-learning agents and produces a
clear, honestly mixed result: scalar money wins on welfare in a stationary
world (0.84 vs 0.52) but collapses the resource stocks when the world drifts
(cumulative overshoot 60.0 vs 29.8), while vector money is 5-10x
more egalitarian in essential consumption (Gini 0.01 vs
0.05–0.10). This award funds the piece of the program that is squarely inside
Anthropic's remit: replacing the rule-based and RL populations with populations
of **Claude agents** (claude-haiku-4-5 as the workhorse model, with a
model-scaling arm to Sonnet and Opus) making structured-output economic
decisions, and subjecting that substrate to the robustness checks the
generative-agent-based-modeling literature says are mandatory before anyone
should trust an LLM-economy result: prompt-sensitivity sweeps, persona/role
framing sweeps, and cross-model replication. The output is dual-purpose: (a) a
substantive answer about which institutional designs constrain AI agent
populations to physical/ecological limits, directly on-topic for "AI's
economic impacts," and (b) a validation template — reusable code and a public
dataset — for the wider question of whether LLM-agent economic simulations
say anything that survives basic robustness testing (Homo Silicus, EconAgent,
GovSim all raise this question; none of them answer it with a systematic
robustness battery on a monetary-institution manipulation).

## 2. Why this is an AI-economic-impacts question, not just an economics question

Two literatures are converging on the same practical problem from opposite
directions. Ecological/monetary economics (Daly, Weitzman, Raworth — see
`docs/thesis.md` §1) asks whether a single-dimensional price signal can keep
throughput inside physical limits when the environment is non-stationary.
Separately, the LLM-agent-economics literature (Horton 2023's *Homo Silicus*,
EconAgent, and especially GovSim, Piatti et al. 2024, NeurIPS) has shown that
populations of LLM agents *manage commons resources badly by default* — GovSim
found LLM agents mostly failed to sustain a shared resource absent any
monetary institution at all. No published work asks the obvious next
question: **does changing the monetary institution change that outcome, and
does the answer hold up once you stress-test the prompt, the persona, and the
model?** As populations of LLM agents start making real allocation decisions
in actual digital and physical economies — decentralized-agent marketplaces,
multi-agent commerce, agentic API consumption—the question of which
institutional constraints keep those populations inside real limits (compute
budgets, energy budgets, rate limits, literal physical resource constraints in
robotics/logistics deployments) is a live, near-term AI-economic-impacts
question, not a metaphor. This project treats Claude models simultaneously as
the **object of study** (how do agents built on Claude behave under different
institutional constraints?) and as a **scientific instrument** (structured
output makes their decisions legible and reproducible in a way human subjects
and black-box heuristics are not).

## 3. What is already built (no funding needed for this part)

From `docs/thesis.md` and the repository (github.com/Hylaean/Vector.Money.Sim,
GPLv3, Python/Mesa), reproducible today via
`pip install -e . && pytest && python -m experiments.run_matrix`:

- A working 2×2 engine: scalar vs. vector money (a convertibility parameter
  λ ∈ [0,1] makes them endpoints of one continuum) × static vs. shifting
  (climate-like drift + shocks) environments.
- Four agent substrates already specified in the codebase: rule-based
  (satisficing baseline), tabular Q-learning, Claude LLM agents via
  structured output, and a browser-based human-subject arm
  (`experiments/human/protocol.md`, pre-registration-ready, 2×2
  between-subjects, n=45/cell target, Prolific-costed — funded separately,
  not part of this ask).
- First results, 12 seeds × 200 periods, rule-based agents:

  | Condition | Welfare | Cumulative overshoot | Essential-consumption Gini |
  |---|---|---|---|
  | Scalar × static | 0.84 | 0.0 | 0.10 |
  | Scalar × shifting | 0.62 | 60.0 (stock collapse) | 0.05 |
  | Vector × static | 0.52 | 0.0 | 0.01 |
  | Vector × shifting | 0.46 | 29.8 (recovers) | 0.01 |

  Read honestly: scalar money delivers ~60% more welfare at zero overshoot in
  a stationary world (vector over-conserves against a naive sustainable-yield
  rule); scalar money collapses stocks when the world drifts while vector
  money bends but recovers, at a shrinking welfare cost (~0.16 gap) against a
  large overshoot gap (~30 points); vector money is consistently more
  egalitarian in essential consumption regardless of environment.

This award does not pay to build the engine or re-derive these numbers. It
pays to run the **Claude-agent arm** at the scale and robustness level needed
to trust it, and to compare it against the rule/RL baselines already in hand.

## 4. What this award funds

**(1) Full matrix with Claude-agent populations.** 4 conditions (scalar/vector
× static/shifting) × 6 seeds × 150 steps × 20 agents per economy, Claude
agents choosing consumption level and investment via structured JSON output
each round, prompt-cached system context (institution rules, wallet state) to
control cost. This replicates H1–H3 (overshoot, non-stationarity interaction,
equity) from `docs/thesis.md` §6 on an LLM substrate for the first time.

**(2) Robustness battery**, because a single prompt/persona/model result is
not evidence in the generative-ABM sense (the validation-crisis critique this
proposal takes seriously, per Piatti et al. and the broader "does the LLM
economy replicate under trivial rewording" literature):
- *Prompt-sensitivity sweep*: 5 semantically-equivalent phrasings of the
  task instructions (matching the human protocol's neutral-language
  discipline in `experiments/human/protocol.md` §8) run across the full
  matrix.
- *Persona/role-framing sweep*: 4 persona primings (neutral, "cautious
  household," "profit-maximizing household," "environmentally-minded
  household") run across the full matrix, to characterize how much of any
  institutional effect is persona-contingent rather than institution-driven.
- *Model-scaling arm*: a reduced matrix (2 conditions × 3 seeds) re-run on
  claude-sonnet-4-5 and claude-opus-4-1 to test whether the institutional
  result (H1/H2) is a haiku-specific artifact or holds as capability scales —
  directly relevant to Anthropic's own interest in how model scale changes
  economic reasoning and rule-following.

**(3) Four-substrate comparison.** The Claude-agent results are compared
against the existing rule-based and Q-learning runs (already computed) on the
same metrics (welfare, Gini, overshoot depth, return time), producing
`docs/thesis.md` H4 (substrate ordering: do effect sizes shrink or invert
going from rules → RL → LLM → human?) as an empirical answer rather than a
conjecture. The human-subject leg of H4 is out of scope for this award (it is
costed and pre-registered separately in `experiments/human/protocol.md`); this
award produces the LLM point of comparison that makes that future four-way
comparison possible.

**(4) Public dataset and reproducible harness.** All prompts, structured-output
schemas, raw per-decision logs (not just aggregates), and analysis notebooks
are released under GPLv3/CC-BY alongside a DOI'd dataset (Zenodo/OSF), so the
robustness battery itself — not just this project's conclusions from it — is
reusable as a template for testing any other LLM-agent-economics claim.

## 5. Deliverables and timeline (9 months)

| Month | Deliverable |
|---|---|
| 1–2 | Structured-output schema finalized; prompt-caching harness built; pilot runs (1 seed/condition) for cost and stability validation |
| 3–5 | Full core matrix (4×6×150×20) on claude-haiku-4-5; prompt-sensitivity sweep |
| 5–6 | Persona/role sweep; model-scaling arm (Sonnet, Opus) |
| 7 | Four-substrate comparison analysis (LLM vs. rule vs. RL, existing data) against H1–H4 |
| 8 | Public dataset release (Zenodo DOI), code cleanup, external adversarial-replication pass |
| 9 | Working paper / preprint; submission to a relevant venue (e.g., a cooperative-AI or generative-agents workshop) |

## 6. Budget — $45,000 cash, 9 months

| Line | Basis | Amount |
|---|---|---|
| PI time (0.5 FTE, 9 months) | $65,000/yr independent-researcher FTE rate × 0.5 × 9/12 | $24,375 |
| API costs, cash portion (overruns beyond credits, re-runs, extra seeds) | see §7 for full API estimate; credits cover the bulk | $1,500 |
| Compute & data infrastructure | orchestration VM, log storage, CI minutes, Zenodo/OSF hosting, 9 months | $1,800 |
| Data curation & public dataset release | ~100 hrs contractor @ $30/hr: schema docs, redaction, DOI packaging | $3,000 |
| Independent adversarial-replication honoraria | 2 external reviewers re-run a subset and report discrepancies | $2,500 |
| Dissemination | preprint hosting, one workshop registration + travel/virtual fee | $3,000 |
| Equipment & dev tooling (amortized) | monitor/peripheral refresh, backup storage for logs | $1,325 |
| Contingency (~17%) | schedule slip, API price changes, additional seeds if variance is high | $7,500 |
| **Total cash ask** | | **$45,000** |

**In addition:** $5,000 in Anthropic API credits, applied against the API
costs itemized in §7 below.

## 7. API cost estimate (the reason this is costed, not guessed)

Real measured cost on claude-haiku-4-5 with structured output and prompt
caching: **≈ $0.003 per agent-decision**.

- **Core matrix**: 4 conditions × 6 seeds × 150 steps × 20 agents = 72,000
  decisions × $0.003 ≈ **$216**, budgeted at **$250–400** to allow for retries,
  malformed-output re-asks, and cache misses.
- **Prompt-sensitivity sweep** (5 phrasings × core matrix scope) ≈
  **$1,250–2,000**.
- **Persona/role sweep** (4 personas × core matrix scope) ≈ **$1,000–1,600**.
- **Model-scaling arm**: reduced matrix (2 conditions × 3 seeds × 150 × 20 =
  18,000 decisions) on claude-sonnet-4-5 (~8× haiku per-decision cost) ≈
  **$430**, and claude-opus-4-1 (~30× haiku per-decision cost) ≈ **$1,620**.
- **Estimated total API spend**: **≈ $4,750–6,300** across the full program —
  consistent with the "robustness battery ≈ 10× the core matrix" rule of
  thumb, plus the model-scaling premium for higher-tier models.

The $5,000 Anthropic API credit line is expected to cover essentially all of
this; the $1,500 cash API line above is contingency for a run that needs more
seeds than planned once real variance is observed (the same logic the human
protocol uses for its own pilot-before-confirmatory-scale-up, §5 of
`experiments/human/protocol.md`).

## 8. Institutional status and independence

Jean Llorca is an independent researcher based in Switzerland (day job in
pharma logistics engineering; software background; no university
affiliation). The engine, all experiment code, and this proposal are
developed and released independently under GPLv3. No human-subjects research
is conducted under this award — the LLM-agent track requires no IRB review.
If a fiscal sponsor or institutional host is required for grant
administration, one can be arranged; the applicant flags this proactively
rather than assuming it is unnecessary.

## 9. Honest limitations

- The core institutional result (vector money trades welfare for resilience)
  is established on rule-based agents at 12 seeds; this award's job is to
  find out whether it survives contact with LLM agents, not to assume it
  will. A negative or null result (Claude agents do not reproduce H1/H2, or
  reproduce them only under one persona/prompt framing) is a publishable,
  useful finding and will be reported as such.
- Structured-output LLM agents are not a model of human economic behavior;
  they are a distinct, third substrate whose relationship to human behavior
  is itself an open empirical question (this is why the human-subject arm
  exists, funded separately). Claims from this award are about **LLM-agent**
  behavior under institutional constraints, not human behavior.
- Six seeds per condition in the core matrix (vs. 12 in the existing
  rule-based results) is a cost-driven compromise; the budget's contingency
  line is sized precisely to allow more seeds if early variance is high
  enough to threaten the comparison.
- Prompt-sensitivity and persona sweeps characterize *some* of the surface
  area of LLM sensitivity, not all of it (e.g., they do not test
  cross-lingual framing or adversarial prompt injection); this is scoped
  explicitly as a first robustness pass, not an exhaustive one.

## 10. Contact

Jean Llorca — jean@hylaean.com — github.com/Hylaean/Vector.Money.Sim
