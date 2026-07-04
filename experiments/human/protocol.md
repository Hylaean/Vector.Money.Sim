# Experimental protocol: human decision-making under scalar vs. vector money

Status: draft v1.0, for pre-registration prior to data collection.
Companion files: `instructions.md` (participant-facing text), `web/index.html`
(task implementation), `README.md` (how to run a pilot).

## 1. Background and research questions

`src/economy.py` shows that in an agent-based model, replacing a single
fungible currency ("scalar money") with a multi-dimensional, partly
non-convertible token system ("vector money") changes ecological and
distributional outcomes when rule-based agents make consumption decisions.
The open question this protocol addresses is whether the same qualitative
effects appear when the decision-maker is a human being embedded in the same
economy, facing the same information and the same budget constraint every
round.

This is not a test of "is vector money a good idea" in the abstract. It is a
test of whether a specific institutional design — issuing per-resource,
partially non-tradeable allowances instead of letting price alone ration
scarce resources — measurably changes what a human does with their round-by-
round choices, relative to a rule-based (bot) baseline that has already been
characterised in simulation.

### 1.1 Hypotheses

- **H1 (overshoot).** Sessions run under vector money show lower ecological
  overshoot (depth and duration of stock levels below the safety boundary,
  aggregated across the four material stocks) than sessions run under scalar
  money, holding environment condition fixed.
- **H2 (environment interaction).** The vector-money advantage in H1 is
  larger in the shifting (non-stationary) environment than in the static
  environment. Mechanically: under scalar money, prices are set from a lagged
  health estimate that is *systematically* stale when the environment is
  drifting, so scalar money's error compounds where vector money's physical
  quantity cap does not.
- **H3 (equity of essential consumption).** Vector money reduces the
  dispersion of achieved need satisfaction between the human participant and
  the simulated population (operationalised as |human satisfaction − mean bot
  satisfaction| per round, and as the human's rank in the bot satisfaction
  distribution), relative to scalar money. This mirrors the simulation
  finding that vector money's satisfaction Gini (~0.01) is roughly an order
  of magnitude lower than scalar's (~0.05–0.10).
- **H4 (behavioural divergence from the rule agent).** Humans deviate
  systematically from the `RuleBasedPolicy` heuristic that governs the bots,
  in ways that are money-system-specific:
  - under vector money, humans **hoard** tokens (end-of-session token
    balances above what the carryover mechanism would leave a non-acting
    agent) and/or attempt to **trade down** consumption in early rounds to
    bank tokens for later high-consumption rounds, a strategy the rule
    heuristic cannot express;
  - under scalar money, humans show more **round-to-round consumption
    volatility** than the smooth threshold behaviour of the rule agent,
    consistent with price signals being harder to act on consistently than
    a visible physical quota.
  H4 is exploratory/descriptive rather than a single directional test; the
  pre-registered analysis (Section 7) specifies the exact statistics before
  data collection.

## 2. Design

**2×2 between-subjects factorial.**

| | Static environment | Shifting environment |
|---|---|---|
| **Scalar money** | Cell A | Cell B |
| **Vector money** | Cell C | Cell D |

- Factor 1 — **money system**: `scalar` vs. `vector` (λ = 0, strictly
  non-convertible tokens, `carryover = 0.5`), exactly the parameterisation in
  `EconomyConfig`.
- Factor 2 — **environment**: `static` (stationary regeneration, no shocks)
  vs. `shifting` (regeneration drift 0.004/round toward a floor of 0.45×
  nominal, shock probability 0.02 + 0.002·t capped at 0.15, destroying 15%
  of the water and biomass stocks).
- Each participant is randomly assigned to exactly one cell (between-subjects
  — a participant never learns there are other conditions, which rules out
  demand effects from within-subject comparison).
