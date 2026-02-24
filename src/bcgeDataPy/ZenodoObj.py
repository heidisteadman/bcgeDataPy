import requests

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