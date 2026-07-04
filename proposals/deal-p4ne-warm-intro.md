---
Funder: Doughnut Economics Action Lab (DEAL) → pathway to Partners for a New
  Economy (P4NE) / KR Foundation via warm introduction
Program: #Research-for-Action network / Global Donut Days / (eventual)
  P4NE invitation-only grantmaking
Ask amount: $0 (this document; no funds requested at this stage)
Duration: N/A for the DEAL outreach; pathway memo spans Aug 2026 – Q1 2027
Date: 2026-07-04
Status: DRAFT — before sending, verify against DEAL's own site: Rob's actual
  name/email/role at DEAL, Tom Foster's name/affiliation, and the exact
  seminar title/date; do not send with any of these unconfirmed
---

# DEAL / P4NE outreach package

This document contains three deliverables for building a relationship with
the Doughnut Economics Action Lab (DEAL) community, with an eye toward an
eventual warm introduction to Partners for a New Economy (P4NE) and the KR
Foundation. No funding is requested from DEAL in either piece of
correspondence below — DEAL is not a grantmaker for this project, it is the
network through which a P4NE/KR introduction becomes possible.

---

## 1. Introduction email to DEAL's community lead

**To:** rob@doughnuteconomics.org
**Subject:** Vector money — simulation results relevant to the 27 May seminar

Hi Rob,

I'm Jean Llorca, an independent researcher based in Switzerland (day job in
pharma logistics engineering, research on the side). I caught the recording
of Tom Foster's 27 May seminar, "Rethinking Money for a Doughnut Economy,"
and wanted to get in touch because I've spent the last several months
building and running exactly the kind of instrument he was gesturing at:
money whose balance is a vector, not a scalar — ordinary cash plus
non-fungible tokens issued one-to-one against biophysical stocks (carbon,
freshwater, biomass, minerals), at their estimated sustainable yield.

The core motivation is a gap Raworth names directly: the doughnut has no
money in it. Prices allocate within limits but don't discover the limits,
and every real climate policy instrument (carbon taxes, ETS) uses at most
one or two scalar levers on a system with nine planetary boundaries. Vector
money is a testable alternative, not an advocacy position — I built an
open-source agent-based simulation (Python/Mesa, GPLv3) where the same
economy is played by rule-based agents, reinforcement learners, LLM agents,
and (soon) humans, in both stationary and climate-shifting environments,
across a convertibility parameter λ that lets scalar and vector money sit on
one continuum.

First results, reported honestly including where vector money loses: in a
stationary world scalar money delivers ~60% more welfare at zero ecological
overshoot (0.84 vs 0.52) — prices win when the world holds still. In a
shifting-climate world, scalar money's stocks collapse (cumulative overshoot
60.0, welfare 0.62) while vector money bends but recovers (overshoot 29.8,
welfare 0.46) and cuts inequality of essential consumption by roughly 5x
(Gini 0.01 vs 0.05–0.10). Everything is reproducible in three commands.

I'd like to ask for two things, neither financial: could the project be
registered on DEAL's community platform, and would there be interest in a
15–20 minute presentation of these results at a #Research-for-Action seminar
or at Global Donut Days (20–24 October)? I think it pairs well with both
Tom's seminar and the Doughnut Price Index work.

Happy to send the repo (github.com/Hylaean/Vector.Money.Sim) and the full
write-up ahead of any conversation.

Best,
Jean Llorca
jean@hylaean.com

(~350 words)

---

## 2. Follow-up note to Tom Foster (EcoProsper Consulting)

**Subject:** Following up on your 27 May DEAL seminar — a simulation of the mechanism

Hi Tom,

I watched your "Rethinking Money for a Doughnut Economy" seminar for DEAL and
wanted to reach out directly, since what I've been building looks like an
empirical test of the territory you were mapping.

I run an open-source agent-based simulation (Python/Mesa, GPLv3) of a
currency whose balance is a vector rather than a scalar: cash plus
non-fungible tokens issued per capita at the sustainable yield of each of
four biophysical stocks (carbon, water, biomass, minerals), with a single
convertibility parameter λ that lets you dial continuously between pure
vector money (λ=0) and ordinary scalar money (λ=1). The same economy — same
observations, same budget constraint — is played by rule-based agents,
Q-learners, Claude-based LLM agents, and (in a protocol now drafted for
Prolific/oTree) human participants, in both a stationary world and a world
with drifting regeneration (toward a floor of 45% of nominal) and rising
shock frequency (capped at 15%/period) meant to stand in for climate drift.

