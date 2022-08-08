import pandas as pd
import numpy as np
import rasterio

class Simulations:
    def __init__(self, name:str):
        self.name = name

    def calc_ia(self, threshold:float):
        
        hmax_link = 'https://figshare.com/ndownloader/files/36593274?private_link=94c4ff3a1abab53adb79'
        with rasterio.open(hmax_link) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            
            ia = []
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, 1, 0)
                ia_band = np.sum(valid_cells) * self.res**2 / 1000000
                ia.append(ia_band)
        return ia
    
    def calc_da(self, threshold:float):
        
        hfin_link = 'https://figshare.com/ndownloader/files/36593289?private_link=b438683c9280d1c91dcb'
        with rasterio.open(hfin_link) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            
            da = []
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, 1, 0)
                da_band = np.sum(valid_cells) * self.res**2 / 1000000
                da.append(da_band)
        return da
    
    def calc_dv(self, threshold:float):
        
        hfin_link = 'https://figshare.com/ndownloader/files/36593289?private_link=b438683c9280d1c91dcb'
        with rasterio.open(hfin_link) as src:
            self.sim_size = src.count
            self.res= src.res[0]
        
            dv = []
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, self.res**2, 0)
                volume = np.multiply(src.read(band), valid_cells)
                dv_band = np.sum(volume) / 1000000
                dv_band = round(dv_band, 3)
                dv.append(dv_band)
        return dv