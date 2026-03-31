from SEPy import SummarizedExperimentPy
import tempfile 
from helpers import makeCache, chooseVersion
from identifierFile import getIdentifiers
from ZenodoObj import ZenObj
from pathlib import Path

def getDataset(datasetID: str, version: int|None=None, cacheDirPath: str=tempfile.gettempdir()) -> SummarizedExperimentPy:
    if (cacheDirPath != tempfile.gettempdir()):
        cache = makeCache(cacheDirPath)
    else:
        cache = cacheDirPath
    
    identifiers = getIdentifiers()
    identifierList = identifiers[datasetID]
    data = ZenObj(identifierList[0])
    
    if version is not None:
        seData: SummarizedExperimentPy = chooseVersion(datasetID, data, cache, version)
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