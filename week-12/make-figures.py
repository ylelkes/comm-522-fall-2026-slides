"""Generate Week 12 figures: the naive and designed DAGs for the Correll and
Craig & Richeson cases.

Run from anywhere: python3 week-12/make-figures.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)

NAVY, BLUE, RUST, GOLD = "#18324a", "#2f6687", "#b24a3c", "#d5aa55"
INK, PAPER, MUTED, LINE = "#18232d", "#f7f4ee", "#62717d", "#c8c2b7"

plt.rcParams.update({
    "font.family": ["Aptos", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "font.size": 15,
    "svg.fonttype": "none",
})

PREVIEW = Path("/tmp/w12")
PREVIEW.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, format="svg", transparent=True, bbox_inches="tight")
    fig.savefig(PREVIEW / name.replace(".svg", ".png"), dpi=70, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


# ---------------------------------------------------------------- DAG helper (same convention as Week 10)
def dag(ax, nodes, edges, conditioned=(), unobserved=(), box_w=0.26, box_h=0.13, fs=16, title=None):
    """nodes: {key: (x, y, label)}; edges: [(a, b, style)] style in
    {'solid','dashed','causal','bias','faint','cut'}."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    if title:
        ax.text(0.5, 1.0, title, ha="center", va="bottom", fontsize=fs + 2, color=NAVY, fontweight="bold")
    widths, heights = {}, {}
    for k, (x, y, label) in nodes.items():
        w = box_w
        h = box_h + 0.085 * label.count("\n")
        widths[k], heights[k] = w, h
        face, edge, ls, lw = "white", NAVY, "-", 2
        if k in conditioned:
            face, edge, lw = "#f4dfae", RUST, 3.2
        if k in unobserved:
            ls = (0, (4, 3))
            face = PAPER
        box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                             boxstyle="round,pad=0.012,rounding_size=0.025",
                             fc=face, ec=edge, lw=lw, ls=ls, zorder=3)
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=INK, zorder=4, linespacing=1.05)
    colors = {"solid": NAVY, "causal": BLUE, "bias": RUST, "dashed": MUTED, "faint": LINE, "cut": MUTED}
    for a, b, style in edges:
        xa, ya, _ = nodes[a]
        xb, yb, _ = nodes[b]
        dx, dy = xb - xa, yb - ya

        def clip(w, h, dx, dy):
            tx = (w / 2 + 0.014) / abs(dx) if dx else float("inf")
            ty = (h / 2 + 0.014) / abs(dy) if dy else float("inf")
            return min(tx, ty)

        ta = clip(widths[a], heights[a], dx, dy)
        tb = clip(widths[b], heights[b], dx, dy)
        start = (xa + dx * ta, ya + dy * ta)
        end = (xb - dx * tb, yb - dy * tb)
        arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=22,
                              color=colors[style], lw=3 if style in ("causal", "bias") else 2.2,
                              ls="--" if style in ("dashed", "cut") else "-", zorder=2,
                              shrinkA=0, shrinkB=0, alpha=0.45 if style == "cut" else 1)
        ax.add_patch(arr)
        if style == "cut":
            mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
            ax.plot([mx - 0.025, mx + 0.025], [my - 0.025, my + 0.025], color=RUST, lw=3.4, zorder=5)
            ax.plot([mx - 0.025, mx + 0.025], [my + 0.025, my - 0.025], color=RUST, lw=3.4, zorder=5)


def single_dag(name, nodes, edges, size=(9, 4.4), **kw):
    fig, ax = plt.subplots(figsize=size)
    dag(ax, nodes, edges, **kw)
    save(fig, name)


def multi_dag(name, panels, size_per=(4.6, 4.4)):
    """panels: list of (nodes, edges, title, kwargs)."""
    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(size_per[0] * n, size_per[1]))
    if n == 1:
        axes = [axes]
    for ax, (nodes, edges, title, kw) in zip(axes, panels):
        dag(ax, nodes, edges, title=title, **kw)
    save(fig, name)


