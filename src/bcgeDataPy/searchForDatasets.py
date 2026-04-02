import pandas as pd
import tempfile 
from pathlib import Path
from ZenodoObj import ZenObj

def searchForDatasetFields(terms: list[str]) -> pd.DataFrame:
    identifiers = ['10.5281/zenodo.17583904', 'filtered_mapped_data.tsv.gz']
    dataPath = Path(f"{tempfile.gettempdir()}/mappedData")
    filePath = dataPath / identifiers[1]
    zendata = ZenObj(identifiers[0])
    if not filePath.exists():
        download_link = zendata.parse_json()
        zendata.download_file(download_link, dataPath)
    
    mappedTerms = pd.read_csv(filePath, sep= "\t")
    matches = mappedTerms[mappedTerms['NCIT_field_code'].isin(terms)]
    matches = matches[['dataset', 'orig_field', 'NCIT_field_code']]
    matches = matches.rename(columns={'dataset': 'Dataset_ID', 'orig_field': 'Field', 'NCIT_field_code': 'Code'})

    return matches

def searchForDatasetValues(terms: list[str]) -> pd.DataFrame:
    identifiers = ['10.5281/zenodo.17583904', 'filtered_mapped_data.tsv.gz']
    dataPath = Path(f"{tempfile.gettempdir()}/mappedData")
    filePath = dataPath / identifiers[1]
    zendata = ZenObj(identifiers[0])
    if not filePath.exists():
        download_link = zendata.parse_json()
        zendata.download_file(download_link, dataPath)
    
    mappedTerms = pd.read_csv(filePath, sep= "\t")
    matches = mappedTerms[mappedTerms['NCIT_value_code'].isin(terms)]
    matches = matches[['dataset', 'orig_field', 'NCIT_field_code', 'orig_values', 'NCIT_value_code']]
    matches = matches.rename(columns={'dataset': 'Dataset_ID', 'orig_field': 'Field', 'NCIT_field_code': 'Field_Code', 'orig_values': 'Values', 'NCIT_value_code': 'Code'})

    return matches