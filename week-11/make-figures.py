"""Generate Week 11 figures: the naive and designed DAGs for the Correll and
Craig & Richeson cases.

Run from anywhere: python3 week-11/make-figures.py
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

PREVIEW = Path("/tmp/w11")
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


# ===================================================================== Correll
single_dag(
    "dag-motherhood-naive.svg",
    {
        "prod": (0.5, 0.85, "Productivity /\nhuman capital\n(mostly unmeasured)"),
        "mom": (0.2, 0.2, "Is a mother"),
        "wage": (0.8, 0.2, "Wages"),
    },
    [("prod", "mom", "bias"), ("prod", "wage", "bias"), ("mom", "wage", "dashed")],
    box_w=0.32,
)

multi_dag(
    "dag-discrimination-compare.svg",
    [
        (
            {
                "prod": (0.5, 0.85, "Actual\nproductivity"),
                "mom": (0.2, 0.2, "Mother\nlabel"),
                "eval": (0.8, 0.2, "Evaluation"),
            },
            [("prod", "mom", "faint"), ("prod", "eval", "causal"), ("mom", "eval", "cut")],
            "Statistical discrimination",
            {"box_w": 0.3},
        ),
        (
            {
                "prod": (0.5, 0.85, "Actual\nproductivity\n(held equal)"),
                "mom": (0.2, 0.2, "Mother\nlabel"),
                "eval": (0.8, 0.2, "Evaluation"),
            },
            [("prod", "eval", "faint"), ("mom", "eval", "bias")],
            "Status-based discrimination",
            {"box_w": 0.3, "conditioned": ("prod",)},
        ),
    ],
)

single_dag(
    "dag-motherhood-randomized.svg",
    {
        "rand": (0.12, 0.85, "Random\nassignment"),
        "prod": (0.5, 0.85, "Actual\nproductivity\n(fixed equal\nwithin pair)"),
        "mom": (0.3, 0.2, "Mother\nlabel"),
        "eval": (0.82, 0.2, "Evaluation"),
    },
    [("rand", "mom", "causal"), ("prod", "mom", "cut"), ("prod", "eval", "faint"), ("mom", "eval", "bias")],
    box_w=0.28,
    conditioned=("prod",),
    size=(10.5, 4.6),
)

# ===================================================================== Craig & Richeson
multi_dag(
    "dag-racial-shift-candidates.svg",
    [
        (
            {
                "con": (0.2, 0.8, "Already\nconservative"),
                "shift": (0.8, 0.8, "Notices /\nreports shift"),
            },
            [("con", "shift", "bias")],
            "Reverse causation",
            {"box_w": 0.34, "fs": 15},
        ),
        (
            {
                "reg": (0.5, 0.85, "Region\n(economy,\nurbanicity)"),
                "shift": (0.2, 0.2, "Racial\ncomposition\nchange"),
                "con": (0.8, 0.2, "Conservatism"),
            },
            [("reg", "shift", "bias"), ("reg", "con", "bias"), ("shift", "con", "dashed")],
            "Regional confounder",
            {"box_w": 0.3, "fs": 15},
        ),
        (
            {
                "shift": (0.17, 0.5, "Racial-shift\ninfo"),
                "threat": (0.5, 0.5, "Status\nthreat"),
                "con": (0.83, 0.5, "Conser-\nvatism"),
            },
            [("shift", "threat", "causal"), ("threat", "con", "causal")],
            "Direct causal chain",
            {"box_w": 0.17, "fs": 14},
        ),
    ],
    size_per=(4.9, 4.6),
)

single_dag(
    "dag-racial-shift-full.svg",
    {
        "rand": (0.06, 0.82, "Random\nassignment"),
        "info": (0.3, 0.82, "Racial-shift\ninformation"),
        "assuage": (0.3, 0.18, "+ “status will\nstay stable”\nparagraph"),
        "threat": (0.58, 0.5, "Status\nthreat"),
        "con": (0.86, 0.5, "Conservatism"),
    },
    [
        ("rand", "info", "causal"),
        ("info", "threat", "causal"),
        ("threat", "con", "causal"),
        ("assuage", "threat", "cut"),
    ],
    box_w=0.21,
    fs=14,
    size=(13, 5),
)

# ===================================================================== extra practice DAGs
single_dag(
    "dag-practice-sleep.svg",
    {
        "stress": (0.5, 0.85, "Stress\n(before term)"),
        "sleep": (0.15, 0.2, "Hours of\nsleep"),
        "att": (0.5, 0.2, "Class\nattendance"),
        "gpa": (0.85, 0.2, "GPA"),
    },
    [
        ("stress", "sleep", "bias"),
        ("stress", "gpa", "bias"),
        ("sleep", "att", "causal"),
        ("att", "gpa", "causal"),
    ],
    box_w=0.26,
    fs=15,
    size=(10.5, 4.6),
)

single_dag(
    "dag-practice-doctor-collider.svg",
    {
        "ex": (0.18, 0.75, "Exercise\nhabits"),
        "mh": (0.82, 0.75, "Mental\nhealth"),
        "doc": (0.5, 0.2, "Visited a\ndoctor"),
    },
    [("ex", "doc", "solid"), ("mh", "doc", "solid"), ("ex", "mh", "dashed")],
    conditioned=("doc",),
    box_w=0.26,
    size=(9.5, 4.4),
)

# ===================================================================== mediation vs. moderation (Druckman, Part 2)
single_dag(
    "dag-mediation.svg",
    {
        "x": (0.12, 0.25, "X"),
        "m": (0.5, 0.78, "M\n(mechanism)"),
        "y": (0.88, 0.25, "Y"),
    },
    [("x", "m", "causal"), ("m", "y", "causal"), ("x", "y", "faint")],
    box_w=0.22,
    fs=17,
    size=(7.6, 4.6),
)

fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
xw, xh = 0.22, 0.14
for (key, xc, label) in [("x", 0.12, "X"), ("y", 0.88, "Y")]:
    box = FancyBboxPatch((xc - xw / 2, 0.25 - xh / 2), xw, xh,
                         boxstyle="round,pad=0.012,rounding_size=0.025",
                         fc="white", ec=NAVY, lw=2, zorder=3)
    ax.add_patch(box)
    ax.text(xc, 0.25, label, ha="center", va="center", fontsize=17, color=INK, zorder=4)
arr = FancyArrowPatch((0.12 + xw / 2 + 0.014, 0.25), (0.88 - xw / 2 - 0.014, 0.25),
                      arrowstyle="-|>", mutation_scale=22, color=BLUE, lw=3, zorder=2)
ax.add_patch(arr)
zw, zh = 0.24, 0.16
zbox = FancyBboxPatch((0.5 - zw / 2, 0.78 - zh / 2), zw, zh,
                      boxstyle="round,pad=0.012,rounding_size=0.025",
                      fc="white", ec=RUST, lw=2.4, zorder=3)
ax.add_patch(zbox)
ax.text(0.5, 0.78, "Z\n(moderator)", ha="center", va="center", fontsize=17, color=INK, zorder=4, linespacing=1.05)
zarr = FancyArrowPatch((0.5, 0.78 - zh / 2 - 0.014), (0.5, 0.25 + 0.025),
                       arrowstyle="-|>", mutation_scale=20, color=RUST, lw=2.6,
                       ls=(0, (4, 3)), zorder=2)
ax.add_patch(zarr)
save(fig, "dag-moderation.svg")

# ===================================================================== SUTVA / independence / exclusion violations
single_dag(
    "dag-independence-violation.svg",
    {
        "control": (0.5, 0.88, "Self-control /\nmotivation"),
        "assign": (0.1, 0.5, "Randomly\nassigned to\ndeactivate?"),
        "comply": (0.5, 0.18, "Actually\ndeactivated\n(compliance)"),
        "dep": (0.9, 0.5, "Depression"),
    },
    [("assign", "comply", "causal"), ("control", "comply", "bias"), ("control", "dep", "bias"), ("comply", "dep", "dashed")],
    box_w=0.26,
    fs=14,
    size=(10.5, 4.8),
)

single_dag(
    "dag-sutva-violation.svg",
    {
        "assignA": (0.14, 0.85, "A assigned:\ndeactivate"),
        "useA": (0.14, 0.5, "A's own\nuse"),
        "depA": (0.14, 0.15, "A's\ndepression"),
        "assignB": (0.86, 0.85, "B assigned:\ncontinue as normal"),
        "depB": (0.86, 0.15, "B's\ndepression"),
    },
    [
        ("assignA", "useA", "causal"), ("useA", "depA", "causal"),
        ("assignB", "depB", "faint"),
        ("useA", "depB", "bias"),
    ],
    box_w=0.28,
    fs=14,
    size=(11, 4.8),
)

single_dag(
    "dag-exclusion-violation.svg",
    {
        "assign": (0.12, 0.5, "Random\nassignment"),
        "use": (0.5, 0.82, "Actual social\nmedia use"),
        "aware": (0.5, 0.18, "Awareness of\nbeing studied"),
        "dep": (0.88, 0.5, "Depression"),
    },
    [("assign", "use", "causal"), ("use", "dep", "causal"), ("assign", "aware", "bias"), ("aware", "dep", "bias")],
    box_w=0.26,
    fs=15,
    size=(10.5, 4.6),
)

print(f"Wrote figures to {OUT}")
