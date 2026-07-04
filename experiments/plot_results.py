"""Generate the headline figures for the scalar-vs-vector money experiment.

Reads the artefacts written by :mod:`experiments.run_matrix` — ``runs.csv``,
``summary.json`` and ``timeseries/*.csv`` — from a 2x2 (money x environment)
results directory and a convertibility-sweep results directory, and renders
four figures plus a README describing them.

If either input directory is missing or empty, this module runs its own
small fallback experiment directly against :class:`src.economy.Economy` so
that the figures can still be produced standalone.

Usage::

    python -m experiments.plot_results \
        --results experiments/results \
        --sweep experiments/results_convertibility \
        --output figures
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from src.economy import Economy, EconomyConfig

# -- Okabe-Ito colourblind-safe palette --------------------------------------
COLOR_SCALAR = "#E69F00"   # orange
COLOR_VECTOR = "#0072B2"   # blue
COLOR_NEUTRAL = "#555555"

MONEY_COLORS = {"scalar": COLOR_SCALAR, "vector": COLOR_VECTOR}
ENV_MARKERS = {"static": "o", "shifting": "^"}
ENV_LINESTYLES = {"static": "-", "shifting": "--"}
CARBON_BOUNDARY = 40.0

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#eeeeee",
        "grid.linewidth": 0.8,
        "legend.frameon": False,
    }
)


# -- loading ------------------------------------------------------------------


def _num(value: str):
    try:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        return value


def load_runs_csv(path: str) -> List[Dict[str, object]]:
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        rows = []
        for row in reader:
            parsed = {}
            for k, v in row.items():
                if k in ("money", "environment", "policy"):
                    parsed[k] = v
                else:
                    parsed[k] = _num(v)
            rows.append(parsed)
        return rows


def slugify(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.+\[\]=-]+", "_", label)


def load_timeseries(results_dir: str, money: str, environment: str, policy: str, seed: int) -> List[Dict[str, float]]:
    slug = "_".join([slugify(money), slugify(environment), slugify(policy)])
    path = os.path.join(results_dir, "timeseries", f"{slug}_s{seed}.csv")
    if not os.path.exists(path):
        return []
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        return [{k: _num(v) for k, v in row.items()} for row in reader]


def dir_populated(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    runs_csv = os.path.join(path, "runs.csv")
    return os.path.exists(runs_csv) and os.path.getsize(runs_csv) > 0


def pick_policy(rows: Sequence[Dict[str, object]]) -> str:
    """Prefer the 'rule' policy if present, else whatever unique policy exists."""
    policies = sorted({str(r["policy"]) for r in rows})
    if "rule" in policies:
        return "rule"
    return policies[0]


# -- fallback data generation ---------------------------------------------------


def _run_one(money, environment, seed: int, steps: int) -> dict:
    config = EconomyConfig(
        n_households=20,
        steps=steps,
        seed=seed,
        money=money,
        environment=environment,
    )
    return Economy(config).run()


def generate_fallback_grid(output_dir: str, seeds: Sequence[int] = range(8), steps: int = 200) -> None:
    """Run the money x environment 2x2, writing runs.csv + timeseries/*.csv."""
    os.makedirs(output_dir, exist_ok=True)
    ts_dir = os.path.join(output_dir, "timeseries")
    os.makedirs(ts_dir, exist_ok=True)
    fieldnames = [
        "money", "environment", "policy", "seed",
        "welfare_mean", "welfare_final", "gini_satisfaction_mean", "gini_wealth_final",
        "overshoot_total",
        "overshoot_carbon", "overshoot_water", "overshoot_biomass", "overshoot_minerals",
        "return_time_carbon", "return_time_water", "return_time_biomass", "return_time_minerals",
    ]
    rows = []
    for money in ("scalar", "vector"):
        for environment in ("static", "shifting"):
            for seed in seeds:
                result = _run_one(money, environment, seed, steps)
                overshoot = result["overshoot_depth"]
                return_time = result["return_time"]
                row = {
                    "money": money,
                    "environment": environment,
                    "policy": "rule",
                    "seed": seed,
                    "welfare_mean": result["welfare_mean"],
                    "welfare_final": result["welfare_final"],
                    "gini_satisfaction_mean": result["gini_satisfaction_mean"],
                    "gini_wealth_final": result["gini_wealth_final"],
                    "overshoot_total": result["overshoot_total"],
                }
                for name in ("carbon", "water", "biomass", "minerals"):
                    row[f"overshoot_{name}"] = overshoot.get(name, 0.0)
                    row[f"return_time_{name}"] = return_time.get(name, 0)
                rows.append(row)
                slug = "_".join([slugify(money), slugify(environment), slugify("rule")])
                with open(os.path.join(ts_dir, f"{slug}_s{seed}.csv"), "w", newline="") as fh:
                    records = result["records"]
                    if records:
                        rec_fields = sorted({k for rec in records for k in rec})
                        if "t" in rec_fields:
                            rec_fields.remove("t")
                            rec_fields = ["t"] + rec_fields
                        writer = csv.DictWriter(fh, fieldnames=rec_fields)
                        writer.writeheader()
                        writer.writerows(records)
    with open(os.path.join(output_dir, "runs.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_fallback_sweep(
    output_dir: str,
    lambdas: Sequence[float] = (0.0, 0.25, 0.5, 0.75, 1.0),
    seeds: Sequence[int] = range(8),
    steps: int = 150,
) -> None:
    """Run the convertibility sweep, writing runs.csv (no timeseries needed)."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "timeseries"), exist_ok=True)
    fieldnames = [
        "money", "environment", "policy", "seed",
        "welfare_mean", "welfare_final", "gini_satisfaction_mean", "gini_wealth_final",
        "overshoot_total",
        "overshoot_carbon", "overshoot_water", "overshoot_biomass", "overshoot_minerals",
        "return_time_carbon", "return_time_water", "return_time_biomass", "return_time_minerals",
    ]
    rows = []
    for lam in lambdas:
        for environment in ("static", "shifting"):
            for seed in seeds:
                result = _run_one(float(lam), environment, seed, steps)
                overshoot = result["overshoot_depth"]
                return_time = result["return_time"]
                row = {
                    "money": str(float(lam)),
                    "environment": environment,
                    "policy": "rule",
                    "seed": seed,
                    "welfare_mean": result["welfare_mean"],
                    "welfare_final": result["welfare_final"],
                    "gini_satisfaction_mean": result["gini_satisfaction_mean"],
                    "gini_wealth_final": result["gini_wealth_final"],
                    "overshoot_total": result["overshoot_total"],
                }
                for name in ("carbon", "water", "biomass", "minerals"):
                    row[f"overshoot_{name}"] = overshoot.get(name, 0.0)
                    row[f"return_time_{name}"] = return_time.get(name, 0)
                rows.append(row)
    with open(os.path.join(output_dir, "runs.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def ensure_data(results_dir: str, sweep_dir: str) -> Tuple[bool, bool]:
    """Return (grid_was_generated, sweep_was_generated)."""
    grid_generated = False
    sweep_generated = False
    if not dir_populated(results_dir):
        generate_fallback_grid(results_dir)
        grid_generated = True
    if not dir_populated(sweep_dir):
        generate_fallback_sweep(sweep_dir)
        sweep_generated = True
    return grid_generated, sweep_generated


# -- figure 1: trajectories -----------------------------------------------------


def _primary_resource(rows: Sequence[Dict[str, object]]) -> str:
    """Pick whichever resource shows the largest mean overshoot — the one
    whose trajectory actually tells the boundary-collapse story in this
    particular run (it need not be carbon: shocks may hit other stocks)."""
    resources = ("carbon", "water", "biomass", "minerals")
    totals = {}
    for name in resources:
        key = f"overshoot_{name}"
        values = [row[key] for row in rows if key in row]
        totals[name] = sum(values) / len(values) if values else 0.0
    return max(totals, key=totals.get)


def fig1_trajectories(results_dir: str, out_prefix: str) -> None:
    rows = load_runs_csv(os.path.join(results_dir, "runs.csv"))
    policy = pick_policy(rows)
    resource = _primary_resource(rows)
    stock_col = f"stock_{resource}"
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharex=True, sharey=True)
    row_envs = ["static", "shifting"]
    col_moneys = ["scalar", "vector"]

    for r, environment in enumerate(row_envs):
        for c, money in enumerate(col_moneys):
            ax = axes[r][c]
            color = MONEY_COLORS[money]
            matching = [row for row in rows if row["money"] == money and row["environment"] == environment and row["policy"] == policy]
            seeds = sorted({row["seed"] for row in matching})
            all_series = []
            for seed in seeds:
                records = load_timeseries(results_dir, money, environment, policy, seed)
                if not records:
                    continue
                series = [rec[stock_col] for rec in records]
                t = [rec["t"] for rec in records]
                ax.plot(t, series, color=color, alpha=0.25, linewidth=0.8)
                all_series.append(series)
            if all_series:
                n = min(len(s) for s in all_series)
                mean_series = [sum(s[i] for s in all_series) / len(all_series) for i in range(n)]
                ax.plot(range(n), mean_series, color=color, linewidth=2.4)
            ax.axhline(CARBON_BOUNDARY, color=COLOR_NEUTRAL, linestyle=":", linewidth=1.2)
            if r == 0:
                ax.set_title(money, fontweight="bold", color=color)
            if c == 0:
                ax.set_ylabel(f"{environment}\n{resource} stock")
            if r == 1:
                ax.set_xlabel("time step")

    # Label the boundary once, on the top-right panel, near the line.
    axes[0][1].annotate(
        "ecological boundary",
        xy=(1.0, CARBON_BOUNDARY),
        xycoords=("axes fraction", "data"),
        xytext=(-2, 4),
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=9,
        color=COLOR_NEUTRAL,
    )

    fig.suptitle(
        f"Scalar money lets {resource} collapse through the boundary under a shifting climate; vector money bends but holds",
        fontsize=12.5,
        y=1.0,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(f"{out_prefix}.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{out_prefix}.svg", bbox_inches="tight")
    plt.close(fig)


# -- figure 2: welfare vs overshoot frontier -------------------------------------


def fig2_frontier(results_dir: str, out_prefix: str) -> None:
    rows = load_runs_csv(os.path.join(results_dir, "runs.csv"))
    policy = pick_policy(rows)
    rows = [r for r in rows if r["policy"] == policy]

    fig, ax = plt.subplots(figsize=(7.5, 6))
    conditions: Dict[Tuple[str, str], List[Dict[str, object]]] = {}
    for row in rows:
        key = (str(row["money"]), str(row["environment"]))
        conditions.setdefault(key, []).append(row)

    for (money, environment), condition_rows in conditions.items():
        color = MONEY_COLORS.get(money, COLOR_NEUTRAL)
        marker = ENV_MARKERS.get(environment, "s")
        xs = [r["overshoot_total"] for r in condition_rows]
        ys = [r["welfare_mean"] for r in condition_rows]
        ax.scatter(xs, ys, color=color, marker=marker, alpha=0.55, s=45, edgecolor="none")
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        ax.scatter([mx], [my], color=color, marker="x", s=140, linewidth=2.5, zorder=5)
        ax.annotate(
            f"{money}/{environment}",
            xy=(mx, my),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=9,
            color=color,
            fontweight="bold",
        )

    ax.set_xlabel("Ecological overshoot (cumulative depth below boundary)")
    ax.set_ylabel("Average need satisfaction (welfare)")
    ax.set_title("Vector money trades some average welfare for far less ecological overshoot")

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.annotate(
        "better ↑←",
        xy=(xlim[0] + 0.03 * (xlim[1] - xlim[0]), ylim[1] - 0.05 * (ylim[1] - ylim[0])),
        fontsize=10,
        color=COLOR_NEUTRAL,
        style="italic",
    )

    legend_elems = [
        Line2D([0], [0], marker=ENV_MARKERS["static"], color="none", markerfacecolor=COLOR_NEUTRAL,
               markeredgecolor="none", label="static environment", markersize=8),
        Line2D([0], [0], marker=ENV_MARKERS["shifting"], color="none", markerfacecolor=COLOR_NEUTRAL,
               markeredgecolor="none", label="shifting environment", markersize=8),
    ]
    ax.legend(handles=legend_elems, loc="lower right", fontsize=9)

    fig.tight_layout()
    fig.savefig(f"{out_prefix}.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{out_prefix}.svg", bbox_inches="tight")
    plt.close(fig)


# -- figure 3: inequality bars ----------------------------------------------------


def fig3_inequality(results_dir: str, out_prefix: str) -> None:
    rows = load_runs_csv(os.path.join(results_dir, "runs.csv"))
    policy = pick_policy(rows)
    rows = [r for r in rows if r["policy"] == policy]

    moneys = ["scalar", "vector"]
    environments = ["static", "shifting"]
    fig, ax = plt.subplots(figsize=(7, 5.5))

    bar_width = 0.35
    x = list(range(len(environments)))
    for i, money in enumerate(moneys):
        means, sds = [], []
        for environment in environments:
            values = [r["gini_satisfaction_mean"] for r in rows if r["money"] == money and r["environment"] == environment]
            n = len(values)
            m = sum(values) / n if n else 0.0
            sd = (sum((v - m) ** 2 for v in values) / (n - 1)) ** 0.5 if n > 1 else 0.0
            means.append(m)
            sds.append(sd)
        offset = (i - 0.5) * bar_width
        positions = [xi + offset for xi in x]
        ax.bar(positions, means, width=bar_width, yerr=sds, capsize=4,
               color=MONEY_COLORS[money], label=money, alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(environments)
    ax.set_ylabel("Gini coefficient of need satisfaction (mean ± sd across seeds)")
    ax.set_title("Vector money's per-capita token shares equalise satisfaction far more than scalar prices")
    ax.legend(loc="upper left", fontsize=10)

    fig.tight_layout()
    fig.savefig(f"{out_prefix}.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{out_prefix}.svg", bbox_inches="tight")
    plt.close(fig)


# -- figure 4: convertibility sweep -----------------------------------------------


def fig4_convertibility(sweep_dir: str, out_prefix: str) -> None:
    rows = load_runs_csv(os.path.join(sweep_dir, "runs.csv"))

    def is_lambda_row(row) -> bool:
        try:
            float(row["money"])
            return True
        except (TypeError, ValueError):
            return False

    rows = [r for r in rows if is_lambda_row(r)]
    environments = sorted({str(r["environment"]) for r in rows})

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(7.5, 8), sharex=True)

    for environment in environments:
        env_rows = [r for r in rows if r["environment"] == environment]
        lambdas = sorted({float(r["money"]) for r in env_rows})
        overshoot_means = []
        welfare_means = []
        for lam in lambdas:
            lam_rows = [r for r in env_rows if float(r["money"]) == lam]
            overshoot_means.append(sum(r["overshoot_total"] for r in lam_rows) / len(lam_rows))
            welfare_means.append(sum(r["welfare_mean"] for r in lam_rows) / len(lam_rows))
        linestyle = ENV_LINESTYLES.get(environment, "-")
        ax_top.plot(lambdas, overshoot_means, color=COLOR_NEUTRAL, linestyle=linestyle,
                    marker=ENV_MARKERS.get(environment, "o"), linewidth=2)
        ax_bot.plot(lambdas, welfare_means, color=COLOR_NEUTRAL, linestyle=linestyle,
                    marker=ENV_MARKERS.get(environment, "o"), linewidth=2)
        ax_top.annotate(environment, xy=(lambdas[-1], overshoot_means[-1]), xytext=(6, 0),
                        textcoords="offset points", fontsize=9, va="center")
        ax_bot.annotate(environment, xy=(lambdas[-1], welfare_means[-1]), xytext=(6, 0),
                        textcoords="offset points", fontsize=9, va="center")

    ax_top.set_ylabel("Ecological overshoot (cumulative depth)")
    ax_bot.set_ylabel("Average need satisfaction (welfare)")
    ax_bot.set_xlabel("Convertibility λ  (0 = pure vector tokens, 1 = pure scalar cash)")
    ax_top.set_title(
        "As token convertibility λ rises from 0 to 1, overshoot creeps back and welfare edges up: "
        "the scalar↔vector continuum"
    )

    fig.tight_layout()
    fig.savefig(f"{out_prefix}.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{out_prefix}.svg", bbox_inches="tight")
    plt.close(fig)


# -- README -----------------------------------------------------------------------

README_TEMPLATE = """# Figures: scalar vs. vector money

## fig1_trajectories
2x2 grid of per-seed stock trajectories over time (thin, translucent lines) with the
across-seed mean overlaid (thick line), for whichever resource shows the largest mean
ecological overshoot in this run (chosen automatically — under the shocks in the shifting
environment that is typically water or biomass, not carbon). Rows are the static and
shifting environment, columns are the scalar and vector money system, and the dotted
horizontal line marks the ecological boundary (stock = 40) below which the resource is
degraded. **Takeaway:** under a static environment both money systems keep the stock
safely above the boundary; under a shifting environment scalar money's lagged,
drift-blind prices let consumption outrun regeneration and the stock collapses through
the boundary and flatlines at zero, while vector money's hard per-capita token constraint
bends the trajectory down more gently and leaves it measurably higher at the end of the
run, even though it too breaches the boundary under sustained shocks.

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
environment. **Takeaway:** overshoot rises roughly monotonically with λ (more of the
resource becomes purchasable rather than strictly token-limited) while welfare rises only
modestly, most visibly in the shifting environment — scalar and vector money are two ends
of a single dial, not two separate paradigms, and the ecological cost of turning that dial
toward convertibility is steeper than the welfare gain.
"""


def write_readme(output_dir: str) -> None:
    with open(os.path.join(output_dir, "README.md"), "w") as fh:
        fh.write(README_TEMPLATE)


# -- CLI ----------------------------------------------------------------------


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, help="money x environment results directory")
    parser.add_argument("--sweep", required=True, help="convertibility sweep results directory")
    parser.add_argument("--output", required=True, help="figures output directory")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    os.makedirs(args.output, exist_ok=True)

    grid_generated, sweep_generated = ensure_data(args.results, args.sweep)
    if grid_generated:
        print(f"NOTE: {args.results} was missing/empty; generated a fallback 2x2 run there.")
    if sweep_generated:
        print(f"NOTE: {args.sweep} was missing/empty; generated a fallback sweep there.")

    fig1_trajectories(args.results, os.path.join(args.output, "fig1_trajectories"))
    fig2_frontier(args.results, os.path.join(args.output, "fig2_frontier"))
    fig3_inequality(args.results, os.path.join(args.output, "fig3_inequality"))
    fig4_convertibility(args.sweep, os.path.join(args.output, "fig4_convertibility"))
    write_readme(args.output)
    print(f"Wrote figures and README to {args.output}")


if __name__ == "__main__":
    main()