import numpy as np

# ===================================================================== Mediation recap
single_dag("dag-med-vs-mod.svg",
           {"x": (0.12, 0.3, "Treatment X"), "m": (0.5, 0.82, "Mediator M"), "y": (0.88, 0.3, "Outcome Y")},
           [("x", "m", "causal"), ("m", "y", "causal"), ("x", "y", "causal")], box_w=0.24, size=(8, 3.6))

# ===================================================================== Mutz & Rao: four candidate roles
LIB, LAT = "Liberal\nideology", "Latte\ndrinking"
multi_dag("dag-mutz-four.svg", [
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "z": (0.5, 0.2, "Female")},
     [("z", "i", "bias"), ("z", "l", "bias"), ("i", "l", "dashed")], "Gender: confounder", {"box_w": 0.44, "fs": 13}),
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "z": (0.5, 0.2, "Income")},
     [("z", "i", "bias"), ("z", "l", "bias"), ("i", "l", "dashed")], "Income: confounder", {"box_w": 0.44, "fs": 13}),
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "z": (0.5, 0.2, "Coffee shops\nnearby")},
     [("i", "z", "causal"), ("z", "l", "causal"), ("i", "l", "dashed")], "Availability: mediator?", {"box_w": 0.44, "fs": 13}),
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "z": (0.5, 0.2, "Low\nnationalism")},
     [("i", "z", "causal"), ("z", "l", "causal"), ("i", "l", "dashed")], "Nationalism: mediator?", {"box_w": 0.44, "fs": 13}),
], size_per=(4.2, 3.9))

multi_dag("dag-mutz-nationalism-ambiguous.svg", [
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "z": (0.5, 0.2, "Nationalism")},
     [("i", "z", "causal"), ("z", "l", "causal")], "Mediator", {"box_w": 0.42, "fs": 14}),
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "z": (0.5, 0.2, "Nationalism")},
     [("z", "i", "bias"), ("z", "l", "bias")], "Confounder", {"box_w": 0.42, "fs": 14}),
    ({"i": (0.2, 0.75, LIB), "l": (0.8, 0.75, LAT), "u": (0.5, 0.2, "Cosmopolitan\nworldview")},
     [("u", "i", "bias"), ("u", "l", "bias")], "One worldview, measured twice", {"box_w": 0.42, "fs": 14, "unobserved": ("u",)}),
], size_per=(5.2, 3.9))

# ===================================================================== Petty et al.: moderation
fig, ax = plt.subplots(figsize=(8.5, 3.8))
dag(ax, {"q": (0.15, 0.3, "Argument\nquality"), "a": (0.85, 0.3, "Attitude toward\nexam policy"),
         "inv": (0.5, 0.86, "Personal involvement\n(does the policy affect me?)")},
    [("q", "a", "causal")], box_w=0.36, fs=15)
ax.add_patch(FancyArrowPatch((0.5, 0.72), (0.5, 0.33), arrowstyle="-|>", mutation_scale=22,
                             color=GOLD, lw=3.2, shrinkA=0, shrinkB=0, zorder=2))
ax.text(0.53, 0.52, "changes the size\nof this effect", color=INK, fontsize=13, va="center")
save(fig, "dag-petty-moderation.svg")

def interaction_plot(name, panels):
    fig, axes = plt.subplots(1, len(panels), figsize=(6.2 * len(panels), 4.6), sharey=True)
    for ax, (title, lines) in zip(axes, panels):
        ax.set_facecolor("none")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for label, vals, col in lines:
            ax.plot([0, 1], vals, "-o", color=col, lw=3.5, ms=11)
            ax.text(1.06, vals[1], label, color=col, va="center", fontsize=15, fontweight="bold")
        ax.axhline(0, color=LINE, lw=1)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["Low\ninvolvement", "High\ninvolvement"], fontsize=14)
        ax.set_xlim(-0.25, 1.55)
        ax.set_title(title, fontsize=16, color=NAVY, loc="left")
    axes[0].set_ylabel("Agreement with the policy\n(standardized)", fontsize=14)
    fig.tight_layout(w_pad=3)
    save(fig, name)

