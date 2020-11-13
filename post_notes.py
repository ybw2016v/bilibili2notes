import requests
import json
import time

def post_dog(dog_p,dog_c,dog_f):
    url=dog_p.PostUrl
    key=dog_p.ApiKey
    payload={'text':dog_c,"localOnly":False,"visibility":"public","viaMobile":False,"i":key}
    res=requests.post(url,json=payload)
    return res.text

def dog_img_id(url):
    pic_dog=requests.get(url)
    data={'i':'OZoL7E89P9PB72Mh','force':'true'}
    now_doge = time.gmtime()
    now_doge_w = int(time.mktime(now_doge))
    name_dog='upload_{}.jpg'.format(now_doge_w)
    files={'file': (name_dog,pic_dog.content, 'image/png')}
    sdo=requests.post('https://m.dogcraft.top/api/drive/files/create',data=data,files=files)
    return sdo
