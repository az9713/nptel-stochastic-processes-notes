"""Preimages, ensemble transfer and a finite-precision individual orbit."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch24-results.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10,
                     'svg.fonttype':'none','svg.hashsalt':'ch24'})
fig, ax = plt.subplots(3, 1, figsize=(7, 8), layout='constrained')
ax[0].plot([0,.5], [0,1], color='#245b89')
ax[0].plot([.5,1], [0,1], color='#245b89')
for preimage in [.15,.65]:
    ax[0].plot([preimage,preimage], [0,.3], ':', color='#a64032')
    ax[0].scatter([preimage],[.3],color='#a64032')
ax[0].axhline(.3, color='#a64032', linestyle='--', linewidth=.8)
ax[0].set(xlabel='Initial coordinate x',ylabel='T(x)',
          title='A. Two preimages of y = 0.3: x = 0.15 and 0.65')
for n in [0,1,3,6]:
    ax[1].plot(d['centers'], d['density_rows'][n],label=f'Step {n}')
ax[1].set(xlabel='Coordinate y',ylabel='Probability density',
          title='B. Ensemble density approaches uniform under exact transfer')
ax[1].legend(frameon=False, ncol=4)
orbit = d['float_orbit']+[0]*20
ax[2].plot(np.arange(len(orbit)), orbit, color='#357246', linewidth=.9)
ax[2].axvline(d['float_zero_step'], color='#a64032', linestyle='--',
              label=f"Float reaches zero at step {d['float_zero_step']}")
ax[2].set(xlabel='Iteration n',ylabel='One float orbit',
          title='C. Finite precision exhausts the stored binary digits')
ax[2].legend(frameon=False)
for a in ax:
    a.grid(alpha=.18)
    a.spines[['top','right']].set_visible(False)
fig.savefig(ROOT/'assets/ch24-deterministic.svg',metadata={'Date':None})
fig.savefig(ROOT/'work/ch24-figure.png',dpi=130)
