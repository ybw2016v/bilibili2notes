import requests
import json

def post_dog(dog_p,dog_c):
    url=dog_p.PostUrl
    key=dog_p.ApiKey
    payload={'text':dog_c,"localOnly":False,"visibility":"public","viaMobile":False,"i":key}
    res=requests.post(url,json=payload)
    return res.text