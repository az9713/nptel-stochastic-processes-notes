"""Stationary rectangular shot noise: exact moments and a padded simulation."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.signal import welch

ROOT = Path(__file__).resolve().parents[1]
RATE, WIDTH, DT, DURATION = 3.0, 0.4, 0.01, 5000.0
rng = np.random.default_rng(2026110821)
events = np.sort(rng.uniform(-WIDTH, DURATION,
                            rng.poisson(RATE*(DURATION+WIDTH))))
marks = rng.integers(1, 3, size=events.size)
prefix = np.r_[0, np.cumsum(marks)]
time = np.arange(0.0, DURATION, DT)
right = np.searchsorted(events, time, side='right')
left = np.searchsorted(events, time-WIDTH, side='right')
signal = prefix[right]-prefix[left]
mean = RATE*1.5*WIDTH
variance = RATE*2.5*WIDTH
third = RATE*4.5*WIDTH
independent = (rng.poisson(RATE*WIDTH/2, 300000)
               + 2*rng.poisson(RATE*WIDTH/2, 300000))
assert abs(independent.mean()-mean) < 6*np.sqrt(variance/independent.size)
assert abs(independent.var()-variance) < 0.08
assert abs(np.mean((independent-mean)**3)-third) < 0.35
lags = [0, 10, 20, 40, 80]
covariance = []
for lag in lags:
    observed = np.mean((signal[:len(signal)-lag or None]-mean)
                       * (signal[lag:]-mean))
    expected = RATE*2.5*max(WIDTH-lag*DT, 0.0)
    covariance.append({'lag': lag*DT, 'exact': expected,
                       'observed': float(observed)})
    assert abs(observed-expected) < 0.12
freq, psd_hz = welch(signal.astype(float)-mean, fs=1/DT,
                     nperseg=8192, detrend=False)
psd_angular = psd_hz.copy()
psd_angular[1:-1] /= 2  # DC and Nyquist are undoubled endpoints.
theory = RATE*2.5*WIDTH**2*np.sinc(freq*WIDTH)**2
assert abs(np.trapezoid(psd_hz, freq)-variance) < 0.15
area, error = quad(lambda u: RATE*2.5*max(WIDTH-abs(u), 0),
                   -WIDTH, WIDTH, epsabs=1e-12)
assert abs(area-RATE*2.5*WIDTH**2) < 1e-12
result = {
    'seed': 2026110821, 'rate': RATE, 'width': WIDTH,
    'dt': DT, 'duration': DURATION, 'event_count': int(events.size),
    'exact_mean': mean, 'exact_variance': variance,
    'exact_third_cumulant': third,
    'independent_mean': float(independent.mean()),
    'independent_variance': float(independent.var()),
    'stationary_record_mean': float(signal.mean()),
    'stationary_record_variance': float(signal.var()),
    'covariance': covariance,
    'spectrum_zero': float(theory[0]),
    'welch_integrated_variance': float(np.trapezoid(psd_hz, freq)),
    'first_spectral_zero_hz': 1/WIDTH,
    'trace_time': time[:1001].tolist(),
    'trace_signal': signal[:1001].tolist(),
    'frequency_hz': freq[:1230].tolist(),
    'angular_spectrum_estimate': psd_angular[:1230].tolist(),
    'angular_spectrum_exact': theory[:1230].tolist(),
}
(ROOT/'code/ch18-results.json').write_text(json.dumps(result, indent=2)+'\n')
report = (f"mean={mean:.6f}; variance={variance:.6f}; "
          f"third cumulant={third:.6f}\n"
          f"stationary record mean={signal.mean():.6f}; "
          f"variance={signal.var():.6f}\n"
          f"integrated Welch variance={result['welch_integrated_variance']:.6f}\n"
          f"first spectral zero={1/WIDTH:.6f} Hz\n")
(ROOT/'code/ch18-output.txt').write_text(report)
print(report, end='')