# Table 1 cell means averaged over the third factor
interaction_plot("petty-interactions.svg", [
    ("Argument quality matters under HIGH involvement",
     [("Strong arguments", [0.14, 0.625], BLUE), ("Weak arguments", [-0.195, -0.48], RUST)]),
    ("Source expertise matters under LOW involvement",
     [("Expert source", [0.325, 0.13], BLUE), ("Non-expert source", [-0.38, 0.015], RUST)]),
])

# ===================================================================== Natural-experiment toolbox: naive vs design
def pair(name, naive, design, size_per=(6.6, 4.4)):
    fixed = []
    for nodes, edges, title, kw in (naive, design):
        kw = dict(kw)
        kw["box_w"] = 0.36
        kw.setdefault("fs", 14)
        fixed.append((nodes, edges, title, kw))
    multi_dag(name, fixed, size_per=size_per)

# Snow: water supply and cholera
pair("dag-snow.svg",
     ({"p": (0.5, 0.85, "Poverty, crowding,\nneighborhood"), "w": (0.2, 0.2, "Dirty water\nsupplier"), "c": (0.8, 0.2, "Cholera\ndeath")},
      [("p", "w", "bias"), ("p", "c", "bias"), ("w", "c", "dashed")], "Naive: compare neighborhoods", {"box_w": 0.32}),
     ({"p": (0.62, 0.85, "Poverty, crowding,\nneighborhood"), "l": (0.15, 0.85, "Landlord's choice\nyears earlier"),
       "w": (0.2, 0.2, "Dirty water\nsupplier"), "c": (0.8, 0.2, "Cholera\ndeath")},
      [("l", "w", "causal"), ("p", "w", "cut"), ("p", "c", "bias"), ("w", "c", "causal")],
      "Design: suppliers intermixed house by house", {"box_w": 0.3}))

# Lottery (Lindqvist et al.)
pair("dag-lottery.svg",
     ({"u": (0.5, 0.85, "Education, ability,\nconscientiousness"), "x": (0.2, 0.2, "Wealth"), "y": (0.8, 0.2, "Well-being")},
      [("u", "x", "bias"), ("u", "y", "bias"), ("x", "y", "dashed")], "Naive: rich vs. poor", {"box_w": 0.32}),
     ({"u": (0.65, 0.85, "Education, ability,\nconscientiousness"), "z": (0.15, 0.85, "Lottery\nprize"),
       "x": (0.2, 0.2, "Wealth"), "y": (0.8, 0.2, "Well-being")},
      [("z", "x", "causal"), ("u", "x", "cut"), ("u", "y", "bias"), ("x", "y", "causal")],
      "Design: compare winners with matched players", {"box_w": 0.3}))

# RD
pair("dag-rd.svg",
     ({"a": (0.5, 0.85, "Ability / quality"), "t": (0.2, 0.2, "Gets the\nprogram"), "y": (0.8, 0.2, "Later\noutcome")},
      [("a", "t", "bias"), ("a", "y", "bias"), ("t", "y", "dashed")], "Naive: winners vs. losers", {"box_w": 0.3}),
     ({"a": (0.62, 0.86, "Ability / quality"), "s": (0.18, 0.86, "Score near\nthe cutoff"),
       "t": (0.2, 0.18, "Gets the\nprogram"), "y": (0.8, 0.18, "Later\noutcome")},
      [("a", "s", "bias"), ("s", "t", "causal"), ("a", "y", "bias"), ("t", "y", "causal")],
      "Design: compare at (almost) the same score", {"conditioned": ("s",)}))

