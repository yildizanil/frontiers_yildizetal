import frontiers_yildizetal as fy
from frontiers_yildizetal.emulators import *
import pkg_resources
import pandas as pd
import numpy as np
from scipy.stats import skew
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

pem = Simulations('synth_pem')
pem_scalar = pem.curate_scalars(threshold=0.1, loc_x=1000, loc_y=2000)

synth = ScalarEmulators('synth', threshold=0.1, loc_x=1000, loc_y=2000)

scalars = list(pem_scalar.keys())
mcs_analysis = ['mcs1','mcs2','mcs3']
pem_analysis = ['pem1','pem2','pem3']
funcs = [np.mean, np.var, skew]
f_names = ['mean','var','skew']

mcs_moments = {}
for i in scalars:
    for j in mcs_analysis:
        path = 'files/input/input_' + j + '_synth.csv'
        filepath = pkg_resources.resource_filename(
            'frontiers_yildizetal', path)
        input_test = np.genfromtxt(filepath, delimiter=',', skip_header=1)
        
        predicted = synth.predict_scalar(i, input_test)[0]
        for k, f in enumerate(funcs):
            naming = j + '_' + i + '_' + f_names[k]
            if f is np.var:
                mcs_moments[naming] = round(f(predicted, ddof=1), 3)
            else:
                mcs_moments[naming] = round(f(predicted), 3)

pem_moments = {}
for i, mcs in enumerate(pem_analysis):
    for scalar in scalars:
        data = pem_scalar[scalar][8*i:8*(i+1)]
        for j, f in enumerate(funcs):
            naming = mcs + '_' + scalar + '_' + f_names[j]
            if f is np.var:
                pem_moments[naming] = round(f(data,ddof=1), 3)
            else:
                pem_moments[naming] = round(f(data), 3)
                
locs = [1,2,3]

summary_pem = {}
summary_mcs = {}
diff_col = {}

for scalar in scalars:
    for f in f_names:
        summary_name = scalar + '_' + f
        summary_pem[summary_name] = []
        summary_mcs[summary_name] = []
        diff_col[summary_name] = []
        
        for mcs, pem in zip(mcs_analysis, pem_analysis):
            name_mcs = mcs + '_' + scalar + '_' + f
            name_pem = pem + '_' + scalar + '_' + f
            
            val_mcs = mcs_moments[name_mcs]
            val_pem = pem_moments[name_pem]
     
            diff = '#F19EB1' if (val_mcs - val_pem) > 0 else '#8EBAE5'
     
            summary_mcs[summary_name].append(val_mcs)
            summary_pem[summary_name].append(val_pem)
            diff_col[summary_name].append(diff)

sk = list(summary_mcs.keys())
         
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6),
      (ax7, ax8, ax9), (ax10, ax11, ax12),
      (ax13, ax14, ax15)) = plt.subplots(nrows=5, ncols=3, sharey='row')

ax1.scatter(summary_mcs[sk[0]], locs, color='k', marker='o', s=10)
ax1.scatter(summary_pem[sk[0]], locs, color='k', marker='s', s=10)
ax1.hlines(y=locs, xmin=summary_mcs[sk[0]], xmax=summary_pem[sk[0]],
           color=diff_col[sk[0]], zorder=0, linewidth=2)

ax1.set_xlim(2.3, 2.38)
ax1.set_xticks(np.arange(2.3, 2.39, 0.02))
ax1.set_ylim(0.75, 3.25)
ax1.set_yticks((1, 2, 3))
ax1.set_yticklabels(('COV = 10%', 'COV = 25%', 'COV = 50%'))

ax2.scatter(summary_mcs[sk[1]], locs, color='k', marker='o', s=10)
ax2.scatter(summary_pem[sk[1]], locs, color='k', marker='s', s=10)
ax2.hlines(y=locs, xmin=summary_mcs[sk[1]], xmax=summary_pem[sk[1]],
           color=diff_col[sk[1]], zorder=0, linewidth=2)

ax2.set_ylim(0.75, 3.25)
ax2.set_xlim(0, 0.36)
ax2.set_xticks(np.arange(0, 0.37, 0.09))
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4),
           ncol=2, frameon=False, fancybox=False)
ax2.legend([Line2D([0], [0], color='#F19EB1'),
            Line2D([0], [0], marker='o', color='k', lw=0),
            Line2D([0], [0], color='#8EBAE5'),
            Line2D([0], [0], marker='s', color='k', lw=0)],
           ['MCS > PEM','Monte Carlo simulations (MCS)',
            'MCS < PEM', 'Point estimate method (PEM)'],
           loc='upper center', bbox_to_anchor=(0.5, 1.7),
           ncol=2, frameon=False, fancybox=False)

