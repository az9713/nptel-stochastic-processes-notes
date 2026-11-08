"""Oscillator response and equilibrium FDT on consistent conventions."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "code/ch17-results.json").read_text())
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch17",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
w = np.linspace(.02, 4.8, 600)
chi = 1/(1-w*w-.6j*w)
axes[0].plot(w, chi.real, color="#7bd6d2", label="Real displacement response")
axes[0].plot(w, chi.imag, color="#e9bd74", label="Imaginary displacement response")
axes[0].set(xlabel="Angular frequency ω (dimensionless)", ylabel="Susceptibility χₓ(ω)",
            title="A  In-phase and dissipative response")
axes[1].semilogy(w, 2*chi.imag/w, color="#e9bd74", lw=2,
                 label="FDT prediction: 2 Im(χₓ) / ω")
axes[1].semilogy(d["plot_omega"], d["plot_estimated_spectrum"],
                 color="#7bd6d2", lw=1, label="Mean equilibrium periodogram")
axes[1].set(xlabel="Angular frequency ω (dimensionless)", ylabel="Position spectrum Sₓ(ω)",
            title="B  Spontaneous noise predicts weak response")
for ax in axes:
    ax.grid(alpha=0.17)
    ax.legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
fig.savefig(ROOT / "assets/ch17-response.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch17-response.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
