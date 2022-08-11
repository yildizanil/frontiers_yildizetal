from logging import raiseExceptions
import pandas as pd
import numpy as np
import rasterio
import yaml
from yaml.loader import SafeLoader

class Simulations:
    def __init__(self, name:str):
        self.name = name
        with open(r'docs/download_links.yml') as f:
            download_links = yaml.load(f, Loader=SafeLoader)
        self.links = download_links[self.name]

    def calc_ia(self, threshold:float):
        with rasterio.open(self.links['hmax']) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            
            ia = []
            print('Calculating IA...')
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, 1, 0)
                ia_band = np.sum(valid_cells) * self.res**2 / 1000000
                ia.append(ia_band)
            print('IA calculated.')
        return ia
    
    def calc_da(self, threshold:float):
        with rasterio.open(self.links['hfin']) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            
            da = []
            print('Calculating DA...')
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, 1, 0)
                da_band = np.sum(valid_cells) * self.res**2 / 1000000
                da.append(da_band)
            print('DA calculated.')
        return da
    
    def calc_dv(self, threshold:float):
        with rasterio.open(self.links['hfin']) as src:
            self.sim_size = src.count
            self.res= src.res[0]
        
            dv = []
            print('Calculating DV...')
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, self.res**2, 0)
                volume = np.multiply(src.read(band), valid_cells)
                dv_band = np.sum(volume) / 1000000
                dv_band = round(dv_band, 3)
                dv.append(dv_band)
            print('DV calculated.')
        return dv
    
    def extract_qoi_at(self, qoi, loc_x, loc_y):
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raiseExceptions('Invalid QoI. It should be hmax, vmax, or pmax.')
            
        with rasterio.open(self.links[qoi]) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            self.bounds = src.bounds
            self.row = src.index(loc_x,loc_y)[0]
            self.col = src.index(loc_x,loc_y)[1]
            
            extracted_qoi = []
            print('Extracting QoI: ' + qoi + '... ')
            for band in range(1, self.sim_size+1, 1):
                val_qoi = src.read(band)[self.row, self.col]
                extracted_qoi.append(val_qoi)
            print('QoI: ' + qoi + ' extracted.')
        return extracted_qoi
    
    def curate_scalars(self, threshold:float, loc_x:float, loc_y:float):
        ia = self.calc_ia(threshold)
        da = self.calc_da(threshold)
        dv = self.calc_dv(threshold)
        vmax = self.extract_qoi_at(qoi='vmax', loc_x=loc_x, loc_y=loc_y)
        hmax = self.extract_qoi_at(qoi='hmax', loc_x=loc_x, loc_y=loc_y)
        
        scalars = pd.DataFrame({'ia':ia, 'da':da, 'dv':dv, 'vmax':vmax, 'hmax':hmax})
        return scalars