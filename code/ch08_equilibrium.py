"""Stationary weights, immigration-death transients, and linear birth/death moments."""
from pathlib import Path
import json

import numpy as np
from scipy.stats import binom, poisson


def immigration_death_end(rng, initial, immigration, death, time):
    state, clock = initial, 0.0
    while True:
        total = immigration+death*state
        clock += rng.exponential(1/total)
        if clock > time:
            return state
        if rng.random() < immigration/total:
            state += 1
        else:
            state -= 1


def main():
    rng = np.random.default_rng(202611088)
    a, b, initial, time, samples = 3.0, 1.0, 12, 2.0, 40_000
    survival = np.exp(-b*time)
    mean = initial*survival+a/b*(1-survival)
    variance = initial*survival*(1-survival)+a/b*(1-survival)
    empirical = np.array([immigration_death_end(rng, initial, a, b, time)
                          for _ in range(samples)])
    assert abs(empirical.mean()-mean) < 6*np.sqrt(variance/samples)
    grid = np.arange(100)
    exact_mass = np.convolve(binom.pmf(grid, initial, survival),
                            poisson.pmf(grid, a/b*(1-survival)))[:100]
    assert abs(exact_mass.sum()-1) < 1e-12
    assert abs(exact_mass @ grid-mean) < 1e-11
    assert abs(exact_mass @ (grid-mean)**2-variance) < 1e-10
    # Stationary immigration/death weights independently from neighboring ratios.
    weights = np.ones(100)
    for n in range(1, 100):
        weights[n] = weights[n-1]*a/(b*n)
    stationary = weights/weights.sum()
    assert np.allclose(stationary, poisson.pmf(grid, a/b), atol=1e-14)
    geometric = []
    for ratio in (.4, .8, .98, 1, 1.02):
        sums = {str(cutoff): float(np.sum(ratio**np.arange(cutoff+1)))
                for cutoff in (10, 100, 1000)}
        geometric.append({"ratio": ratio, "partial_weight_sums": sums,
                          "normalizable": ratio < 1,
                          "exact_mean_if_normalizable": ratio/(1-ratio) if ratio < 1 else None})
    birth, death, n0, duration = .7, .4, 2, 2
    growth = birth-death
    branching_mean = n0*np.exp(growth*duration)
    branching_variance = n0*(birth+death)/growth*np.exp(growth*duration)*np.expm1(growth*duration)
    result = {"seed": 202611088, "samples": samples,
              "immigration_death": {"a": a, "b": b, "initial": initial, "time": time,
                                    "exact_mean": float(mean), "exact_variance": float(variance),
                                    "sample_mean": float(empirical.mean()),
                                    "sample_variance": float(empirical.var()),
                                    "stationary_mean": a/b},
              "geometric_weights": geometric,
              "branching": {"birth": birth, "death": death, "initial": n0,
                            "time": duration, "mean": float(branching_mean),
                            "variance": float(branching_variance)}}
    directory = Path(__file__).resolve().parent
    (directory / "ch08-results.json").write_text(json.dumps(result, indent=2)+"\n")
    report = (f"Immigration-death mean: exact={mean:.9f}, sample={empirical.mean():.9f}\n"
              f"Immigration-death variance: exact={variance:.9f}, sample={empirical.var():.9f}\n"
              f"Stationary mean=variance={a/b:.6f}\n"
              f"Linear branching mean={branching_mean:.9f}, variance={branching_variance:.9f}\n")
    (directory / "ch08-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