# IV
pair("dag-iv.svg",
     ({"u": (0.5, 0.85, "Unmeasured\nconfounders U"), "x": (0.2, 0.2, "Treatment X"), "y": (0.8, 0.2, "Outcome Y")},
      [("u", "x", "bias"), ("u", "y", "bias"), ("x", "y", "dashed")], "Naive: X vs. Y", {"box_w": 0.3}),
     ({"u": (0.65, 0.85, "Unmeasured\nconfounders U"), "z": (0.15, 0.85, "Instrument Z\n(random)"),
       "x": (0.2, 0.18, "Treatment X"), "y": (0.8, 0.18, "Outcome Y")},
      [("z", "x", "causal"), ("u", "x", "bias"), ("u", "y", "bias"), ("x", "y", "causal")],
      "Design: use only the part of X that Z moves", {"box_w": 0.28}))

# DiD (staggered rollout, from Weeks 10-11)
pair("dag-did.svg",
     ({"u": (0.5, 0.85, "Place traits\n(wealth, politics)"), "x": (0.2, 0.2, "Gets TV /\npolicy"), "y": (0.8, 0.2, "Outcome")},
      [("u", "x", "bias"), ("u", "y", "bias"), ("x", "y", "dashed")], "Naive: places with vs. without", {"box_w": 0.3}),
     ({"u": (0.65, 0.86, "Stable place traits\n(differenced away)"), "t": (0.15, 0.86, "Timing of\narrival"),
       "x": (0.2, 0.18, "Gets TV /\npolicy"), "y": (0.8, 0.18, "Change in\noutcome")},
      [("t", "x", "causal"), ("u", "x", "faint"), ("u", "y", "cut"), ("x", "y", "causal")],
      "Design: compare changes, not levels", {"box_w": 0.3}))

# ===================================================================== Bol et al.
pair("dag-bol.svg",
     ({"q": (0.5, 0.85, "Talent, proposal\nquality, network"), "g": (0.2, 0.2, "Wins early-\ncareer grant"), "f": (0.8, 0.2, "Later\nfunding")},
      [("q", "g", "bias"), ("q", "f", "bias"), ("g", "f", "dashed")], "Naive: winners vs. losers", {"box_w": 0.32}),
     ({"q": (0.64, 0.86, "Talent, proposal\nquality, network"), "r": (0.16, 0.86, "Rank near the\nthreshold"),
       "g": (0.2, 0.18, "Wins early-\ncareer grant"), "f": (0.8, 0.18, "Later\nfunding")},
      [("q", "r", "bias"), ("r", "g", "causal"), ("q", "f", "bias"), ("g", "f", "causal")],
      "Design: compare at (almost) the same rank", {"conditioned": ("r",)}))

single_dag("dag-bol-mechanism.svg",
           {"g": (0.13, 0.3, "Wins early-\ncareer grant"), "s": (0.5, 0.82, "Status signal /\nreviewers' view"),
            "a": (0.5, 0.3, "Applies for\nmid-career grant"), "w": (0.87, 0.3, "Wins mid-\ncareer grant")},
           [("g", "a", "causal"), ("a", "w", "causal"), ("g", "s", "causal"), ("s", "w", "causal")],
           box_w=0.24, size=(10, 3.8))

# ===================================================================== Balcells & Torrats-Espinosa
pair("dag-balcells.svg",
     ({"c": (0.5, 0.85, "Conflict intensity,\nregion, politics"), "a": (0.2, 0.2, "Attack where /\nwhen you live"), "v": (0.8, 0.2, "Intends\nto vote")},
      [("c", "a", "bias"), ("c", "v", "bias"), ("a", "v", "dashed")], "Naive: places or years with attacks", {}),
     ({"c": (0.72, 0.88, "Conflict intensity,\nregion, politics"), "s": (0.2, 0.88, "Interview date vs.\nattack date"),
       "a": (0.2, 0.45, "Interviewed\nafter attack"), "v": (0.8, 0.45, "Intends\nto vote"),
       "r": (0.5, 0.08, "Hard to reach?\n(interviewed late)")},
      [("s", "a", "causal"), ("c", "a", "cut"), ("c", "v", "bias"), ("a", "v", "causal"), ("r", "a", "dashed"), ("r", "v", "dashed")],
      "Design: same survey, same province, before vs. after", {"unobserved": ("r",)}))

