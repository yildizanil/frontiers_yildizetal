import rasterio
import numpy as np
import pandas as pd

def calculate(raster_path, threshold):
    """ calculates the maximum lateral spread and finds its location

    Args:
        raster_path (str): path of the hmax_stack.tif raster file
        threshold (float): threshold of flow height, e.g. 0.1 m

    Returns:
        Pandas DataFrame: a data frame with two columns, i.e. location and value of the maximum lateral spread
    """
    with rasterio.open(raster_path) as src:
        sim_size = src.count
        res= src.res[0]
        
        max_vals = []
        max_locs = []
        for i in range(sim_size):
            data = np.where(src.read(i+1) < threshold, 0, src.read(i+1))
            columns = np.unique(np.nonzero(data)[1]).tolist()
    
            rows = []
            for col in columns:
                rows.append(len(np.nonzero(data[:,col])[0]))
            max_loc = res * np.argmax(rows)
            max_val = res * np.max(rows)
            max_vals.append(max_val)
            max_locs.append(max_loc)
    
    lateral = pd.DataFrame({'location':max_locs, 'value':max_vals})
    return lateral