import requests
from pathlib import Path
import zipfile
import io

class ZenObj:
    def __init__(self, conceptdoi):
        self.conceptdoi = conceptdoi 
        cdoi = f"conceptdoi:{conceptdoi}"
        self.jsonresp = requests.get(url="https://zenodo.org/api/records",
                                     params={
                                         "q": cdoi,
                                         "size": 25,
                                         "sort": "mostrecent"
                                     })
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
        versresp = requests.get(url=versions)
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
        downloaded_file = requests.get(link)
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