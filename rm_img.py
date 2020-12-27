import json
import time

import requests as r


def rm_exp_pic(dog_p):
    dog_rm_url = dog_p.PostUrl+'api/drive/files/delete'
    dog_rm_time = dog_p.Extime
    pic_log_file = open('./db.json', 'r')
    pic_log_str = pic_log_file.read()
    pic_log_file.close()
    pic_log_json = json.loads(pic_log_str)
    now_doge = time.gmtime()
    now_doge_w = int(time.mktime(now_doge))
    del_list = []
    for dog_pic_item in pic_log_json[dog_p.DogName]:
        print('{} : {} '.format(dog_pic_item,
                                pic_log_json[dog_p.DogName][dog_pic_item]))

        if now_doge_w-int(dog_pic_item) > int(dog_rm_time):
            print('应该删除{}'.format(pic_log_json[dog_p.DogName][dog_pic_item]))
            pic_id_list = pic_log_json[dog_p.DogName][dog_pic_item]
            for dog_id in pic_id_list:
                dog_rd = dog_img_rm(
                    dog_p.PostUrl+'api/drive/files/delete', dog_p.ApiKey, dog_id)
                print(dog_rd)
                # input()
                pass
            del_list.append(dog_pic_item)
            # pic_log_json[dog_p.DogName].pop(dog_pic_item)
        pass
    for del_item in del_list:
        pic_log_json[dog_p.DogName].pop(del_item)
    print(del_list)
    pic_log_str = json.dumps(pic_log_json)
    pic_log_file = open('./db.json', 'w')
    pic_log_file.write(pic_log_str)
    pic_log_file.close()
    pass


def dog_img_rm(url, key, picid):
    """
    删除指定id的图片
    """
    print(url)
    dog_rmpic_json = {"i": key, "fileId": picid}
    dog_res = r.post(url, json=dog_rmpic_json)
    # print(dog_res.text)
    return dog_res.text
