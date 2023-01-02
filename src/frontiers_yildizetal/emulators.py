import numpy as np
import rasterio
from sklearn import metrics
import os
from frontiers_yildizetal.ravaflow import Simulations
from frontiers_yildizetal.utilities import data

import os
if os.name == 'nt':
    r_path = os.environ["CONDA_PREFIX"] + '/lib/R'
    os.environ['R_HOME'] = r_path 

import rpy2.robjects.packages as rpackages
import rpy2.robjects.numpy2ri

robustgasp = rpackages.importr('RobustGaSP')
rpy2.robjects.numpy2ri.activate()

class ScalarEmulators:
    """
    A class to represent GP emulators
    
    Attributes
    ----------
    name:str
        Name of the emulators set. Can be one of the following: synth, synth_validate, acheron, acheron_validate
    input_train: Numpy array
        Input dataset for training
    input_validate: Numpy array
        Input dataset for validation
    links: dict
        Download links to access output files
    """
    def __init__(self, name:str, threshold:float, loc_x:float, loc_y:float):
        """
        Initialising Emulators class

        Args:
            name (str): Name of the emulators set. Can be one of the following: synth, synth_validate, acheron, acheron_validate

        Raises:
            TypeError: name must be a string
            Exception: Invalid name. It must be synth, synth_validate, acheron, or acheron_validate
        """
        if not isinstance(name,str):
            raise TypeError('name must be a string')
        if name not in ['synth', 'acheron']:
            raise Exception('Invalid name. It must be synth, synth_validate, acheron, or acheron_validate')
        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')
        if not isinstance(loc_x, (int, float)):
            raise TypeError('x-coordinate (loc_x) must be an integer or a float')
        if not isinstance(loc_y, (int, float)):
            raise TypeError('y-coordinate (loc_y) must be an integer or a float')
        
        self.name = name
        self.sims = Simulations(self.name)
        self.loc_x, self.loc_y = loc_x, loc_y
        
        self.input_train = data.load_input(self.name, 'emulator')
        self.input_validate = data.load_input((name + '_validate'), 'emulator')
        
        self.output = self.sims.curate_scalars(threshold=threshold, loc_x=loc_x, loc_y=loc_y)

    def model(self, scalar:str):
        """
        Constructs the GP emulator a scalar

        Args:
            scalar (str): name of the scalar to be emulated. Can be impact area (ia), deposit area (da), deposit volume, maximum flow height (hmax) or maximum flow velocity (vmax)

        Raises:
            TypeError: scalar must be a string
            Exception: Invalid name. It must be ia, da, dv, hmax or vmax

        Returns:
           model: An R object of rgasp emulator
        """
        
        if not isinstance(scalar,str):
            raise TypeError('scalar must be a string')
        if scalar not in ['ia', 'da', 'dv', 'hmax', 'vmax']:
            raise Exception('Invalid name. It must be ia, da, dv, hmax or vmax')
        
        model = robustgasp.rgasp(design=self.input_train, response=self.output[scalar])
        return model
    
    def cv_loo(self,scalar:str):
        """
        Cross validation with leave-one-out technique

        Args:
            scalar (str): name of the scalar to be emulated. Can be impact area (ia), deposit area (da), deposit volume, maximum flow height (hmax) or maximum flow velocity (vmax)

        Raises:
            TypeError: scalar must be a string
            Exception: Invalid name. It must be ia, da, dv, hmax or vmax

        Returns:
            loo_metrics (dict): Error metrics (r2, mape, nrmse) from the cross validation
        """
        if not isinstance(scalar,str):
            raise TypeError('scalar must be a string')
        if scalar not in ['ia', 'da', 'dv', 'hmax', 'vmax']:
            raise Exception('Invalid name. It must be ia, da, dv, hmax or vmax')
        
        trained = self.model(scalar)
        loo = robustgasp.leave_one_out_rgasp(trained)
        loo_metrics = {}
        
        loo_metrics['r2'] = metrics.r2_score(y_true=self.output[scalar], y_pred=loo[0])
        loo_metrics['mape'] = metrics.mean_absolute_percentage_error(y_true=self.output[scalar], y_pred=loo[0]) * 100
        loo_metrics['nrmse'] = 100 * np.sqrt(metrics.mean_squared_error(y_true=self.output[scalar], y_pred=loo[0])) / (self.output[scalar].mean())
        return loo_metrics
    
    def predict_scalar(self, scalar:str, input_pred:np.ndarray):
        """
        Performs prediction using trained models

        Args:
            scalar (str): name of the scalar to be emulated. Can be impact area (ia), deposit area (da), deposit volume, maximum flow height (hmax) or maximum flow velocity (vmax)
            input_pred (np.ndarray): Input testing dataset to perform prediction

        Raises:
            TypeError: scalar must be a string
            Exception: Invalid name. It must be ia, da, dv, hmax or vmax

        Returns:
            predicted: An R object with the predictions. Consists of mean, lower95, upper95, and sd.
        """
        if not isinstance(scalar,str):
            raise TypeError('scalar must be a string')
        if scalar not in ['ia', 'da', 'dv', 'hmax', 'vmax']:
            raise Exception('Invalid name. It must be ia, da, dv, hmax or vmax')
        
        trained = self.model(scalar)
        predicted = robustgasp.predict_rgasp(object=trained, testing_input=input_pred)
        return predicted
    
