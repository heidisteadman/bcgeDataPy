import pandas as pd

class SummarizedExperimentPy:
    def __init__(self, data, metadata):
        self.data = data 
        self.metadata = metadata 
    
    def assay(self):
        exp_data = pd.read_csv(self.data, sep="\t")
        exp_data = exp_data[~exp_data["Chromosome"].str.startswith("H")]
        exp_data = exp_data.set_index("Ensembl_Gene_ID")
        exp_data = exp_data.iloc[:, 5:]
        return exp_data  
    
    def colData(self):
        meta = pd.read_csv(self.metadata, sep="\t")
        return meta
    
    def rowData(self):
        exp = pd.read_csv(self.data, sep="\t")
        exp = exp[~exp["Chromosome"].str.startswith("H")]
        features = exp[["Dataset_ID", "Entrez_Gene_ID", "HGNC_Symbol", "Ensembl_Gene_ID", "Chromosome", "Gene_Biotype"]]
        features = features.set_index("Ensembl_Gene_ID")
        return features