from frontiers_yildizetal.ravaflow import Simulations
from frontiers_yildizetal.emulators import ScalarEmulators
from scipy.stats import skew
import numpy as np
from frontiers_yildizetal.utilities import data

def moments(name:str):
    """
    pem_analyse _summary_

    Args:
        name (str): _description_

    Raises:
        TypeError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if not isinstance(name,str):
        raise TypeError('name must be a string')
    if name not in ['synth', 'acheron']:
        raise ValueError('name must be either synth or acheron')

    locs = {
        'synth': [1000, 2000],
        'acheron': [1490100, 5204100]
        }

    funcs = [np.mean, np.var, skew]
    f_names = ['mean', 'var', 'skew']

    mcss = ['mcs' + str(i) for i in range(1, 4)]
    emulator = ScalarEmulators(name, 0.1, locs[name][0], locs[name][1])
    scalars = list(emulator.output.keys())
    
    moments = {}

    for f, n in zip(funcs, f_names):
        moments[n] = {}
        for key in scalars:
            moments[n][key] = []
            for j, k in enumerate(mcss):
                input_test = data.InputData(name=emulator.name, analysis=k).data
                predicted = emulator.predict_scalar(key, input_test)[0]
                
                if f is np.var:
                    val = f(predicted, ddof=1)
                    moments[n][key].append(round(val, 3))
                else:
                    val = f(predicted)
                    moments[n][key].append(round(val, 3))
    return moments