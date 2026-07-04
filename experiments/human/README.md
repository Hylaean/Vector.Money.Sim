# Human experiment: scalar vs. vector money

This directory packages a complete human-subjects replication of the
scalar-vs-vector money comparison in `src/economy.py`. Three files, one job
each:

- **`protocol.md`** — the full experimental protocol: hypotheses, design,
  incentives, power analysis, pre-registration plan, ethics, and threats to
  validity. Read this first; it is the thing you register on OSF before
  collecting any confirmatory data.
- **`instructions.md`** — the exact participant-facing text (neutral
  framing: "materials A–D" and "stamps", no climate language), the
  comprehension-check questions and answer key, the post-task questionnaire,
  and the debrief text. This is what's actually shown inside the web page,
  reproduced here for review, translation, and the pre-registration record.
- **`web/index.html`** — the task itself: a single self-contained HTML file
  (no build step, no external requests, works from `file://`) that runs a
  20-household economy — 1 human, 19 rule-based bots — with the same
  environment dynamics, money-system mechanics, and rule-based policy as
  `src/economy.py`, `src/climate.py`, `src/money.py`, and
  `src/policies.RuleBasedPolicy`.

## How the web task maps to the Python model

| Concept | Python | Web page |
|---|---|---|
| Resources | `carbon, water, biomass, minerals` | Materials `A, B, C, D` (same order) |
| Tokens | resource tokens | "stamps" |
| `EconomyConfig.money` | `"scalar"` / `"vector"` (λ=0) | `?money=scalar` / `?money=vector` |
| `EconomyConfig.environment` | `"static"` / `"shifting"` | `?env=static` / `?env=shifting` |
| `EconomyConfig.seed` | int | hashed from `?pid=` (FNV-1a → mulberry32 seed) |
| `EconomyConfig.steps` | int | `?rounds=` (default 30) |
| Household population | 20, index 0..19 | 20; the human is household index 0, always processed (and its extraction resolved) **before** the 19 bots each round, exactly mirroring the Python household-loop order |
| Bot decisions | `RuleBasedPolicy(greed=0)` | `ruleBasedDecide()` in the page — same thresholds, ported line for line |
| RNG | Python `random.Random(seed)`, Mersenne Twister | `mulberry32(seed)` — **not bit-identical** to the Python stream, but the same mechanism (independent streams for wages and for environment shocks, matching `Economy.__init__` creating two separate `Random(seed)` instances) |

All numeric constants (satisfaction levels, unit footprints, efficiency
parameters, climate trajectory, wage distribution, observation lag,
price-sensitivity, carryover, convertibility) were copy-verified against
`src/economy.py`, `src/climate.py`, and `src/money.py` — see "Verification"
below.

## Running a pilot on Prolific: step by step

1. **Host the page.** `web/index.html` is fully self-contained and needs no
   backend for the game logic itself, but you do need somewhere to receive
   the data. Two options:
   - **Simplest (download-only):** host the file as a static page (GitHub
     Pages, S3 + CloudFront, Netlify drop, or even a plain web server) and
     rely on participants clicking "Download my data" at the end, then
     uploading that JSON file back to you via the Prolific submission flow
     (e.g. a completion-code field, or a separate upload form/service you
     control). Simple, no server-side code, but adds a manual step for
     participants.
   - **Recommended (auto-submit):** stand up a minimal HTTPS endpoint that
     accepts a POST of JSON (any serverless function — Cloudflare Worker,
     AWS Lambda + API Gateway, a one-route Flask app — is enough) and pass
     its URL via `?post=https://your-endpoint/submit`. The page POSTs the
     full session log there automatically once the questionnaire is
     submitted, in addition to still offering the manual download as a
     fallback if the POST fails (e.g. participant is offline).
