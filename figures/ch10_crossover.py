"""Plot analytical inertial Brownian crossover; no fitted measurements."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch10",
                     "font.size": 12, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
t = np.geomspace(0.003, 200, 800)
msd = 2*(t+np.expm1(-t))
slope = t*(-np.expm1(-t))/(t+np.expm1(-t))
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
axes[0].loglog(t, msd, color="#7bd6d2", lw=2.5, label="Exact thermal-start MSD")
axes[0].loglog(t, t*t, "--", color="#e9bd74", label="Ballistic: u²")
axes[0].loglog(t, 2*t, ":", color="#c9a0e5", label="Diffusive: 2u")
axes[0].set(xlabel="u = γt (dimensionless)", ylabel="γ² MSD / θ",
            ylim=(1e-5, 1000), title="A  One trajectory model, two scales")
axes[0].legend(fontsize=9, facecolor="#172230", labelcolor="#e5edf5")
axes[1].semilogx(t, slope, color="#7bd6d2", lw=2.5)
axes[1].set(xlabel="u = γt (dimensionless)", ylabel="d log(MSD) / d log(t)",
            ylim=(0.95, 2.05), title="B  The exponent changes continuously")
for ax in axes:
    ax.grid(alpha=0.17)
fig.savefig(ROOT / "assets/ch10-crossover.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch10-crossover.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
