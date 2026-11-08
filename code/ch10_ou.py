"""Exact inertial OU moments, correlated updates, and Euler bias.

Run from any directory. Writes deterministic JSON and text beside this file.
Parameters use dimensionless units with thermal velocity variance one.
"""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad


def conditional_covariance(t, gamma=1.0, theta=1.0):
    """Covariance of (displacement, velocity) given both initial values."""
    if t <= 0 or gamma <= 0 or theta <= 0:
        raise ValueError("t, gamma, theta must be positive")
    r = np.exp(-gamma*t)
    qvv = theta*(1-r*r)
    qxv = theta/gamma*(1-r)**2
    qxx = 2*theta/gamma*(t-2*(1-r)/gamma+(1-r*r)/(2*gamma))
    return np.array([[qxx, qxv], [qxv, qvv]])


def run():
    gamma, theta = 1.0, 1.0
    times = [0.01, 0.1, 1.0, 10.0, 100.0]
    rows = []
    for t in times:
        covariance = conditional_covariance(t)
        integrated = np.array([
            [quad(lambda s: 2*(1-np.exp(-s))**2, 0, t)[0],
             quad(lambda s: 2*(1-np.exp(-s))*np.exp(-s), 0, t)[0]],
            [quad(lambda s: 2*(1-np.exp(-s))*np.exp(-s), 0, t)[0],
             quad(lambda s: 2*np.exp(-2*s), 0, t)[0]],
        ])
        assert np.allclose(covariance, integrated, rtol=1e-8, atol=1e-12)
        assert np.linalg.eigvalsh(covariance).min() > 0
        stationary_msd = 2*(t+np.expm1(-t))
        initial_component = (1-np.exp(-t))**2
        assert np.isclose(covariance[0, 0]+initial_component, stationary_msd)
        slope = t*(-np.expm1(-t))/(t+np.expm1(-t))
        rows.append({"t": t, "stationary_msd": stationary_msd,
                     "fixed_v0_variance": float(covariance[0, 0]),
                     "local_slope": float(slope)})
    rng = np.random.default_rng(2026110810)
    count, h = 250000, 0.2
    q = conditional_covariance(h)
    r = np.exp(-h)
    v0 = rng.normal(size=count)
    noise = rng.normal(size=(count, 2)) @ np.linalg.cholesky(q).T
    x = (1-r)*v0+noise[:, 0]
    v = r*v0+noise[:, 1]
    expected = np.array([[2*(h+np.expm1(-h)), 1-r], [1-r, 1]])
    sampled = np.cov(np.vstack([x, v]), ddof=0)
    assert np.allclose(sampled, expected, rtol=0.015, atol=0.002)
    euler = [{"h": step, "stationary_variance": 1/(1-step/2),
              "relative_bias": 1/(1-step/2)-1}
             for step in [0.1, 0.5, 1.0]]
    result = {"units": "gamma=theta=1", "seed": 2026110810,
              "rows": rows, "euler": euler,
              "joint_sample_covariance": sampled.tolist(),
              "joint_exact_covariance": expected.tolist(),
              "checks": "quadrature, positive covariance, initial ensemble, sampling"}
    folder = Path(__file__).resolve().parent
    (folder / "ch10-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = "t       stationary MSD  fixed-v0 variance  local slope\n"
    report += "\n".join(
        f"{row['t']:6.2f}  {row['stationary_msd']:14.8f}  "
        f"{row['fixed_v0_variance']:17.8f}  {row['local_slope']:11.6f}"
        for row in rows)
    report += "\nAll analytical and numerical checks passed.\n"
    (folder / "ch10-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
