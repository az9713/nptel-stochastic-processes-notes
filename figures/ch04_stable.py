"""Sample mean quantile widths expose the difference in stable scaling."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

matplotlib.rcParams.update({"svg.hashsalt": "stochastic-ch04", "font.size": 11,
                           "axes.facecolor": "#15202d", "figure.facecolor": "#101821",
                           "text.color": "#e6edf3", "axes.labelcolor": "#e6edf3",
                           "xtick.color": "#b8cadb", "ytick.color": "#b8cadb",
                           "axes.edgecolor": "#7b91a5", "svg.fonttype": "none"})
root = Path(__file__).resolve().parents[1]
(root / "work/validation").mkdir(parents=True, exist_ok=True)
data = json.loads((root / "code/ch04-results.json").read_text())
fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
n = np.geomspace(1, 256, 300)
ax.loglog(n, 2*norm.ppf(.75)/np.sqrt(n), color="#65c6ff", label="Gaussian exact")
ax.loglog(n, np.full_like(n, 2), color="#ffc471", label="Cauchy exact")
rows = data["mean_iqr_rows"]
ax.scatter([r["n"] for r in rows], [r["gaussian_iqr"] for r in rows],
           color="#65c6ff", marker="o", label="Gaussian ensembles")
ax.scatter([r["n"] for r in rows], [r["cauchy_iqr"] for r in rows],
           color="#ffc471", marker="x", label="Cauchy ensembles")
ax.set(xlabel="Number n of independent measurements", ylabel="IQR of the sample mean",
       title="Averaging reduces Gaussian scatter, but not Cauchy scatter")
ax.grid(alpha=.15)
ax.legend(facecolor="#15202d", edgecolor="#7b91a5", labelcolor="#e6edf3")
fig.savefig(root / "assets/ch04-stable.svg", metadata={"Date": None})
fig.savefig(root / "work/validation/ch04-stable.png", dpi=150)
