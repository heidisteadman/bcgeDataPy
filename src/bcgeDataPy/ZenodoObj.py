from pathlib import Path
import zipfile
import io
from .helpers import tryDownload, tryGetRecord
from .SEPy import SummarizedExperimentPy

class ZenObj:
    def __init__(self, conceptdoi):
        self.conceptdoi = conceptdoi 
        self.jsonresp = tryGetRecord(conceptdoi)
        self.json = self.jsonresp.json()
    
    def parse_json(self) -> str:
        hits = self.json['hits']['hits'][0]
        doi_id = hits['id']
        download_link = f"https://zenodo.org/api/records/{doi_id}/files-archive"
        return download_link 
    
    def get_versions(self, v:int) -> str:
        hits = self.json['hits']['hits'][0]
        links = hits['links']
        versions = links['versions']
        versresp = tryDownload(versions)
        versjson = versresp.json() 
        verhits = versjson['hits']['hits']

        if ((len(verhits)-v-1)>=0):
            vers = verhits[(len(verhits)-v-1)]
            verid = vers['id']
            download_link = f"https://zenodo.org/api/records/{verid}/files-archive"
            return download_link 
        else:
            return self.parse_json()
    
    def download_file(self, link: str, path: Path) -> None:
        downloaded_file = tryDownload(link)
        path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(downloaded_file.content)) as z:
            for filename in z.infolist():
                with z.open(filename) as zf:
                    (path / filename.filename).write_bytes(zf.read())
        return 
    
    def most_recent(self) -> int:
        hits = self.json['hits']['hits'][0]
        version = hits['metadata']['relations']['version']
        index = version[0]['index']
        return (int(index)+1)
    
    def chooseVersion(self, path: Path, v:int, datasetID: str) -> SummarizedExperimentPy:
        expData = path / f"{datasetID}.tsv.gz"
        metadata = path / f"{datasetID}_metadata.tsv"
        if not expData.exists():
            print("Either the data was not found in the cache or a new version was requested. Downloading now.")
            link = self.get_versions(v)
            self.download_file(link, path)
        

        return SummarizedExperimentPy(expData, metadata)