"""Compare a heavy hitting tail with bounded-domain survival."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch20-results.json').read_text())
t = np.array(d['time'])
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch20'})
fig, ax = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
ax[0].loglog(t, d['first_passage_density'], color='#245b89', label='Exact; target distance 1 m')
ax[0].loglog(t, 1/np.sqrt(4*np.pi*t**3), '--', color='#a64032', label='Long-time t to power -3/2')
ax[0].set(xlabel='Time (s)', ylabel='First-passage density (1/s)',
          ylim=(1e-5, 2), title='A. Eventual arrival is certain; mean time is infinite')
ax[0].legend(frameon=False, fontsize=9)
ax[1].semilogy(t, d['survival_halfline_a_half'], color='#245b89', label='One target; distance 0.5 m')
ax[1].semilogy(t, d['survival_interval_center'], color='#357246', label='Absorbing interval length 1 m; start center')
ax[1].set(xlabel='Time (s)', ylabel='Survival probability', xlim=(0, 2),
          ylim=(1e-6, 1.1), title='B. A second absorbing boundary removes the heavy tail')
ax[1].legend(frameon=False, fontsize=9)
for axis in ax:
    axis.spines[['top', 'right']].set_visible(False)
    axis.grid(alpha=.18)
fig.savefig(ROOT/'assets/ch20-first-passage.svg', metadata={'Date': None})
fig.savefig(ROOT/'work/ch20-figure.png', dpi=130)
