"""Rotating correlations and transverse diffusion suppression."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch15",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
t = np.linspace(0, 5, 600)
axes[0].plot(t, np.exp(-t)*np.cos(4*t), color="#7bd6d2", label="Cₓₓ(t) / θ")
axes[0].plot(t, np.exp(-t)*np.sin(4*t), color="#e9bd74", label="Cₓᵧ(t) / θ")
axes[0].plot(t, np.exp(-t), "--", color="#c9a0e5", label="Czz(t) / θ")
axes[0].set(xlabel="γt", ylabel="Normalized lag covariance",
            title="A  Signed rotation creates cross-correlations")
w = np.linspace(0, 10, 500)
axes[1].plot(w, 1/(1+w*w), color="#7bd6d2", label="D⊥ / D∥")
axes[1].plot(w, np.ones_like(w), "--", color="#c9a0e5", label="D∥ / D∥")
axes[1].set(xlabel="Cyclotron magnitude ωc / γ", ylabel="Diffusion ratio",
            title="B  Thermal speed stays fixed; transport changes")
for ax in axes:
    ax.grid(alpha=0.17)
    ax.legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
fig.savefig(ROOT / "assets/ch15-magnetic.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch15-magnetic.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
