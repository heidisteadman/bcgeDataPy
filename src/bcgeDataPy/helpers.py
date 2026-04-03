from pathlib import Path
from pybiocfilecache import BiocFileCache
import time 
from requests import get, Response, HTTPError

def makeCache(filepath):
    path = Path(filepath)
    if not path.exists():
        raise ValueError("Invalid filepath")
    else:
        cache = BiocFileCache(filepath)
        return cache 



def tryDownload(link: str) -> Response:
    req = get(link)
    status = req.status_code
    sleep_time = 0
    while status != 200:
        if sleep_time >= 60:
            raise HTTPError("Unable to connect to Zenodo")
        sleep_time += 15
        time.sleep(15)
        req = get(link)
        status = req.status_code
    return req

def tryGetRecord(conceptDOI: str) -> Response:
    cdoi = f"conceptdoi:{conceptDOI}"
    req = get(url="https://zenodo.org/api/records",
                                     params={
                                         "q": cdoi,
                                         "size": 25,
                                         "sort": "mostrecent"
                                     })
    status = req.status_code
    sleep_time = 0
    while status != 200:
        if sleep_time >= 60:
            raise HTTPError("Unable to connect to Zenodo")
        sleep_time += 15
        time.sleep(15)
        req = get(url="https://zenodo.org/api/records",
                                     params={
                                         "q": cdoi,
                                         "size": 25,
                                         "sort": "mostrecent"
                                     })
        status = req.status_code
    return req