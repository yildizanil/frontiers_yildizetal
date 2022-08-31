from logging import raiseExceptions
import pandas as pd
import numpy as np
import rasterio
import yaml
from yaml.loader import SafeLoader
import pkg_resources

class Simulations:
    """
    A class to represent r.avaflow simulations
    
    Attributes
    ----------
    name:str
        name of the simulation set
    links:dict
        dictionary of download links
    
    Methods
    -------
    calc_ia(threshold):
        Calculates the impact area of a collection of simulations
    calc_da(threshold):
        Calculates the deposit area of a collection of simulations
    calc_dv(threshold):
        Calculates the deposit volume of a collection of simulations    
    extract_qoi_at(qoi, loc_x, loc_y):
        Extracts an quantitiy of interest from a given coordinate
    curate_scalars(threshold, loc_x, loc_y):
        Curates a dataframe consisting of calculated or extracted scalars from simulations
    create_vector(qoi, threshold, valid_cols=None):
        Creates a dataframe of simulation outputs to be used in vector emulators
    """
    def __init__(self, name:str):
        self.name = name
        path = 'files/download_links.yml'
        filepath = pkg_resources.resource_filename(__name__, path)
        with open(filepath) as f:
            self.download_links = yaml.load(f, Loader=SafeLoader)
        self.links = self.download_links[self.name]

    def calc_ia(self, threshold:float):
        """ Calculates the impact area of a collection of simulations

        Args:
            threshold (float): Threshold value to define the impact area of the simulation

        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative
        
        Returns:
            ia (list): a list of impact area values from simulations
        """
        
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        
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
        """ Calculates the deposit area of a collection of simulations

        Args:
            threshold (float): Threshold value to define the deposit area of the simulation

        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative
        
        Returns:
            da (list): a list of deposit area values from simulations
        """
        
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        
        with rasterio.open(self.links['hfin']) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            
            da = []
            print('Calculating DA...')
            for band in range(1, self.sim_size+1, 1):
                valid_cells = np.where(src.read(band) >= threshold, 1, 0)
                da_band = np.sum(valid_cells) * self.res**2 / 1000000
                da.append(da_band)
            print('DA calculated.', flush=True)
        return da
    
    def calc_dv(self, threshold:float):
        """ Calculates the deposit volume of a collection of simulations

        Args:
            threshold (float): Threshold value to define the deposit volume of the simulation
            
        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative

        Returns:
            dv (list): a list of deposit volume values from simulations
        """
        
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        
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
            print('DV calculated.', flush=True)
        return dv
    
    def extract_qoi_at(self, qoi, loc_x, loc_y):
        """ Extract a quantity of interest from a location

        Args:
            qoi (str): quantity of interest, i.e. hmax for maximum flow height,
            vmax for maximum flow height, and pmax for maximum flow pressure
            loc_x (int, float): x coordinate of the point of extract
            loc_y (int, float): y coordinate of the point of extract
            
        Raises:
            TypeError: qoi must be a string
            Exception: Invalid QoI. It should be hmax, vmax, or pmax.
            TypeError: x-coordinate (loc_x) must be an integer or a float
            TypeError: y-coordinate (loc_y) must be an integer or a float
            Exception: x-coordinate is out of bounds
            Exception: y-coordinate is out of bounds

        Returns:
            extracted_qoi (list): a list of extracted quantity of interest from each simulation
        """
        
        if not isinstance(qoi, (str)):
            raise TypeError("qoi must be a string")
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raise Exception('Invalid QoI. It should be hmax, vmax, or pmax.')
        if not isinstance(loc_x, (int, float)):
            raise TypeError("x-coordinate (loc_x) must be an integer or a float")
        if not isinstance(loc_y, (int, float)):
            raise TypeError("y-coordinate (loc_y) must be an integer or a float")
        
        with rasterio.open(self.links[qoi]) as src:
            self.sim_size = src.count
            self.res= src.res[0]
            self.bounds = src.bounds
            self.row = src.index(loc_x,loc_y)[0]
            self.col = src.index(loc_x,loc_y)[1]
            
            if loc_x <= self.bounds[0] or loc_x >= self.bounds[2]:
               raise Exception('x-coordinate is out of bounds')
            if loc_y <= self.bounds[1] or loc_y >= self.bounds[3]:
                raise Exception('y-coordinate is out of bounds')
                    
            extracted_qoi = []
            print('Extracting QoI: ' + qoi + '... ')
            for band in range(1, self.sim_size+1, 1):
                val_qoi = src.read(band)[self.row, self.col]
                extracted_qoi.append(val_qoi)
            print('QoI: ' + qoi + ' extracted.', flush=True)
        return extracted_qoi
    
    def curate_scalars(self, threshold:float, loc_x:float, loc_y:float):
        """_summary_

        Args:
            threshold (float): Threshold value to define the scalars from simulations
            loc_x (int, float): x coordinate of the point of extract
            loc_y (int, float): y coordinate of the point of extract

        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative
            TypeError: x-coordinate (loc_x) must be an integer or a float
            TypeError: y-coordinate (loc_y) must be an integer or a float
            Exception: x-coordinate is out of bounds
            Exception: y-coordinate is out of bounds

        Returns:
            scalars(pandas DataFrame): a data frame of curated scalars
        """
        
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        if not isinstance(loc_x, (int, float)):
            raise TypeError("x-coordinate (loc_x) must be an integer or a float")
        if not isinstance(loc_y, (int, float)):
            raise TypeError("y-coordinate (loc_y) must be an integer or a float")
        if loc_x <= self.bounds[0] or loc_x >= self.bounds[2]:
               raise Exception('x-coordinate is out of bounds')
        if loc_y <= self.bounds[1] or loc_y >= self.bounds[3]:
                raise Exception('y-coordinate is out of bounds')
        
        ia = self.calc_ia(threshold)
        da = self.calc_da(threshold)
        dv = self.calc_dv(threshold)
        
        vmax = self.extract_qoi_at(qoi='vmax', loc_x=loc_x, loc_y=loc_y)
        hmax = self.extract_qoi_at(qoi='hmax', loc_x=loc_x, loc_y=loc_y)
        
        scalars = pd.DataFrame({'ia':ia, 'da':da, 'dv':dv, 'vmax':vmax, 'hmax':hmax})
        return scalars
    
    def create_vector(self, qoi, threshold, valid_cols=None):
        """ Creates am output to train vector emulators

        Args:
            qoi (_type_): quantity of interest, i.e. hmax for maximum flow height,
            vmax for maximum flow height, and pmax for maximum flow pressure
            threshold (_type_): Threshold value to define valid cells from simulations
            valid_cols (list, optional): column numbers to extract. Defaults to None.

        Raises:
            Exception: Invalid QoI. It should be hmax, vmax, or pmax.
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative

        Returns:
            training (pandas DataFrame): A data frame consisting of the vector outputs from simulations
            valid_cols (numpy Array): An array consisting of the valid column names
        """
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raise Exception('Invalid QoI. It should be hmax, vmax, or pmax.')
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        
        with rasterio.open(self.links[qoi]) as src:
            self.sim_size = src.count
            self.rows = src.height
            self.cols = src.width
        
            unstacked = np.zeros((self.sim_size, self.rows * self.cols))
        
            for sim in range(1, self.sim_size+1, 1):
                index = sim - 1
                unstacked[index,:] = src.read(sim).reshape(1, self.rows * self.cols)
            
        if valid_cols is None:
            valid_cols = np.where(unstacked >= threshold, 1, 0).sum(axis=0)
        indices = np.flatnonzero(valid_cols)
        training = pd.DataFrame(unstacked[:,indices], columns=indices)
        return training, valid_cols