- Participants are the single human household among 19 simulated
  (`RuleBasedPolicy`, greed = 0) households in a 20-household economy — the
  same population size as the reference simulations. This gives every human
  session a fully reproducible bot population (seeded from the participant
  ID) that lets us situate the human's outcomes relative to the canonical
  12-seed × 200-period simulation-only study reported for the same money ×
  environment cells (`experiments/results/summary.json`) — not a literal
  seed-for-seed slotting, since a 30-round human session is much shorter than
  the 200-period reference runs (see below).
- Session length: 30 rounds (see `EconomyConfig.steps`), a 15% sample of the
  200-period reference simulation runs, chosen for a 12–15 minute session;
  power to detect cross-cell differences is addressed via aggregation across
  many *sessions*, not via long single sessions.
- Randomisation: assignment to cell is done by the recruiting platform
  (Prolific study allocation, or a simple hash of participant ID mod 4 for a
  self-hosted deployment) *before* the participant sees any instructions, and
  is fixed for the session — no adaptive/response-contingent assignment.

## 3. Procedure

1. **Landing / consent.** Participant reads the informed consent text
   (Section 9) and clicks "I agree" before anything else loads.
2. **Instructions.** Neutral-language description of the task (see
   `instructions.md`): materials, stamps, wallet, rounds, rules for
   consumption levels and investing. No mention of climate, ecology, or moral
   framing (see Section 8 on framing as a threat to validity).
3. **Comprehension check.** Four multiple-choice questions administered
   before Round 1 (full text and answer key in `instructions.md`, Section
   "Comprehension check"). A participant who answers fewer than 3 of 4
   correctly is shown the relevant instruction passage again and must retake
   the check once; a second failure ends the session with a screened-out
   payment (Section 6) and the record is flagged `excluded_comprehension`
   pre-registered as an exclusion criterion (Section 7.3), not analysed
   further.