The headline result, reported with the losses included: scalar money wins
comfortably when the world is stationary (0.84 vs 0.52 welfare, both zero
overshoot) but collapses the underlying stocks under drift (overshoot 60.0,
near-boundary minimum) while vector money survives the same drift (overshoot
29.8) at a much smaller welfare cost (0.46 vs 0.62) and roughly a fifth the
inequality in essential consumption. I've tried to build in the standard
critiques — Hayek's information problem, Friedman's black-market argument,
lab evidence that added monetary complexity can backfire on humans even when
theory says it shouldn't — as things the simulation measures rather than
argues past.

I'd value 30 minutes of your time to hear how this lands against the
frameworks you were presenting, and whether there's a natural connection to
the Doughnut Price Index work. I'm also offering to present the results at a
future #Research-for-Action seminar, pending Rob's read on fit.

Repo: github.com/Hylaean/Vector.Money.Sim. Thanks for the seminar — it's
rare to see the "no money in the doughnut" gap named that plainly.

Best,
Jean Llorca
jean@hylaean.com

(~300 words)

---

## 3. Pathway memo: DEAL → P4NE/KR relationship strategy

**Purpose.** Partners for a New Economy (P4NE) and the KR Foundation do not
accept unsolicited applications; both fund by invitation, largely through
warm introductions from trusted intermediaries. DEAL is P4NE's flagship
grantee and the most credible intermediary this project has a plausible path
to. This memo documents the strategy and sequencing — it is not itself a
funding request.

**Strategy: earn the introduction, don't ask for it.**

1. **Register (Aug–Sep 2026).** List Vector Money Simulation on DEAL's
   community platform under #Research-for-Action, with the repo, the thesis
   document, and the honest results table (including the static-world loss).
   No ask attached. This is a low-friction, reversible first step that puts
   the work in front of the network DEAL already curates for P4NE.
2. **Present (Oct 2026 target).** Deliver the seminar offered in the emails
   above — either a standalone #Research-for-Action session or a slot at
   Global Donut Days (20–24 Oct 2026). Goal: substantive engagement from
   DEAL staff and network members with the actual results and the critique
   section (Hayek, Friedman, complexity-backfire, mental accounting), not
   just the pitch. A seminar that survives hard questions from
   doughnut-literate economists is worth more, credibility-wise, than any
   pitch deck.
3. **Contribute (Oct 2026 – Q4 2026/Q1 2027).** Look for ways to be useful to
   DEAL's own agenda before asking for anything — e.g. offering the
   simulation as a teaching or illustrative tool for the Doughnut Price Index
   work, commenting on related #Research-for-Action projects, or a short
   co-authored note connecting the vector-money continuum to Raworth's
   framing gap. The aim is to become a known, useful node in the network,
   not a name that shows up once with a hand out.
4. **Only then, ask DEAL staff for a P4NE conversation (Q1 2027 earliest).**
   Once steps 1–3 have produced a real relationship — not before — ask a
   DEAL staff member directly (most plausibly Rob, or whoever owns the
   #Research-for-Action portfolio by then) whether an introduction to P4NE
   or KR Foundation program staff would be appropriate, and let them make
   that judgment. This is their capital to spend, not mine to demand.

**Timeline.**

| Date | Milestone |
|---|---|
| Aug 2026 | Registered on DEAL platform |
| Sep–Oct 2026 | Seminar delivered (Research-for-Action or Global Donut Days) |
| Oct 2026–Dec 2026 | Substantive contribution to the DEAL network (co-note, teaching use, cross-reference) |
| Jan–Mar 2027 | Ask DEAL staff, not P4NE directly, whether an introduction is warranted |

**Honest caveat, stated plainly.** P4NE makes roughly 15 grants per year and
most of those are renewals to existing grantees, not new awards. The realistic
base rate for a first-time, independent-researcher project reaching a P4NE
grant via this pathway within a year is low. The value of this sequence is
not "guaranteed funding by Q1 2027" — it is that DEAL registration,
presentation, and network contribution are worthwhile on their own terms
(visibility, critique from a knowledgeable audience, possible collaborators
and a university/fiscal-sponsor partner for the human-subject arm), and a
P4NE introduction is a possible, not expected, downstream outcome that should
only be requested once the relationship has earned it.
