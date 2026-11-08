"""Nested Brownian mesh checks and occupation-time illustration."""
from pathlib import Path
import json

import numpy as np


def run():
    rng = np.random.default_rng(2026110812)
    count, n = 6000, 2048
    fine = rng.normal(scale=1/np.sqrt(n), size=(count, n))
    rows = []
    for cells in (16, 64, 256, 1024, 2048):
        increments = fine.reshape(count, cells, n//cells).sum(axis=2)
        qv = (increments**2).sum(axis=1)
        velocity_variance = float(np.var(increments*cells))
        assert abs(qv.mean()-1) < 6*np.sqrt(2/(cells*count))
        assert abs(np.var(qv)-2/cells) < 0.12*(2/cells)
        assert abs(velocity_variance/cells-1) < 0.03
        rows.append({"cells": cells, "qv_mean": float(qv.mean()),
                     "qv_variance": float(np.var(qv)),
                     "qv_variance_exact": 2/cells,
                     "velocity_variance": velocity_variance})
    paths = np.cumsum(fine, axis=1)
    occupation = (paths > 0).mean(axis=1)
    thresholds = [0.1, 0.25, 0.5, 0.75, 0.9]
    empirical = [float(np.mean(occupation <= x)) for x in thresholds]
    exact = [float(2/np.pi*np.arcsin(np.sqrt(x))) for x in thresholds]
    assert max(abs(a-b) for a, b in zip(empirical, exact)) < 0.035
    gamma, b, s, t = 0.8, 1.3, 0.4, 1.7
    clock = np.expm1(2*gamma*min(s, t))/(2*gamma)
    changed = b*b*np.exp(-gamma*(s+t))*clock
    ou = b*b/(2*gamma)*(np.exp(-gamma*abs(t-s))-np.exp(-gamma*(s+t)))
    assert np.isclose(changed, ou)
    result = {"seed": 2026110812, "paths": count, "fine_cells": n,
              "rows": rows, "occupation_thresholds": thresholds,
              "occupation_empirical_cdf": empirical,
              "occupation_exact_cdf": exact, "ou_covariance": float(ou),
              "single_path": paths[0, ::4].tolist(),
              "single_path_times": (np.arange(1, n+1)[::4]/n).tolist(),
              "checks": "QV mean/variance, slope variance, occupation illustration, OU clock"}
    folder = Path(__file__).resolve().parent
    (folder / "ch12-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = "cells   mean QV   variance QV   velocity variance\n"
    report += "\n".join(f"{r['cells']:5d}  {r['qv_mean']:9.6f}  "
                        f"{r['qv_variance']:11.8f}  {r['velocity_variance']:17.5f}"
                        for r in rows)
    report += "\nOccupation CDF at .1,.25,.5,.75,.9: "
    report += ", ".join(f"{v:.5f}" for v in empirical)+"\n"
    (folder / "ch12-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
