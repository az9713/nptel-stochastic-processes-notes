"""Gaussian-to-energy checks; run from any working directory, without a network."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma
from scipy.stats import gamma as gamma_law
from scipy.stats import kstest, norm


def energy_density(energy, dimension, theta=1.0):
    """Density for positive energies; theta = k_B T, dimension is an integer."""
    if dimension < 1 or int(dimension) != dimension or theta <= 0:
        raise ValueError("positive integer dimension and positive theta required")
    if energy <= 0:
        raise ValueError("evaluate the density strictly inside its support")
    shape = dimension / 2
    return energy**(shape-1)*np.exp(-energy/theta)/(gamma(shape)*theta**shape)


def main():
    rng = np.random.default_rng(202611082)
    count = 200_000
    results = {"seed": 202611082, "samples": count, "dimensionless_theta": 1.0}
    rows = []
    for dimension in (1, 2, 3):
        velocities = rng.normal(size=(count, dimension))
        energies = 0.5 * np.sum(velocities**2, axis=1)
        mass, error = quad(lambda e: energy_density(e, dimension), 0, np.inf)
        mean = dimension/2
        variance = dimension/2
        sample_mean = float(energies.mean())
        assert abs(mass-1) < 2e-9
        assert abs(sample_mean-mean) < 6*np.sqrt(variance/count)
        ks = float(kstest(energies, gamma_law(dimension/2).cdf).statistic)
        rows.append({"d": dimension, "integrated_mass": mass,
                     "quadrature_error_estimate": error, "exact_mean": mean,
                     "exact_variance": variance, "sample_mean": sample_mean,
                     "sample_variance": float(energies.var()), "ks_distance": ks,
                     "probability_energy_over_3theta":
                     float(gamma_law(dimension/2).sf(3))})
    moments = {}
    for order in (2, 4, 6):
        value = quad(lambda z: z**order * norm.pdf(z), -np.inf, np.inf)[0]
        expected = {2: 1, 4: 3, 6: 15}[order]
        assert abs(value-expected) < 1e-10
        moments[str(order)] = value
    char = []
    for k in (0, 0.5, 1, 2):
        numerical = quad(lambda z: np.cos(k*z)*norm.pdf(z), -np.inf, np.inf)[0]
        exact = float(np.exp(-k*k/2))
        assert abs(numerical-exact) < 1e-10
        char.append({"k": k, "quadrature": numerical, "exact": exact})
    # An intentionally incorrect one-branch square transformation loses half mass.
    wrong_mass = quad(lambda e: 0.5*energy_density(e, 1), 0, np.inf)[0]
    assert abs(wrong_mass-0.5) < 1e-9
    # A non-Gaussian three-point law agrees with the first four Gaussian moments.
    x = np.array([-np.sqrt(3), 0, np.sqrt(3)])
    weights = np.array([1/6, 2/3, 1/6])
    results.update({"energy_rows": rows, "standard_gaussian_moments": moments,
                    "characteristic_function": char,
                    "incorrect_one_branch_mass": wrong_mass,
                    "three_point_fourth_moment": float(weights @ x**4),
                    "three_point_sixth_moment": float(weights @ x**6),
                    "fwhm_over_sigma": float(2*np.sqrt(2*np.log(2)))})
    output = Path(__file__).resolve().parent
    (output / "ch02-results.json").write_text(json.dumps(results, indent=2)+"\n")
    lines = ["Reduced units: k_B T = m = 1; E/(k_B T) is dimensionless."]
    for row in rows:
        lines.append("d={d}: mass={integrated_mass:.9f}, mean={sample_mean:.6f}, "
                     "variance={sample_variance:.6f}, KS={ks_distance:.6f}, "
                     "P(E>3 k_B T)={probability_energy_over_3theta:.8f}".format(**row))
    lines.append(f"Incorrect one-branch mass: {wrong_mass:.9f}")
    lines.append(f"Gaussian FWHM/sigma: {results['fwhm_over_sigma']:.9f}")
    report = "\n".join(lines)+"\n"
    (output / "ch02-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
