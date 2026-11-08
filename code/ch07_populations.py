"""State-dependent jump rates and a deterministic time-dependent event clock."""
from pathlib import Path
import json

import numpy as np
from scipy.stats import geom, skellam


def yule_path_end(rng, birth_rate, time):
    state, clock = 1, 0.0
    while True:
        clock += rng.exponential(1/(birth_rate*state))
        if clock > time:
            return state
        state += 1


def main():
    rng = np.random.default_rng(202611087)
    samples = 40_000
    b, time = .8, 1.5
    final = np.array([yule_path_end(rng, b, time) for _ in range(samples)])
    mean = float(np.exp(b*time))
    variance = mean*(mean-1)
    assert abs(final.mean()-mean) < 6*np.sqrt(variance/samples)
    grid = np.arange(1, 501)
    masses = geom.pmf(grid, np.exp(-b*time))
    assert abs(masses.sum()-1) < 1e-12
    assert abs(masses @ grid-mean) < 1e-11
    # NHPP intensity 2 for 0<=t<1; 6 for 1<=t<=2, so integrated intensity=8.
    counts = []
    for _ in range(samples):
        integrated_time, count = 0.0, 0
        while True:
            integrated_time += rng.exponential()
            if integrated_time > 8:
                break
            count += 1
        counts.append(count)
    counts = np.array(counts)
    assert abs(counts.mean()-8) < 6*np.sqrt(8/samples)
    # First four physical displacement cumulants of an independent Poisson walk.
    ell, rplus, rminus, duration = .5, 3, 1, 2
    x = ell*np.arange(-50, 81)
    p = skellam.pmf(np.arange(-50, 81), rplus*duration, rminus*duration)
    mu = p @ x
    var = p @ (x-mu)**2
    cumulants = [mu, var, p @ (x-mu)**3, p @ (x-mu)**4-3*var**2]
    exact = [ell**k*(rplus+(-1)**k*rminus)*duration for k in range(1, 5)]
    assert np.allclose(cumulants, exact, atol=1e-10)
    result = {"seed": 202611087, "samples": samples,
              "yule": {"birth_rate": b, "time": time, "exact_mean": mean,
                       "exact_variance": variance, "sample_mean": float(final.mean()),
                       "sample_variance": float(final.var()),
                       "probability_still_one": float(np.exp(-b*time))},
              "nhpp": {"integrated_intensity_at_1": 2,
                       "integrated_intensity_at_2": 8,
                       "sample_mean_at_2": float(counts.mean()),
                       "sample_variance_at_2": float(counts.var())},
              "walk_cumulants": list(map(float, cumulants)),
              "walk_exact_cumulants": exact}
    directory = Path(__file__).resolve().parent
    (directory / "ch07-results.json").write_text(json.dumps(result, indent=2)+"\n")
    report = (f"Yule mean: exact={mean:.9f}, sample={final.mean():.9f}\n"
              f"Yule variance: exact={variance:.9f}, sample={final.var():.9f}\n"
              f"NHPP at t=2: exact mean=variance=8, sample mean={counts.mean():.6f}, "
              f"variance={counts.var():.6f}\n"
              "Walk cumulants: "+", ".join(f"{c:.6f}" for c in cumulants)+"\n")
    (directory / "ch07-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