ax3.scatter(summary_mcs[sk[2]], locs, color='k', marker='o', s=10)
ax3.scatter(summary_pem[sk[2]], locs, color='k', marker='s', s=10)
ax3.hlines(y=locs, xmin=summary_mcs[sk[2]], xmax=summary_pem[sk[2]],
           color=diff_col[sk[2]], zorder=0, linewidth=2)
ax3.set_xlim(-0.5, 0.5)
ax3.set_ylim(0.75, 3.25)
ax3.set_xticks(np.arange(-0.5, 0.51, 0.25))
ax20 = ax3.twinx()
ax20.set_ylabel('A', rotation=0, weight='bold', loc='top', labelpad=6)
ax20.set_yticks([])

ax4.scatter(summary_mcs[sk[3]], locs, color='k', marker='o', s=10)
ax4.scatter(summary_pem[sk[3]], locs, color='k', marker='s', s=10)
ax4.hlines(y=locs, xmin=summary_mcs[sk[3]], xmax=summary_pem[sk[3]],
           color=diff_col[sk[3]], zorder=0, linewidth=2)
ax4.set_xlim(1.12, 1.20)
ax4.set_xticks(np.arange(1.12, 1.21, 0.02))
ax4.set_ylim(0.75, 3.25)
ax4.set_yticks((1, 2, 3))
ax4.set_yticklabels(('COV = 10%', 'COV = 25%', 'COV = 50%'))

ax5.scatter(summary_mcs[sk[4]], locs, color='k', marker='o', s=10)
ax5.scatter(summary_pem[sk[4]], locs, color='k', marker='s', s=10)
ax5.hlines(y=locs, xmin=summary_mcs[sk[4]], xmax=summary_pem[sk[4]],
           color=diff_col[sk[4]], zorder=0, linewidth=2)
ax5.set_ylim(0.75, 3.25)
ax5.set_xlim(0, 0.2)
ax5.set_xticks(np.arange(0, 0.21, 0.05))

ax6.scatter(summary_mcs[sk[5]], locs, color='k', marker='o', s=10)
ax6.scatter(summary_pem[sk[5]], locs, color='k', marker='s', s=10)
ax6.hlines(y=locs, xmin=summary_mcs[sk[5]], xmax=summary_pem[sk[5]],
           color=diff_col[sk[5]], zorder=0, linewidth=2)
ax6.set_ylim(0.75, 3.25)
ax6.set_xlim(-0.4, 0.4)
ax6.set_xticks(np.arange(-0.4, 0.41, 0.2))
ax19 = ax6.twinx()
ax19.set_ylabel('B', rotation=0, weight='bold', loc='top', labelpad=6)
ax19.set_yticks([])

ax7.scatter(summary_mcs[sk[6]], locs, color='k', marker='o', s=10)
ax7.scatter(summary_pem[sk[6]], locs, color='k', marker='s', s=10)
ax7.hlines(y=locs, xmin=summary_mcs[sk[6]], xmax=summary_pem[sk[6]],
           color=diff_col[sk[6]], zorder=0, linewidth=2)
ax7.set_xlim(1.35, 1.39)
ax7.set_xticks(np.arange(1.35, 1.391, 0.01))
ax7.set_ylim(0.75, 3.25)
ax7.set_yticks((1, 2, 3))
ax7.set_yticklabels(('COV = 10%', 'COV = 25%', 'COV = 50%'))

ax8.scatter(summary_mcs[sk[7]], locs, color='k', marker='o', s=10)
ax8.scatter(summary_pem[sk[7]], locs, color='k', marker='s', s=10)
ax8.hlines(y=locs, xmin=summary_mcs[sk[7]], xmax=summary_pem[sk[7]],
           color=diff_col[sk[7]], zorder=0, linewidth=2)
ax8.set_ylim(0.75, 3.25)
ax8.set_xlim(0, 0.6)
ax8.set_xticks(np.arange(0, 0.61, 0.15))

ax9.scatter(summary_mcs[sk[8]], locs, color='k', marker='o', s=10)
ax9.scatter(summary_pem[sk[8]], locs, color='k', marker='s', s=10)
ax9.hlines(y=locs, xmin=summary_mcs[sk[8]], xmax=summary_pem[sk[8]],
           color=diff_col[sk[8]], zorder=0, linewidth=2)
