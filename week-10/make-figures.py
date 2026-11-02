"""Generate Week 10 figures: DAGs, structure simulations, collider and HRT plots.

Run from anywhere: python3 week-10/make-figures.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.patheffects
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)

NAVY, BLUE, RUST, GOLD = "#18324a", "#2f6687", "#b24a3c", "#d5aa55"
INK, PAPER, MUTED, LINE = "#18232d", "#f7f4ee", "#62717d", "#c8c2b7"

plt.rcParams.update({
    "font.family": ["Aptos", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "font.size": 15,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "svg.fonttype": "none",
})


PREVIEW = Path("/tmp/w10")
PREVIEW.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, format="svg", transparent=True, bbox_inches="tight")
    fig.savefig(PREVIEW / name.replace(".svg", ".png"), dpi=70, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


# ---------------------------------------------------------------- DAG helper
def dag(ax, nodes, edges, conditioned=(), unobserved=(), box_w=0.26, box_h=0.13, fs=16):
    """nodes: {key: (x, y, label)}; edges: [(a, b, style)] style in {'solid','dashed','causal','bias','faint'}."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    widths, heights = {}, {}
    for k, (x, y, label) in nodes.items():
        w = box_w
        h = box_h + 0.085 * label.count("\n")
        widths[k], heights[k] = w, h
        face = "white"
        edge = NAVY
        ls = "-"
        lw = 2
        if k in conditioned:
            face, edge, lw = "#f4dfae", RUST, 3.2
        if k in unobserved:
            ls = (0, (4, 3))
            face = PAPER
        box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                             boxstyle="round,pad=0.012,rounding_size=0.025",
                             fc=face, ec=edge, lw=lw, ls=ls, zorder=3)
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=INK, zorder=4,
                linespacing=1.05)
    colors = {"solid": NAVY, "causal": BLUE, "bias": RUST, "dashed": MUTED, "faint": LINE}
    for a, b, style in edges:
        xa, ya, _ = nodes[a]
        xb, yb, _ = nodes[b]
        # shrink to box edges
        dx, dy = xb - xa, yb - ya
        def clip(w, h, dx, dy):
            tx = (w / 2 + 0.014) / abs(dx) if dx else np.inf
            ty = (h / 2 + 0.014) / abs(dy) if dy else np.inf
            return min(tx, ty)
        ta = clip(widths[a], heights[a], dx, dy)
        tb = clip(widths[b], heights[b], dx, dy)
        start = (xa + dx * ta, ya + dy * ta)
        end = (xb - dx * tb, yb - dy * tb)
        arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=22,
                              color=colors[style], lw=3 if style in ("causal", "bias") else 2.2,
                              ls="--" if style == "dashed" else "-", zorder=2,
                              shrinkA=0, shrinkB=0)
        ax.add_patch(arr)


def single_dag(name, nodes, edges, size=(9, 4.2), **kw):
    fig, ax = plt.subplots(figsize=size)
    dag(ax, nodes, edges, **kw)
    save(fig, name)


# ----------------------------------------------------------- opening-case DAGs
single_dag("dag-preuss.svg",
           {"tal": (0.5, 0.85, "Talent and\nparental investment"),
            "att": (0.2, 0.2, "Attends Preuss"),
            "y": (0.8, 0.2, "Test scores")},
           [("tal", "att", "bias"), ("tal", "y", "bias"), ("att", "y", "dashed")],
           box_w=0.3)

single_dag("dag-preuss-lottery.svg",
           {"lot": (0.12, 0.85, "Wins\nlottery"),
            "tal": (0.62, 0.85, "Talent and\nparental investment"),
            "att": (0.3, 0.2, "Attends Preuss"),
            "y": (0.82, 0.2, "Test scores")},
           [("lot", "att", "causal"), ("tal", "y", "bias"), ("att", "y", "causal")],
           box_w=0.26, size=(10, 4.4))

single_dag("dag-hrt.svg",
           {"h": (0.5, 0.85, "Health, wealth,\nhealth-consciousness"),
            "t": (0.2, 0.2, "Takes hormones"),
            "y": (0.8, 0.2, "Heart disease")},
           [("h", "t", "bias"), ("h", "y", "bias"), ("t", "y", "dashed")],
           box_w=0.3)

