from .SEPy import SummarizedExperimentPy
import tempfile 
from .helpers import makeCache
from .identifierFile import getIdentifiers
from .ZenodoObj import ZenObj
from pathlib import Path

def getDataset(datasetID: str, version: int|None=None, cacheDirPath: str=tempfile.gettempdir()) -> SummarizedExperimentPy:
    """
    Function that retrieves a breast cancer gene expression dataset.

    Accepts the identifier of a desired dataset, an optional directory path for
    the data to be cached in, and an optional version number. The function 
    looks for the data in the cache. If the data is not found, it is downloaded
    and cached. The data are packaged as SummarizedExperiment objects. If the
    user specifies a cache directory, downloaded files are stored in this
    location so they don't need to be re-downloaded. The default is to use the
    the system's temporary directory.

    Args:
        datasetID (str): The name of the dataset to retrieve
        version (int or None): The version of the data to retrieve, default None
        cacheDirPath (str): The path to the cache directory, default temp directory
    
    Returns:
        SummarizedExperimentPy: An object containing the expression data, metadata, and feature data.
    
    Examples:
        >>> getDataset("GSE41197")
        SummarizedExperimentPy Object
    
    """
    
    identifiers = getIdentifiers()
    identifierList = identifiers[datasetID]
    data = ZenObj(identifierList[0])
    
    if version is not None:
        p = Path(f"{cacheDirPath}/{datasetID}v{version}")
        seData: SummarizedExperimentPy = data.chooseVersion(p, version, datasetID)
        return seData
    
    version_recent = data.most_recent()
    dirPath = Path(f"{cacheDirPath}/{datasetID}v{version_recent}")
    expPath = Path(f"{cacheDirPath}/{datasetID}v{version_recent}/{identifierList[1]}")
    metaPath = Path(f"{cacheDirPath}/{datasetID}v{version_recent}/{identifierList[2]}")
    
    if not expPath.exists():
        link = data.parse_json()
        print("The data was not found in the cache. Downloading now.")
        data.download_file(link, dirPath)

    
    return SummarizedExperimentPy(expPath, metaPath)