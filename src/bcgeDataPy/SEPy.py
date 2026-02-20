import pandas as pd

class SummarizedExperimentPy():
    def __init__(self, data, metadata):
        self.data = data 
        self.metadata = metadata 
    
    def assay(self):
        exp_data = pd.read_csv(self.data, sep="\t")
        return exp_data  
    
    def colData(self):
        meta = pd.read_csv(self.metadata, sep="\t")
        return meta 