single_dag("dag-police.svg",
           {"c0": (0.15, 0.78, "Crime\n(earlier)"),
            "p": (0.5, 0.22, "Police\ndeployed"),
            "c1": (0.85, 0.78, "Crime\n(later)"),
            "atk": (0.15, 0.22, "1994 attack:\nguards posted")},
           [("c0", "p", "bias"), ("c0", "c1", "bias"), ("p", "c1", "causal"), ("atk", "p", "causal")],
           box_w=0.24, size=(10, 4.4))

single_dag("dag-covid-collider.svg",
           {"s": (0.18, 0.75, "Smokes"),
            "c": (0.82, 0.75, "Has COVID"),
            "h": (0.5, 0.22, "Hospitalized")},
           [("s", "h", "solid"), ("c", "h", "solid"), ("s", "c", "dashed")],
           conditioned=("h",), box_w=0.26)

single_dag("dag-publication-text.svg",
           {"a": (0.18, 0.75, "Newsworthy"),
            "b": (0.82, 0.75, "Well sourced"),
            "h": (0.5, 0.22, "In the archive")},
           [("a", "h", "solid"), ("b", "h", "solid")],
           conditioned=("h",), box_w=0.26)

single_dag("dag-education-income.svg",
           {"iq": (0.5, 0.85, "Intelligence"),
            "e": (0.18, 0.2, "College degree\n(by age 30)"),
            "y": (0.82, 0.2, "Income\n(at age 40)")},
           [("iq", "e", "bias"), ("iq", "y", "bias"), ("e", "y", "causal")],
           box_w=0.28)

single_dag("dag-fever.svg",
           {"cond": (0.5, 0.85, "Good underlying\ncondition"),
            "f": (0.2, 0.2, "Mounts a fever"),
            "y": (0.8, 0.2, "Recovers")},
           [("cond", "f", "bias"), ("cond", "y", "bias"), ("f", "y", "dashed")],
           box_w=0.3)

single_dag("dag-fever-trial.svg",
           {"rand": (0.12, 0.85, "Randomized:\nantipyretic\nor not"),
            "cond": (0.65, 0.85, "Good underlying\ncondition"),
            "temp": (0.35, 0.2, "Body\ntemperature"),
            "y": (0.85, 0.2, "Recovers")},
           [("rand", "temp", "causal"), ("cond", "y", "bias"), ("temp", "y", "causal")],
           box_w=0.26, size=(10, 4.4))

# ------------------------------------------- opening cases (non-book versions)
# Case 1: social media and teen depression, three candidate structures
for key, nodes, edges in [
    ("a", {"s": (0.2, 0.5, "Social media\nuse"), "d": (0.8, 0.5, "Depressive\nsymptoms")},
     [("s", "d", "causal")]),
    ("b", {"s": (0.2, 0.5, "Social media\nuse"), "d": (0.8, 0.5, "Depressive\nsymptoms")},
     [("d", "s", "bias")]),
    ("c", {"s": (0.2, 0.22, "Social media\nuse"), "d": (0.8, 0.22, "Depressive\nsymptoms"),
           "l": (0.5, 0.8, "Bullied at\nschool")},
     [("l", "s", "bias"), ("l", "d", "bias")]),
]:
    single_dag(f"dag-social-{key}.svg", nodes, edges, size=(6, 3.2), box_w=0.36, fs=17)

single_dag("dag-social-bullying.svg",
           {"b": (0.5, 0.84, "Bullied at school\n(before both)"),
            "w": (0.18, 0.5, "Withdraws from\nin-person life"),
            "s": (0.18, 0.14, "Social media use"),
            "d": (0.82, 0.14, "Depressive symptoms")},
           [("b", "w", "bias"), ("w", "s", "bias"), ("b", "d", "bias"), ("s", "d", "dashed")],
           box_w=0.34, size=(9, 4.6))

# Case 4: elite colleges and earnings (selection into treatment)
single_dag("dag-college.svg",
           {"a": (0.5, 0.82, "Ability, ambition,\nfamily resources"),
            "c": (0.2, 0.2, "Attends a more\nselective college"),
            "y": (0.8, 0.2, "Later earnings")},
           [("a", "c", "bias"), ("a", "y", "bias"), ("c", "y", "dashed")],
           box_w=0.3)

single_dag("dag-college-design.svg",
           {"a": (0.62, 0.8, "Ability, ambition,\nfamily resources"),
            "s": (0.2, 0.78, "Same colleges\napplied to and\nadmitted by"),
            "c": (0.2, 0.18, "Attends a more\nselective college"),
            "y": (0.8, 0.18, "Later earnings")},
           [("a", "s", "bias"), ("s", "c", "bias"), ("a", "y", "bias"), ("c", "y", "dashed")],
           conditioned=("s",), box_w=0.28, size=(10, 4.6))

