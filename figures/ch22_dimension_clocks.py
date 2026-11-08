"""Show parity-correct lattice return decay and two clocks on one jump path."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch22-results.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch22'})
fig, ax = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
for law, color in zip(d['laws'], ['#245b89', '#357246', '#a64032']):
    ax[0].loglog(d['even_time'], law['even_return'], color=color,
                 label=f"Dimension {law['dimension']}")
ax[0].set(xlabel='Step n (even times only)', ylabel='Return probability',
          title='A. Exact lattice masses decay as n to power -d/2')
ax[0].legend(frameon=False)
for key, label, color in [('exponential_epochs', 'Exponential waits, mean 1 s', '#245b89'),
                           ('lomax_epochs', 'Lomax waits, index 1/2, scale 1 s', '#a64032')]:
    keep = [i for i, epoch in enumerate(d[key]) if epoch <= 100]
    stop = keep[-1]+1
    ax[1].step(d[key][:stop]+[100], d['position'][:stop]+[d['position'][stop-1]],
               where='post', label=label, color=color)
ax[1].set(xlabel='Physical time (s)', ylabel='Position (lattice units)',
          xlim=(0, 100), title='B. Identical spatial jumps; different elapsed-time progress')
ax[1].legend(frameon=False, fontsize=9)
for axis in ax:
    axis.grid(alpha=.18)
    axis.spines[['top', 'right']].set_visible(False)
fig.savefig(ROOT/'assets/ch22-dimension-clocks.svg', metadata={'Date': None})
fig.savefig(ROOT/'work/ch22-figure.png', dpi=130)
