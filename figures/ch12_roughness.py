"""Mesh refinement separates continuity from finite velocity."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "code/ch12-results.json").read_text())
plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ch12",
                     "font.size": 11, "figure.facecolor": "#101720",
                     "axes.facecolor": "#101720", "text.color": "#e5edf5",
                     "axes.labelcolor": "#e5edf5", "axes.edgecolor": "#8795a5",
                     "xtick.color": "#bcc8d6", "ytick.color": "#bcc8d6"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
times = np.r_[0, data["single_path_times"]]
path = np.r_[0, data["single_path"]]
axes[0].plot(times, path, color="#7bd6d2", lw=1, label="Fine sampled path")
axes[0].plot(times[::32], path[::32], "o--", color="#e9bd74", ms=3,
             label="Coarse samples of same path")
axes[0].set(xlabel="Time (dimensionless)", ylabel="W(t)",
            title="A  Straight segments hide unresolved roughness")
cells = np.array([r["cells"] for r in data["rows"]])
axes[1].loglog(cells, [r["qv_variance"] for r in data["rows"]], "o-",
               color="#7bd6d2", label="Sample QV variance")
axes[1].loglog(cells, 2/cells, "--", color="#e9bd74", label="Exact: 2 / cells")
axes[1].set(xlabel="Partition cells on [0,1]", ylabel="Variance across paths",
            title="B  Quadratic variation concentrates")
for ax in axes:
    ax.grid(alpha=0.17)
    ax.legend(fontsize=8, facecolor="#172230", labelcolor="#e5edf5")
fig.savefig(ROOT / "assets/ch12-roughness.svg", metadata={"Date": None})
preview = ROOT / "work/validation/ch12-roughness.png"
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=130)