# Case 3: TV and test scores (confounding)
single_dag("dag-tv.svg",
           {"f": (0.5, 0.82, "Family background"),
            "tv": (0.2, 0.22, "Hours of TV"),
            "y": (0.8, 0.22, "Test scores")},
           [("f", "tv", "bias"), ("f", "y", "bias"), ("tv", "y", "dashed")],
           box_w=0.3)

single_dag("dag-tv-rollout.svg",
           {"m": (0.15, 0.82, "TV arrives in\nlocal market\n(1940s–50s)"),
            "f": (0.62, 0.82, "Family background"),
            "tv": (0.35, 0.22, "Preschool TV\nexposure"),
            "y": (0.85, 0.22, "Test scores\n(1965)")},
           [("m", "tv", "causal"), ("f", "y", "bias"), ("tv", "y", "causal")],
           box_w=0.26, size=(10, 4.4))

# Three building blocks, one figure each (DAG only)
blocks = {
    "chain": ({"x": (0.15, 0.5, "X"), "m": (0.5, 0.5, "M"), "y": (0.85, 0.5, "Y")},
              [("x", "m", "causal"), ("m", "y", "causal")]),
    "fork": ({"x": (0.15, 0.25, "X"), "c": (0.5, 0.78, "C"), "y": (0.85, 0.25, "Y")},
             [("c", "x", "bias"), ("c", "y", "bias")]),
    "collider": ({"x": (0.15, 0.78, "X"), "c": (0.5, 0.25, "C"), "y": (0.85, 0.78, "Y")},
                 [("x", "c", "solid"), ("y", "c", "solid")]),
}
for k, (n, e) in blocks.items():
    single_dag(f"dag-{k}.svg", n, e, size=(7, 2.6), box_w=0.16, fs=20)


# ------------------------------------------------ structure simulations (2 panels)
# The middle variable takes four discrete levels so "controlling" = comparing within a level.
rng = np.random.default_rng(522)
N = 1200
LEVEL_COLORS = ["#c9dbe6", "#7fa9c4", "#2f6687", "#18324a"]


def sim_panels(name, x, y, level, mid_name, left_title, right_title):
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.9), sharex=True, sharey=True)
    for ax in axes:
        ax.set_facecolor("none")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("X", fontsize=17)
        ax.set_ylabel("Y", fontsize=17)
    # left: ignore the middle variable
    axes[0].scatter(x, y, s=9, color=MUTED, alpha=0.35, lw=0)
    b = np.polyfit(x, y, 1)
    xs = np.linspace(np.percentile(x, 1), np.percentile(x, 99), 10)
    axes[0].plot(xs, np.polyval(b, xs), color=INK, lw=3.5)
    axes[0].set_title(f"{left_title}\none line for everyone: slope {b[0]:+.2f}", fontsize=15, color=INK, loc="left")
    # right: one line within each level
    slopes = []
    for k in range(4):
        m = level == k
        axes[1].scatter(x[m], y[m], s=9, color=LEVEL_COLORS[k], alpha=0.55, lw=0)
        bk = np.polyfit(x[m], y[m], 1)
        slopes.append(bk[0])
        xk = np.linspace(np.percentile(x[m], 5), np.percentile(x[m], 95), 10)
        axes[1].plot(xk, np.polyval(bk, xk), color=LEVEL_COLORS[k], lw=3.5,
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=5.5, foreground="white")])
        axes[1].text(xk[-1], np.polyval(bk, xk[-1]), f" {mid_name}={k + 1}", fontsize=13,
                     color=LEVEL_COLORS[k] if k > 0 else MUTED, va="center", fontweight="bold")
    axes[1].set_title(f"{right_title}\none line per level of {mid_name}: average slope {np.mean(slopes):+.2f}",
                      fontsize=15, color=RUST, loc="left")
    fig.tight_layout(w_pad=3)
    save(fig, name)


def four_levels(v):
    return np.digitize(v, np.quantile(v, [0.25, 0.5, 0.75]))


# chain: X -> M -> Y, M discrete; within a level of M, X tells us nothing about Y
x = rng.normal(size=N)
m = four_levels(x + rng.normal(scale=0.5, size=N))
y = 1.2 * m + rng.normal(scale=0.7, size=N)
sim_panels("sim-chain.svg", x, y, m, "M",
           "Ignore M: X and Y are related", "Control for M: within each level, flat")

