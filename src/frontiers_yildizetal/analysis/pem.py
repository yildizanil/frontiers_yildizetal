from frontiers_yildizetal.ravaflow import Simulations
from scipy.stats import skew
import numpy as np

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

    pems = ['pem' + str(i) for i in range(1, 4)]
    scalars = Simulations(name + '_pem').curate_scalars(0.1, locs[name][0], locs[name][1])
    
    moments = {}

    for f, n in zip(funcs, f_names):
        moments[n] = {}
        for key in scalars:
            moments[n][key] = []
            for j, pem in enumerate(pems):
                if f is np.var:
                    val = f(scalars[key][8 * j : 8 * (j + 1)], ddof=1)
                    moments[n][key].append(round(val, 3))
                else:
                    val = f(scalars[key][8 * j : 8 * (j + 1)])
                    moments[n][key].append(round(val, 3))
    return moments



