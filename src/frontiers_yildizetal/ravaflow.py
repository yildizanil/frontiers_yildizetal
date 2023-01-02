import numpy as np
import rasterio
from frontiers_yildizetal.utilities import data

class Simulations:
    """
    A class to represent r.avaflow simulations
    
    Attributes
    ----------
    name:str
        Name of the simulation set. Can be one of the following: synth, synth_pem, synth_validate, acheron, acheron_pem, acheron_validate
    links:dict
        Dictionary of download links
    
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

    def __init__(self, name: str):
        """
        Initialising Simulations class

        Args:
            name (str): Name of the simulation set. Can be one of the following: synth, synth_pem, synth_validate, acheron, acheron_pem, acheron_validate

        Attributes:
            data_import: Method to import Figshare data
            size (int): Number of simulations
            res (float): Resolution at which the simulations were conducted
            bounds: Bounds of the region in which the simulations were conducted
            
        Raises:
            TypeError: name must be a string
            Exception: Invalid set of simulations. It must be synth, synth_pem, synth_validate, acheron, acheron_pem or acheron_validate
        """
        if not isinstance(name, str):
            raise TypeError('name must be a string')
        if name not in [
            'synth',
            'synth_pem',
            'synth_validate',
            'acheron',
            'acheron_pem',
            'acheron_validate',
        ]:
            raise Exception(
                'Invalid set of simulations. It must be synth, synth_pem, synth_validate, acheron, acheron_pem or acheron_validate'
            )
        self.name = name
        self.data_import = data.FigshareData(self.name)
        
        with rasterio.open(self.data_import.raster_link('hmax')) as src:
            self.size = src.count
            self.res = src.res[0]
            self.bounds = src.bounds

    def calc_ia(self, threshold: float) -> np.ndarray:
        """ Calculates the impact area of a collection of simulations

        Args:
            threshold (float): Threshold value to define the impact area of the simulation

        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative
        
        Returns:
            ia (ndarray): an array of impact area values from simulations
        """

        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')
        
        ia = np.empty((self.size))
        
        with rasterio.open(self.data_import.raster_link('hmax')) as src:
            print('Calculating IA', end='\r')
            for band in range(self.size):
                valid_cells = np.where(src.read(band + 1) >= threshold, 1, 0)
                ia_band = np.sum(valid_cells) * self.res ** 2 / 1000000
                ia[band] = ia_band
            print('IA calculated.')
            
        return ia

    def calc_da(self, threshold: float) -> np.ndarray :
        """ Calculates the deposit area of a collection of simulations

        Args:
            threshold (float): Threshold value to define the deposit area of the simulation

        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative
        
        Returns:
            da (ndarray): an array of deposit area values from simulations
        """

        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')
        
        da = np.empty((self.size))
        
        with rasterio.open(self.data_import.raster_link('hfin')) as src:
            print('Calculating DA', end='\r')
            for band in range(self.size):
                valid_cells = np.where(src.read(band + 1) >= threshold, 1, 0)
                da_band = np.sum(valid_cells) * self.res ** 2 / 1000000
                da[band] = da_band
            print('DA calculated.')
        
        return da

    def calc_dv(self, threshold: float) -> np.ndarray:
        """ Calculates the deposit volume of a collection of simulations

        Args:
            threshold (float): Threshold value to define the deposit volume of the simulation
            
        Raises:
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative

        Returns:
            dv (ndarray): an array of deposit volume values from simulations
        """

        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')

        dv = np.empty((self.size))
        
        with rasterio.open(self.data_import.raster_link('hfin')) as src:
            print('Calculating DV', end='\r')
            for band in range(self.size):
                valid_cells = np.where(src.read(band + 1) >= threshold, self.res ** 2, 0)
                volume = np.multiply(src.read(band + 1), valid_cells)
                dv_band = round((np.sum(volume) / 1000000), 3)
                dv[band] = dv_band
            print('DV calculated.')
            
        return dv

    def extract_qoi_at(self, qoi, loc_x, loc_y) -> np.ndarray:
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

        if not isinstance(qoi, str):
            raise TypeError('qoi must be a string')
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raise Exception('Invalid QoI. It should be hmax, vmax, or pmax.')
        if not isinstance(loc_x, (int, float)):
            raise TypeError('x-coordinate (loc_x) must be an integer or a float')
        if not isinstance(loc_y, (int, float)):
            raise TypeError('y-coordinate (loc_y) must be an integer or a float')
        if loc_x <= self.bounds[0] or loc_x >= self.bounds[2]:
            raise Exception('x-coordinate is out of bounds')
        if loc_y <= self.bounds[1] or loc_y >= self.bounds[3]:
            raise Exception('y-coordinate is out of bounds')
        
        extracted_qoi = np.empty((self.size))
        
        with rasterio.open(self.data_import.raster_link(qoi)) as src:
            row = src.index(loc_x, loc_y)[0]
            col = src.index(loc_x, loc_y)[1]
            print('Extracting ' + qoi, end='\r')
            for band in range(self.size):
                val_qoi = src.read(band + 1)[row, col]
                extracted_qoi[band] = val_qoi
            print(qoi + ' extracted.')
            
        return extracted_qoi

    def curate_scalars(self, threshold: float, loc_x: float, loc_y: float) -> dict:
        """ Curates scalar outputs from simulations

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
            scalars(dict): a dictionary of curated scalars
        """

        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')
        if not isinstance(loc_x, (int, float)):
            raise TypeError('x-coordinate (loc_x) must be an integer or a float')
        if not isinstance(loc_y, (int, float)):
            raise TypeError('y-coordinate (loc_y) must be an integer or a float')

        scalars = {}

        scalars['ia'] = self.calc_ia(threshold)
        scalars['da'] = self.calc_da(threshold)
        scalars['dv'] = self.calc_dv(threshold)

        scalars['vmax'] = self.extract_qoi_at(qoi='vmax', loc_x=loc_x, loc_y=loc_y)
        scalars['hmax'] = self.extract_qoi_at(qoi='hmax', loc_x=loc_x, loc_y=loc_y)

        return scalars

    def create_vector(self, qoi, threshold, valid_cols=None):
        """ Creates an output to train vector emulators

        Args:
            qoi (str): quantity of interest, i.e. hmax for maximum flow height,
            vmax for maximum flow height, and pmax for maximum flow pressure
            threshold (int, float): Threshold value to define valid cells from simulations
            valid_cols (list, optional): column numbers to extract. Defaults to None.

        Raises:
            Exception: Invalid QoI. It should be hmax, vmax, or pmax.
            TypeError: threshold must be a number
            ValueError: threshold cannot be negative

        Returns:
            training (np.ndarray): A data frame consisting of the vector outputs from simulations
            valid_cols (np.ndarray): An array consisting of the valid column names
        """
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raise Exception('Invalid QoI. It should be hmax, vmax, or pmax.')
        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')

        with rasterio.open(self.data_import.raster_link(qoi)) as src:
            rows = src.height
            cols = src.width

            unstacked = np.zeros((self.size, rows * cols))

            for sim in range(self.size):
                unstacked[sim, :] = src.read(sim + 1).reshape(1, rows * cols)

        if valid_cols is None:
            valid_cols = np.where(unstacked >= threshold, 1, 0).sum(axis=0)
        indices = np.flatnonzero(valid_cols)
        training = unstacked[:, indices]
        return training, valid_cols