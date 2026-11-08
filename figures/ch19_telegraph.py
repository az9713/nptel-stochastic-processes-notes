"""Plot a mixed law without depicting atomic weights as density heights."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch19-results.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch19'})
fig, ax = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
ax[0].plot(d['density_x'], d['density_t1'], color='#245b89')
ax[0].set(xlabel='Position (m)', ylabel='Interior density (1/m)',
          xlim=(-1.3, 1.3), ylim=(0, .7), title='A. Time 1 s: continuous part and two atoms')
for sign in (-1, 1):
    ax[0].annotate('', xy=(sign, .52), xytext=(sign, 0),
                   arrowprops={'arrowstyle': '->', 'color': '#a64032', 'lw': 2})
    ax[0].text(sign, .55, 'mass 0.18394', ha='center', fontsize=10, color='#a64032')
ax[0].text(0, .1, 'Arrow heights are schematic; labels give masses.',
           ha='center', fontsize=9)
t = np.array(d['time_grid'])
ax[1].loglog(t, d['msd_grid'], color='#245b89', label='Exact mean square displacement')
ax[1].loglog(t, t*t, '--', color='#a64032', label='Ballistic: t squared')
ax[1].loglog(t, t, ':', color='#357246', label='Long-time diffusion: t')
ax[1].set(xlabel='Time (s)', ylabel='Mean square displacement (m squared)',
          title='B. Speed 1 m/s; reversal rate 1/s', ylim=(1e-5, 200))
ax[1].legend(fontsize=9, frameon=False)
for axis in ax:
    axis.spines[['top', 'right']].set_visible(False)
    axis.grid(alpha=.18)
fig.savefig(ROOT/'assets/ch19-telegraph.svg', metadata={'Date': None})
fig.savefig(ROOT/'work/ch19-figure.png', dpi=130)
