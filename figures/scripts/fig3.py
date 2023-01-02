from frontiers_yildizetal.analysis import uq
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import string

pem_mom = uq.Moments('synth').get_pem()
mcs_mom = uq.Moments('synth').get_mcs()

f_names = list(uq.Moments.funcs.keys())
scalars = list(pem_mom['mean'].keys())

diff_col = {}
for f in f_names:
    diff_col[f] = {}
    for s in scalars:
        x1 = pem_mom[f][s]
        x2 = mcs_mom[f][s]
        diff_col[f][s] = ['#F19EB1' if (y - x) > 0 else '#8EBAE5' for x, y in zip(x1, x2)]

locs = [1, 2, 3]
xlimits = (
    (2.3, 2.38),
    (0, 0.36),
    (-0.5, 0.5),
    (1.12, 1.20),
    (0, 0.2),
    (-0.4, 0.4),
    (1.35, 1.39),
    (0, 0.6),
    (-0.1, 0.1),
    (47, 51),
    (0, 80),
    (-0.8, 0.8),
    (10, 12),
    (0, 16),
    (-0.8, 0.8),
)
letters = list(string.ascii_uppercase)

fig, axs = plt.subplots(5, 3)
axs = axs.ravel()

for i, f in enumerate(f_names):
    for j, s in enumerate(scalars):
        axs[i + 3 * j].scatter(mcs_mom[f][s], locs, color='k', marker='o', s=10)
        axs[i + 3 * j].scatter(pem_mom[f][s], locs, color='k', marker='s', s=10)
        axs[i + 3 * j].hlines(
            y=locs,
            xmin=mcs_mom[f][s],
            xmax=pem_mom[f][s],
            color=diff_col[f][s],
            zorder=0,
            linewidth=2,
        )
        axs[i + 3 * j].set_ylim(0.75, 3.25)
        axs[i + 3 * j].set_yticks((1, 2, 3))
        axs[i + 3 * j].set_xlim(xlimits[i + 3 * j])
        axs[i + 3 * j].set_xticks(np.linspace(xlimits[i + 3 * j][0], xlimits[i + 3 * j][1], 5))
        if i == 0:
            axs[i + 3 * j].set_yticklabels(('COV = 10%', 'COV = 25%', 'COV = 50%'))
        else:
            axs[i + 3 * j].set_yticklabels([])
        if i == 2:
            axs[i + 3 * j].text(1.1 * xlimits[i + 3 * j][1], 3, letters[j], weight='bold')

axs[1].legend(
    loc='upper center', bbox_to_anchor=(0.5, 1.4), ncol=2, frameon=False, fancybox=False
)
axs[1].legend(
    [
        Line2D([0], [0], color='#F19EB1'),
        Line2D([0], [0], marker='o', color='k', lw=0),
        Line2D([0], [0], color='#8EBAE5'),
        Line2D([0], [0], marker='s', color='k', lw=0),
    ],
    ['MCS > PEM', 'Monte Carlo simulations (MCS)', 'MCS < PEM', 'Point estimate method (PEM)'],
    loc='upper center',
    bbox_to_anchor=(0.5, 1.7),
    ncol=2,
    frameon=False,
    fancybox=False,
)

axs[12].set_xlabel('Mean')
axs[13].set_xlabel('Variance')
axs[14].set_xlabel('Skewness')

plt.rcParams['figure.figsize'] = [18 / 2.54, 18 / 2.54]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.tight_layout()
plt.subplots_adjust(wspace=0.2, hspace=0.3)

plt.savefig('figures/PDF/fig3.pdf', format='pdf', bbox_inches='tight', facecolor='w')
plt.savefig('figures/EPS/fig3.eps', format='eps', bbox_inches='tight', facecolor='w')
