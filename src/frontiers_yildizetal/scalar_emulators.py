import pandas as pd
from sklearn import metrics
from frontiers_yildizetal import Simulations

import rpy2.robjects.packages as rpackages
import rpy2.robjects.numpy2ri

robustgasp = rpackages.importr('RobustGaSP')
rpy2.robjects.numpy2ri.activate()

class ScalarEmulators:
    
    def __init__(self, name:str, h_threshold, loc_x, loc_y):
        self.name = name
        filepath = 'tests/input/input_emulator_' + self.name + '.csv' 
        self.input = pd.read_csv(filepath)
        self.output = Simulations(self.name).curate_scalars(threshold=h_threshold, loc_x=loc_x, loc_y=loc_y)
        
    def emulate_scalar(self, scalar):
        model = robustgasp.rgasp(design=self.input.to_numpy(), response=self.output[scalar].to_numpy())
        return (model)