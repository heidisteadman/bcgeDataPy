import pandas as pd
import tempfile 
from pathlib import Path
from ZenodoObj import ZenObj

def searchForDatasetFields(terms: list[str]) -> pd.DataFrame:
    """
    Function that searches breast cancer datasets based on ontology terms mapped to data fields.

    Accepts an ontology term code and searches for datasets based on fields
    (metadata columns) that have been mapped to that ontology term.
    Returns a data frame with the dataset identifier, field name, and  
    code. Users can then pass the dataset identifiers to the getDataset
    function.

    Args:
        terms (list[str]): is an ontology term code retrieved using the searchOntologyTerms function.
    
    Returns:
        pd.DataFrame: a data frame providing information about any identified datasets.
    
    Examples:
        >>> searchForDatasetFields(["C16149"])
        pandas DataFrame object
    
    """

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
    """
    Function that searches breast cancer datasets based on ontology terms mapped to data values.

    Accepts an ontology term code and searches for datasets based on metadata values
    that have been mapped to that ontology term.
    Returns a data frame with the dataset identifier, field name, original values, and  
    code. Users can then pass the dataset identifiers to the getDataset
    function.

    Args:
        terms (list[str]): is an ontology term code retrieved using the searchOntologyTerms function.
    
    Returns:
        pd.DataFrame: a data frame providing information about any identified datasets.
    
    Examples:
        >>> searchForDatasetValues(["C15496"])
        pandas DataFrame object
    
    """

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