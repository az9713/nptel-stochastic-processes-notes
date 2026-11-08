"""Plot the retained rectangular-pulse simulation and exact spectral envelope."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch18-results.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'ch18'})
fig, ax = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
ax[0].step(d['trace_time'], d['trace_signal'], where='post', color='#245b89')
ax[0].axhline(d['exact_mean'], color='#a64032', linestyle='--', label='Mean 1.8')
ax[0].set(xlabel='Time (s)', ylabel='Signal (arbitrary units)',
          title='A. Overlapping pulses, widths 0.4 s; heights 1 or 2')
ax[0].legend(frameon=False)
ax[1].plot(d['frequency_hz'], d['angular_spectrum_estimate'],
           color='#888888', linewidth=.7, label='Finite-record Welch estimate')
ax[1].plot(d['frequency_hz'], d['angular_spectrum_exact'],
           color='#a64032', label='Exact continuous-time envelope')
ax[1].set(xlabel='Frequency f = angular frequency / (2 pi) (Hz)',
          ylabel='Spectrum (signal units squared s)',
          title='B. Pulse-width zeros at multiples of 2.5 Hz',
          xlim=(0, 10), ylim=(0, 1.5))
ax[1].legend(frameon=False, fontsize=9)
for axis in ax:
    axis.spines[['top', 'right']].set_visible(False)
    axis.grid(alpha=.18)
fig.savefig(ROOT/'assets/ch18-shot-noise.svg', metadata={'Date': None})
fig.savefig(ROOT/'work/ch18-figure.png', dpi=130)
