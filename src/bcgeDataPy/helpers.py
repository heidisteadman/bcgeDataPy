from pathlib import Path
from pybiocfilecache import BiocFileCache
from ZenodoObj import ZenObj
from SEPy import SummarizedExperimentPy
import requests

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
    expData = (f"{dirPath}/{datasetID}.tsv.gz")
    metadata = (f"{dirPath}/{datasetID}_metadata.tsv")

    return SummarizedExperimentPy(expData, metadata)

def downloadZenFile(conceptDOI:str, path:str) -> None:
    cdoi = f"conceptdoi:{conceptDOI}"
    jsonresp = requests.get(url="https://zenodo.org/api/records",
                                     params={
                                         "q": cdoi,
                                         "size": 25,
                                         "sort": "mostrecent"
                                     })

    js = jsonresp.json()
    hits = js['hits']['hits'][0]
    doi_id = hits['id']
    download_link = f"https://zenodo.org/api/records/, {doi_id}, /files-archive"
    downloaded_file = requests.get(download_link)
    with open(path, 'wb') as f:
        f.write(downloaded_file.content)
    return
