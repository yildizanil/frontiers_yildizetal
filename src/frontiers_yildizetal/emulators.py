import pandas as pd
import numpy as np
from sklearn import metrics
import pkg_resources
from frontiers_yildizetal import Simulations

import rpy2.robjects.packages as rpackages
import rpy2.robjects.numpy2ri

robustgasp = rpackages.importr('RobustGaSP')
rpy2.robjects.numpy2ri.activate()

class Emulators:
    
    def __init__(self, name:str):
        self.name = name
        path = 'files/input/input_emulator_' + self.name + '.csv'
        path_validate = 'files/input/input_emulator_' + self.name + '_validate.csv'
        filepath = pkg_resources.resource_filename(__name__, path)
        validpath = pkg_resources.resource_filename(__name__, path_validate)
        self.input = pd.read_csv(filepath)
        self.input_validate = pd.read_csv(validpath)
        
class ScalarEmulators(Emulators):
    def __init__(self, name, h_threshold, loc_x, loc_y):
        super().__init__(name)
        self.output = Simulations(self.name).curate_scalars(threshold=h_threshold, loc_x=loc_x, loc_y=loc_y)

    def model(self, scalar):
        model = robustgasp.rgasp(design=self.input.to_numpy(), response=self.output[scalar].to_numpy())
        return model
    
    def cv_loo(self,scalar):
        trained = self.model(scalar)
        loo = robustgasp.leave_one_out_rgasp(trained)
        loo_r2 = metrics.r2_score(y_true=self.output[scalar], y_pred=loo[0])
        loo_mape = metrics.mean_absolute_percentage_error(y_true=self.output[scalar], y_pred=loo[0]) * 100
        loo_nrmse = 100 * np.sqrt(metrics.mean_squared_error(y_true=self.output[scalar], y_pred=loo[0])) / (self.output[scalar].mean())
        loo_metrics = {'r2':loo_r2, 'mape':loo_mape, 'nrmse':loo_nrmse}
        return loo_metrics
    
    def predict_scalar(self, scalar, input_pred):
        trained = self.model(scalar)
        predicted = robustgasp.predict_rgasp(object=trained, testing_input=input_pred)
        return predicted

class VectorEmulators(Emulators):
    def __init__(self, name, qoi, threshold):
        super().__init__(name)
        self.vector, self.valid_cols = Simulations(self.name).create_vector(qoi=qoi, threshold=threshold)
        self.vector_validate, self.valid_cols = Simulations((self.name + '_validate')).create_vector(qoi=qoi, threshold=threshold, valid_cols=self.valid_cols)
    
    def model(self):
        model = robustgasp.ppgasp(design=self.input.to_numpy(), response=self.vector.to_numpy())
        return model
    
    def validate(self):
        trained = self.model()
        predicted = robustgasp.predict_ppgasp(object=trained, testing_input=self.input_validate.to_numpy())
        
        predict_mean = np.where(predicted[0] < 0, 0 , predicted[0])
        predict_lower = np.where(predicted[1] < 0, 0 , predicted[1])
        predict_upper = np.where(predicted[2] < 0, 0 , predicted[2])
        
        self.pci95 = np.mean(np.where((self.vector_validate >= predict_lower) & (self.vector_validate <= predict_upper), 1, 0))
        self.mean_squared_error = np.mean((predict_mean - self.vector_validate)**2)
        self.lci95 = np.mean(predict_upper-predict_lower)
        
        prediction = {'prediction':predicted, 'pci95':self.pci95, 'lci95':self.lci95, 'mean_sq_err':self.mean_squared_error}

        return prediction