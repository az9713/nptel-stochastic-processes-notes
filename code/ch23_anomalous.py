"""An exact index-one-half renewal clock and random-sum moment checks."""
from pathlib import Path
import json

import numpy as np
from scipy.special import erfc

ROOT = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(2026110827)
times = np.array([1., 10., 100., 1000.])
count = 20000
epochs = np.zeros(count)
counts = np.zeros((count, len(times)), dtype=int)
trace_epochs = [[] for _ in range(64)]
while np.any(epochs <= times[-1]):
    active = np.flatnonzero(epochs <= times[-1])
    waits = .5/rng.normal(size=len(active))**2
    epochs[active] += waits
    counts[active] += epochs[active, None] <= times
    for index in active[active < 64]:
        if epochs[index] <= times[-1]:
            trace_epochs[index].append(float(epochs[index]))
rows = []
for column, time in enumerate(times):
    n = np.arange(1, int(20*np.sqrt(time))+100)
    survival = erfc(n/(2*np.sqrt(time)))
    mean_n = float(survival.sum())
    second_n = float(np.dot(2*n-1, survival))
    var_n = second_n-mean_n**2
    sample_n = counts[:, column]
    assert abs(sample_n.mean()-mean_n) < 6*np.sqrt(var_n/count)
    biased = 2*rng.binomial(sample_n, .65)-sample_n
    unbiased = 2*rng.binomial(sample_n, .5)-sample_n
    mean_x, var_x = .3*mean_n, .91*mean_n+.09*var_n
    assert abs(biased.mean()-mean_x) < 6*np.sqrt(var_x/count)
    assert abs(unbiased.var()-mean_n) < .10*mean_n
    rows.append({'time': time, 'mean_count': mean_n, 'variance_count': var_n,
                 'sample_mean_count': float(sample_n.mean()),
                 'unbiased_variance': mean_n, 'biased_mean': mean_x,
                 'biased_variance': var_x, 'biased_msd': var_x+mean_x**2,
                 'sample_biased_mean': float(biased.mean()),
                 'sample_biased_variance': float(biased.var())})
averages = []
grid = np.arange(1001)
for event_times in trace_epochs:
    jumps = rng.choice([-1, 1], len(event_times))
    path = np.r_[0, jumps.cumsum()][np.searchsorted(event_times, grid, side='right')]
    averages.append(float(np.mean((path[10:]-path[:-10])**2)))
result = {'seed': 2026110827, 'ensemble_size': count, 'rows': rows,
          'tamsd_protocol': {'trajectories': 64, 'duration': 1000, 'lag': 10,
                             'sample_spacing': 1},
          'tamsd_mean': float(np.mean(averages)),
          'tamsd_standard_deviation': float(np.std(averages, ddof=1)),
          'ensemble_msd_lag10': rows[1]['unbiased_variance']}
(ROOT/'code/ch23-results.json').write_text(json.dumps(result, indent=2)+'\n')
report = '\n'.join(f"t={r['time']:g}: E[N]={r['mean_count']:.6f}; "
                   f"sample={r['sample_mean_count']:.6f}; "
                   f"biased variance={r['biased_variance']:.6f}; "
                   f"biased MSD={r['biased_msd']:.6f}" for r in rows)
report += f"\nLag10 ensemble MSD={result['ensemble_msd_lag10']:.6f}; "
report += f"time-average mean={result['tamsd_mean']:.6f}, "
report += f"across-path SD={result['tamsd_standard_deviation']:.6f}\n"
(ROOT/'code/ch23-output.txt').write_text(report)
print(report, end='')
