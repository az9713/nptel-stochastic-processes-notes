"""Original velocity/energy comparison in reduced units, with both branches."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma, norm

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch02", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
fig, axes = plt.subplots(2, 1, figsize=(8, 7.2), layout="constrained")
velocity = np.linspace(-3.5, 3.5, 600)
axes[0].plot(velocity, norm.pdf(velocity), color="#65c6ff", lw=2)
for location in (-np.sqrt(2), np.sqrt(2)):
    axes[0].axvline(location, color="#ffc471", ls="--", lw=1)
axes[0].set_xticks([-3, -np.sqrt(2), 0, np.sqrt(2), 3],
                  ["−3", "−√2", "0", "+√2", "3"])
axes[0].set(xlabel="Velocity v / √(kBT/m)", ylabel="Reduced velocity density",
            title="A. The marked velocities both give reduced energy E = 1")
energy = np.linspace(.012, 5, 700)
for dimension, color in ((1, "#ffc471"), (3, "#84e0bd")):
    axes[1].plot(energy, gamma.pdf(energy, dimension/2), lw=2,
                 label=f"d = {dimension}", color=color)
axes[1].set(xlabel="Energy E / (kBT)", ylabel="Reduced energy density",
            ylim=(0, 1.4), title="B. Counting quadratic coordinates changes the shape")
axes[1].legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
for ax in axes:
    ax.grid(alpha=.15)
fig.savefig(root / "assets/ch02-energy.svg", metadata={"Date": None})
preview = root / "work/validation/ch02-energy.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=150)
