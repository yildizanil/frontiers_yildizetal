# Task 2
import requests
import numpy as np
from pkg_resources import resource_filename

class FigshareData:
    """
    Figshare class to access datasets over API.

   Attributes
    ----------
    article_id : int
        ID number of the article hosted on Figshare
        
    Methods
    ----------
        list_files(self):
            lists the different files in the article
        import_files(self, file_index = 0, rows_to_skip = 0):
            import the csv and xlsx files into pandas dataframe
    """
    article_id = {
            'synth':20449395,
            'synth_pem':20454924,
            'synth_validation':20454933,
            'acheron':20449410,
            'acheron_pem': 20454927,
            'acheron_validation':20454936}
    def __init__(self, name):
        """ Constructus all the necessary attributes for Figshare class.

        Parameters
        ----------
            article_id (int): ID number of the article hosted on Figshare
            link (str): API link to the article hosted on Figshare
        """
        self.name = name
        self.link = 'https://api.figshare.com/v2/articles/' + str(self.article_id[name])
        self.files = requests.get(self.link + '/files').json()
        self.filenames = [file['name'] for file in self.files]
        self.parameters = [filename.strip('_stack.tif') for filename in self.filenames]
        
    def raster_link(self, parameter):
        
        index_no = self.parameters.index(parameter)
        url = self.files[index_no]['download_url']
        
        return url
        
class InputData:
    def __init__(self, name, analysis):
        self.name = name
        self.analysis = analysis
        
        path = 'utilities/input/' + self.name + '_' + self.analysis + '.csv'
        filepath = resource_filename('frontiers_yildizetal', path)
        self.data = np.genfromtxt(filepath, delimiter=',', skip_header=1)