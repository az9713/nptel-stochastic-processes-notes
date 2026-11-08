"""Contrast population-dependent rates with a deterministic time-dependent rate."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch07", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(2, 1, figsize=(8, 7), layout="constrained")
t = np.linspace(0, 2, 500)
mean = np.exp(.8*t)
axes[0].plot(t, mean, color="#65c6ff", label="Mean E[N(t)]")
axes[0].plot(t, np.sqrt(mean*(mean-1)), color="#ffc471", label="Standard deviation")
axes[0].set(title="A. Birth rate 0.8n grows with the present population",
            xlabel="Time t (s)", ylabel="Population count")
integrated = np.where(t < 1, 2*t, 2+6*(t-1))
axes[1].plot(t, integrated, color="#84e0bd", label="Mean = variance = integrated rate")
axes[1].axvline(1, color="#b8cadb", ls="--", label="Rate changes from 2 to 6 per second")
axes[1].set(title="B. Deterministic rate changes produce a nonhomogeneous Poisson clock",
            xlabel="Time t (s)", ylabel="Integrated intensity Λ(t)")
for ax in axes:
    ax.grid(alpha=.15)
    ax.legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
fig.savefig(root / "assets/ch07-populations.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch07-populations.png", dpi=150)
