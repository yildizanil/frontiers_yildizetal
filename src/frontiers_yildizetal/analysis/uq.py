from frontiers_yildizetal.ravaflow import Simulations
from frontiers_yildizetal.emulators import ScalarEmulators
from scipy.stats import skew
import numpy as np
from frontiers_yildizetal.utilities import data

class Moments:
    """
    A class to represent moments, i.e. mean, variance and skewness, for UQ analysis
    
    Arguments:
        name (str): name of the set. It can be either synth or acheron
        
    Attributes:
        locs (list): coordinates at which hmax and vmax are extracted.
        
    Methods:
        get_mcs: returns the moments calculated with Monte Carlo simulations
        get_pem: returns the moments calculated with Point Estimate Method

    Raises:
        TypeError: name must be a string
        ValueError: name must be either synth or acheron

    """
    funcs = {'mean':np.mean, 'var':np.var, 'skew':skew}

    def __init__(self, name:str):
        if not isinstance(name,str):
            raise TypeError('name must be a string')
        if name not in ['synth', 'acheron']:
            raise ValueError('name must be either synth or acheron')
        self.name = name
        loc_all = {'synth': [1000, 2000], 'acheron': [1490100, 5204100]}
        self.locs = loc_all[self.name]
        
    def get_mcs(self):
        """
        Calculates the three moments using Monte Carlo Simulations facilitated with Gaussian Process Emulation

        Returns:
            mcs_moments (dict): A dictionary storing the moments according to scalars
        """
        mcss = ['mcs' + str(i) for i in range(1, 4)]
        emulator = ScalarEmulators(self.name, 0.1,
                                   self.locs[0],
                                   self.locs[1])
        scalars = list(emulator.output.keys())    
    
        mcs_moments = {}

        for n, f in self.funcs.items():
            mcs_moments[n] = {}
            for key in scalars:
                mcs_moments[n][key] = []
                for mcs in mcss:
                    input_test = data.load_input(name=emulator.name, analysis=mcs)
                    predicted = emulator.predict_scalar(key, input_test)[0]
                
                    if f is np.var:
                        val = f(predicted, ddof=1)
                        mcs_moments[n][key].append(round(val, 3))
                    else:
                        val = f(predicted)
                        mcs_moments[n][key].append(round(val, 3))
        return mcs_moments
    
    def get_pem(self):
        """
        Calculates the three moments using Point Estimate Method
        
        Returns:
            pem_moments (dict): A dictionary storing the moments according to scalars
        """
        pems = ['pem' + str(i) for i in range(1, 4)]
        scalars = Simulations((self.name + '_pem')).curate_scalars(0.1, self.locs[0], self.locs[1])
    
        pem_moments = {}

        for n, f in self.funcs.items():
            pem_moments[n] = {}
            for key in scalars:
                pem_moments[n][key] = []
                for j, pem in enumerate(pems):
                    if f is np.var:
                        val = f(scalars[key][8 * j : 8 * (j + 1)], ddof=1)
                        pem_moments[n][key].append(round(val, 3))
                    else:
                        val = f(scalars[key][8 * j : 8 * (j + 1)])
                        pem_moments[n][key].append(round(val, 3))
        return pem_moments