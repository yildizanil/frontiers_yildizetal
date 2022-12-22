from frontiers_yildizetal.ravaflow import Simulations
import matplotlib.pyplot as plt
import rasterio
import numpy as np
from pkg_resources import resource_filename
import matplotlib as mpl
from rasterio.plot import plotting_extent

ac = Simulations('acheron')

path = 'files/raster/hillshade_acheron.tif'
hill_path = resource_filename('frontiers_yildizetal', path)

with rasterio.open(hill_path, 'r') as hill:
    hill_arr = hill.read(1)
    hill_ma = np.ma.masked_where(hill_arr < -30000, hill_arr, copy=True)
with rasterio.open(ac.links['hmax'], 'r') as src:
    hmax = src.read(1)
    hmax_ma = np.ma.masked_where(hmax < 0.1, hmax, copy=True)
with rasterio.open(ac.links['hfin'], 'r') as src2:
    hfin = src2.read(1)
    hfin_ma = np.ma.masked_where(hfin < 0.1, hfin, copy=True)

fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [1, 1]})

ax1.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c1 = ax1.imshow(hmax_ma, cmap='viridis', extent=plotting_extent(hill), zorder=1)
fig.colorbar(
    c1,
    ax=ax1,
    location='top',
    orientation='horizontal',
    label='Maximum flow height [m]',
    shrink=1,
)

ax1.set_xlabel('Easting [x 10$^6$ m]')
ax1.set_ylabel('Northing [x 10$^6$ m]')
ax1.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax1.set_yticks(
    ticks=np.arange(5201000, 5205001, 1000), labels=[5.201, 5.202, 5.203, 5.204, 5.205]
)
ax1.text(1488500, 5207000, 'A', weight='bold')

ax2.imshow(hill_ma, cmap='Greys', extent=plotting_extent(hill))
c2 = ax2.imshow(hfin_ma, cmap='viridis', extent=plotting_extent(hill), zorder=1)
fig.colorbar(
    c2, ax=ax2, location='top', orientation='horizontal', label='Deposit height [m]', shrink=1
)

ax2.set_xlabel('Easting [x 10$^6$ m]')
ax2.set_xticks(
    ticks=np.arange(1489000, 1493600, 1000), labels=[1.498, '1.490', 1.491, 1.492, 1.493]
)
ax2.axes.get_yaxis().set_ticklabels([])
ax2.text(1488500, 5207000, 'B', weight='bold')

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = [12 / 2.54, 9 / 2.54]
plt.tight_layout()
plt.subplots_adjust(wspace=0.1, hspace=0.1)

plt.savefig('figures/PDF/fig2.pdf', format='pdf', bbox_inches='tight', facecolor='w')
plt.savefig('figures/EPS/fig2.eps', format='eps', bbox_inches='tight', facecolor='w')
