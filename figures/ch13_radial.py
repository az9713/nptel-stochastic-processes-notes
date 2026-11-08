"""Noise-induced radial drift and the missing squared-radius drift."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch13",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
r = np.linspace(.15, 3, 500)
for dim, color in [(2, "#e9bd74"), (3, "#7bd6d2")]:
    axes[0].plot(r, .5*(dim-1)/r, color=color, label=f"Dimension d = {dim}")
axes[0].set(xlabel="Radius R (dimensionless)", ylabel="Radial drift D(d−1) / R",
            title="A  Cartesian unbiasedness allows radial drift")
t = np.linspace(0, 2, 200)
axes[1].plot(t, 3*t, color="#7bd6d2", label="Correct Itô result: 3t")
axes[1].plot(t, 2*t, "--", color="#e9bd74", label="Ordinary-chain-rule error: 2t")
axes[1].set(xlabel="Time (dimensionless)", ylabel="Mean squared radius E[Z(t)]",
            title="B  Squaring radius adds the missing drift")
for ax in axes:
    ax.grid(alpha=0.17)
    ax.legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
fig.savefig(ROOT / "assets/ch13-radial.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch13-radial.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
