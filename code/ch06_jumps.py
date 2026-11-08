"""Generator, event-driven two-state, Poisson, and lattice checks."""
from pathlib import Path
import json

import numpy as np
from scipy.linalg import expm
from scipy.stats import poisson, skellam


def final_state(rng, time, rate12, rate21, initial=0):
    state, clock = initial, 0.0
    while True:
        clock += rng.exponential(1/(rate12 if state == 0 else rate21))
        if clock > time:
            return state
        state = 1-state


def main():
    rng = np.random.default_rng(202611086)
    rate12, rate21, time = 2.0, 1.0, .7
    generator = np.array([[-rate12, rate21], [rate12, -rate21]])
    total = rate12+rate21
    exact = np.eye(2)+(1-np.exp(-total*time))*generator/total
    assert np.allclose(exact, expm(time*generator))
    rate = max(-np.diag(generator))
    kernel = np.eye(2)+generator/rate
    uniformized = sum(poisson.pmf(n, rate*time)*np.linalg.matrix_power(kernel, n)
                      for n in range(35))
    assert np.allclose(uniformized, exact, atol=1e-13)
    count = 60_000
    sample = np.array([final_state(rng, time, rate12, rate21) for _ in range(count)])
    empirical = float(np.mean(sample == 0))
    probability = exact[0, 0]
    assert abs(empirical-probability) < 6*np.sqrt(probability*(1-probability)/count)
    rplus, rminus, ell, duration = 3.0, 1.0, .5, 2.0
    plus = rng.poisson(rplus*duration, count)
    minus = rng.poisson(rminus*duration, count)
    displacement = ell*(plus-minus)
    mean = ell*(rplus-rminus)*duration
    variance = ell**2*(rplus+rminus)*duration
    assert abs(displacement.mean()-mean) < 6*np.sqrt(variance/count)
    grid = np.arange(-40, 61)
    mass = skellam.pmf(grid, rplus*duration, rminus*duration)
    assert abs(mass.sum()-1) < 1e-12
    assert abs(mass @ (ell*grid)-mean) < 1e-11
    assert abs(mass @ (ell*grid-mean)**2-variance) < 1e-10
    # A clockwise ring is stationary without detailed balance.
    ring = np.array([[-1., 0., 1.], [1., -1., 0.], [0., 1., -1.]])
    stationary = np.full(3, 1/3)
    assert np.allclose(ring @ stationary, 0)
    current = float(ring[1, 0]*stationary[0]-ring[0, 1]*stationary[1])
    result = {"seed": 202611086, "samples": count,
              "two_state": {"rate12": rate12, "rate21": rate21, "time": time,
                            "transition": exact.tolist(), "sample_P11": empirical,
                            "correlation_time": 1/total,
                            "mean_residence_times": [1/rate12, 1/rate21]},
              "walk": {"rplus": rplus, "rminus": rminus, "ell": ell,
                       "time": duration, "exact_mean": mean, "exact_variance": variance,
                       "sample_mean": float(displacement.mean()),
                       "sample_variance": float(displacement.var()),
                       "zero_probability": float(skellam.pmf(0, 6, 2))},
              "clockwise_ring_stationary_current": current}
    directory = Path(__file__).resolve().parent
    (directory / "ch06-results.json").write_text(json.dumps(result, indent=2)+"\n")
    report = (f"Two-state P11(0.7): exact={probability:.9f}, sample={empirical:.9f}\n"
              f"Residence times: 0.5, 1; correlation time={1/total:.9f}\n"
              f"Walk mean: exact={mean:.6f}, sample={displacement.mean():.6f}\n"
              f"Walk variance: exact={variance:.6f}, sample={displacement.var():.6f}\n"
              f"Stationary ring current: {current:.9f}\n")
    (directory / "ch06-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