4. **Task.** 30 rounds. Each round: participant sees their wallet, the
   current health of the four materials, and the cash/stamp cost of each
   consumption level (0–3); they choose a consumption level and whether to
   invest, then see one line of feedback ("You gained 0.85 satisfaction
   points this round.") before the next round begins. Median expected
   duration 12–15 minutes based on ~15–20 seconds of decision time per round
   plus reading time; a session hard-stops at 25 minutes regardless of
   progress (partial data retained and flagged `timeout`).
5. **Post-task questionnaire.** Five items: (a) free-text — "What strategy
   did you use to decide how much to consume each round?"; (b) 7-point Likert
   — "How much did you feel your choices affected the shared materials?"; (c)
   7-point Likert — "How fair did the rules feel to you?"; (d) free-text —
   "Was anything about the task confusing?"; (e) demographic items already
   collected by the platform (age band, not additional PII) are *not*
   re-collected — see Section 9 on minimal data collection.
6. **Debrief and payment confirmation.** Explains the true purpose of the
   study (comparing money systems) now that responses cannot be
   contaminated, restates the bonus calculation, and thanks the participant.

## 4. Incentives

- **Base participation fee**: flat, paid regardless of in-task performance,
  set to the platform's minimum wage-equivalent rate. Prolific's guidance
  (2024–2025) is a minimum of £6/hr (US$8/hr) and *recommends* ≥ £9/hr for
  reliable recruitment; we target **£9/hr**. At an estimated 15-minute
  session (comprehension check + 30 rounds + questionnaire, with buffer) this
  is **£2.25**, which we round up to **£2.50** flat fee to absorb the
  occasional slower session without dropping effective pay below the
  recommended rate.
- **Performance bonus**: proportional to the sum of the participant's 30
  round satisfaction scores (max possible = 30 × 1.0 = 30 points). Bonus =
  `£1.50 × (points earned / 30)`, i.e. up to **£1.50** for a maximised-every-
  round session, paid continuously (not a threshold/lottery bonus, which
  would create variance unrelated to the manipulation). Expected total
  session pay is therefore **≈ £2.50–£4.00** (base + realistic bonus range),
  i.e. an effective rate comfortably at or above £9/hr for a 15-minute
  session, satisfying Prolific's fair-payment policy.
- The bonus is calculated identically across all four cells from the same
  satisfaction formula (`SATISFACTION = (0, 0.55, 0.85, 1.0)` scaled by
  physical availability) — the incentive structure itself is not a
  confound between conditions.
- Comprehension-check failures and timeouts still receive the base fee (no
  participant is unpaid for engaging in good faith) but are excluded from
  analysis per Section 7.3.

## 5. Sample size

**Effect size target.** The canonical 12-seed × 200-period simulation
comparisons (`experiments/results/summary.json`) put scalar/shifting
overshoot at 60.0 ± 18.1 (stock-units below boundary, summed) vs.
vector/shifting at 29.8 ± 9.6 — a large relative gap, but with only 12 seeds
the simulation study cannot itself estimate a between-subject standard
deviation for human sessions, and its 200-period runs are more than six times
the length of a 30-round human session. We therefore plan conservatively for
a **medium-to-large effect** (Cohen's d ≈ 0.6), typical of the smallest
effect this design is worth running to detect, rather than assume the full
simulation-scale gap transfers to single-session human behaviour.

**Power calculation.** For a two-independent-sample comparison (e.g.
Cell B vs. Cell D — scalar vs. vector, both in the shifting environment) at
α = .05 (two-tailed) and power = .80, detecting d = 0.6 requires:

```
n per group ≈ 2 × ((z_{α/2} + z_{β}) / d)^2
            = 2 × ((1.96 + 0.84) / 0.6)^2
            = 2 × (4.667)^2
            ≈ 2 × 21.78 ≈ 43.6 → round up to 45
```

**Target n = 45 completed, analysable sessions per cell (180 total)** for the
confirmatory study, using a Mann-Whitney U test (Section 7) rather than a
t-test as the primary test — the power figure above is the standard
parametric approximation used for planning purposes; Mann-Whitney loses at
most ~5% asymptotic relative efficiency versus a t-test under near-normal
data, which the n=45 target already absorbs as margin.

**Pilot.** Before committing to the full 180-session run, a **pilot of
n = 15 per cell (60 total)** is run to (a) confirm comprehension-check pass
rates and completion times are as expected, (b) obtain a real (not assumed)
estimate of the between-session standard deviation of overshoot and welfare
in each cell, feeding a revised power calculation, and (c) surface any UI or
instruction-wording problems before spending the full budget. The pilot data
are **not** pooled into the confirmatory analysis (to avoid inflating Type I
error through optional stopping / multiple looks); if pilot and confirmatory
data are later combined, this will be pre-registered as an update with a
stated combination rule before the confirmatory data are unblinded.

## 6. Recruitment and payment logistics (Prolific-oriented)

- Platform: Prolific, prescreened for fluent English, desktop or laptop
  device (the task's precision buttons and reading are impractical on small
  mobile screens; screen out mobile via Prolific's device filter), and
  completion of at least one prior study (basic attention-check
  qualification) to reduce bot/inattentive submissions.
  the platform's screening filters are set once for the whole study, not
  varied by cell, so they cannot create a cell-specific selection effect.
- Balanced cell assignment: create 4 Prolific "studies" (or one study with
  the self-hosted page allocating condition by hashed participant ID) so
  that recruitment is balanced without adaptive assignment based on prior
  responses.
- Study listing states the flat fee and a truthful, non-deceptive summary
  ("You will play 30 rounds of a resource-allocation game as one of 20
  simulated households; pay is a flat fee plus a bonus based on your
  in-game score") consistent with Section 9 (no deception).

## 7. Pre-registration plan (OSF-template outline)

To be registered on OSF (or AsPredicted for a shorter form) before any
confirmatory data are collected. Structure below follows the OSF
"Preregistration Template" section headings.

### 7.1 Hypotheses
H1–H4 as stated in Section 1.1, each stated as a directional prediction
(H1–H3) or a pre-specified descriptive comparison (H4).

### 7.2 Design
2×2 between-subjects, as Section 2. Primary comparisons:
- H1: Cells {A,B} pooled (scalar) vs. {C,D} pooled (vector), and separately
  B (scalar/shifting) vs. D (vector/shifting) as the sharpest test.
- H2: the interaction contrast (D−B) vs. (C−A) on overshoot — i.e. does the
  vector-minus-scalar gap differ between shifting and static.
- H3: C vs. A and D vs. B on satisfaction-dispersion metrics.

### 7.3 Sampling plan and exclusions
- Stopping rule: recruit to n = 45 completed analysable sessions per cell (or
  the revised pilot-informed n, whichever is registered as final before
  confirmatory collection starts); no interim analysis or peeking.
- Pre-registered exclusions (applied identically across cells, decided
  before any outcome data are examined):
  1. Failed comprehension check twice (`excluded_comprehension`).
  2. Session hit the 25-minute hard timeout before round 30
     (`excluded_timeout`).
  3. Modal round-decision latency < 500 ms across the whole session
     (`excluded_speeding` — evidence of not reading the screen); all 30
     rounds, including Round 1, are pooled for this calculation regardless
     of position in the session.
  4. Duplicate participant (same Prolific ID or, for the self-hosted page,
     same `pid` query parameter, appears more than once) — only the first
     completed session is analysed.
  Replacement participants are recruited to reach the target n per cell;
  exclusion counts and reasons are reported for all cells.

### 7.4 Analysis plan
- **Cell-level (one row per session) outcomes**, tested with **Mann-Whitney
  U** (non-parametric, appropriate given the modest, possibly skewed n per
  cell and no distributional assumption needed):
  - total overshoot (Σ over the four stocks of `overshoot_depth`) — H1, H2.
  - welfare_mean (mean satisfaction over 30 rounds) — exploratory secondary.
  - |human welfare_mean − bot welfare_mean| and human's percentile rank in
    the bot satisfaction distribution — H3.
  - end-of-session token hoarding index (vector cells only: final token
    balance ÷ mean per-round issuance) and round-to-round consumption
    standard deviation (all cells) — H4, reported descriptively with
    Mann-Whitney comparisons against the *simulated bot population's* own
    session-level distribution of the same statistics (a human-vs-bot
    within-session test, since H4 is about a human/bot divergence, not a
    between-cell one).
- **Round-level (30 rows per session) outcomes**, modelled with **linear
  mixed-effects models** (participant as random intercept), predicting
  per-round satisfaction or consumption level from money system ×
  environment × round number (to capture learning/adaptation across the
  session), reported as a robustness check on the cell-level tests, not as
  the primary confirmatory test (to avoid pseudo-replication inflating
  significance from 30 correlated observations per participant).
- Interaction term (H2) reported with its own CI; a significant main effect
  of money system without a significant interaction is still consistent with
  H1 but not H2.
- All tests two-tailed, α = .05, no multiplicity correction across H1–H3
  because they are ordered, non-overlapping, pre-registered directional
  hypotheses on distinct outcome variables; H4 comparisons are exploratory
  and reported unadjusted with that label.

### 7.5 Data availability
Anonymised per-round and per-session data (JSON exports from
`web/index.html`, see Section 6 of `README.md`) are deposited on OSF at
study completion; no free-text questionnaire response is published verbatim
if it contains identifying information (manual redaction pass before
release).

## 8. Threats to validity

- **Framing effects.** The most important internal-validity risk for a study
  that exists to demonstrate a *policy-relevant* result is that
  eco-moralised language ("save the planet", "sustainable", "climate") could
  bias participants toward conserving resources regardless of the money
  mechanism, contaminating the comparison between money systems with a
  comparison between narratives. This protocol therefore uses **strictly
  neutral vocabulary throughout the task**: resources are "materials A–D",
  tokens are "stamps", the environment condition is never named or
  explained causally to the participant (they see numbers, not a story).
  Framing is treated as a *separate, future* manipulated variable (a planned
  follow-up 2×2×2 adding a framing factor), not something to fold
  silently into this study.
- **One human among nineteen bots.** The design necessarily has the human
  facing a population whose behaviour is fixed by a heuristic
  (`RuleBasedPolicy`) rather than by other humans. This is a deliberate
  simplification (see Section 2) that isolates the human-vs-money-system
  question from human-vs-human strategic dynamics (coordination, learned
  norms, communication) that a multi-human design would introduce as a
  second source of variance. The limitation is that findings here speak to
  *individual* decision-making under each institution, not to *emergent
  group* dynamics under either institution when everyone is human; a
  follow-up multi-human session design is out of scope for this protocol
  and should be treated as a distinct study with its own pre-registration.
- **Learning / order effects within a session.** Because each participant
  sees only one condition (between-subjects), there is no risk of order
  effects across conditions, but there is a within-session learning
  trajectory (participants likely act differently in round 5 than round 25)
  that could differ in shape between cells. The round-level mixed-model
  analysis (Section 7.4) explicitly includes round number and a
  round × condition interaction to characterise this rather than average
  over it silently.
- **Selection / non-response.** Screening for platform reliability
  (Section 6) trades some generalisability for lower noise; this is noted
  as a limitation on external validity to "general population" claims.
- **Novelty/instruction-reading effort.** A genuinely new task format
  (materials, stamps) may see higher early-round noise than a familiar
  economic game; the comprehension check (Section 3.3) and the 500ms
  speeding exclusion (Section 7.3) are the primary mitigations.
- **Demand characteristics from the bonus.** Because the bonus is
  monotonic in satisfaction and identical in formula across cells, it
  cannot by itself explain a *between-cell* difference, but it does mean
  participants are motivated to actually try, which is intended (a
  low-effort task would wash out any real behavioural difference in noise).
- **The bonus formula works against H4's hoarding prediction.** The
  performance bonus (Section 4) pays strictly in proportion to the sum of
  the participant's own 30 per-round satisfaction scores, with no term tied
  to stock health, overshoot, or the population's outcomes. Since per-round
  satisfaction is capped at 1.0, a purely bonus-maximising participant has
  no incentive to under-consume now in order to consume more later — banking
  tokens cannot raise the sum of per-round scores. H4's prediction that
  vector-money participants will hoard tokens or smooth consumption is
  therefore a prediction *against* the myopic incentive gradient the bonus
  creates. Any hoarding/smoothing observed should be read as a conservative,
  against-incentive finding (if anything, harder to detect than it would be
  under an incentive scheme that rewarded forward-looking behaviour); absence
  of hoarding is not strong evidence against H4 given this incentive
  structure, and this asymmetry should be reported alongside any H4 result
  rather than left implicit.

## 9. Ethics (independent researcher, no institutional IRB assumed)

This protocol is written for an independent researcher without a standing
university ethics committee, while remaining suitable for submission to one
if available; where a researcher has access to a university partner or
departmental ethics board, that route is preferred over the commercial
options below and should be substituted for Section 9.3.

### 9.1 No deception
Participants are told, before consenting, that they will play a
resource-allocation game with a real cash bonus tied to their score, that
19 of the 20 "players" are computer-simulated, and that the study compares
different resource-allocation rules (without naming the specific hypotheses,
which would bias behaviour). The debrief (Section 3.6) fills in the
comparison being made. This satisfies "no deception" in the strict sense: no
participant is told anything false about what is happening; the only thing
withheld until debrief is *which* comparison is being made and *why*, which
is standard, non-deceptive incomplete disclosure.

### 9.2 Consent, population, and data
- Adults only (18+), confirmed by the recruiting platform's own age gate;
  no additional sensitive data collected.
- Informed consent screen (verbatim, shown before instructions):

  > **Study information and consent**
  >
  > You are invited to take part in a short online study about how people
  > make decisions in a simulated economy. You will play a resource game for
  > about 15 minutes, alongside computer-simulated players, and answer a
  > short questionnaire afterwards.
  >
  > **What you will do.** Choose how much to "consume" each round from a
  > shared pool of materials, for 30 rounds, then answer 5 short questions.
  >
  > **Payment.** You will receive a flat fee for completing the study, plus a
  > bonus based on your score in the game. Full amounts are stated on the
  > study listing before you start.
  >
  > **Risks.** This study poses no more than minimal risk. It is not a test
  > of intelligence or ability, there are no right or wrong personal answers,
  > and no health, financial, or otherwise sensitive information is
  > collected from you.
  >
  > **Data.** We record your in-game choices, the times you took to decide,
  > and your questionnaire answers. We do **not** collect your name, email,
  > or any directly identifying information — you are identified only by an
  > anonymous participant code assigned by the recruiting platform. Data are
  > stored securely and only the anonymised dataset (no platform ID) is
  > shared publicly as part of the research record.
  >
  > **Voluntary participation.** Taking part is voluntary. You can stop at
  > any point by closing the browser tab; if you complete at least
  > 10 rounds before stopping, you will still receive the flat fee (no
  > bonus for incomplete sessions beyond points already earned). You can
  > request that your data be deleted within 14 days of taking part by
  > contacting the researcher at the email on the study listing, quoting
  > your participant code.
  >
  > **Contact.** Questions about this study can be directed to the
  > researcher listed on the study page. [Independent-researcher variant:
  > if this study has not been reviewed by a formal ethics board, that is
  > disclosed here explicitly, e.g.: "This study has been reviewed under
  > [Prolific's / the commercial IRB's] independent ethics review process
  > rather than a university ethics committee."]
  >
  > By clicking "I agree," you confirm you are 18 or older, have read the
  > above, and consent to take part.

- **GDPR compliance** (applies regardless of participant location if the
  researcher or infrastructure is UK/EU-based, and is good practice
  regardless): the only personal data processed is the platform-issued
  pseudonymous participant ID, which is (a) never linked to name/email by
  the researcher, (b) used solely to enable payment via the platform (the
  platform, not the researcher, holds the identity mapping) and to detect
  duplicate sessions, and (c) not published — published data uses a
  re-randomised session code with no link back to the platform ID. Data are
  stored on infrastructure the researcher controls (e.g. an institutional or
  personal encrypted store), retained for a stated period (recommended:
  5 years, standard for research data, or per institutional policy),
  and a data processing record documenting purpose, lawful basis (consent),
  and retention is kept alongside the pre-registration. No special-category
  data (Article 9 GDPR) is collected.

### 9.3 Ethics review route for an independent researcher
Two viable routes, in order of preference:
1. **University partnership.** If the researcher has any university
   affiliation (current, visiting, or via a co-author), submit through that
   institution's ethics board — the preferred route, since it provides
   independent oversight and is what most journals/venues expect.
2. **Commercial/independent IRB.** If no university affiliation is
   available, an independent ethics review can be obtained from a
   commercial IRB offering minimal-risk online-study review (e.g.
   Pearl IRB, Advarra, or equivalent low-cost minimal-risk review tracks
   aimed at online behavioural studies; exact vendor and cost should be
   confirmed at the time of the study since offerings and pricing change).
   Prolific also publishes ethics guidance for independent researchers and
   requires studies to meet its own minimal-risk standards as a condition of
   listing, which provides a baseline platform-level check even before an
   external IRB is engaged.
Either way, the study should not proceed to data collection before written
ethics approval (or, at minimum, a completed and dated self-certification
against a minimal-risk checklist if genuinely no review route is available)
is on file alongside the OSF pre-registration.

### 9.4 Minimal-risk justification
The task is a low-stakes numerical decision game with real but small
financial stakes (max ≈ £4 total), no manipulation of participants' beliefs
about themselves, no exposure to disturbing content, and no collection of
sensitive personal data — consistent with a minimal-risk classification
under both UK/EU research-ethics norms and Prolific's own study-approval
criteria.
