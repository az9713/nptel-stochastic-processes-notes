"""Identical single-time laws can hide different temporal persistence."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch05", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(202611085)
steps = np.arange(45)
iid = rng.choice([-1, 1], size=len(steps))
persistent = np.ones(len(steps))
for j in range(1, len(steps)):
    persistent[j] = persistent[j-1] * (-1 if rng.random() < .1 else 1)
fig, axes = plt.subplots(3, 1, figsize=(8, 8.2), layout="constrained")
axes[0].step(steps, iid, where="post", color="#65c6ff")
axes[1].step(steps, persistent, where="post", color="#ffc471")
axes[0].set(title="A. Independent signs, equal one-time probabilities")
axes[1].set(title="B. Persistent signs, the same stationary marginal law")
for ax in axes[:2]:
    ax.set(xlabel="Discrete time index", ylabel="Observed sign", yticks=[-1, 1],
           ylim=(-1.4, 1.4))
lags = np.arange(16)
axes[2].plot(lags, .8**lags, "o-", color="#ffc471", label="Persistent: 0.8ᵏ")
axes[2].plot(lags, (lags == 0).astype(float), "o-", color="#65c6ff", label="Independent")
axes[2].set(title="C. Exact stationary correlations distinguish the mechanisms",
            xlabel="Lag k (time steps)", ylabel="E[XₙXₙ₊ₖ]")
axes[2].legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
for ax in axes:
    ax.grid(alpha=.15)
fig.savefig(root / "assets/ch05-markov.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch05-markov.png", dpi=150)
