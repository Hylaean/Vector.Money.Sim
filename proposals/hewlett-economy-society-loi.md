**Funder:** William & Flora Hewlett Foundation — Economy and Society Initiative
**Program:** Reimagining the Economy (unsolicited Letter of Inquiry)
**Ask:** $220,000
**Duration:** 24 months
**Date:** 2026-07-04
**Status:** DRAFT — for PI review before submission

---

**To:** Economy and Society Initiative, William & Flora Hewlett Foundation
**From:** Jean Llorca (jean@hylaean.com), independent researcher, Switzerland
**Subject:** Letter of Inquiry — Vector Money: testing whether the fungibility of value is load-bearing

Dear Program Officer,

I am writing to propose a two-year, $220,000 program of simulation and human-subjects research that turns a foundational assumption of market economics — that value is fungible, that a dollar earned anywhere can be spent anywhere — into an experimental variable instead of a philosophical position. I believe this is squarely inside what the Economy and Society Initiative and its partners (including the Hewlett–Omidyar-seeded Reimagining Capitalism field) mean by building the intellectual infrastructure for a new economic common sense: not another critique of markets, but working evidence about the abstraction underneath them.

**The claim.** Most challenges to neoliberal orthodoxy — from Doughnut Economics to degrowth to post-growth macroeconomics — argue about what markets should prioritize while leaving untouched the instrument that does the prioritizing: a single-dimensional currency. A price is a compression of every ecological fact a purchase implies — a shrinking carbon budget, a falling aquifer, a fished-out stock — into one number, and that compression is well understood in mechanism-design terms (Weitzman, 1974) to lose exactly the information that matters most when the underlying system is not stationary. Fungibility of money is not a neutral technical convenience; it is a policy choice with a name (Hayek's price-discovery argument for it, Polanyi's and Zelizer's historical evidence against its universality) that almost no one treats as adjustable. This project adjusts it and measures what happens.

**The instrument.** Working code (Python/Mesa, GPLv3, github.com/Hylaean/Vector.Money.Sim) implements an agent-based economy in which household wallets are vectors — ordinary cash plus non-fungible tokens tied one-to-one to biophysical stocks (carbon, freshwater, biomass, minerals), issued per capita at an institution's estimate of sustainable yield. A single parameter, convertibility λ, makes scalar money and vector money the two endpoints of one continuum (λ=1 is ordinary fungible cash; λ=0 is strict rationing), so "should money be fungible" becomes a dial we can sweep rather than a debate we can only have in the abstract. The nearest historical precedent is not theoretical: WWII-era points rationing ran an industrial economy on exactly this kind of dual currency for four years. We generalize it to multiple ecological stocks and put it in a laboratory.

**What we have found so far**, honestly, including the result that cuts against the thesis. Twelve seeds × 200 periods, rule-based agents, two environments that differ in one respect — whether resource regeneration is stationary or drifting (a stylized climate trajectory with rising shock frequency):

| Condition | Welfare | Cumulative ecological overshoot | Gini (essential consumption) |
|---|---|---|---|
| Scalar money, static world | 0.84 | 0.0 | 0.10 |
| Scalar money, shifting world | 0.62 | 60.0 (stock collapse) | 0.05 |
| Vector money, static world | 0.52 | 0.0 | 0.01 |
| Vector money, shifting world | 0.46 | 29.8 (recovers) | 0.01 |

In a stationary world, scalar money wins outright — ~60% more welfare, at no ecological cost, because prices have time to learn. That is not a footnote we are suppressing; it is the finding that makes the rest credible. In a drifting world, the picture reverses on the dimension that matters: scalar money's water stock drains to roughly 7, well below its own safety boundary of 40 (about 17-18%), and never recovers, while vector money dips to about 29 before recovering above the 40-unit boundary, at a welfare cost that shrinks to about 0.16 — and vector money's essential-consumption inequality is five to ten times lower throughout, regardless of environment. None of this is advocacy; it is the behavior of one transparent, adversarially-poseable model, published so it can be attacked, alongside the four standing critiques (Hayek's information problem, Friedman's black-market argument, lab evidence that added monetary complexity can backfire on real people, and Thaler's mental-accounting objection) that the design has to survive, not just the ones it flatters.

**What we do not yet know, and what this grant buys.** Every simulation result above was produced by rule-following software. The open scientific question — and the reason this is a human-subjects proposal, not just a modeling paper — is whether the same institutional effect survives contact with actual people, who mis-budget, hoard, and satisfice in ways no heuristic captures. A pilot browser experiment and full protocol already exist (neutral framing: tokens are "stamps," resources are "materials," to isolate the monetary mechanism from moral narrative). Phase 3 of the project's five-phase roadmap — the phase this grant funds — is the first *powered*, pre-registered version of that study (2×2 between-subjects, scalar/vector × static/shifting, n=45 analyzable sessions per cell via Prolific, d=0.6, Mann-Whitney primary analysis), run alongside a multi-model LLM robustness battery (because populations of AI economic agents are arriving whether or not any monetary institution is designed to keep them inside physical limits), and written up as a design-space paper mapping the (λ, carryover, issuance-headroom) frontier where most of scalar money's stationary-world welfare can coexist with most of vector money's drift-world survival. That frontier — not a verdict for or against fungible money — is the deliverable a funder should expect: an empirically characterized design space where "should money be fungible" has a quantified answer instead of a rhetorical one.

**Institutional home.** I am an independent researcher (day job in pharma logistics engineering, prior software background) without a current university affiliation, which I raise directly rather than leave for you to discover. I understand ESI generally grants to institutions. Securing a university partner or fiscal sponsor for this grant — someone able to house the funds, provide a named faculty sponsor for the human-subjects ethics review, and co-author the design-space paper — is the first, time-boxed task of the funded period (target: within the first two months), not a hoped-for side effect. If Hewlett can suggest a fiscal sponsor or a partner institution already active in this space, I would welcome the introduction. To be direct about the budget below: the 1.0-FTE-equivalent PI line assumes I reduce or transition off the day job for the funded period rather than run this program as unpaid nights-and-weekends work on top of full-time outside employment — I flag that dependency here rather than let the two documents describing this project imply otherwise.

**Indicative budget ($220,000 / 24 months).** Figures are planning estimates to be finalized with the fiscal sponsor; participant costs are computed from Prolific's own fee schedule, LLM costs from measured per-call usage on the current codebase.

| Item | Amount |
|---|---|
| PI salary (1.0 FTE-equivalent, prorated, ~$67,500/yr — modest independent-researcher rate) | $135,000 |
| Research assistant / data analyst (part-time, data processing, LLM-battery operation) | $18,000 |
| University-partner / fiscal-sponsor search and named faculty-sponsor honorarium (Phase 1) | $8,000 |
| Statistical & pre-registration consulting (one-time review) | $4,000 |
| Prolific participants: 240 sessions (60 pilot + 180 confirmatory), reward ≈ £3.25/session × Prolific's 1.333× service fee | $1,300 |
| oTree hosting, 24 months × $60/mo | $1,440 |
| Commercial IRB / ethics review (absent a university board) | $1,500 |
| LLM robustness battery: multi-model, prompt-sensitivity sweeps, ~10× the base 72k-call matrix at ~$0.003/call | $3,500 |
| Cloud compute, data storage, OSF archiving | $2,500 |
| Dissemination: open-access fees (2 papers), one conference, policy-brief production | $7,000 |
| **Subtotal, direct costs** | **$182,240** |
| Fiscal-sponsor administrative fee (~10% of direct costs) | $18,224 |
| Contingency (~10% of direct costs) | $18,224 (adjusted to close) |
| **Total** | **≈ $220,000** |

**Timeline.** Months 1–2: fiscal sponsor secured, IRB/ethics review filed. Months 2–5: pilot human study (n=15/cell) and LLM robustness battery run in parallel. Months 5–8: revised power calculation, OSF pre-registration of the confirmatory study. Months 8–16: confirmatory data collection (180 sessions). Months 16–22: analysis, design-space parameter sweep, manuscript drafting. Months 22–24: submission of the design-space paper, a public write-up aimed at policy audiences, and a stakeholder workshop scoping Phase 5 (national-scale calibration against planetary-boundary downscaling) as a distinct future proposal.

**Track record and reproducibility.** The engine, both environments, the 2×2 matrix, the pre-registered human protocol, and the full thesis document with cited lineage (Polanyi, Daly, Weitzman, Raworth, Hayek, Friedman, Thaler, and the nearest computational-economics precedents: DSK, AI Economist, RICE-N, GovSim) are public now: `github.com/Hylaean/Vector.Money.Sim` (GPLv3). Anyone can run `pip install -e . && pytest && python -m experiments.run_matrix` and reproduce the table above today.

I would welcome a call to discuss fit with the Initiative's current priorities, and I am glad to send the full thesis document (`docs/thesis.md`) or the pre-registered experimental protocol on request.

Thank you for your consideration.

Sincerely,
Jean Llorca
jean@hylaean.com
