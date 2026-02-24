import requests 

response = requests.get(url="https://zenodo.org/api/records",
                        params={
                            "q": "conceptdoi:10.5281/zenodo.17428997",
                            "size": 25,
                            "sort": "mostrecent"}
                        )
data = response.json()
print(data)
