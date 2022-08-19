import frontiers_yildizetal as fy
import matplotlib.pyplot as plt
import rasterio
import numpy as np
from pkg_resources import resource_filename

simple = fy.Simulations('simple')

path = 'files/raster/elev.tif'
dem_path = resource_filename('frontiers_yildizetal', path)
dem = rasterio.open(dem_path, 'r').read(1)

hmax = rasterio.open(simple.links['hmax'],'r').read(1)
hfin = rasterio.open(simple.links['hfin'],'r').read(1)

hmax_ma = np.ma.masked_where(hmax < 0.1, hmax, copy=True)
hfin_ma = np.ma.masked_where(hfin < 0.1, hfin, copy=True)

plt.subplot(121)

plt.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
plt.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyles='dotted')
plt.imshow(hmax_ma, cmap='viridis', extent=[0, 5000, 0, 4000],zorder=1, vmin=0.1, vmax=20)
plt.colorbar(location='top', orientation='horizontal', label='Maximum flow height [m]')
plt.xlabel('Easting [m]')
plt.ylabel('Northing [m]')
plt.xticks(np.arange(0, 5001, 1000))
plt.yticks(np.arange(0, 5001, 500))
plt.xlim(0,5000)
plt.ylim(1000,3000)
plt.text(0, 4100, 'A', weight='bold')
plt.text(3100, 1000,'Flat land at 0 m',ha='left',va='bottom')

plt.subplot(122)
plt.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
plt.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyle='dotted')
plt.imshow(hfin_ma, cmap='viridis', extent=[0, 5000, 0, 4000],zorder=1, vmin=0.1,vmax=4)
plt.colorbar(location='top', orientation='horizontal', label='Deposit height [m]')
plt.xlabel('Easting [m]')
plt.xticks(np.arange(0, 5001, 1000))
plt.yticks(np.arange(0, 5001, 500), labels=None)
plt.xlim(0,5000)
plt.ylim(1000,3000)
ax2=plt.gca()
ax2.axes.get_yaxis().set_ticklabels([])
plt.text(0, 4100, 'B', weight='bold')
plt.text(3100, 1000,'Flat land at 0 m',ha='left',va='bottom')

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = [18/2.54,8/2.54]
plt.tight_layout()
plt.subplots_adjust(wspace=0.1)

plt.savefig('figures/PDF/fig1.pdf', format='pdf', bbox_inches='tight', facecolor='w')