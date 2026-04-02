from pathlib import Path
from pybiocfilecache import BiocFileCache
from ZenodoObj import ZenObj
from SEPy import SummarizedExperimentPy

def makeCache(filepath):
    path = Path(filepath)
    if not path.exists():
        raise ValueError("Invalid filepath")
    else:
        cache = BiocFileCache(filepath)
        return cache 

def chooseVersion(datasetID: str, dataset: ZenObj, cache: BiocFileCache|str, v: int) -> SummarizedExperimentPy:
    dirPath = f"{cache}/{datasetID}v{v}"
    path = Path(dirPath)
    if not path.exists():
        print("Either the data was not found in the cache or a new version was requested. Downloading now.")
        link = dataset.get_versions(v)
        dataset.download_file(link, path)
    expData = (Path(f"{dirPath}/{datasetID}.tsv.gz"))
    metadata = (Path(f"{dirPath}/{datasetID}_metadata.tsv"))

    return SummarizedExperimentPy(expData, metadata)