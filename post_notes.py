import json
import time
import requests


def new_post_dog(dog_p, dog_c, dog_img_list):
    pic_url = dog_p.PostUrl + 'api/drive/files/create'
    key = dog_p.ApiKey
    pic_dog_list = []
    dog_name_value = dog_p.DogName

    for dog_pic in dog_img_list[:16]:
        print(dog_pic)
        dog_img_id_l = dog_img_id(dog_pic, pic_url, key)
        pic_dog_list.append(dog_img_id_l)

    if not pic_dog_list:
        print('没有图片，纯文本内容')
    else:
        print('有图片，已经上传完毕')
        pic_log_path = f'./db_{dog_name_value}.json'
        try:
            with open(pic_log_path, 'r') as pic_log_file:
                pic_log_json = json.load(pic_log_file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: ", FileNotFoundError)
            pic_log_json = {}
        
        if dog_name_value not in pic_log_json:
            pic_log_json[dog_name_value] = {}

        now_doge = time.gmtime()
        now_doge_w = int(time.mktime(now_doge))
        pic_log_json[dog_name_value][now_doge_w] = pic_dog_list

        with open(pic_log_path, 'w') as pic_log_file:
            json.dump(pic_log_json, pic_log_file)
        print('记录完毕')

    post_dog(dog_p, dog_c, pic_dog_list)


def post_dog(dog_p, dog_c, dog_f):
    url = dog_p.PostUrl + 'api/notes/create'
    key = dog_p.ApiKey
    payload = {
        'text': dog_c,
        "localOnly": False,
        "visibility": "public",
        "viaMobile": False,
        "i": key
    }

    if dog_f:
        payload['fileIds'] = dog_f

    res = requests.post(url, json=payload)
    return res.text


def dog_img_id(url, purl, key):
    pic_dog = requests.get(url)
    data = {'i': key, 'force': 'true'}
    now_doge = time.gmtime()
    now_doge_w = int(time.mktime(now_doge))
    name_dog = 'upload_{}.jpg'.format(now_doge_w)

    files = {'file': (name_dog, pic_dog.content, 'image/png')}
    print(f'upload {now_doge_w} starting')

    try:
        sdo = requests.post(purl, data = data, files = files, timeout = 20)
        sdo.raise_for_status()
        print(f'upload {now_doge_w} finished')
    except requests.RequestException as e:
        print(f"Error uploading image: {e}")
        print(name_dog, pic_dog)
        print(sdo.content)
        return None

    return sdo.json()['id']
