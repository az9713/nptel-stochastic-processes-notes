"""Generate the pilot's first figure from exact chapter-1 results."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'code/ch01-results.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 12,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch01-equal-mean'})
fig, axes = plt.subplots(2, 1, figsize=(7, 7.6), layout='constrained')
colors = ['#245b89', '#a64032', '#357246', '#865aa4']
labels = ['Binomial: variance 3.2', 'Poisson: variance 4',
          'Geometric: variance 20', 'Neg. binomial: variance 8']
for law, color, label in zip(data['laws'], colors, labels):
    axes[0].plot(np.arange(21), law['pmf_0_to_40'][:21], marker='o',
                 markersize=3, linewidth=1.6, color=color, label=label)
axes[0].set(xlabel='Count n', ylabel='Probability P(X = n)',
            title='A. Same mean: 4 counts; different laws', xlim=(-.3, 20.3),
            ylim=(0, .26))
axes[0].legend(fontsize=10, loc='upper right', frameon=False)
axes[0].set_xticks([0, 4, 8, 12, 16, 20])
r = np.geomspace(1, 100, 301)
axes[1].plot(r, 1+4/r, color='#357246', linewidth=2)
axes[1].axhline(1, color='#a64032', linestyle='--', linewidth=1.2)
axes[1].scatter([1, 2, 4, 20, 100], [5, 3, 2, 1.2, 1.04],
                 color='#357246', s=30, zorder=3)
axes[1].set(xscale='log', xlabel='Equal-mean thermal components r',
            ylabel='Variance / mean', title='B. Fixed total mean: F = 1 + 4/r',
            ylim=(.7, 5.4), xlim=(.85, 120))
axes[1].set_xticks([1, 2, 4, 20, 100], labels=['1', '2', '4', '20', '100'])
axes[1].text(3.5, 4.6, 'Poisson limit: F = 1', color='#a64032', fontsize=11)
for axis in axes:
    axis.spines[['top', 'right']].set_visible(False)
    axis.grid(axis='y', alpha=.18)
target = ROOT / 'assets/ch01-equal-mean.svg'
fig.savefig(target, metadata={'Date': None})
preview = ROOT / 'work/validation'
preview.mkdir(parents=True, exist_ok=True)
fig.savefig(preview / 'ch01-equal-mean.png', dpi=150)
print(target.name)
