# Figures: scalar vs. vector money

## fig1_trajectories
2x2 grid of per-seed stock trajectories over time (thin, translucent lines) with the
across-seed mean overlaid (thick line), for whichever resource shows the largest mean
ecological overshoot in this run (chosen automatically — under the shocks in the shifting
environment that is typically water or biomass, not carbon). Rows are the static and
shifting environment, columns are the scalar and vector money system, and the dotted
horizontal line marks the ecological boundary (stock = 40) below which the resource is
degraded. **Takeaway:** under a static environment both money systems keep the stock
safely above the boundary; under a shifting environment scalar money's lagged,
drift-blind prices let consumption outrun regeneration and the mean stock drains to
roughly 7 and never recovers, while vector money's hard per-capita token constraint
dips to roughly 29 before recovering back above the boundary (to roughly 43) by the
end of the run, even though it too breaches the boundary under sustained shocks.

## fig2_frontier
Scatter of average need satisfaction (welfare, y-axis) against cumulative ecological
overshoot (x-axis), one point per run (money system by colour, environment by marker
shape), with a large cross marking each condition's mean. Better outcomes sit up and to
the left: high welfare, low overshoot. **Takeaway:** vector money's cluster sits
consistently to the left of scalar money's at a similar or only modestly lower welfare,
showing it buys a large reduction in ecological overshoot for a small welfare cost,
especially once the environment is shifting.

## fig3_inequality
Bar chart of the mean (± standard deviation across seeds) Gini coefficient of
need-satisfaction inequality for each of the four money x environment conditions.
**Takeaway:** vector money's equal per-capita token issuance produces markedly more equal
outcomes than scalar money's price-based rationing, in both environments — scarcity under
vector money is shared, while scarcity under scalar money is priced out for poorer
households first.

## fig4_convertibility
Two stacked panels — cumulative ecological overshoot (top) and average welfare (bottom) —
plotted against the convertibility parameter λ, which interpolates continuously
between pure vector tokens (λ = 0) and pure scalar cash (λ = 1), one line per
environment. **Takeaway:** in the shifting environment, overshoot jumps sharply as soon
as any convertibility is allowed — λ = 0 holds overshoot near 32, but λ ≥ 0.25 is already
indistinguishable from pure scalar money's ~61-63, so even 25% convertibility erases the
ecological protection. In the static environment the relationship is not monotonic:
interior λ values (0.25-0.75) achieve the best of both worlds, with welfare around
0.90-0.91 — beating both pure scalar (0.84) and pure vector (0.52) — at low inequality
(Gini ≈ 0.06). Scalar and vector money are two ends of a single dial, not two separate
paradigms, but the dial's middle is not a simple interpolation of their costs and
benefits.