2. **Set up the pre-registration.** Before recruiting anyone for the
   confirmatory study, register the plan in `protocol.md` Section 7 on OSF
   (or AsPredicted). Do this even for the pilot in spirit (state that the
   pilot is a pilot and won't be pooled into confirmatory analysis).
3. **Get ethics sign-off.** Follow `protocol.md` Section 9.3 — university
   partner ethics board if you have one, otherwise a commercial/independent
   IRB, plus Prolific's own study-approval process. Do not open recruitment
   before this is on file.
4. **Build the four study links.** For each of the 4 cells, construct a URL:
   ```
   https://your-host/index.html?money=scalar&env=static&rounds=30&post=https://your-endpoint/submit
   https://your-host/index.html?money=scalar&env=shifting&rounds=30&post=https://your-endpoint/submit
   https://your-host/index.html?money=vector&env=static&rounds=30&post=https://your-endpoint/submit
   https://your-host/index.html?money=vector&env=shifting&rounds=30&post=https://your-endpoint/submit
   ```
   Append `&pid={{%PROLIFIC_PID%}}` if using Prolific's URL-parameter
   substitution (or whatever templating your recruiting flow supports) so
   each participant gets a unique, reproducible seed; the page falls back to
   a random anonymous id if `pid` is omitted, which still works but is not
   reproducible if you need to re-derive a session's random draws later.
5. **Create 4 Prolific studies** (one per cell — this gives you exact
   per-cell N control and independent balancing), each:
   - pointing at the corresponding URL above,
   - listing the flat fee (`protocol.md` §4: £2.50) and stating the bonus
     structure (up to £1.50, proportional to in-game score) truthfully in
     the study description,
   - screened for fluent English, desktop/laptop device, and at least one
     prior completed study (see `protocol.md` §6),
   - completion-code driven: Prolific gives you a code to show on your own
     "study complete" step, or you can rely on Prolific's own
     redirect-on-completion if your host supports a query-param redirect at
     the end of the questionnaire (the current page does not auto-redirect;
     add a `window.location = "https://app.prolific.com/submissions/complete?cc=YOUR_CODE"`
     call after `finishGame()`'s questionnaire submit if you want that).
6. **Pilot run.** Launch each of the 4 studies at **n = 15**
   (`protocol.md` §5) — 60 participants total. Monitor completion time and
   comprehension-check pass rate as the first few responses arrive; a pass
   rate much below expectations or a median time far outside 12–15 minutes
   is a signal to pause and revisit the instructions before spending the
   full budget.
7. **Collect and inspect pilot data.** Pull the JSON payloads (from your
   POST endpoint, or from manually collected downloads) and compute, per
   cell: mean/SD of `overshoot_total` (sum of `overshoot_depth` across the
   four `records[].stock_*` series against each resource's boundary = 40)
   and of `welfare_mean` (mean of `records[].welfare` — or, for the
   human-specific comparison, mean of `records[].human_satisfaction`).
   Feed the observed SDs into a revised power calculation (`protocol.md`
   §5) before committing to the confirmatory n=45/cell run.
8. **Confirmatory run.** Recruit fresh participants (do not reuse pilot
   respondents — Prolific lets you exclude prior participants by study) to
   the pre-registered target n per cell, using the same 4 study links.
9. **Analyse per the pre-registered plan** (`protocol.md` §7.4): Mann-Whitney
   U on cell-level outcomes, mixed-effects models on round-level outcomes.
   Apply the pre-registered exclusions (§7.3) before any hypothesis test.
10. **Deposit data and debrief participants** per `protocol.md` §7.5 and the
    debrief text in `instructions.md`.

## Verification performed for this package

The web port (`web/index.html`) was checked against the Python source three
ways (see the session transcript for the exact commands):

1. **Constant-for-constant diff.** Every numeric/structural constant used in
   the JS (satisfaction levels, unit footprints, efficiency cost/factor/
   floor, resource defaults `stock=70, capacity=100, regen_rate=0.10,
   boundary=40`, climate trajectory `drift=0.004 (floor=0.45×), shock_prob=
   0.02+0.002t (capped at 0.15), severity=0.15` on `water,biomass`, `n_households=20`, wage
   `mean=3.0, sigma=0.5`, `observation_lag=3`, `issuance_headroom=1.0`,
   `price_sensitivity=0.15`, `carryover=0.5`, `convertibility=0.0`) was
   extracted programmatically from the page's `<script>` block and compared
   against the corresponding literals in `src/economy.py`, `src/climate.py`,
   and `src/money.py` — all match exactly.
2. **Headless 150-step, 8-seed simulation.** The JS `Economy`/`Environment`/
   `MoneySystem` classes were driven for 150 rounds × 8 seeds × all-bot
   decisions (every household including the "human" slot decided by the
   ported `ruleBasedDecide`) under all four money×environment cells via
   Node, and the aggregate welfare/overshoot were compared against a fresh
   run of the actual Python `Economy` under the same seeds/config:

   | Cell | Python welfare / overshoot | JS welfare / overshoot |
   |---|---|---|
   | scalar / static | 0.84 / 0.0 | 0.85 / 0.0 |
   | scalar / shifting | 0.62 / 45.0 | 0.61 / 43.9 |
   | vector / static | 0.52 / 0.0 | 0.50 / 0.0 |
   | vector / shifting | 0.46 / 22.4 | 0.47 / 21.6 |

   Both implementations reproduce the same qualitative pattern reported in
   the project's known 2×2 results (scalar collapses under a shifting
   environment; vector holds overshoot far lower; static environments show
   no overshoot in either system). The small numeric gaps are expected and
   attributable to using an independent PRNG stream (mulberry32) rather than
   a bit-identical replay of Python's Mersenne Twister — the mechanism, not
   the random stream, is what was ported.
3. **NaN / sanity sweep.** 80 full 30-round sessions (4 conditions × 20
   distinct `pid` seeds) were run headlessly with the bot policy driving
   every household including the human slot: zero NaNs, zero negative
   stocks, zero negative cash balances across all 80 × 30 rounds.

Node (`node@22`, confirmed via `which node`) was used for all of the above;
no Python changes were made and no file outside `experiments/human/` was
touched.
