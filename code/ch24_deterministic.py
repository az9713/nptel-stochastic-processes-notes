"""Exact density transfer, symbolic cylinders, and a floating-point caveat."""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
cells = 64
edges = np.linspace(0, 1, cells+1)
centers = (edges[:-1]+edges[1:])/2
density_rows, tv_rows = [], []
for n in range(7):
    preimages = (centers[:, None]+np.arange(2**n))/(2**n)
    density = np.mean(2*preimages, axis=1)
    mass = density/cells  # midpoint rule is exact for this linear density
    expected = 1+2.0**(-n)*(2*centers-1)
    assert np.allclose(density, expected, atol=2e-14)
    assert abs(mass.sum()-1) < 1e-14
    tv = .5*np.abs(mass-1/cells).sum()
    assert abs(tv-2.0**(-n)/4) < 1e-14
    density_rows.append(density.tolist())
    tv_rows.append({'step': n, 'tv_distance': float(tv)})

# Uniform dyadic grid integrates these cylinder indicators exactly.
x = np.arange(4096)/4096
symbols = []
for n in range(3):
    symbols.append((x >= .5).astype(int))
    x = (2*x) % 1
words = 4*symbols[0]+2*symbols[1]+symbols[2]
counts = np.bincount(words, minlength=8)
assert np.all(counts == 512)

x = np.arange(4096)/4096
coarse = []
for n in range(3):
    coarse.append(x >= .75)  # True means B
    x = (2*x) % 1
current_a = ~coarse[1]
unconditioned = float(np.mean(coarse[2][current_a]))
history = coarse[0] & current_a
history_conditioned = float(np.mean(coarse[2][history]))
assert abs(unconditioned-1/6) < 1e-15 and history_conditioned == 0

value = .1
orbit = [value]
while value != 0:
    value = (2*value) % 1
    orbit.append(value)
    assert len(orbit) < 100
zero_step = len(orbit)-1
ratio = Fraction(1, 7)
rational_orbit = []
for _ in range(3):
    rational_orbit.append(str(ratio))
    ratio = (2*ratio) % 1
assert ratio == Fraction(1, 7)

result = {'cells': cells, 'centers': centers.tolist(),
          'density_rows': density_rows, 'tv_rows': tv_rows,
          'three_bit_word_counts': counts.tolist(),
          'coarse_next_B_given_A': unconditioned,
          'coarse_next_B_given_previous_B_current_A': history_conditioned,
          'float_initial': .1, 'float_zero_step': zero_step,
          'float_orbit': orbit, 'exact_rational_period3': rational_orbit}
(ROOT/'code/ch24-results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
lines = [f"step={row['step']}: total variation={row['tv_distance']:.8f}" for row in tv_rows]
lines += [f'Three-bit cylinder counts (4096 initial points): {counts.tolist()}',
          f'P(next B | A)={unconditioned:.8f}; P(next B | previous B, A)={history_conditioned:.8f}',
          f'Binary float starting at0.1 reaches zero at step{zero_step}.',
          f'Exact rational orbit: {rational_orbit}, period3.']
output = '\n'.join(lines)+'\n'
(ROOT/'code/ch24-output.txt').write_text(output, encoding='utf-8')
print(output, end='')
