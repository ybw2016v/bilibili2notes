import json
import time
import requests as r


def rm_exp_pic(dog_p):
    dog_rm_url = dog_p.PostUrl + 'api/drive/files/delete'
    dog_rm_time = dog_p.Extime
    pic_log_path = f'./db_{dog_p.DogName}.json'

    try:
        with open(pic_log_path, 'r') as pic_log_file:
            pic_log_json = json.load(pic_log_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f'日志文件 {pic_log_path} 不存在或为空，跳过删除操作')
        return

    now_doge = time.gmtime()
    now_doge_w = int(time.mktime(now_doge))
    del_list = []

    for dog_pic_item in pic_log_json:
        print(f'{dog_pic_item} : {pic_log_json[dog_pic_item]}')

        if now_doge_w - int(dog_pic_item) > int(dog_rm_time):
            print(f'应该删除 {pic_log_json[dog_pic_item]}')
            pic_id_list = pic_log_json[dog_pic_item]
            for dog_id in pic_id_list:
                dog_rd = dog_img_rm(dog_rm_url, dog_p.ApiKey, dog_id)
                print(dog_rd)
            del_list.append(dog_pic_item)

    for del_item in del_list:
        pic_log_json.pop(del_item)
    print(f'删除的记录: {del_list}')

    with open(pic_log_path, 'w') as pic_log_file:
        json.dump(pic_log_json, pic_log_file)


def dog_img_rm(url, key, picid):
    """
    删除指定id的图片
    """
    dog_rmpic_json = {"i": key, "fileId": picid}
    dog_res = r.post(url, json=dog_rmpic_json)
    return dog_res.text
