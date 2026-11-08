"""Itô square identity, radial moments, and geometric Brownian checks."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm


def run():
    rng = np.random.default_rng(2026110813)
    dcoef, count, cells = 0.5, 100000, 128
    steps = rng.normal(scale=np.sqrt(2*dcoef/cells), size=(count, cells))
    positions = np.cumsum(steps, axis=1)
    left = np.column_stack([np.zeros(count), positions[:, :-1]])
    chain = 2*np.sum(left*steps, axis=1)
    correction = np.sum(steps**2, axis=1)
    residual = positions[:, -1]**2-chain-correction
    assert np.max(np.abs(residual)) < 1e-12
    assert abs(correction.mean()-2*dcoef) < 0.002
    radial = []
    for dim in (1, 2, 3):
        coords = rng.normal(scale=np.sqrt(2*dcoef), size=(count, dim))
        square = np.sum(coords**2, axis=1)
        radial.append({"dimension": dim, "sample_mean_r2": float(square.mean()),
                       "exact_mean_r2": 2*dim*dcoef,
                       "sample_variance_r2": float(square.var()),
                       "exact_variance_r2": 8*dim*dcoef*dcoef})
        assert abs(square.mean()-2*dim*dcoef) < 0.035
        assert abs(square.var()/(8*dim*dcoef*dcoef)-1) < 0.04
    a, b, t = 0.1, 1.2, 1.0
    logs = (a-b*b/2)*t+b*np.sqrt(t)*rng.normal(size=count)
    exact = np.exp(logs)
    euler = 1+a*t+b*np.sqrt(t)*rng.normal(size=count)
    mean = np.exp(a*t)
    variance = np.exp(2*a*t)*np.expm1(b*b*t)
    quadrature = quad(lambda z: np.exp((a-b*b/2)*t+b*np.sqrt(t)*z)
                     * np.exp(-z*z/2)/np.sqrt(2*np.pi), -12, 12)[0]
    assert np.isclose(quadrature, mean)
    assert abs(exact.mean()-mean) < 6*np.sqrt(variance/count)
    neg_probability = norm.cdf(-(1+a*t)/(b*np.sqrt(t)))
    assert abs(np.mean(euler < 0)-neg_probability) < 0.005
    result = {"seed": 2026110813, "D": dcoef, "paths": count,
              "square_identity_max_error": float(abs(residual).max()),
              "mean_quadratic_correction": float(correction.mean()),
              "radial": radial,
              "gbm": {"a": a, "b": b, "time": t,
                      "exact_mean": float(mean), "sample_mean": float(exact.mean()),
                      "median": float(np.exp((a-b*b/2)*t)),
                      "euler_negative_probability": float(neg_probability),
                      "euler_negative_fraction": float(np.mean(euler < 0))}}
    folder = Path(__file__).resolve().parent
    (folder / "ch13-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = f"Mean squared-increment correction: {correction.mean():.8f}\n"
    report += "dimension   sample mean R²   exact mean R²\n"
    report += "\n".join(f"{r['dimension']:9d}   {r['sample_mean_r2']:14.8f}   "
                        f"{r['exact_mean_r2']:13.8f}" for r in radial)
    report += f"\nGBM exact mean={mean:.8f}, median={np.exp(a-b*b/2):.8f}\n"
    report += f"One-step Euler negative probability={neg_probability:.8f}\n"
    (folder / "ch13-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
