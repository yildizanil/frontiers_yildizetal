from frontiers_yildizetal.emulators import ScalarEmulators
from pkg_resources import resource_filename
import matplotlib.pyplot as plt
import numpy as np

acheron = ScalarEmulators('acheron', threshold=0.1, loc_x=1490100, loc_y=5204100)

path = 'files/input/input_mcs3_acheron.csv'
filepath = resource_filename('frontiers_yildizetal', path)
input_mcs3 = np.genfromtxt(filepath, delimiter=',', skip_header=1)

scalars = list(acheron.output.keys())

predicted = {}
for scalar in scalars:
    predicted[scalar] = acheron.predict_scalar(scalar, input_mcs3)[0]

(
    fig,
    (
        (ax1, ax2, ax3, ax4),
        (ax5, ax6, ax7, ax8),
        (ax9, ax10, ax11, ax12),
        (ax13, ax14, ax15, ax16),
        (ax17, ax18, ax19, ax20),
    ),
) = plt.subplots(
    5, 4, figsize=(18 / 2.54, 22 / 2.54), sharex='col', sharey='row', squeeze=True
)

ax1.hist2d(input_mcs3[:, 0], predicted['ia'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax1.set_ylim(1, 6)
ax1.set_yticks(np.arange(1, 6.1, 1))
ax1.set_ylabel('Impact area \n [x10$^6$ m$^2$]')

ax2.hist2d(input_mcs3[:, 1], predicted['ia'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax2.set_ylim(1, 6)

ax3.hist2d(input_mcs3[:, 2], predicted['ia'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax3.set_ylim(1, 6)

ax4.hist(
    predicted['ia'], bins=30, color='#FABE50', label='Impact area', orientation='horizontal'
)
ax4.text(1300, 6, 'A', weight='bold', ha='left', va='top', fontsize=10)

ax5.hist2d(input_mcs3[:, 0], predicted['da'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax5.set_ylim(0, 3)
ax5.set_yticks(np.arange(0, 3.1, 0.6))
ax5.set_ylabel('Deposit area \n [x10$^6$ m$^2$]')

ax6.hist2d(input_mcs3[:, 1], predicted['da'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax6.set_ylim(0, 3)

ax7.hist2d(input_mcs3[:, 2], predicted['da'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax7.set_ylim(0, 3)

ax8.hist(
    predicted['da'], bins=30, color='#FABE50', label='Deposit area', orientation='horizontal'
)
ax8.set_xlim(0, 1200)
ax8.tick_params(labelbottom=False)
ax8.text(1300, 3, 'B', weight='bold', ha='left', va='top', fontsize=10)

ax9.hist2d(input_mcs3[:, 0], predicted['dv'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax9.set_ylim(2.5, 10)
ax9.set_yticks(np.arange(2.5, 10.1, 1.5))
ax9.set_ylabel('Deposit volume \n [x10$^6$ m$^3$]')

ax10.hist2d(input_mcs3[:, 1], predicted['dv'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax10.set_ylim(2.5, 10)

ax11.hist2d(input_mcs3[:, 2], predicted['dv'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax11.set_ylim(2.5, 10)

ax12.hist(
    predicted['dv'], bins=30, color='#FABE50', label='Deposit area', orientation='horizontal'
)
ax12.set_xlim(0, 1200)
ax12.set_xticks(np.arange(0, 1201, 400))
ax12.tick_params(labelbottom=False)
ax12.text(1300, 10, 'C', weight='bold', ha='left', va='top', fontsize=10)

ax13.hist2d(input_mcs3[:, 0], predicted['vmax'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax13.set_ylim(15, 45)
ax13.set_yticks(np.arange(15, 46, 6))
ax13.set_ylabel('Max. flow velocity \n [m/s]')

ax14.hist2d(input_mcs3[:, 1], predicted['vmax'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax14.set_ylim(15, 45)

ax15.hist2d(input_mcs3[:, 2], predicted['vmax'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax15.set_ylim(15, 45)

ax16.hist(
    predicted['vmax'], bins=30, color='#FABE50', label='Deposit area', orientation='horizontal'
)
ax16.set_xlim(0, 1200)
ax16.set_xticks(np.arange(0, 1201, 400))
ax16.tick_params(labelbottom=False)
ax16.text(1300, 45, 'D', weight='bold', ha='left', va='top', fontsize=10)

ax17.hist2d(input_mcs3[:, 0], predicted['hmax'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax17.set_ylim(25, 60)
ax17.set_yticks(np.arange(25, 61, 7))
ax17.set_xlim(0.02, 0.3)
ax17.set_ylabel('Max. flow height \n [m]')
ax17.set_xlabel('Coulomb fric. coef. \n [-]')

ax18.hist2d(input_mcs3[:, 1], predicted['hmax'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax18.set_ylim(25, 60)
ax18.set_xlim(100, 2200)
ax18.set_xlabel('Turbulent fric. coef. \n [m/s$^2$]')

ax19.hist2d(input_mcs3[:, 2], predicted['hmax'], cmap='viridis', cmin=1, cmax=3000, bins=30)
ax19.set_ylim(25, 60)
ax19.set_xlim(6.4 / 2, 6.4 * 1.5)
ax19.set_xlabel('Release volume \n [x10$^6$ m$^3$]')

ax20.hist(
    predicted['hmax'], bins=30, color='#FABE50', label='Deposit area', orientation='horizontal'
)
ax20.set_xlabel('Counts [-]')
ax20.set_xlim(0, 1200)
ax20.set_xticks(np.arange(0, 1201, 400))
ax20.tick_params(labelbottom=True)
ax20.text(1300, 60, 'E', weight='bold', ha='left', va='top', fontsize=10)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.tight_layout()

plt.subplots_adjust(hspace=0.1, wspace=0.1)

plt.savefig('figures/PDF/fig6.pdf', format='pdf', facecolor='white', bbox_inches='tight')
plt.savefig('figures/EPS/fig6.eps', format='eps', facecolor='white', bbox_inches='tight')
