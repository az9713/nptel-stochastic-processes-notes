"""Distinguish entrance, occupied-time, and symbolic first-return sampling."""
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SEED = 2026110829
rng = np.random.default_rng(SEED)
q = .7
occupancy = rng.random(1_000_000) < q
changes = np.diff(np.r_[False, occupancy, False].astype(int))
starts = np.flatnonzero(changes == 1)
ends = np.flatnonzero(changes == -1)
complete = (starts > 0) & (ends < len(occupancy))
lengths = ends[complete]-starts[complete]
entrance_mean = float(lengths.mean())
length_biased_mean = float(np.dot(lengths, lengths)/lengths.sum())
residual_mean = float(np.sum(lengths*(lengths+1)/2)/lengths.sum())
assert abs(entrance_mean-1/(1-q)) < .06
assert abs(length_biased_mean-(1+q)/(1-q)) < .1
assert abs(residual_mean-1/(1-q)) < .06

# Exact cylinder enumeration for C={first two binary digits are11}.
N = 14
integers = np.arange(2**(N+2), dtype=np.uint32)
bits = ((integers[:, None] >> np.arange(N+1, -1, -1)) & 1).astype(bool)
visits = bits[:, :-1] & bits[:, 1:]
active = visits[:, 0].copy()
denominator = active.sum()
returns = []
Q = np.array([[.5, .5], [.5, 0]])  # trailing0, trailing1; success absorbs
success = np.array([0, .5])
state = np.array([0., 1.])  # after an observed11 the last bit is1
for n in range(1, N+1):
    hit = active & visits[:, n]
    mass = float(hit.sum()/denominator)
    prediction = float(state@success)
    assert mass == prediction
    returns.append(mass)
    active &= ~visits[:, n]
    state = state@Q
mean_waits = np.linalg.solve(np.eye(2)-Q, np.ones(2))
assert np.allclose(mean_waits, [6, 4])

run_n = np.arange(1, 16)
fair_entrance = .5**run_n
fair_length_biased = run_n*.5**(run_n+1)
result = {'seed':SEED, 'occupancy_probability':q, 'record_length':len(occupancy),
          'complete_runs':len(lengths), 'sample_entrance_mean':entrance_mean,
          'sample_occupied_total_run_mean':length_biased_mean,
          'sample_occupied_residual_mean':residual_mean,
          'exact_entrance_mean':1/(1-q),
          'exact_occupied_total_run_mean':(1+q)/(1-q),
          'exact_occupied_residual_mean':1/(1-q),
          'run_n':run_n.tolist(), 'fair_entrance_mass':fair_entrance.tolist(),
          'fair_occupied_total_run_mass':fair_length_biased.tolist(),
          'cylinder11_return_mass':returns, 'cylinder11_mean':float(mean_waits[1]),
          'cylinder11_enumeration_horizon':N,
          'cylinder11_unreturned_mass_at_horizon':float(active.sum()/denominator)}
(ROOT/'code/ch25-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
output = (f'Complete occupied runs: {len(lengths)}\n'
          f'Entrance mean: sample={entrance_mean:.6f}; exact={1/(1-q):.6f}\n'
          f'Occupied-time total-run mean: sample={length_biased_mean:.6f}; exact={(1+q)/(1-q):.6f}\n'
          f'Occupied-time residual mean: sample={residual_mean:.6f}; exact={1/(1-q):.6f}\n'
          f'Cylinder11 return masses n=1..6: {returns[:6]}\n'
          f'Cylinder11 mean from backward equations: {mean_waits[1]:.6f}\n'
          f'Cylinder11 unreturned at step14: {result["cylinder11_unreturned_mass_at_horizon"]:.8f}\n')
(ROOT/'code/ch25-output.txt').write_text(output,encoding='utf-8')
print(output,end='')
