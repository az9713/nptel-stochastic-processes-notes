"""Stationary position correlations across the damping regimes."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch11",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
colors = ["#7bd6d2", "#e9bd74", "#c9a0e5"]
for gamma, color in zip([0.5, 2., 10.], colors):
    u = np.linspace(0, 5, 500)
    a = np.array([[0., 1.], [-1., -gamma]])
    corr = [expm(a*gamma*x)[0, 0] for x in u]
    axes[0].plot(u, corr, color=color, label=f"γ/ω₀ = {gamma:g}")
axes[0].plot(u, np.exp(-u), "--", color="white", label="Overdamped reduction")
axes[0].set(xlabel="Slow time: ω₀²t / γ", ylabel="Cₓ(t) / Cₓ(0)",
            title="A  Equilibrium alone hides dynamical error")
g = np.geomspace(0.05, 20, 600)
disc = np.sqrt(g*g-4+0j)
axes[1].loglog(g, np.abs((-g+disc)/2), color="#7bd6d2", label="Root magnitude: r₊")
axes[1].loglog(g, np.abs((-g-disc)/2), color="#e9bd74", label="Root magnitude: r₋")
axes[1].loglog(g, 1/g, ":", color="white", label="Slow estimate: ω₀²/γ")
axes[1].set(xlabel="γ / ω₀", ylabel="Relaxation-root magnitude / ω₀",
            title="B  Rate separation requires high friction")
for ax in axes:
    ax.grid(alpha=0.17)
    ax.legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
fig.savefig(ROOT / "assets/ch11-relaxation.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch11-relaxation.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
