"""Endpoint conventions, length bias, and correlated cylinder returns."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'work').mkdir(exist_ok=True)
d = json.loads((ROOT/'code/ch25-results.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10,
                    'svg.fonttype':'none','svg.hashsalt':'ch25'})
fig, ax = plt.subplots(3,1,figsize=(7,8),layout='constrained')
record = np.array([0,0,1,1,1,1,0,0,0,1,1,0])
ax[0].step(np.arange(12),record,where='post',color='#245b89',linewidth=2)
ax[0].scatter(np.arange(12),record,color='#245b89',s=18)
for left,right,height,label,color in [(2,6,.78,'Entrance run: 4','#357246'),
                                      (4,6,.53,'Residual: 2','#a64032'),
                                      (6,9,.28,'Outside excursion: 3','#72549b')]:
    ax[0].annotate('',(right,height),(left,height),
                   arrowprops={'arrowstyle':'<->','color':color})
    ax[0].text((left+right)/2,height+.035,label,ha='center',color=color,fontsize=9)
ax[0].axvline(4,color='#a64032',linestyle=':',linewidth=.8)
ax[0].set(xlabel='Sample index (entrance2; observation4; exit6; re-entry9)',
          ylabel='Occupied indicator',ylim=(-.1,1.15),
          title='A. Count occupied samples; the exit sample is excluded')
n=np.array(d['run_n'])
ax[1].bar(n-.18,d['fair_entrance_mass'],width=.36,color='#245b89',label='Entrance run; also occupied residual')
ax[1].bar(n+.18,d['fair_occupied_total_run_mass'],width=.36,color='#a64032',label='Total run at occupied observation')
ax[1].set(xlim=(.4,8.6),xlabel='Length (samples)',ylabel='Probability mass',
          title='B. Fair independent occupancy: total intervals are length-biased')
ax[1].legend(frameon=False,fontsize=9)
k=np.arange(1,15)
ax[2].bar(k-.18,d['cylinder11_return_mass'],width=.36,color='#245b89',label='Exact overlapping11 cylinder')
ax[2].bar(k+.18,.25*.75**(k-1),width=.36,color='#a64032',label='Independent-visits guess')
ax[2].set(xlabel='First positive return step',ylabel='Probability mass',
          title='C. Same stationary measure1/4; different return distribution')
ax[2].legend(frameon=False,fontsize=9)
for a in ax:
    a.grid(axis='y',alpha=.18)
    a.spines[['top','right']].set_visible(False)
fig.savefig(ROOT/'assets/ch25-sojourn.svg',metadata={'Date':None})
fig.savefig(ROOT/'work/ch25-figure.png',dpi=130)
