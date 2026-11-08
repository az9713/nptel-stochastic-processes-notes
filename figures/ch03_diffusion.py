"""Exact central-limit densities and parity-aware lattice masses."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, irwinhall, norm

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch03", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(2, 1, figsize=(8, 7.2), layout="constrained")
z = np.linspace(-4, 4, 800)
for n, color in ((1, "#ffc471"), (2, "#65c6ff"), (8, "#84e0bd")):
    scale = np.sqrt(n/12)
    axes[0].plot(z, scale*irwinhall(n).pdf(n/2+scale*z),
                 label=f"n = {n}", color=color, lw=2)
axes[0].plot(z, norm.pdf(z), "--", color="#e5a1ee", label="Gaussian", lw=2)
axes[0].set(title="A. Centered uniform sums, each rescaled to variance one",
            xlabel="Standardized sum z", ylabel="Probability density")
n = 20
location = (2*np.arange(n+1)-n)/np.sqrt(n)
axes[1].plot(location, binom.pmf(np.arange(n+1), n, .5)*np.sqrt(n)/2,
             "o", color="#65c6ff", label="Mass / (2 / √n)")
axes[1].plot(z, norm.pdf(z), color="#ffc471", label="Gaussian density", lw=2)
axes[1].set(title="B. A lattice comparison must use the reachable spacing",
            xlabel="Normalized displacement (n = 20)", ylabel="Mass per reachable spacing")
for ax in axes:
    ax.grid(alpha=.15)
    ax.legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
fig.savefig(root / "assets/ch03-diffusion.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch03-diffusion.png", dpi=150)
