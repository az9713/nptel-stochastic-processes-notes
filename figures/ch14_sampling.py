"""Crossing loss under coarse sampling, with Gaussian endpoint check."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "code/ch14-results.json").read_text())
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch14",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
t, x = d["example_times"], d["example_path"]
axes[0].plot(t, x, color="#7bd6d2", lw=1, label="Fine observations")
axes[0].plot(t[::100], x[::100], "o--", color="#e9bd74", ms=3,
             label="Every 1 time unit")
axes[0].axhline(0, color="#bcc8d6", lw=0.8)
axes[0].set(xlabel="Time (dimensionless)", ylabel="Position X(t)",
            xlim=(max(0, d["example_block"]-2), d["example_block"]+3),
            title="A  Same path, missed paired crossings")
local = np.array(x)[(np.array(t) >= max(0, d["example_block"]-2))
                    & (np.array(t) <= d["example_block"]+3)]
axes[0].set_ylim(local.min()-0.15, local.max()+0.15)
for i, color in enumerate(["#7bd6d2", "#e9bd74", "#c9a0e5"]):
    axes[1].semilogx([r["step"] for r in d["rows"]],
                     [r["rates"][i]["sampled_rate"]
                      / r["rates"][i]["continuous_rice_rate"] for r in d["rows"]],
                     "o-", color=color, label=f"Threshold u = {i}")
axes[1].set(xlabel="Sampling interval (dimensionless)",
            ylabel="Observed rate / continuous Rice rate",
            title="B  Sampling changes the counted events", ylim=(0.5, 1.08))
for ax in axes:
    ax.grid(alpha=0.17)
    ax.legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
fig.savefig(ROOT / "assets/ch14-sampling.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch14-sampling.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
