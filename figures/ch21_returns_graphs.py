"""Plot finite graph geometry and exact first-return tails."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch21-results.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch21'})
fig, ax = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
for a, b in d['graph_edges']:
    ax[0].plot([a[0]+a[1]/2, b[0]+b[1]/2],
               [a[1]*np.sqrt(3)/2, b[1]*np.sqrt(3)/2],
               color='#245b89', linewidth=.8)
ax[0].scatter([0, 8, 4], [0, 0, 4*np.sqrt(3)], color=['#357246', '#a64032', '#a64032'])
ax[0].set(aspect='equal', title='A. Generation-3 gasket: 125 mean steps from green to red')
ax[0].axis('off')
for r, color in zip(d['return_checks'], ['#245b89', '#a64032']):
    ax[1].loglog(2*np.array(d['m_plot']), r['first_return_even'],
                 label=f"Right-step probability {r['p']}", color=color)
ax[1].set(xlabel='Positive return step (even only)', ylabel='First-return probability',
          ylim=(1e-12, 1), title='B. Unbiased algebraic tail; biased exponential suppression')
ax[1].legend(frameon=False)
ax[1].grid(alpha=.18)
ax[1].spines[['top', 'right']].set_visible(False)
fig.savefig(ROOT/'assets/ch21-returns-graphs.svg', metadata={'Date': None})
fig.savefig(ROOT/'work/ch21-figure.png', dpi=130)
