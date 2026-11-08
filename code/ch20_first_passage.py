"""Backward exit equations, first-passage tails, and missed crossings."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve_banded
from scipy.special import erf, erfc

ROOT = Path(__file__).resolve().parents[1]
D, LENGTH = 1.0, 1.0
grid_checks = []
for intervals in (20, 40, 80, 160):
    dx = LENGTH/intervals
    x = np.arange(1, intervals)*dx
    matrix = np.zeros((3, intervals-1))
    matrix[0, 1:] = -D/dx**2
    matrix[1] = 2*D/dx**2
    matrix[2, :-1] = -D/dx**2
    times = solve_banded((1, 1), matrix, np.ones(intervals-1))
    error = float(np.max(abs(times-x*(LENGTH-x)/(2*D))))
    assert error < 2e-13
    grid_checks.append({'intervals': intervals, 'maximum_error': error})
target, horizon = 1.0, 1.0
exact_hit = float(erfc(target/np.sqrt(4*D*horizon)))
rng = np.random.default_rng(2026110824)
crossings = []
for dt in (.1, .02, .005):
    count = 100000
    position = np.zeros(count)
    endpoint_hit = np.zeros(count, dtype=bool)
    bridge_hit = np.zeros(count, dtype=bool)
    for step in range(round(horizon/dt)):
        new = position+rng.normal(0, np.sqrt(2*D*dt), count)
        endpoint_hit |= new >= target
        below = (position < target) & (new < target)
        probability = np.zeros(count)
        probability[below] = np.exp(-(target-position[below])
                                   *(target-new[below])/(D*dt))
        bridge_hit |= (new >= target) | (rng.random(count) < probability)
        position = new
    observed = float(bridge_hit.mean())
    assert abs(observed-exact_hit) < .007
    assert endpoint_hit.mean() <= bridge_hit.mean()
    crossings.append({'dt': dt, 'endpoints_only': float(endpoint_hit.mean()),
                       'bridge_corrected': observed})
tail_checks = []
for cutoff in (10., 100., 1000.):
    partial_mean = quad(lambda t: target*np.exp(-target**2/(4*D*t))
                        / np.sqrt(4*np.pi*D*t), 0, cutoff)[0]
    tail_checks.append({'cutoff': cutoff, 'unnormalized_partial_mean': partial_mean})
time = np.geomspace(.003, 10, 400)
f = target*np.exp(-target**2/(4*D*time))/np.sqrt(4*np.pi*D*time**3)
survival_halfline = erf(.5/np.sqrt(4*D*time))
n = np.arange(100)
survival_interval = np.sum(4/np.pi*((-1.)**n/(2*n+1))[:, None]
                           * np.exp(-(((2*n+1)*np.pi)**2)[:, None]*time), axis=0)
result = {'diffusion': D, 'length': LENGTH, 'grid_checks': grid_checks,
          'interval_center_mean_exit': .125,
          'reflecting_left_center_mean_exit': .375,
          'exact_hit_by_t1': exact_hit, 'crossing_checks': crossings,
          'tail_checks': tail_checks, 'time': time.tolist(),
          'first_passage_density': f.tolist(),
          'survival_halfline_a_half': survival_halfline.tolist(),
          'survival_interval_center': survival_interval.tolist()}
(ROOT/'code/ch20-results.json').write_text(json.dumps(result, indent=2)+'\n')
report = f"Exact hit probability by t=1: {exact_hit:.8f}\n"
report += '\n'.join(f"dt={c['dt']:.3f}: endpoint={c['endpoints_only']:.5f}; "
                    f"bridge={c['bridge_corrected']:.5f}" for c in crossings)+'\n'
report += '\n'.join(f"cutoff={c['cutoff']:g}: partial first moment="
                    f"{c['unnormalized_partial_mean']:.6f}" for c in tail_checks)+'\n'
(ROOT/'code/ch20-output.txt').write_text(report)
print(report, end='')