class VectorEmulators:
    def __init__(self, name, qoi:str, threshold:float):
        """
        Initialising VectorEmulators class

        Args:
            name (_type_): _description_
            qoi (_type_): _description_
            threshold (_type_): _description_

        Raises:
            Exception: _description_
            TypeError: _description_
            ValueError: _description_
        """
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raise Exception('Invalid QoI. It should be hmax, vmax, or pmax.')
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        
        self.name = name
        self.sims = Simulations(self.name)
        self.qoi = qoi
        self.threshold = threshold

        with rasterio.open(self.sims.data_import.raster_link('hmax')) as src:
            self.size = src.count
            self.res = src.res[0]
            self.bounds = src.bounds
 
        self.vector, self.valid_cols = self.sims.create_vector(qoi=qoi, threshold=threshold)
        self.vector_validate, self.valid_cols = Simulations((self.name + '_validate')).create_vector(qoi=self.qoi, threshold=self.threshold, valid_cols=self.valid_cols)
        
        self.input_train = data.load_input(self.name, 'emulator')
        self.input_validate = data.load_input((name + '_validate'), 'emulator')
        
        with rasterio.open(self.sims.data_import.raster_link(qoi)) as src:
            self.size = src.count
            self.rows = src.height
            self.cols = src.width

        self.model = robustgasp.ppgasp(design=self.input_train, response=self.vector)
    
    def validate(self):
        
        validated = robustgasp.predict_ppgasp(object=self.model, testing_input=self.input_validate)
        val_arr = [np.array(matrix) for matrix in list(validated)]
        
        validated_mean = np.where(val_arr[0] < 0, 0 , val_arr[0])
        validated_lower = np.where(val_arr[1] < 0, 0 , val_arr[1])
        validated_upper = np.where(val_arr[2] < 0, 0 , val_arr[2])
        
        self.pci95 = np.mean(np.where((self.vector_validate >= validated_lower) & (self.vector_validate <= validated_upper), 1, 0))
        self.mean_squared_error = np.mean((validated_mean - self.vector_validate)**2)
        self.lci95 = np.mean(validated_upper-validated_lower)
        
        validation = {'validation':validated_mean, 'pci95':self.pci95, 'lci95':self.lci95, 'mean_sq_err':self.mean_squared_error}
        return validation
    
    def predict_vector(self,input_pred:np.ndarray):
        """
        predict_vector _summary_

        Args:
            input_pred (np.ndarray): _description_

        Returns:
            _type_: _description_
        """
        predicted = robustgasp.predict_ppgasp(object=self.model, testing_input=input_pred)
        
        pred_size = input_pred.shape[0]
        indices = np.flatnonzero(self.valid_cols)
        pred_index = [int(i) for i in list(indices)]
        
        pred = np.empty((pred_size, self.rows * self.cols))
        pred[:,pred_index] = predicted[0]
            
        pred_mean = pred.mean(axis=0).reshape(self.rows, self.cols)
        pred_sd = pred.std(axis=0).reshape(self.rows, self.cols)
            
        return pred_mean, pred_sd