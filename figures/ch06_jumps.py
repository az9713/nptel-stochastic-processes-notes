"""Two-state relaxation and a synthetic event-count trajectory."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch06", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(2, 1, figsize=(8, 7), layout="constrained")
t = np.linspace(0, 3, 500)
axes[0].plot(t, 1/3+2/3*np.exp(-3*t), color="#65c6ff", label="P₁₁(t), rates 2 and 1")
axes[0].plot(t, np.exp(-3*t), color="#ffc471", label="C(t) / C(0)")
axes[0].axhline(1/3, color="#b8cadb", ls="--", label="Stationary probability 1/3")
axes[0].set(xlabel="Time t (s)", ylabel="Probability or normalized covariance",
            title="A. Conditional probability has a plateau; covariance decays to zero")
rng = np.random.default_rng(202611086)
arrivals = np.cumsum(rng.exponential(.5, 50))
arrivals = arrivals[arrivals < 6]
times = np.r_[0, arrivals, 6]
values = np.r_[0, np.arange(1, len(arrivals)+1), len(arrivals)]
axes[1].step(times, values, where="post", color="#84e0bd", lw=2, label="One realization")
axes[1].plot(t*2, 4*t, "--", color="#ffc471", label="Mean count 2t")
axes[1].set(xlabel="Time t (s)", ylabel="Number of arrivals N(t)",
            title="B. A Poisson count increases, despite stationary increments")
for ax in axes:
    ax.grid(alpha=.15)
    ax.legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
fig.savefig(root / "assets/ch06-jumps.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch06-jumps.png", dpi=150)
