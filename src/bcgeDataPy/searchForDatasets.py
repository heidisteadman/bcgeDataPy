import pandas as pd
from helpers import downloadZenFile 
import tempfile 
from pathlib import Path

def searchForDatasetFields(terms: list[str]) -> pd.DataFrame:
    identifiers = ['10.5281/zenodo.17583904', 'filtered_mapped_data.tsv.gz']
    dataPath = Path(f"{tempfile.gettempdir()}/{identifiers[1]}")
    
    if not dataPath.exists():
        downloadZenFile(identifiers[0], dataPath)
    
    mappedTerms = pd.read_csv(dataPath, sep= "\t")
    matches = mappedTerms[mappedTerms['NCIT_field_code'].isin(terms)]
    matches = matches[['dataset', 'orig_field', 'NCIT_field_code']]
    matches = matches.rename(columns={'dataset': 'Dataset_ID', 'orig_field': 'Field', 'NCIT_field_code': 'Code'})

    return matches

def searchForDatasetValues(terms: list[str]) -> pd.DataFrame:
    identifiers = ['10.5281/zenodo.17583904', 'filtered_mapped_data.tsv.gz']
    dataPath = Path(f"{tempfile.gettempdir()}/{identifiers[1]}")
    
    if not dataPath.exists():
        downloadZenFile(identifiers[0], dataPath)
    
    mappedTerms = pd.read_csv(dataPath, sep= "\t")
    matches = mappedTerms[mappedTerms['NCIT_value_code'].isin(terms)]
    matches = matches[['dataset', 'orig_field', 'NCIT_field_code', 'orig_values', 'NCIT_value_code']]
    matches = matches.rename(columns={'dataset': 'Dataset_ID', 'orig_field': 'Field', 'NCIT_field_code': 'Field_Code', 'orig_values': 'Values', 'NCIT_value_code': 'Code'})

    return matches