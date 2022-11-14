import pandas as pd
import numpy as np
from sklearn import metrics
import pkg_resources
from frontiers_yildizetal import Simulations
import rasterio
import yaml
from yaml.loader import SafeLoader

import os
if os.name == 'nt':
    r_path = os.environ["CONDA_PREFIX"] + '/lib/R'
    os.environ['R_HOME'] = r_path 

import rpy2.robjects.packages as rpackages
import rpy2.robjects.numpy2ri

robustgasp = rpackages.importr('RobustGaSP')
rpy2.robjects.numpy2ri.activate()

class Emulators:
    def __init__(self, name:str):
        if not isinstance(name,str):
            raise TypeError('name must be a string')
        if name not in ['synth', 'acheron']:
            raise Exception('Invalid name. It must be synth, synth_validate, acheron, or acheron_validate')
        
        self.name = name
        
        path = 'files/input/input_emulator_' + self.name + '.csv'
        path_validate = 'files/input/input_emulator_' + self.name + '_validate.csv'
        filepath = pkg_resources.resource_filename(__name__, path)
        validpath = pkg_resources.resource_filename(__name__, path_validate)
        
        self.input_train = np.genfromtxt(filepath, delimiter=',', skip_header=1)
        self.input_validate = np.genfromtxt(validpath, delimiter=',', skip_header=1)
        
        path_download = 'files/download_links.yml'
        filepath_download = pkg_resources.resource_filename(__name__, path_download)
        with open(filepath_download) as f:
            download_links = yaml.load(f, Loader=SafeLoader)
        self.links = download_links[self.name]
        
class ScalarEmulators(Emulators):
    def __init__(self, name:str, threshold:float, loc_x:float, loc_y:float):
        
        if not isinstance(name,str):
            raise TypeError('name must be a string')
        if name not in ['synth', 'synth_validate', 'acheron', 'acheron_validate']:
            raise Exception('Invalid name. It must be synth, synth_validate, acheron, or acheron_validate')
        if not isinstance(threshold, (int, float)):
            raise TypeError('threshold must be a number')
        if threshold < 0:
            raise ValueError('threshold cannot be negative')
        if not isinstance(loc_x, (int, float)):
            raise TypeError('x-coordinate (loc_x) must be an integer or a float')
        if not isinstance(loc_y, (int, float)):
            raise TypeError('y-coordinate (loc_y) must be an integer or a float')
        
        super().__init__(name)
        self.output = Simulations(self.name).curate_scalars(threshold=threshold, loc_x=loc_x, loc_y=loc_y)

    def model(self, scalar:str):
        
        if not isinstance(scalar,str):
            raise TypeError('scalar must be a string')
        if scalar not in ['ia', 'da', 'dv', 'hmax', 'vmax']:
            raise Exception('Invalid name. It must be ia, da, dv, hmax or vmax')
        
        model = robustgasp.rgasp(design=self.input_train, response=self.output[scalar])
        return model
    
    def cv_loo(self,scalar:str):
        
        if not isinstance(scalar,str):
            raise TypeError('scalar must be a string')
        if scalar not in ['ia', 'da', 'dv', 'hmax', 'vmax']:
            raise Exception('Invalid name. It must be ia, da, dv, hmax or vmax')
        
        trained = self.model(scalar)
        loo = robustgasp.leave_one_out_rgasp(trained)
        
        loo_r2 = metrics.r2_score(y_true=self.output[scalar], y_pred=loo[0])
        loo_mape = metrics.mean_absolute_percentage_error(y_true=self.output[scalar], y_pred=loo[0]) * 100
        loo_nrmse = 100 * np.sqrt(metrics.mean_squared_error(y_true=self.output[scalar], y_pred=loo[0])) / (self.output[scalar].mean())
        loo_metrics = {'r2':loo_r2, 'mape':loo_mape, 'nrmse':loo_nrmse}
        return loo_metrics
    
    def predict_scalar(self, scalar:str, input_pred):
        
        if not isinstance(scalar,str):
            raise TypeError('scalar must be a string')
        if scalar not in ['ia', 'da', 'dv', 'hmax', 'vmax']:
            raise Exception('Invalid name. It must be ia, da, dv, hmax or vmax')
        
        trained = self.model(scalar)
        predicted = robustgasp.predict_rgasp(object=trained, testing_input=input_pred)
        return predicted

class VectorEmulators(Emulators):
    def __init__(self, name, qoi, threshold):
        
        if qoi not in ['hmax', 'vmax', 'pmax']:
            raise Exception('Invalid QoI. It should be hmax, vmax, or pmax.')
        if not isinstance(threshold, (int, float)):
            raise TypeError("threshold must be a number")
        if threshold < 0:
            raise ValueError("threshold cannot be negative")
        
        super().__init__(name)
        self.qoi = qoi
        self.threshold = threshold
        self.vector, self.valid_cols = Simulations(self.name).create_vector(qoi=qoi, threshold=threshold)
        self.vector_validate, self.valid_cols = Simulations((self.name + '_validate')).create_vector(qoi=qoi, threshold=threshold, valid_cols=self.valid_cols)
                
        with rasterio.open(self.links[qoi]) as src:
            self.sim_size = src.count
            self.rows = src.height
            self.cols = src.width
    
    def model(self):
        model = robustgasp.ppgasp(design=self.input_train, response=self.vector.to_numpy())
        return model
    
    def validate(self):
        trained = self.model()
        predicted = robustgasp.predict_ppgasp(object=trained, testing_input=self.input_validate)
        
        predict_mean = np.where(predicted[0] < 0, 0 , predicted[0])
        predict_lower = np.where(predicted[1] < 0, 0 , predicted[1])
        predict_upper = np.where(predicted[2] < 0, 0 , predicted[2])
        
        self.pci95 = np.mean(np.where((self.vector_validate >= predict_lower) & (self.vector_validate <= predict_upper), 1, 0))
        self.mean_squared_error = np.mean((predict_mean - self.vector_validate)**2)
        self.lci95 = np.mean(predict_upper-predict_lower)
        
        prediction = {'prediction':predicted, 'pci95':self.pci95, 'lci95':self.lci95, 'mean_sq_err':self.mean_squared_error}
        return prediction
    
    def predict_vector(self,input_pred):
        trained= self.model()
        predicted = robustgasp.predict_ppgasp(object=trained, testing_input=input_pred)
        
        pred_size = input_pred.shape[0]
        pred_index = [int(i) for i in list(self.vector.columns)]
        
        pred = np.empty((pred_size, self.rows * self.cols))
        pred[:,pred_index] = predicted[0]
            
        pred_mean = pred.mean(axis=0).reshape(self.rows, self.cols)
        pred_sd = pred.std(axis=0).reshape(self.rows, self.cols)
            
        return pred_mean, pred_sd