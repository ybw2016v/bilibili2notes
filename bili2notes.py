import json
import os
import time

from core import core_dog
from par_dog_conf import Pardogconf
from post_notes import *
from rm_img import rm_exp_pic
from bd import getdynamic

timef = open('./last', 'r')
dogtime = int(timef.read())
timef.close()

time_dog_file = open('./last.json', 'r')
time_dog_json = time_dog_file.read()
time_dog_file.close()
time_dog = json.loads(time_dog_json)

pic_time_dog_file = open('./db.json', 'r')
pic_time_dog_json = pic_time_dog_file.read()
pic_time_dog_file.close()
pic_time_dog = json.loads(pic_time_dog_json)
dog_conf_files = os.listdir('conf')

for conf_file in dog_conf_files:
    conf_file_path = os.path.join('conf', conf_file)
    dogconf = Pardogconf(conf_file_path)
    if dogconf.DogName not in time_dog:
        time_dog[dogconf.DogName] = dogtime 
    if dogconf.DogName not in pic_time_dog:
        # 检查是否存在于时间记录文件中
        pic_time_dog[dogconf.DogName] = {}
        pic_w = json.dumps(pic_time_dog)
        pic_time_dog_file = open('./db.json', 'w')
        pic_time_dog_json = pic_time_dog_file.write(pic_w)
        pic_time_dog_file.close()
    print(">>>{}\nExtime:{}".format(dogconf.DogName,dogconf.Extime))
    if int(dogconf.Extime) > 0:
        print('checking……')
        rm_exp_pic(dogconf)
        pass
    last_dog_time = time_dog[dogconf.DogName]
    doglist=getdynamic(dogconf.Uid)
    for doge in doglist[::-1]:
        if int(doge['time']) > last_dog_time:
            text,pic=core_dog(doge)
            new_post_dog(dogconf, (str(dogconf.Pex)+text+str(dogconf.Afr)), pic)
            print('好像是还没有发布过:'+str(doge['time']))
        else:
            print('好像是已经发布过了:'+str(doge['time']))
            pass
        time_dog[dogconf.DogName] = int(doge['time'])+1
        jr = open('last.json', 'w')
        jr.write(json.dumps(time_dog))
        jr.close()

timef = open('last', 'w')
now_dog = time.gmtime()
now_dog_w = int(time.mktime(now_dog))
timef.write(str(now_dog_w))
timef.close()

jr = open('last.json', 'w')
jr.write(json.dumps(time_dog))
jr.close()

os.system("date > run.log")
