"""Check the mixed telegraph law by quadrature and exact event simulation."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.special import iv

ROOT = Path(__file__).resolve().parents[1]


def density(x, time, speed=1.0, rate=1.0):
    if abs(x) >= speed*time:
        return 0.0
    radius = np.sqrt((speed*time)**2-x*x)
    z = rate*radius/speed
    return (rate*np.exp(-rate*time)/(2*speed)
            * (iv(0, z)+speed*time/radius*iv(1, z)))


def msd(time, speed=1.0, rate=1.0):
    return speed**2/rate*(time+np.expm1(-2*rate*time)/(2*rate))


rng = np.random.default_rng(2026110822)
checks = []
for time in (0.1, 1.0, 5.0):
    mass = quad(lambda x: density(x, time), -time, time)[0]
    second = quad(lambda x: x*x*density(x, time), -time, time)[0]
    atom_total = np.exp(-time)
    assert abs(mass+atom_total-1) < 1e-10
    assert abs(second+time*time*atom_total-msd(time)) < 1e-10
    counts = rng.poisson(time, 100000)
    initial = rng.choice([-1, 1], len(counts))
    position = np.empty(len(counts))
    for count in range(counts.max()+1):
        select = np.flatnonzero(counts == count)
        epochs = np.sort(rng.uniform(0, time, (len(select), count)), axis=1)
        spans = np.diff(np.column_stack((np.zeros(len(select)), epochs,
                                        np.full(len(select), time))), axis=1)
        position[select] = initial[select]*(spans*(-1.)**np.arange(count+1)).sum(1)
    assert abs(np.mean(position**2)-msd(time)) < 0.035*msd(time)
    assert abs(np.mean(counts == 0)-atom_total) < 0.008
    checks.append({'time': time, 'interior_mass': mass,
                   'total_atom_mass': float(atom_total),
                   'exact_msd': float(msd(time)),
                   'sample_msd': float(np.mean(position**2)),
                   'sample_atom_mass': float(np.mean(counts == 0))})
result = {'seed': 2026110822, 'speed': 1.0, 'rate': 1.0,
          'ensemble_size': 100000, 'checks': checks,
          'density_x': np.linspace(-.9999, .9999, 401).tolist(),
          'density_t1': [density(x, 1.) for x in np.linspace(-.9999, .9999, 401)],
          'time_grid': np.geomspace(.01, 100, 301).tolist(),
          'msd_grid': msd(np.geomspace(.01, 100, 301)).tolist()}
(ROOT/'code/ch19-results.json').write_text(json.dumps(result, indent=2)+'\n')
report = '\n'.join(f"t={d['time']:g}: interior={d['interior_mass']:.8f}; "
                   f"atoms={d['total_atom_mass']:.8f}; "
                   f"MSD={d['exact_msd']:.8f}; sample={d['sample_msd']:.8f}"
                   for d in checks)+'\n'
(ROOT/'code/ch19-output.txt').write_text(report)
print(report, end='')
