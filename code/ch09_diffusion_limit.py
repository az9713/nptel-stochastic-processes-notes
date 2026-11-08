"""Lattice-to-diffusion error and positivity checks for generator truncation."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, skellam


def main():
    drift, diffusion, time = .7, .4, 1.0
    rows = []
    for ell in (.5, .25, .125, .0625):
        positive = diffusion/ell**2+drift/(2*ell)
        negative = diffusion/ell**2-drift/(2*ell)
        assert min(positive, negative) >= 0
        extent = int(np.ceil((abs(drift*time)+12*np.sqrt(2*diffusion*time))/ell))+2
        indices = np.arange(-extent, extent+1)
        locations = ell*indices
        exact = skellam.pmf(indices, positive*time, negative*time)
        gaussian = (norm.cdf((locations+ell/2-drift*time)/np.sqrt(2*diffusion*time))
                    -norm.cdf((locations-ell/2-drift*time)/np.sqrt(2*diffusion*time)))
        assert abs(exact.sum()-1) < 2e-11
        assert abs(exact @ locations-drift*time) < 2e-10
        assert abs(exact @ (locations-drift*time)**2-2*diffusion*time) < 2e-9
        rows.append({"ell": ell, "rplus": positive, "rminus": negative,
                     "cell_mass_total_variation": float(.5*abs(exact-gaussian).sum()),
                     "third_increment_moment_rate": drift*ell**2,
                     "fourth_increment_moment_rate": 2*diffusion*ell**2})
    # Symmetric jumps: third rate moment zero, fourth nonzero.
    rate, jump = 2.0, .5
    a2, a3, a4 = rate*jump**2, 0.0, rate*jump**4
    k = 10.0
    exact_log_phi = rate*(np.cos(k*jump)-1)
    truncated_log_phi = -a2*k*k/2+a4*k**4/24
    assert exact_log_phi <= 0
    assert truncated_log_phi > 0
    # Harmonic Smoluchowski stationary density: mobility1, theta.5, stiffness2.
    mobility, theta, stiffness = 1., .5, 2.
    variance = theta/stiffness
    equilibrium = norm(scale=np.sqrt(variance))
    normalization = quad(equilibrium.pdf, -np.inf, np.inf)[0]
    grid = np.linspace(-3, 3, 501)
    rho = equilibrium.pdf(grid)
    rho_prime = -grid/variance*rho
    current = -mobility*stiffness*grid*rho-mobility*theta*rho_prime
    assert np.max(abs(current)) < 1e-14
    result = {"drift": drift, "diffusion": diffusion, "time": time,
              "rows": rows, "symmetric_jump": {"rate": rate, "ell": jump,
              "A2": a2, "A3": a3, "A4": a4, "k": k,
              "exact_log_phi": float(exact_log_phi),
              "fourth_order_truncated_log_phi": truncated_log_phi},
              "harmonic_equilibrium": {"variance": variance,
              "normalization": normalization, "maximum_current_residual": float(max(abs(current)))}}
    directory = Path(__file__).resolve().parent
    (directory / "ch09-results.json").write_text(json.dumps(result, indent=2)+"\n")
    lines = [f"ell={r['ell']:.4f}: cell-mass TV={r['cell_mass_total_variation']:.9f}, "
             f"A4={r['fourth_increment_moment_rate']:.9f}" for r in rows]
    lines.append(f"Symmetric jump: A3={a3}, A4={a4}")
    lines.append(f"k=10: exact log phi={exact_log_phi:.9f}; "
                 f"fourth-order log phi={truncated_log_phi:.9f}")
    report = "\n".join(lines)+"\n"
    (directory / "ch09-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