ax9.set_ylim(0.75, 3.25)
ax9.set_xlim(-0.1, 0.1)
ax9.set_xticks(np.arange(-0.1, 0.11, 0.05))
ax18 = ax9.twinx()
ax18.set_ylabel('C', rotation=0, weight='bold', loc='top', labelpad=6)
ax18.set_yticks([])

ax10.scatter(summary_mcs[sk[9]], locs, color='k', marker='o', s=10)
ax10.scatter(summary_pem[sk[9]], locs, color='k', marker='s', s=10)
ax10.hlines(y=locs, xmin=summary_mcs[sk[9]], xmax=summary_pem[sk[9]],
            color=diff_col[sk[9]], zorder=0, linewidth=2)
ax10.set_yticks((1, 2, 3))
ax10.set_ylim(0.75, 3.25)
ax10.set_yticklabels(('COV = 10%', 'COV = 25%', 'COV = 50%'))
ax10.set_xlim(47, 51)
ax10.set_xticks(np.arange(47, 51.1, 1))

ax11.scatter(summary_mcs[sk[10]], locs, color='k', marker='o', s=10)
ax11.scatter(summary_pem[sk[10]], locs, color='k', marker='s', s=10)
ax11.hlines(y=locs, xmin=summary_mcs[sk[10]], xmax=summary_pem[sk[10]],
            color=diff_col[sk[10]], zorder=0, linewidth=2)
ax11.set_ylim(0.75, 3.25)
ax11.set_xlim(0, 80)
ax11.set_xticks(np.arange(0, 81, 20))

ax12.scatter(summary_mcs[sk[11]], locs, color='k', marker='o', s=10)
ax12.scatter(summary_pem[sk[11]], locs, color='k', marker='s', s=10)
ax12.hlines(y=locs, xmin=summary_mcs[sk[11]], xmax=summary_pem[sk[11]],
            color=diff_col[sk[11]], zorder=0, linewidth=2)
ax12.set_ylim(0.75, 3.25)
ax12.set_xlim(-0.8, 0.8)
ax12.set_xticks(np.arange(-0.8, 0.81, 0.4))
ax17 = ax12.twinx()
ax17.set_ylabel('D', rotation=0, weight='bold', loc='top', labelpad=6)
ax17.set_yticks([])

ax13.scatter(summary_mcs[sk[12]], locs, color='k', marker='o', s=10)
ax13.scatter(summary_pem[sk[12]], locs, color='k', marker='s', s=10)
ax13.hlines(y=locs, xmin=summary_mcs[sk[12]], xmax=summary_pem[sk[12]],
            color=diff_col[sk[12]], zorder=0, linewidth=2)
ax13.set_yticks((1, 2, 3))
ax13.set_yticklabels(('COV = 10%', 'COV = 25%', 'COV = 50%'))
ax13.set_ylim(0.75, 3.25)
ax13.set_xlim(10, 12)
ax13.set_xticks(np.arange(10, 12.1, 0.5))
ax13.set_xlabel('Mean')

ax14.scatter(summary_mcs[sk[13]], locs, color='k', marker='o', s=10)
ax14.scatter(summary_pem[sk[13]], locs, color='k', marker='s', s=10)
ax14.hlines(y=locs, xmin=summary_mcs[sk[13]], xmax=summary_pem[sk[13]],
            color=diff_col[sk[13]], zorder=0, linewidth=2)
ax14.set_ylim(0.75, 3.25)
ax14.set_xlim(0, 17)
ax14.set_xticks(np.arange(0, 17, 4))
ax14.set_xlabel('Variance')

ax15.scatter(summary_mcs[sk[14]], locs, color='k', marker='o', s=10)
ax15.scatter(summary_pem[sk[14]], locs, color='k', marker='s', s=10)
ax15.hlines(y=locs, xmin=summary_mcs[sk[14]], xmax=summary_pem[sk[14]],
            color=diff_col[sk[14]], zorder=0, linewidth=2)
ax15.set_ylim(0.75, 3.25)
ax15.set_xlim(-0.8, 0.8)
ax15.set_xticks(np.arange(-0.8, 0.81, 0.4))
ax15.set_xlabel('Skewness')
ax16 = ax15.twinx()
ax16.set_ylabel('E', rotation=0, weight='bold', loc='top', labelpad=6)
ax16.set_yticks([])

plt.rcParams['figure.figsize'] = [18/2.54,18/2.54]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.tight_layout()
plt.subplots_adjust(wspace=0.2, hspace=0.3)

plt.savefig('figures/PDF/fig3.pdf', format='pdf',
            bbox_inches='tight', facecolor='w')
plt.savefig('figures/EPS/fig3.eps', format='eps',
            bbox_inches='tight', facecolor='w')