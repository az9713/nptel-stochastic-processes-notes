"""OU covariance and spectra, showing raw versus averaged periodograms."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "code/ch16-results.json").read_text())
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch16",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
t = np.linspace(-6, 6, 500)
axes[0].plot(t, np.exp(-abs(t)), color="#7bd6d2", lw=2)
axes[0].set(xlabel="Lag γτ", ylabel="C(τ) / θ",
            title="A  Exponential covariance has area 2θ / γ")
w = np.array(d["plot_omega"])
axes[1].loglog(w, d["plot_single_spectrum"], color="#8795a5", lw=.65,
               alpha=.7, label="One record")
axes[1].loglog(w, d["plot_ensemble_spectrum"], color="#7bd6d2", lw=1.5,
               label="Mean of 1,024 records")
axes[1].loglog(w, 2/(1+w*w), "--", color="#e9bd74", label="Continuous Lorentzian")
r, h = np.exp(-d["h"]), d["h"]
axes[1].loglog(w, h*(1-r*r)/(1+r*r-2*r*np.cos(w*h)), ":",
               color="#c9a0e5", label="Exact sampled spectrum")
axes[1].set(xlabel="Angular frequency ω / γ", ylabel="S(ω) γ / θ",
            title="B  Averaging suppresses estimator scatter")
axes[1].legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
for ax in axes:
    ax.grid(alpha=0.17)
fig.savefig(ROOT / "assets/ch16-spectra.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch16-spectra.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