# ===================================================================== Maimonides' rule (Angrist & Lavy 1999)
E = np.arange(1, 201)
W = E / (np.floor((E - 1) / 40) + 1)
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.set_facecolor("none")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.plot(E, W, color=BLUE, lw=3)
for c in (40, 80, 120, 160):
    ax.axvline(c + 0.5, color=LINE, lw=1.2, ls="--")
ax.annotate("41st student:\ntwo classes of 20.5", xy=(41, 20.5), xytext=(52, 6),
            fontsize=13, color=RUST, arrowprops=dict(arrowstyle="->", color=RUST, lw=1.8))
ax.set_xlabel("Grade enrollment at the school", fontsize=14)
ax.set_ylabel("Predicted class size", fontsize=14)
ax.set_ylim(0, 44)
ax.set_xticks([0, 40, 80, 120, 160, 200])
save(fig, "maimonides-rule.svg")

# ===================================================================== Not every natural experiment: Connecticut crackdown
# Data: fastR2::Traffic (Campbell & Ross 1968): CT deaths and deaths per 100,000 for CT, NY, MA, RI, 1951-59
yrs = np.arange(1951, 1960)
ct_deaths = [265, 230, 275, 240, 325, 280, 273, 248, 245]
rates = {"Connecticut": [13.0, 10.8, 12.8, 10.8, 14.0, 12.1, 11.9, 10.1, 10.0],
         "New York": [13.9, 13.8, 14.4, 13.0, 13.5, 13.4, 13.3, 13.0, 12.9],
         "Massachusetts": [10.2, 10.0, 11.0, 10.5, 11.8, 11.0, 10.2, 11.8, 11.0],
         "Rhode Island": [8.0, 8.5, 8.5, 7.5, 10.0, 8.2, 9.4, 8.6, 9.0]}

def style(ax):
    ax.set_facecolor("none")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

fig, ax = plt.subplots(figsize=(5.2, 4.4)); style(ax)
ax.plot([1955, 1956], [325, 280], "-o", color=RUST, lw=4, ms=12)
for x, y in [(1955, 325), (1956, 280)]:
    ax.text(x, y + 7, f"{y}", ha="center", fontsize=16, color=RUST, fontweight="bold")
ax.set_xticks([1955, 1956]); ax.set_xlim(1954.6, 1956.4); ax.set_ylim(200, 350)
ax.set_ylabel("Traffic deaths in Connecticut", fontsize=14)
ax.set_title("Before vs. after the crackdown", fontsize=15, color=NAVY, loc="left")
save(fig, "ct-two-point.svg")

fig, ax = plt.subplots(figsize=(8.5, 4.4)); style(ax)
ax.plot(yrs, ct_deaths, "-o", color=RUST, lw=3.5, ms=9)
ax.axvline(1955.5, color=MUTED, ls="--", lw=1.5)
ax.text(1955.55, 335, "crackdown\n(Dec. 1955)", fontsize=12, color=MUTED, va="top")
ax.annotate("1955: a record\nbad year", xy=(1955, 325), xytext=(1952.3, 320), fontsize=13, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.5))
ax.set_ylim(200, 345); ax.set_xticks(yrs)
ax.set_ylabel("Traffic deaths in Connecticut", fontsize=14)
ax.set_title("The full series: 1956 looks like a return to normal", fontsize=15, color=NAVY, loc="left")
save(fig, "ct-series.svg")

