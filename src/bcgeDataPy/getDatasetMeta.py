from ZenodoObj import ZenObj
import pandas as pd
from pathlib import Path 
import tempfile

def getDatasetMetadata(datasets: list[str]) -> pd.DataFrame:
    """
    A function that accepts a vector of dataset IDs and returns a tibble with 
    metadata about the overall study.

    Args:
        datasets (list[str]): The list of datasets to get metadata for
    
    Returns:
        pd.DataFrame: The data frame with the datasets as rows and info as columns
    
    Examples:
        >>> getDatasetMetadata(["GSE41197", "GSE59772"])
        pd.DataFrame containing metadata for given datasets
    """
    
    identifiers = ['10.5281/zenodo.17780657', 'dataset_meta.tsv']
    dataPath = Path(f"{tempfile.gettempdir()}/datasetMeta")
    filePath = dataPath / identifiers[1]
    zendata = ZenObj(identifiers[0])
    if not filePath.exists():
        download_link = zendata.parse_json()
        zendata.download_file(download_link, dataPath)
    
    mappedTerms = pd.read_csv(filePath, sep= "\t")

    for dataset in datasets:
        if "_" in dataset:
            if (dataset == "ICGC_KR"):
                continue
            if dataset == "E_TABM_158":
                datasets.append("E-TABM-158")
                continue
            split_str = dataset.split("_")
            keep = split_str[0]
            datasets.append(keep)
            datasets.remove(dataset)
    
    matches = mappedTerms[mappedTerms['accession_id'].isin(datasets)]
    matches = matches[['accession_id', 'publishing_platform', 'experiment_type', 'title', 'summary', 'overall_design']]
    matches = matches.rename(columns={'accession_id': 'Dataset_ID', 
                                      'publishing_platform': 'Source', 
                                      'experiment_type': 'Experiment_Type', 
                                      'title': 'Title', 
                                      'summary': 'Summary',
                                      'overall_design': 'Overall_Design'})
    return matches 