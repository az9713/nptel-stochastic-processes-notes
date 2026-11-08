"""Exact return coefficients, parity normalization, and independent clocks."""
from pathlib import Path
import json

import numpy as np
from scipy.special import gammaln, logsumexp

ROOT = Path(__file__).resolve().parents[1]
n = np.arange(1, 1001)
log_central = gammaln(2*n+1)-2*gammaln(n+1)
u1 = np.exp(log_central-2*n*np.log(2))
u2 = np.exp(2*log_central-4*n*np.log(2))
u3 = []
for count, central in zip(n, log_central):
    k = np.arange(count+1)
    log_choose = gammaln(count+1)-gammaln(k+1)-gammaln(count-k+1)
    pair = gammaln(2*k+1)-2*gammaln(k+1)
    u3.append(np.exp(central-2*count*np.log(6)+logsumexp(2*log_choose+pair)))
laws = []
for dimension, u in enumerate((u1, u2, np.array(u3)), start=1):
    assert abs(u[0]-1/(2*dimension)) < 1e-14
    asymptotic = 2*(dimension/(4*np.pi*n))**(dimension/2)
    assert abs(u[-1]/asymptotic[-1]-1) < .002
    laws.append({'dimension': dimension, 'even_return': u.tolist(),
                 'asymptotic': asymptotic.tolist(),
                 'green_partial_100': float(1+u[:100].sum()),
                 'green_partial_1000': float(1+u.sum()),
                 'large_time_ratio': float(u[-1]/asymptotic[-1])})
rng = np.random.default_rng(2026110826)
jumps = rng.choice([-1, 1], 200)
position = np.r_[0, jumps.cumsum()]
exp_clock = np.r_[0, np.cumsum(rng.exponential(1., len(jumps)))]
heavy_clock = np.r_[0, np.cumsum(rng.pareto(.5, len(jumps)))]
ages = np.array([0., 1., 10.])
residual = ((1+ages+1)/(1+ages))**(-.5)
assert np.all(np.diff(residual) > 0)
result = {'even_time': (2*n).tolist(), 'laws': laws,
          'clock_seed': 2026110826, 'position': position.tolist(),
          'exponential_epochs': exp_clock.tolist(),
          'lomax_epochs': heavy_clock.tolist(),
          'ages': ages.tolist(), 'one_second_residual_survival': residual.tolist()}
(ROOT/'code/ch22-results.json').write_text(json.dumps(result, indent=2)+'\n')
report = '\n'.join(f"d={r['dimension']}: G_200={r['green_partial_100']:.8f}; "
                   f"G_2000={r['green_partial_1000']:.8f}; "
                   f"parity-correct ratio={r['large_time_ratio']:.8f}" for r in laws)
report += '\nResidual survival at ages 0,1,10: '+', '.join(f'{x:.8f}' for x in residual)+'\n'
(ROOT/'code/ch22-output.txt').write_text(report)
print(report, end='')
