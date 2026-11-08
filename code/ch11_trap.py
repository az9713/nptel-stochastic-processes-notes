"""Exact covariance and overdamped error for a thermal harmonic trap."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad, quad_vec
from scipy.linalg import expm, solve_continuous_lyapunov


def run():
    rows = []
    for gamma in (0.5, 2.0, 10.0):
        drift = np.array([[0., 1.], [-1., -gamma]])
        noise = np.diag([0., 2*gamma])
        equilibrium = solve_continuous_lyapunov(drift, -noise)
        assert np.allclose(equilibrium, np.eye(2), atol=1e-12)
        for t in (0.1, 1.0, gamma):
            e = expm(drift*t)
            q = equilibrium-e @ equilibrium @ e.T
            integrated = quad_vec(
                lambda s: expm(drift*s) @ noise @ expm(drift.T*s),
                0, t)[0]
            assert np.allclose(q, integrated, atol=1e-11)
            assert np.linalg.eigvalsh(q).min() > 0
        t = gamma
        exact = float(expm(drift*t)[0, 0])
        reduced = float(np.exp(-t/gamma))
        correlation_area = quad(lambda s: expm(drift*s)[0, 0], 0, np.inf)[0]
        assert np.isclose(correlation_area, gamma, atol=1e-9)
        rows.append({"gamma": gamma, "t": t,
                     "exact_normalized_position_covariance": exact,
                     "overdamped_covariance": reduced,
                     "integrated_normalized_covariance": correlation_area,
                     "roots": [[float(z.real), float(z.imag)]
                               for z in np.linalg.eigvals(drift)]})
    critical = expm(np.array([[0., 1.], [-1., -2.]]))
    assert np.isclose(critical[0, 0], 2/np.e)
    rng = np.random.default_rng(2026110811)
    a = np.array([[0., 1.], [-1., -10.]])
    e = expm(a*0.1)
    q = np.eye(2)-e @ e.T
    start = rng.normal(size=(200000, 2))
    final = start @ e.T+rng.normal(size=start.shape) @ np.linalg.cholesky(q).T
    assert np.allclose(np.cov(final.T), np.eye(2), atol=0.015)
    result = {"units": "theta=omega0=1", "seed": 2026110811,
              "rows": rows, "critical_Cxx_at_t1": float(critical[0, 0]),
              "sample_covariance": np.cov(final.T).tolist(),
              "checks": "Lyapunov, covariance quadrature, critical limit, sampling"}
    folder = Path(__file__).resolve().parent
    (folder / "ch11-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = "gamma  t       exact Cxx     overdamped Cxx\n"
    report += "\n".join(
        f"{r['gamma']:5.1f}  {r['t']:5.1f}  "
        f"{r['exact_normalized_position_covariance']:12.8f}  "
        f"{r['overdamped_covariance']:14.8f}" for r in rows)
    report += "\nAll covariance and critical-limit checks passed.\n"
    (folder / "ch11-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
