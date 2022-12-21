import frontiers_yildizetal as fy
import matplotlib.pyplot as plt
import rasterio
import numpy as np
from pkg_resources import resource_filename
import matplotlib as mpl

synth = fy.Simulations('synth')

path = 'files/raster/elev.tif'
dem_path = resource_filename('frontiers_yildizetal', path)

with rasterio.open(dem_path, 'r') as src:
    dem = src.read(1)
with rasterio.open(synth.links['hmax'], 'r') as src:
    hmax = src.read(1)
    hmax_ma = np.ma.masked_where(hmax < 0.1, hmax, copy=True)
with rasterio.open(synth.links['hfin'], 'r') as src:
    hfin = src.read(1)
    hfin_ma = np.ma.masked_where(hfin < 0.1, hfin, copy=True)

cmap = mpl.cm.Greys
norm = mpl.colors.Normalize(vmin=0, vmax=1400)

fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2)

c_topo = ax1.contourf(
    dem, extent=[0, 5000, 0, 4000], cmap='Greys', zorder=0, vmin=0, vmax=1400
)
ax1.vlines(x=3000, ymin=0, ymax=4000, zorder=0, color='k', linestyles='dotted')
c1 = ax1.imshow(
    hmax_ma, cmap='viridis', extent=[0, 5000, 0, 4000], zorder=1, vmin=0.1, vmax=20
)
fig.colorbar(
    c1, ax=ax1, location='top', orientation='horizontal', label='Maximum flow height [m]'
)

fig.subplots_adjust(bottom=0.5)
cbar_ax = fig.add_axes([0.05, 0, 0.90, 0.05])
fig.colorbar(
    c_topo,
    cax=cbar_ax,
    cmap=cmap,
    norm=norm,
    orientation='horizontal',
    label='Elevation [m]',
    shrink=0.36,
)

ax1.set_xlabel('Easting [m]')
ax1.set_ylabel('Northing [m]')
ax1.set_xticks(np.arange(0, 5001, 1000))
ax1.set_yticks(np.arange(0, 5001, 500))
ax1.set_xlim(0, 5000)
ax1.set_ylim(1000, 3000)
ax1.text(0, 3900, 'A', weight='bold')
ax1.text(3100, 1000, 'Flat land at 0 m', ha='left', va='bottom')

ax2.contourf(dem, extent=[0, 5000, 0, 4000], cmap='Greys', zorder=0, vmin=0, vmax=1400)
ax2.vlines(x=3000, ymin=0, ymax=4000, zorder=0, color='k', linestyle='dotted')
c2 = ax2.imshow(hfin_ma, cmap='viridis', extent=[0, 5000, 0, 4000], zorder=1, vmin=0.1, vmax=4)
fig.colorbar(c2, ax=ax2, location='top', orientation='horizontal', label='Deposit height [m]')

ax2.set_xlabel('Easting [m]')
ax2.set_xticks(np.arange(0, 5001, 1000))
ax2.set_yticks(np.arange(0, 5001, 500), labels=None)
ax2.set_xlim(0, 5000)
ax2.set_ylim(1000, 3000)
ax2.axes.get_yaxis().set_ticklabels([])
ax2.text(0, 3900, 'B', weight='bold')
ax2.text(3100, 1000, 'Flat land at 0 m', ha='left', va='bottom')

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = [18 / 2.54, 7 / 2.54]
plt.tight_layout()
plt.subplots_adjust(wspace=0.1)

fig.set_rasterized(True)
ax1.set_rasterized(True)
ax2.set_rasterized(True)

plt.savefig('figures/PDF/fig1.pdf', format='pdf', bbox_inches='tight', facecolor='w')
plt.savefig('figures/EPS/fig1.eps', format='eps', bbox_inches='tight', facecolor='w')