# fork: C -> X, C -> Y, no X -> Y
c = rng.integers(0, 4, size=N)
x = 1.2 * c + rng.normal(scale=0.8, size=N)
y = 1.2 * c + rng.normal(scale=0.8, size=N)
sim_panels("sim-fork.svg", x, y, c, "C",
           "Ignore C: X and Y look related", "Control for C: within each level, flat")

# collider: X, Y independent; C = level of X + Y
x = rng.normal(size=N)
y = rng.normal(size=N)
c = four_levels(x + y + rng.normal(scale=0.3, size=N))
sim_panels("sim-collider.svg", x, y, c, "C",
           "Ignore C: X and Y unrelated", "Control for C: within each level, negative")


# ----------------------------------------------------------- COVID collider sim
# Expected values (no sampling noise), matching the arithmetic table on the slide:
# 100,000 people; 20% smoke, 5% have COVID, independently;
# P(hospitalized) = 0.01 + 0.04*smokes + 0.15*covid.
N = 100_000
counts = {}
for sm in (0, 1):
    for cv in (0, 1):
        n = N * (0.20 if sm else 0.80) * (0.05 if cv else 0.95)
        counts[(sm, cv)] = (n, n * (0.01 + 0.04 * sm + 0.15 * cv))
def pct(sm, hosp_only):
    i = 1 if hosp_only else 0
    return 100 * counts[(sm, 1)][i] / (counts[(sm, 1)][i] + counts[(sm, 0)][i])
vals = {
    "Everyone": (pct(1, False), pct(0, False)),
    "Hospitalized only": (pct(1, True), pct(0, True)),
}
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor("none")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
groups = list(vals)
w = 0.34
for i, g in enumerate(groups):
    sm, ns = vals[g]
    ax.bar(i - w / 2, sm, w, color=RUST, label="Smokers" if i == 0 else None)
    ax.bar(i + w / 2, ns, w, color=BLUE, label="Non-smokers" if i == 0 else None)
    ax.text(i - w / 2, sm + 1, f"{sm:.0f}%", ha="center", fontsize=16, color=RUST, fontweight="bold")
    ax.text(i + w / 2, ns + 1, f"{ns:.0f}%", ha="center", fontsize=16, color=BLUE, fontweight="bold")
ax.set_xticks(range(len(groups)))
ax.set_xticklabels(groups, fontsize=17, color=INK)
ax.set_ylabel("Share with COVID (%)", fontsize=15)
ax.set_ylim(0, max(max(v) for v in vals.values()) * 1.25)
ax.legend(frameon=False, fontsize=15, loc="upper left")
save(fig, "sim-covid-collider.svg")
print("COVID sim:", {k: tuple(round(v, 1) for v in t) for k, t in vals.items()})


# ------------------------------------------------------------- HRT comparison
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.set_facecolor("none")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
rows = [
    ("Women's Health Initiative\n(randomized trial, 2002)", 1.29, 1.02, 1.63, RUST),
    ("Nurses' Health Study\n(observational, 1991)", 0.56, 0.40, 0.80, BLUE),
]
for i, (lab, est, lo, hi, col) in enumerate(rows):
    ax.plot([lo, hi], [i, i], color=col, lw=4, solid_capstyle="round")
    ax.plot(est, i, "o", ms=16, color=col)
    ax.text(hi * 1.06, i, f"{est:.2f}", va="center", fontsize=17, color=col, fontweight="bold")
ax.axvline(1, color=MUTED, ls="--", lw=1.5)
ax.set_xscale("log")
ax.set_xticks([0.4, 0.5, 0.7, 1, 1.5, 2])
ax.set_xticklabels(["0.4", "0.5", "0.7", "1", "1.5", "2"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlim(0.35, 2.4)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows], fontsize=15, color=INK)
ax.set_ylim(-0.6, 1.6)
ax.set_xlabel("Risk of coronary heart disease, hormone users vs. non-users (log scale)", fontsize=14)
ax.text(0.37, 1.45, "← lower risk with hormones", fontsize=13, color=MUTED, va="center")
ax.text(2.3, 1.45, "higher risk →", fontsize=13, color=MUTED, ha="right", va="center")
ax.tick_params(axis="y", length=0)
save(fig, "hrt-observational-vs-trial.svg")

print("Wrote figures to", OUT)
