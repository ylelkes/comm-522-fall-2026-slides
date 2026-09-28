"""Recreate the two teaching charts. Requires matplotlib; not a render hook."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

base = Path(__file__).resolve().parent / "assets"
base.mkdir(exist_ok=True)
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 18, "text.color": "#18232d", "axes.labelcolor": "#18232d",
    "xtick.color": "#18232d", "ytick.color": "#18232d",
    "svg.fonttype": "none", "figure.facecolor": "#f7f4ee", "axes.facecolor": "#f7f4ee",
})
# Source: Paxton (2000), pp. 100–102. Categories have revised period boundaries.
original = [30, 25, 19]
revised = [16, 34, 7]
y = np.arange(3)
fig, ax = plt.subplots(figsize=(13.6, 4.8))
ax.barh(y-.19, original, height=.32, color="#18324a", label="Original account")
ax.barh(y+.19, revised, height=.32, color="#2f7a63", label="Paxton's revision")
for i, (a, b) in enumerate(zip(original, revised)):
    ax.text(a+.5, i-.19, str(a), va="center", fontweight="bold")
    ax.text(b+.5, i+.19, str(b), va="center", fontweight="bold")
ax.set_yticks(y, ["First wave", "Second wave", "First reverse wave"])
ax.invert_yaxis()
ax.set_xlim(0, 39)
ax.set_xticks([0, 10, 20, 30])
ax.set_xlabel("Number of countries")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0, pad=15)
ax.legend(loc="lower right", frameon=False, fontsize=16)
fig.tight_layout(pad=1)
fig.savefig(base/"paxton-waves.svg")
plt.close(fig)

fig, axes = plt.subplots(2,1,figsize=(13.6,4.8),sharex=True)
for ax, values, label, color in zip(axes, ([30]*5,[0,0,10,20,120]), ("Group A", "Group B"), ("#18324a","#2f7a63")):
    levels = {}
    heights=[]
    for v in values:
        levels[v]=levels.get(v,0)+1
        heights.append(levels[v])
    ax.scatter(values, heights, s=190, color=color, zorder=3)
    ax.axvline(30, color="#ad8338", linestyle="--", linewidth=2, zorder=1)
    ax.set_yticks([])
    ax.set_ylim(0, 5.8)
    ax.set_ylabel(label, rotation=0, labelpad=60, va="center", fontweight="bold")
    ax.spines[["top","right","left"]].set_visible(False)
axes[0].text(34,4.8,"Mean = 30",color="#826124",fontsize=17)
axes[1].set_xlim(-5,130)
axes[1].set_xticks([0,10,20,30,60,90,120])
axes[1].set_xlabel("Qualifying minutes in one day")
fig.tight_layout(pad=1)
fig.savefig(base/"use-distributions.svg")
plt.close(fig)
