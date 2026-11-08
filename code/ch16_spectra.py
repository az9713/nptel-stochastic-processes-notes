"""OU periodogram normalization, finite-record scatter, and RC thermal area."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.signal import lfilter


def run():
    rng = np.random.default_rng(2026110816)
    h, gamma, theta, count, n = 0.02, 1., 1., 1024, 8192
    r = np.exp(-gamma*h)
    initial = rng.normal(scale=np.sqrt(theta), size=count)
    x, _ = lfilter([np.sqrt(theta*(1-r*r))], [1, -r],
                   rng.normal(size=(count, n)), axis=1,
                   zi=(r*initial)[:, None])
    transform = np.fft.rfft(x, axis=1)
    periodogram = h/n*np.abs(transform)**2
    spectral_area = (periodogram[:, 0]+periodogram[:, -1]
                     + 2*periodogram[:, 1:-1].sum(axis=1))/(n*h)
    assert np.allclose(spectral_area, np.mean(x*x, axis=1))
    rows = []
    target = 2*np.pi*4/(1024*h)
    for length in (1024, 8192):
        index = length//256
        fourier = np.fft.rfft(x[:, :length], axis=1)[:, index]
        values = h/length*np.abs(fourier)**2
        lags = np.arange(1, length)
        expected = h*theta*(1+2*np.sum(
            (1-lags/length)*r**lags*np.cos(target*h*lags)))
        assert abs(values.mean()/expected-1) < 0.12
        ratio = values.var()/values.mean()**2
        assert 0.75 < ratio < 1.3
        rows.append({"cells": length, "duration": length*h,
                     "frequency": target, "mean_periodogram": float(values.mean()),
                     "finite_record_expectation": float(expected),
                     "relative_variance": float(ratio)})
    resistance, capacitance, thermal_energy = 2., 3., 1.
    rc_variance = quad(lambda w: 2*thermal_energy*resistance
                       / (1+(w*resistance*capacitance)**2)/np.pi, 0, np.inf)[0]
    assert np.isclose(rc_variance, thermal_energy/capacitance)
    source = np.array([[1., .7], [.7, 2.]])
    for w in (0., .2, 1., 10.):
        filt = np.diag([1/(1-1j*w), 1/(2-1j*w)])
        output = filt @ source @ filt.conj().T
        assert np.allclose(output, output.conj().T)
        assert np.linalg.eigvalsh(output).min() > 0
    omega = 2*np.pi*np.fft.rfftfreq(n, h)
    indices = np.unique(np.geomspace(1, n//2, 300).astype(int))
    result = {"seed": 2026110816, "h": h, "gamma": gamma, "theta": theta,
              "ensemble": count, "rows": rows, "rc_variance": rc_variance,
              "sample_variance": float(np.mean(x*x)),
              "spectrum_area": float(spectral_area.mean()),
              "plot_omega": omega[indices].tolist(),
              "plot_ensemble_spectrum": periodogram.mean(axis=0)[indices].tolist(),
              "plot_single_spectrum": periodogram[0, indices].tolist()}
    folder = Path(__file__).resolve().parent
    (folder / "ch16-results.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")
    report = "duration   mean periodogram   finite-record mean   relative variance\n"
    report += "\n".join(f"{q['duration']:8.2f}   {q['mean_periodogram']:16.8f}   "
                        f"{q['finite_record_expectation']:18.8f}   "
                        f"{q['relative_variance']:17.8f}" for q in rows)
    report += f"\nRC filtered variance={rc_variance:.8f}; kBT/C={1/3:.8f}\n"
    (folder / "ch16-output.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    run()
