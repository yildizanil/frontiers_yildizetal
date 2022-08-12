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
        filepath = pkg_resources.resource_filename(__name__, path)
        self.input = pd.read_csv(filepath)
        
class ScalarEmulators(Emulators):
    def __init__(self, name, h_threshold, loc_x, loc_y):
        super().__init__(name)
        self.output = Simulations(self.name).curate_scalars(threshold=h_threshold, loc_x=loc_x, loc_y=loc_y)

    def model(self, scalar):
        model = robustgasp.rgasp(design=self.input.to_numpy(), response=self.output[scalar].to_numpy())
        return (model)
    
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