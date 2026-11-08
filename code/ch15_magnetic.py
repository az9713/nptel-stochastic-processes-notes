"""Magnetic OU covariance, symmetric diffusion, and exact Gaussian endpoint."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import expm


def run():
    gamma, theta, omega = 1., 1., 4.
    j = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 0.]])
    a = -gamma*np.eye(3)+omega*j
    assert np.allclose(a+a.T+2*gamma*np.eye(3), 0)
    integral = quad_vec(lambda t: theta*expm(a*t), 0, 50)[0]
    exact_integral = -theta*np.linalg.inv(a)
    assert np.allclose(integral, exact_integral, atol=1e-11)
    diffusion = (integral+integral.T)/2
    target = np.diag([theta*gamma/(gamma**2+omega**2)]*2+[theta/gamma])
    assert np.allclose(diffusion, target)
    mobility_noise = np.sqrt(2*gamma*theta)*np.linalg.inv(-a)
    assert np.allclose(mobility_noise @ mobility_noise.T/2, diffusion)
    t = 80.
    f = np.block([[np.zeros((3, 3)), np.eye(3)],
                  [np.zeros((3, 3)), a]])
    g = np.diag([0., 0., 0., 2*gamma*theta, 2*gamma*theta, 2*gamma*theta])
    cov = quad_vec(lambda s: expm(f*s) @ g @ expm(f.T*s), 0, t)[0]
    e = expm(f*t)
    cov += e @ np.diag([0., 0., 0., theta, theta, theta]) @ e.T
    alpha = gamma-1j*omega
    msd_perp = 2*theta*np.real(t/alpha-(1-np.exp(-alpha*t))/alpha**2)
    msd_parallel = 2*theta/gamma*(t-(1-np.exp(-gamma*t))/gamma)
    assert np.allclose(np.diag(cov)[:3], [msd_perp]*2+[msd_parallel])
    rng = np.random.default_rng(2026110815)
    sample = rng.normal(size=(200000, 6)) @ np.linalg.cholesky(cov).T
    sample_cov = np.cov(sample.T, ddof=0)
    assert np.allclose(np.diag(sample_cov), np.diag(cov), rtol=0.015)
    assert np.allclose(np.diag(sample_cov)[3:], theta, rtol=0.015)
    result = {"seed": 2026110815, "gamma": gamma, "theta": theta,
              "signed_omega": omega, "time": t,
              "integrated_velocity_covariance": exact_integral.tolist(),
              "diffusion_tensor": diffusion.tolist(),
              "exact_displacement_variances": [msd_perp, msd_perp, msd_parallel],
              "sample_displacement_variances": np.diag(sample_cov)[:3].tolist(),
              "sample_velocity_variances": np.diag(sample_cov)[3:].tolist(),
              "suppression_ratio": gamma**2/(gamma**2+omega**2)}
    folder = Path(__file__).resolve().parent
    (folder / "ch15-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = f"D_parallel={theta/gamma:.8f}\nD_perpendicular={target[0, 0]:.8f}\n"
    report += f"Suppression ratio={result['suppression_ratio']:.8f}\n"
    report += f"At t=80: transverse MSD={msd_perp:.8f}, parallel MSD={msd_parallel:.8f}\n"
    report += "All matrix, covariance, and thermal-variance checks passed.\n"
    (folder / "ch15-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
