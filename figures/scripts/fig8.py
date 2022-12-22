import frontiers_yildizetal as fy
from frontiers_yildizetal.emulators.rgasp import VectorEmulators
from pkg_resources import resource_filename
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import rasterio
from rasterio.plot import plotting_extent

path = 'files/raster/hillshade_acheron.tif'
hill_path = resource_filename('frontiers_yildizetal', path)
with rasterio.open(hill_path, 'r') as hill:
    hill_arr = hill.read(1)
hill_ma = np.ma.masked_where(hill_arr < -30000, hill_arr, copy=True)

ac = VectorEmulators('acheron', qoi='hmax', threshold=0.1)

path = 'files/input/input_mcs3_acheron.csv'
filepath = resource_filename('frontiers_yildizetal', path)
input_mcs3 = np.genfromtxt(filepath, delimiter=',', skip_header=1)

mcs3_mean, mcs3_sd = ac.predict_vector(input_mcs3)
mcs3_mean_ma = np.ma.masked_where(mcs3_mean < 0.1, mcs3_mean, copy=True)
mcs3_sd_ma = np.ma.masked_where(mcs3_mean < 0.1, mcs3_sd, copy=True)

ac_pem = fy.Simulations('acheron_pem').create_vector(
    qoi='hmax', threshold=0.1, valid_cols=ac.valid_cols
)

pem3_mean = np.zeros((1, ac.rows * ac.cols))
pem3_mean[:, list(ac.vector.columns)] = ac_pem[0][16:24].mean(axis=0)
pem3_mean = pem3_mean.reshape(ac.rows, ac.cols)
pem3_mean_ma = np.ma.masked_where(pem3_mean < 0.1, pem3_mean, copy=True)

pem3_sd = np.zeros((1, ac.rows * ac.cols))
pem3_sd[:, list(ac.vector.columns)] = ac_pem[0][16:24].std(axis=0)
pem3_sd = pem3_sd.reshape(ac.rows, ac.cols)
pem3_sd_ma = np.ma.masked_where(pem3_mean < 0.1, pem3_sd, copy=True)

diff_mean = pem3_mean - mcs3_mean
diff_sd = pem3_sd - mcs3_sd

diff_mean_ma = np.ma.masked_where(diff_mean == 0, diff_mean, copy=True)
diff_sd_ma = np.ma.masked_where(diff_sd == 0, diff_sd, copy=True)

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(
    nrows=2, ncols=3, gridspec_kw={'width_ratios': [1, 1, 1], 'height_ratios': [1, 1]}
)

ax1.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c1 = ax1.imshow(
    pem3_mean_ma, cmap='viridis', extent=plotting_extent(hill), zorder=1, vmin=0.1, vmax=80
)
fig.colorbar(
    c1, ax=ax1, location='top', orientation='horizontal', label='Mean flow height [m]'
)
ax1.set_ylabel('Northing [x 10$^6$ m]')
ax1.set_xticks(ticks=np.arange(1489000, 1493600, 1000), labels=None)
ax1.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax1.text(1488500, 5207000, 'A', weight='bold')
ax1.axes.get_xaxis().set_ticklabels([])

ax2.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c2 = ax2.imshow(mcs3_mean_ma, cmap='viridis', extent=plotting_extent(hill), vmin=0.1, vmax=80)
fig.colorbar(
    c2, ax=ax2, location='top', orientation='horizontal', label='Mean flow height [m]'
)
ax2.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax2.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax2.text(1488500, 5207000, 'B', weight='bold')
ax2.axes.get_yaxis().set_ticklabels([])
ax2.axes.get_xaxis().set_ticklabels([])

ax3.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c3 = ax3.imshow(diff_mean_ma, cmap='RdBu', extent=plotting_extent(hill), vmin=-4, vmax=4)
fig.colorbar(
    c3,
    ax=ax3,
    location='top',
    orientation='horizontal',
    label='Difference in mean flow height [m]',
)
ax3.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax3.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax3.text(1488500, 5207000, 'C', weight='bold')
ax3.axes.get_yaxis().set_ticklabels([])
ax3.axes.get_xaxis().set_ticklabels([])

ax4.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c4 = ax4.imshow(
    pem3_sd_ma, cmap='viridis', extent=plotting_extent(hill), zorder=1, vmin=0.1, vmax=40
)
fig.colorbar(
    c4,
    ax=ax4,
    location='top',
    orientation='horizontal',
    label='Std. deviation flow height [m]',
)
ax4.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax4.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax4.text(1488500, 5207000, 'D', weight='bold')
ax4.set_xlabel('Easting [x 10$^6$ m]')
ax4.set_ylabel('Northing [x 10$^6$ m]')

ax5.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c5 = ax5.imshow(mcs3_sd_ma, cmap='viridis', extent=plotting_extent(hill), vmin=0.1, vmax=40)
fig.colorbar(
    c5,
    ax=ax5,
    location='top',
    orientation='horizontal',
    label='Std. deviation flow height [m]',
)
ax5.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax5.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax5.text(1488500, 5207000, 'E', weight='bold')
ax5.axes.get_yaxis().set_ticklabels([])
ax5.set_xlabel('Easting [x 10$^6$ m]')

ax6.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c6 = ax6.imshow(diff_sd_ma, cmap='RdBu', extent=plotting_extent(hill), vmin=-20, vmax=20)
fig.colorbar(
    c6,
    ax=ax6,
    location='top',
    orientation='horizontal',
    label='Difference in std. deviation [m]',
)
ax6.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax6.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax6.text(1488500, 5207000, 'F', weight='bold')
ax6.axes.get_yaxis().set_ticklabels([])
ax6.set_xlabel('Easting [x 10$^6$ m]')

plt.rcParams['figure.figsize'] = [18 / 2.54, 18 / 2.54]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.tight_layout()

plt.subplots_adjust(hspace=0, wspace=0.1)

plt.savefig('figures/EPS/fig8.eps', format='eps', bbox_inches='tight', facecolor='w')
plt.savefig('figures/PDF/fig8.pdf', format='pdf', bbox_inches='tight', facecolor='w')
