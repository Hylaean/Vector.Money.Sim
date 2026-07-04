---
Funder: Laudes Foundation
Programme: Partnership Programme — Capital and Finance Markets
Ask amount: €90,000
Duration: 12 months
Date: 2026-07-04
Status: DRAFT
Contact: Jean Llorca — jean@hylaean.com
---

# Money that carries ecological information — initial contact

## Form-ready abstract (150 words max)

Ordinary money carries one piece of information — a price — and no ecological
information at all. We've built and open-sourced a working simulation
(Python, GPLv3) that tests an alternative: **vector money**, where a
household's balance is cash *plus* separate, partly non-convertible tokens
tied one-to-one to a physical stock (carbon, water, biomass, minerals),
issued each period at that stock's estimated sustainable yield. Across
12-seed runs, vector money survives our simulated climate shift where scalar
money's price signal collapses the underlying stocks — at a real welfare
cost we report honestly. We are seeking €90,000 over 12 months to: harden
the simulation and run a multi-model robustness battery; run the first
human-subject pilot (browser-based, Prolific); and co-develop a
practitioner-facing design brief with new-economy organisations, channelled
through the DEAL community. Everything is public and reproducible.

## Why we're writing to Laudes

Your Capital and Finance Markets programme asks what it would take to
redesign finance so that it serves ecological ends rather than treating them
as an externality to be priced in after the fact. Our project takes that
question literally, at the level of the monetary instrument itself. We are
not proposing a new fund, a green bond, or a disclosure standard — we are
testing, in code and then with real people, whether money itself needs a
second dimension to do what a single price cannot: carry a hard ecological
constraint through every transaction, not just a discount on one.

## What exists today

The core claim: a price is a single number that a resource stock's condition
has to be squeezed through before anyone's spending decision feels it. That
squeeze loses information fastest exactly when it matters most — when the
resource itself is changing quickly, e.g. under climate stress. Vector money
is the proposed fix: issue non-fungible ecological "tokens" per person per
period, pegged to what each stock can sustainably regenerate, alongside
ordinary cash. A single dial (called λ) lets us slide continuously between
pure scalar money (λ=1) and pure vector money (λ=0), so the comparison is an
experiment, not an ideology.

We have built the simulation and run it. Across 12 random seeds and 200
simulated periods, in a *stable* environment scalar money wins outright —
~60% higher welfare, at no ecological cost, because prices have time to learn
(welfare 0.84 vs. 0.52; zero overshoot either way). But in an environment
with a *drifting, shock-prone climate* — the case that matters — scalar
money's price signal collapses the underlying stocks (cumulative overshoot
60.0, the water stock drains to roughly 7 — about 17-18% of its 40-unit safe
boundary — and never recovers) while vector money bends but recovers (dips
to roughly 29 before recovering above the boundary; overshoot 29.8, welfare
gap narrows to 0.16). Vector money also
equalises access to essentials far more than prices do (Gini 0.01 vs.
0.05–0.10). We report the static-world loss plainly: this is not a proposal
that vector money is free, and we take seriously the standard objections
(Hayek's information problem, Friedman-style black markets, the risk that
extra monetary complexity just confuses people) as things our own results
have to survive, not footnotes.

## What €90,000 over 12 months buys

Three concrete pieces of work, in order:

1. **Engine hardening and a multi-model robustness battery.** The simulation
   already runs rule-based, reinforcement-learning, and Claude-based LLM
   agents through the same economy. We will extend the LLM robustness
   checks across models and prompt variants, tighten the codebase, and
   publish a reproducible results package.
2. **First human pilot.** A browser-based task (protocol already drafted,
   `experiments/human/protocol.md`) puts one real participant inside a
   20-household economy of simulated agents, under scalar or vector money,
   in a stable or shifting environment. This pilot (~140 Prolific
   participants across 4 conditions) is a dry run for a fully powered,
   preregistered study — it tells us whether people even notice the
   difference before we commit to a larger sample.
3. **A practitioner design brief.** Co-developed with new-economy
   practitioner organisations, channelled through the DEAL (Doughnut
   Economics Action Lab) community, translating what the simulation and
   pilot show into concrete design questions for anyone thinking about
   resource allowances, complementary currencies, or cap-and-share
   instruments: what convertibility rate is enforceable, what issuance rule
   is defensible, where does earmarked money help versus confuse people.

## Budget (EUR)

| Item | Amount |
|---|---|
| PI time — ~0.86 FTE, 12 months (engine hardening, analysis, coordination, writing), at an independent-researcher rate of ~$67,500/yr FTE-equivalent (same rate used across our proposals) | 58,000 |
| Human pilot — Prolific participants (n≈140 across 4 cells, reward ≈€5.50/session + platform fee ≈ reward × 1.333) | 1,050 |
| Human pilot — oTree hosting, 12 months (~€55/mo) | 660 |
| Human pilot — commercial IRB/ethics review (no university IRB available) | 1,690 |
| LLM robustness battery — multi-model API costs (full 4×6×150×20 matrix ≈72k calls ≈$300; 10× robustness sweep ≈$3,000) | 3,100 |
| Compute / CI infrastructure | 500 |
| Practitioner design brief — 2 DEAL-network co-design workshops, reviewer honoraria, editing & layout | 14,000 |
| Travel to one in-person DEAL/new-economy convening (Europe) | 2,200 |
| Fiscal sponsorship / administrative overhead (if a partner organisation is engaged) | 2,800 |
| Contingency (~8%) | 6,000 |
| **Total** | **90,000** |

## Who's asking

I'm Jean Llorca, an independent researcher based in Switzerland; my day job
is pharma logistics engineering, and this project runs on evenings, weekends
and a growing open-source contributor base. The ~0.86 FTE PI line above
assumes I reduce or step back from the day job for the funded period rather
than treat this as unpaid nights-and-weekends work on top of full-time
outside employment — flagging that dependency directly rather than leaving
it implicit. I have no university affiliation. If Laudes requires a fiscal sponsor or partner organisation for
grant administration, I will arrange one — happy to discuss options rather
than treat this as a blocker. All code, data and the pre-registered human
protocol are public now, GPLv3, at
[github.com/Hylaean/Vector.Money.Sim](https://github.com/Hylaean/Vector.Money.Sim);
the full thesis with methods, results and limitations is at `docs/thesis.md`
in that repository. I would welcome a short call to see whether this fits
where the Capital and Finance Markets programme is headed this cycle.
