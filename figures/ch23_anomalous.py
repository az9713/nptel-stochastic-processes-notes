"""Separate unbiased subdiffusion and bias-induced clock dispersion."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch23-results.json').read_text())
times = np.geomspace(.1, 1000, 200)
means, variances = [], []
for time in times:
    n = np.arange(1, int(20*np.sqrt(time))+100)
    tail = erfc(n/(2*np.sqrt(time)))
    mean = tail.sum()
    var_n = np.dot(2*n-1, tail)-mean**2
    means.append(mean)
    variances.append(.91*mean+.09*var_n)
means, variances = np.array(means), np.array(variances)
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch23'})
fig, ax = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
ax[0].loglog(times, means, color='#245b89', label='Heavy clock; unbiased jump variance 1')
ax[0].loglog(times, times, '--', color='#357246', label='Rate-1 Poisson clock')
ax[0].loglog(times, 2*np.sqrt(times/np.pi), ':', color='#a64032', label='Heavy-clock large-time limit')
ax[0].set(xlabel='Time (s)', ylabel='Position variance (lattice units²)',
          title='A. Zero jump mean: variance is the expected jump count')
ax[0].legend(frameon=False, fontsize=9)
ax[1].loglog(times, .3*means, color='#357246', label='Mean position (lattice units)')
ax[1].loglog(times, variances, color='#245b89', label='Centered variance (units squared)')
ax[1].loglog(times, variances+.09*means**2, color='#a64032', label='Uncentered MSD (units squared)')
ax[1].set(xlabel='Time (s)', ylabel='Named moment in stated lattice units',
          title='B. Bias p = 0.65: clock dispersion changes variance scaling')
ax[1].legend(frameon=False, fontsize=9)
for axis in ax:
    axis.grid(alpha=.18)
    axis.spines[['top', 'right']].set_visible(False)
fig.savefig(ROOT/'assets/ch23-anomalous.svg', metadata={'Date': None})
fig.savefig(ROOT/'work/ch23-figure.png', dpi=130)
