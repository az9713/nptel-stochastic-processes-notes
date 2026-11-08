"""Exact distribution checks for central-limit and lattice diffusion limits."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.stats import binom, irwinhall, norm


def main():
    rows = []
    for n in (10, 50, 200, 1000):
        successes = np.arange(n+1)
        x = (2*successes-n)/np.sqrt(n)
        mass = binom.pmf(successes, n, .5)
        cdf = binom.cdf(successes, n, .5)
        # The CDF distance must check both sides of each jump.
        distance = max(np.max(abs(cdf-norm.cdf(x))),
                       np.max(abs(cdf-mass-norm.cdf(x))))
        corrected = norm.cdf(x+1/np.sqrt(n))
        rows.append({"n": n, "cdf_distance": float(distance),
                     "continuity_corrected_grid_error":
                     float(np.max(abs(cdf-corrected))),
                     "exact_variance": float(mass @ x**2),
                     "central_mass": float(mass[n//2]),
                     "parity_aware_central_mass": float(2*norm.pdf(0)/np.sqrt(n))})
        assert abs(mass.sum()-1) < 1e-12
        assert abs(mass @ x**2-1) < 1e-12
    uniform = []
    for n in (2, 4, 16):
        scale = np.sqrt(n/12)
        z = np.linspace(-np.sqrt(3*n), np.sqrt(3*n), 2001)
        exact = irwinhall(n).cdf(n/2+scale*z)
        uniform.append({"n": n, "cdf_grid_error":
                        float(np.max(abs(exact-norm.cdf(z))))})
    n = 4
    limit = 100
    inverse = quad(lambda k: np.sinc(k*np.sqrt(3/n)/np.pi)**n,
                   -limit, limit, epsabs=1e-9)[0]/(2*np.pi)
    exact_density = np.sqrt(n/12)*irwinhall(n).pdf(n/2)
    assert abs(inverse-exact_density) < 5e-7
    dt, diffusion, time = .01, .5, 1.0
    ell = np.sqrt(2*diffusion*dt)
    steps = int(round(time/dt))
    assert abs(steps*ell**2-2*diffusion*time) < 1e-12
    outside_probability = 2*norm.sf(steps*ell/np.sqrt(2*diffusion*time))
    results = {"walk_rows": rows, "uniform_rows": uniform,
               "four_uniform_density_at_zero": float(exact_density),
               "fourier_inversion_cutoff_100": float(inverse),
               "diffusion_example": {"D": diffusion, "dt": dt, "t": time,
                                     "ell": float(ell), "steps": steps,
                                     "mean_square_displacement": steps*ell**2,
                                     "gaussian_probability_outside_walk_support":
                                     float(outside_probability)}}
    root = Path(__file__).resolve().parent
    (root / "ch03-results.json").write_text(json.dumps(results, indent=2)+"\n")
    lines = ["Normalized symmetric lattice walk (variance one):"]
    for row in rows:
        lines.append("n={n}: CDF distance={cdf_distance:.8f}, "
                     "corrected grid error={continuity_corrected_grid_error:.8f}, "
                     "central mass={central_mass:.8f}, "
                     "parity approximation={parity_aware_central_mass:.8f}".format(**row))
    lines.append(f"Four-uniform density at zero: {exact_density:.9f}")
    lines.append(f"Fourier inversion cutoff100: {inverse:.9f}")
    report = "\n".join(lines)+"\n"
    (root / "ch03-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
