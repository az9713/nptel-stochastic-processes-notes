"""Stationary tails and normalization at the birth/death ratio threshold."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch08", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(2, 1, figsize=(8, 7), layout="constrained")
n = np.arange(101)
for q, color in ((.4, "#65c6ff"), (.8, "#ffc471"), (.98, "#84e0bd")):
    axes[0].semilogy(n, (1-q)*q**n, color=color, label=f"q = {q}")
axes[0].set(title="A. Normalized stationary tails broaden as q approaches one",
            xlabel="Population or height index n", ylabel="Stationary mass πₙ", ylim=(1e-6, 1))
for q, color in ((.8, "#65c6ff"), (1, "#ffc471"), (1.02, "#e5a1ee")):
    weights = q**n
    axes[1].semilogy(n, np.cumsum(weights), color=color, label=f"q = {q}")
axes[1].set(title="B. Formal weights require a finite normalization sum",
            xlabel="Upper cutoff M", ylabel="Sum of weights from 0 to M")
for ax in axes:
    ax.grid(alpha=.15)
    ax.legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
fig.savefig(root / "assets/ch08-equilibrium.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch08-equilibrium.png", dpi=150)
