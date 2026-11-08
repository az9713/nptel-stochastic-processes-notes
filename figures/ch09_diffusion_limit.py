"""Diffusion approximation at shrinking lattice spacing and conserved flux."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, skellam

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch09", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(2, 1, figsize=(8, 7), layout="constrained")
drift, diffusion, time = .7, .4, 1.
x = np.linspace(-2.5, 4, 700)
axes[0].plot(x, norm.pdf(x, drift*time, np.sqrt(2*diffusion*time)),
             color="#ffc471", lw=2, label="Continuum Gaussian")
for ell, color in ((.5, "#65c6ff"), (.125, "#84e0bd")):
    rplus, rminus = diffusion/ell**2+drift/(2*ell), diffusion/ell**2-drift/(2*ell)
    j = np.arange(int(-2.5/ell), int(4/ell)+1)
    axes[0].plot(ell*j, skellam.pmf(j, rplus*time, rminus*time)/ell,
                 "o", ms=3, color=color, label=f"Lattice mass / ℓ, ℓ={ell}")
axes[0].set(title="A. Shrinking jumps retain drift0.7 and diffusion0.4",
            xlabel="Position x (m), time1s", ylabel="Density or mass per spacing (1/m)")
x = np.linspace(0, 4, 400)
rho = np.exp(-x)
axes[1].plot(x, -rho, color="#65c6ff", label="Downward drift current −ρ")
axes[1].plot(x, rho, color="#ffc471", label="Upward diffusion current −ρ′")
axes[1].plot(x, np.zeros_like(x), "--", color="#84e0bd", label="Total current0")
axes[1].set(title="B. Reflecting equilibrium balances currents, not their separate parts",
            xlabel="Height x (reduced units)", ylabel="Probability current (reduced units)")
for ax in axes:
    ax.grid(alpha=.15)
    ax.legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
fig.savefig(root / "assets/ch09-diffusion-limit.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch09-diffusion-limit.png", dpi=150)
