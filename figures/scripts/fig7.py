import frontiers_yildizetal as fy
from frontiers_yildizetal.emulators import *
from pkg_resources import resource_filename
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import rasterio

path = 'files/raster/elev.tif'
dem_path = resource_filename('frontiers_yildizetal', path)
dem = rasterio.open(dem_path, 'r').read(1)

simple = VectorEmulators('simple',qoi='hmax',threshold=0.1)

path = 'files/input/input_mcs3_simple.csv'
filepath = resource_filename('frontiers_yildizetal', path)
input_mcs3 = pd.read_csv(filepath)

mcs3_mean, mcs3_sd = simple.predict_vector(input_mcs3)
mcs3_mean_ma = np.ma.masked_where(mcs3_mean < 0.1, mcs3_mean, copy=True)
mcs3_sd_ma = np.ma.masked_where(mcs3_mean < 0.1, mcs3_sd, copy=True)

simple_pem = fy.Simulations('simple_pem').create_vector(qoi='hmax',threshold=0.1,valid_cols=simple.valid_cols)

pem3_mean = np.zeros((1,simple.rows * simple.cols))
pem3_mean[:,list(simple.vector.columns)] = simple_pem[0][16:24].mean(axis=0)
pem3_mean = pem3_mean.reshape(simple.rows,simple.cols)
pem3_mean_ma = np.ma.masked_where(pem3_mean < 0.1, pem3_mean, copy=True)

pem3_sd = np.zeros((1,simple.rows * simple.cols))
pem3_sd[:,list(simple.vector.columns)] = simple_pem[0][16:24].std(axis=0)
pem3_sd = pem3_sd.reshape(simple.rows,simple.cols)
pem3_sd_ma = np.ma.masked_where(pem3_mean < 0.1, pem3_sd, copy=True)

diff_mean = (pem3_mean - mcs3_mean)
diff_sd = (pem3_sd - mcs3_sd)

diff_mean_ma = np.ma.masked_where(diff_mean == 0, diff_mean, copy=True)
diff_sd_ma = np.ma.masked_where(diff_sd == 0, diff_sd, copy=True)


fig, ((ax1,ax2, ax3), (ax4,ax5,ax6)) = plt.subplots(nrows=2, ncols=3,
                                gridspec_kw={'width_ratios': [1, 1, 1],'height_ratios':[1,1]})

ax1.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
ax1.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyles='dotted')
c1 = ax1.imshow(pem3_mean_ma, cmap='viridis', extent=[0, 5000, 0, 4000],zorder=1,vmin=0,vmax=22)
fig.colorbar(c1,ax=ax1,location='top', orientation='horizontal', label='Mean flow height [m]',ticks=np.arange(0,21,5))
ax1.set_ylabel('Northing [m]')
ax1.set_xticks(np.arange(0, 5001, 1000))
ax1.set_yticks(np.arange(0, 5001, 1000))
ax1.set_xlim(0,5000)
ax1.set_ylim(1000,3000)
ax1.text(-500, 4300, 'A', weight='bold')

ax2.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
ax2.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyle='dotted')
c2 = ax2.imshow(mcs3_mean_ma, cmap='viridis', extent=[0, 5000, 0, 4000],vmin=0,vmax=22)
fig.colorbar(c2, ax=ax2, location='top', orientation='horizontal', label='Mean flow height [m]',ticks=np.arange(0,21,5))
ax2.set_xticks(np.arange(0, 5001, 1000))
ax2.set_yticks(np.arange(0, 5001, 1000), labels=None)
ax2.set_xlim(0,5000)
ax2.set_ylim(1000,3000)
ax2.text(-500, 4300, 'B', weight='bold')
ax2.axes.get_yaxis().set_ticklabels([])

ax3.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
ax3.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyle='dotted')
c3 = ax3.imshow(diff_mean_ma, cmap='RdBu', extent=[0, 5000, 0, 4000],vmin=-1,vmax=1)
fig.colorbar(c3, ax=ax3, location='top', orientation='horizontal', label='Difference in mean flow height [m]')
ax3.set_xticks(np.arange(0, 5001, 1000))
ax3.set_yticks(np.arange(0, 5001, 1000), labels=None)
ax3.set_xlim(0,5000)
ax3.set_ylim(1000,3000)
ax3.axes.get_yaxis().set_ticklabels([])
ax3.text(-500, 4300, 'C', weight='bold')

ax4.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
ax4.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyles='dotted')
c4 = ax4.imshow(pem3_sd_ma, cmap='viridis', extent=[0, 5000, 0, 4000],zorder=1,vmin=0,vmax=12)
fig.colorbar(c4, ax=ax4, location='top', orientation='horizontal', label='Std. deviation flow height [m]',ticks=np.arange(0,13,3))
ax4.set_xlabel('Easting [m]')
ax4.set_ylabel('Northing [m]')
ax4.set_xticks(np.arange(0, 5001, 1000))
ax4.set_yticks(np.arange(0, 5001, 1000))
ax4.set_xlim(0,5000)
ax4.set_ylim(1000,3000)
ax4.text(-500, 4300, 'D', weight='bold')

ax5.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
ax5.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyle='dotted')
c5 = ax5.imshow(mcs3_sd_ma, cmap='viridis', extent=[0, 5000, 0, 4000],vmin=0,vmax=12)
fig.colorbar(c5, ax=ax5, location='top', orientation='horizontal', label='Std. deviation flow height [m]',ticks=np.arange(0,13,3))
ax5.set_xlabel('Easting [m]')
ax5.set_xticks(np.arange(0, 5001, 1000))
ax5.set_yticks(np.arange(0, 5001, 1000), labels=None)
ax5.set_xlim(0,5000)
ax5.set_ylim(1000,3000)
ax5.axes.get_yaxis().set_ticklabels([])
ax5.text(-500, 4300, 'E', weight='bold')

ax6.contourf(dem, extent=[0, 5000, 0, 4000],cmap='Greys',zorder=0)
ax6.vlines(x=3000,ymin=0,ymax=4000,zorder=0,color='k',linestyle='dotted')
c6 = ax6.imshow(diff_sd_ma, cmap='RdBu', extent=[0, 5000, 0, 4000],vmin=-5,vmax=5)
fig.colorbar(c6, ax=ax6, location='top', orientation='horizontal', label='Difference in std. deviation [m]')
ax6.set_xlabel('Easting [m]')
ax6.set_xticks(np.arange(0, 5001, 1000))
ax6.set_yticks(np.arange(0, 5001, 1000), labels=None)
ax6.set_xlim(0,5000)
ax6.set_ylim(1000,3000)
ax6.axes.get_yaxis().set_ticklabels([])
ax6.text(-500, 4300, 'F', weight='bold')

plt.rcParams['figure.figsize'] = [18/2.54,12/2.54]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.tight_layout()

plt.subplots_adjust(hspace=0, wspace=0.1)

plt.savefig('figures/EPS/fig7.eps', format='eps', bbox_inches='tight', facecolor='w')
plt.savefig('figures/PDF/fig7.pdf', format='pdf', bbox_inches='tight', facecolor='w')
