"""Equilibrium FDT, driven oscillator, dispersion-band error, nonlinear control."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import expm


def susceptibility(omega, gamma=0.6, omega0=1., mass=1.):
    return 1/(mass*(omega0**2-omega**2-1j*gamma*omega))


def driven_fit(amplitude, cubic=0., drive_omega=1.):
    times = np.linspace(0, 400, 40001)
    def equation(t, y):
        return [y[1], -0.6*y[1]-y[0]-cubic*y[0]**3
                + amplitude*np.cos(drive_omega*t)]
    solution = solve_ivp(equation, [0, 400], [0, 0], t_eval=times,
                         rtol=2e-9, atol=2e-11)
    assert solution.success
    selected = times > 200
    phase = drive_omega*times[selected]
    design = np.column_stack([np.cos(phase), np.sin(phase), np.ones(phase.size)])
    coefficients = np.linalg.lstsq(design, solution.y[0, selected], rcond=None)[0]
    return (coefficients[0]+1j*coefficients[1])/amplitude


def run():
    omega = np.geomspace(0.01, 20, 400)
    chi = susceptibility(omega)
    spectrum = 1.2/((1-omega**2)**2+(0.6*omega)**2)
    assert np.allclose(spectrum, 2*chi.imag/omega)
    area = quad(lambda w: 1.2/((1-w*w)**2+(.6*w)**2)/np.pi,
                0, np.inf)[0]
    assert np.isclose(area, 1)
    fits = []
    for amplitude, cubic in ((0.05, 0.), (1., 0.), (0.05, .5), (1., .5)):
        fit = driven_fit(amplitude, cubic)
        if cubic == 0:
            assert abs(fit-susceptibility(1.)) < 1e-6
        fits.append({"force_amplitude": amplitude, "cubic_stiffness": cubic,
                     "response_per_force": [float(fit.real), float(fit.imag)],
                     "magnitude": float(abs(fit))})
    bands = []
    probe = .7
    for cutoff in (3., 10., 50.):
        value = 2/np.pi*quad(
            lambda w: w*susceptibility(w).imag/(w+probe),
            0, cutoff, weight="cauchy", wvar=probe, epsabs=1e-11)[0]
        bands.append({"cutoff": cutoff, "recovered_real_chi": value,
                      "exact_real_chi": float(susceptibility(probe).real),
                      "absolute_error": float(abs(value-susceptibility(probe).real))})
    assert bands[-1]["absolute_error"] < bands[0]["absolute_error"]
    rng = np.random.default_rng(2026110817)
    h, cells, paths = .02, 32768, 512
    drift = np.array([[0., 1.], [-1., -.6]])
    e = expm(drift*h)
    factor = np.linalg.cholesky(np.eye(2)-e @ e.T)
    y = rng.normal(size=(paths, 2))
    positions = np.empty((paths, cells))
    for j in range(cells):
        y = y @ e.T+rng.normal(size=y.shape) @ factor.T
        positions[:, j] = y[:, 0]
    power = h/cells*np.abs(np.fft.rfft(positions, axis=1))**2
    frequencies = 2*np.pi*np.fft.rfftfreq(cells, h)
    indices = np.where((frequencies > .1) & (frequencies < 5))[0]
    target = 1.2/((1-frequencies[indices]**2)**2+(.6*frequencies[indices])**2)
    relative_rms = np.sqrt(np.mean((power.mean(axis=0)[indices]/target-1)**2))
    assert relative_rms < .09
    result = {"seed": 2026110817, "mass": 1, "gamma": .6, "omega0": 1,
              "kBT": 1, "spectral_area": area, "driven_fits": fits,
              "dispersion_probe_omega": probe, "dispersion_bands": bands,
              "equilibrium_spectrum_relative_rms": float(relative_rms),
              "plot_omega": frequencies[indices].tolist(),
              "plot_estimated_spectrum": power.mean(axis=0)[indices].tolist()}
    folder = Path(__file__).resolve().parent
    (folder / "ch17-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = "force  cubic stiffness  response magnitude / force\n"
    report += "\n".join(f"{r['force_amplitude']:5.2f}  {r['cubic_stiffness']:15.2f}  "
                        f"{r['magnitude']:26.8f}" for r in fits)
    report += "\nFinite-band dispersion errors: "+", ".join(
        f"{r['absolute_error']:.8g}" for r in bands)+"\n"
    report += f"Equilibrium spectrum relative RMS error={relative_rms:.8f}\n"
    (folder / "ch17-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
