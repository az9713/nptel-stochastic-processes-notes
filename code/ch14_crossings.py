"""Rice rate versus finite sampling of an exact thermal oscillator."""
from pathlib import Path
import json

import numpy as np
from scipy.linalg import expm
from scipy.stats import multivariate_normal


def run():
    rng = np.random.default_rng(2026110814)
    gamma, h, cells, paths = 0.8, 0.01, 20000, 512
    a = np.array([[0., 1.], [-1., -gamma]])
    e = expm(a*h)
    c = np.eye(2)-e @ e.T
    chol = np.linalg.cholesky(c)
    y = rng.normal(size=(paths, 2))
    x = np.empty((paths, cells+1))
    x[:, 0] = y[:, 0]
    for j in range(cells):
        y = y @ e.T+rng.normal(size=y.shape) @ chol.T
        x[:, j+1] = y[:, 0]
    rows = []
    for stride in (1, 5, 20, 100):
        sampled = x[:, ::stride]
        row = {"step": h*stride, "rates": []}
        lag_corr = float(expm(a*h*stride)[0, 0])
        for u in (0., 1., 2.):
            rate = np.mean(np.sum((sampled[:, :-1] < u)
                                  & (sampled[:, 1:] >= u), axis=1))/(cells*h)
            joint_below = multivariate_normal.cdf(
                [u, u], mean=[0, 0], cov=[[1, lag_corr], [lag_corr, 1]],
                maxpts=1000000, abseps=1e-10, releps=1e-10,
                rng=np.random.default_rng(1000+stride+int(u)))
            from scipy.special import ndtr
            sampled_exact = (ndtr(u)-joint_below)/(h*stride)
            rice = np.exp(-u*u/2)/(2*np.pi)
            if stride == 1:
                assert abs(rate/rice-1) < 0.08
            row["rates"].append({"level": u, "sampled_rate": float(rate),
                                 "endpoint_exact_rate": float(sampled_exact),
                                 "continuous_rice_rate": float(rice)})
        rows.append(row)
    switches = np.diff(x[:, :5001] >= 0, axis=1)
    repeats = np.argwhere(switches.reshape(paths, 50, 100).sum(axis=2) >= 2)
    example_index, example_block = map(int, repeats[0])
    result = {"seed": 2026110814, "gamma": gamma, "omega0": 1,
              "theta": 1, "paths": paths, "duration": cells*h,
              "rows": rows, "example_times": (h*np.arange(5001)).tolist(),
              "example_path": x[example_index, :5001].tolist(),
              "example_index": example_index, "example_block": example_block,
              "example_selection": "first path/block with >=2 crossings per coarse cell"}
    folder = Path(__file__).resolve().parent
    (folder / "ch14-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = "step  upcrossing rates at levels 0, 1, 2\n"
    report += "\n".join(f"{r['step']:.2f}  "+", ".join(
        f"{q['sampled_rate']:.8f}" for q in r["rates"]) for r in rows)
    report += "\nContinuous Rice rates: "+", ".join(
        f"{q['continuous_rice_rate']:.8f}" for q in rows[0]["rates"])+"\n"
    (folder / "ch14-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