fig, ax = plt.subplots(figsize=(8.5, 4.4)); style(ax)
cols = {"Connecticut": RUST, "New York": BLUE, "Massachusetts": GOLD, "Rhode Island": MUTED}
for k, v in rates.items():
    ax.plot(yrs, v, "-o", color=cols[k], lw=3.5 if k == "Connecticut" else 2.2, ms=7 if k == "Connecticut" else 5)
    ax.text(1959.15, v[-1], k, color=cols[k], fontsize=13, va="center", fontweight="bold" if k == "Connecticut" else "normal")
ax.axvline(1955.5, color=MUTED, ls="--", lw=1.5)
ax.set_xticks(yrs); ax.set_xlim(1950.6, 1960.6)
ax.set_ylabel("Deaths per 100,000", fontsize=14)
ax.set_title("Neighboring states also spiked in 1955", fontsize=15, color=NAVY, loc="left")
save(fig, "ct-states.svg")

# ===================================================================== UN peacekeeping: matching on measured variables
pair("dag-un.svg",
     ({"u": (0.5, 0.86, "Conflict severity\n(partly unmeasured)"), "m": (0.2, 0.2, "UN mission\nsent"), "p": (0.8, 0.2, "Lasting\npeace")},
      [("u", "m", "bias"), ("u", "p", "bias"), ("m", "p", "dashed")], "Naive: missions vs. no missions", {}),
     ({"o": (0.22, 0.86, "Measured: war length,\nethnic divisions"), "u": (0.78, 0.86, "Unmeasured: elite\ndeals, outside powers"),
       "m": (0.2, 0.18, "UN mission\nsent"), "p": (0.8, 0.18, "Lasting\npeace")},
      [("o", "m", "cut"), ("o", "p", "faint"), ("u", "m", "bias"), ("u", "p", "bias"), ("m", "p", "dashed")],
      "Matching closes only the measured back door", {"conditioned": ("o",), "unobserved": ("u",)}))

# ===================================================================== As-if random: daughters, earthquake
single_dag("dag-daughters.svg",
           {"n": (0.14, 0.82, "Chance at\nconception"), "d": (0.14, 0.2, "# of daughters\n(given # children)"),
            "v": (0.86, 0.2, "Votes on\nwomen's issues"), "p": (0.62, 0.82, "Legislator's own\nviews, party"),
            "s": (0.38, 0.52, "Stopping rule?\n(try for a son)")},
           [("n", "d", "causal"), ("d", "v", "causal"), ("p", "v", "bias"), ("p", "s", "dashed"), ("s", "d", "dashed")],
           box_w=0.28, size=(10, 4.6), unobserved=("s",))

single_dag("dag-earthquake.svg",
           {"t": (0.14, 0.82, "Answered before vs.\nafter March 11, 2011"), "q": (0.14, 0.2, "Experienced\nthe quake"),
            "y": (0.86, 0.2, "Life\nsatisfaction"), "w": (0.6, 0.82, "Who answers early\nvs. late?")},
           [("t", "q", "causal"), ("q", "y", "causal"), ("w", "t", "dashed"), ("w", "y", "dashed")],
           box_w=0.27, size=(10, 4.4), unobserved=("w",))

# Week 12 version of the Craig & Richeson Study 3 DAG: random assignment
# feeds both the racial-shift information and the reassurance paragraph.
single_dag(
    "dag-racial-shift-full.svg",
    {
        "rand": (0.1, 0.5, "Random\nassignment"),
        "info": (0.38, 0.84, "Racial-shift\ninformation"),
        "assuage": (0.38, 0.2, "+ “status will\nstay stable”\nparagraph"),
        "threat": (0.66, 0.5, "Status\nthreat"),
        "con": (0.9, 0.5, "Conservatism"),
    },
    [
        ("rand", "info", "causal"),
        ("rand", "assuage", "causal"),
        ("info", "threat", "causal"),
        ("threat", "con", "causal"),
        ("assuage", "threat", "cut"),
    ],
    box_w=0.16,
    fs=14,
    size=(13, 5.6),
)
