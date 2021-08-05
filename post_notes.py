import json
import time

import requests


def new_post_dog(dog_p, dog_c, dog_img_list):
    pic_url = dog_p.PostUrl+'api/drive/files/create'
    key = dog_p.ApiKey
    pic_dog_list = []
    for dog_pic in dog_img_list[:4]:
        print(dog_pic)
        dog_img_id_l = dog_img_id(dog_pic, pic_url, key)
        pic_dog_list.append(dog_img_id_l)
    if pic_dog_list == []:
        print('没有图片，纯文本内容')
    else:
        print('有图片，已经上传完毕')
        pic_log_file = open('./db.json', 'r')
        pic_log_str = pic_log_file.read()
        pic_log_file.close()
        pic_log_json = json.loads(pic_log_str)
        # pic_log_t=pic_log_json[dog_p.DogName]
        now_doge = time.gmtime()
        now_doge_w = int(time.mktime(now_doge))
        pic_log_json[dog_p.DogName][now_doge_w] = pic_dog_list
        pic_log_str = json.dumps(pic_log_json)
        pic_log_file = open('./db.json', 'w')
        pic_log_file.write(pic_log_str)
        pic_log_file.close()
        print('记录完毕')
        pass
    post_dog(dog_p, dog_c, pic_dog_list)
    pass


def post_dog(dog_p, dog_c, dog_f):
    url = dog_p.PostUrl+'api/notes/create'
    key = dog_p.ApiKey
    if dog_f==[]:
        payload = {'text': dog_c, "localOnly": False, "visibility": "public", "viaMobile": False, "i": key}
    else :
        payload = {'text': dog_c, "localOnly": False, "visibility": "public","fileIds": dog_f, "viaMobile": False, "i": key}
    res = requests.post(url, json=payload)
    return res.text



def dog_img_id(url, purl, key):
    pic_dog = requests.get(url)
    data = {'i': key, 'force': 'true'}
    now_doge = time.gmtime()
    now_doge_w = int(time.mktime(now_doge))
    name_dog = 'upload_{}.jpg'.format(now_doge_w)
    files = {'file': (name_dog, pic_dog.content, 'image/png')}
    print('upload {} starting'.format(now_doge_w))
    sdo = requests.post(purl, data=data, files=files)
    print('upload {} finished'.format(now_doge_w))
    return sdo.json()['id']
