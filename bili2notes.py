import json
import os
import time

from core import core_dog
from get_dog_info import get_dog
from par_dog_conf import Pardogconf
from post_notes import *
from xml_dog import dog_p

timef = open('./last', 'r')
dogtime = int(timef.read())
timef.close()

time_dog_file = open('./last.json', 'r')
time_dog_json = time_dog_file.read()
time_dog_file.close()
time_dog = json.loads(time_dog_json)


dog_conf_files = os.listdir('conf')

for conf_file in dog_conf_files:
    conf_file_path = os.path.join('conf', conf_file)
    dogconf = Pardogconf(conf_file_path)
    if dogconf.DogName in time_dog:
        print('存在')
    else:
        time_dog[dogconf.DogName] = dogtime
        print('不存在，被创建')
    print(dogconf.DogName)
    last_dog_time = time_dog[dogconf.DogName]
    dogxml = get_dog(dogconf.SouUrl)
    doglist = dog_p(dogxml)
    for doge in doglist[::-1]:
        if int(doge['pubDate']) > last_dog_time:
            new_post_dog(dogconf, (str(dogconf.Pex)+core_dog(doge)[0]+str(dogconf.Afr)),core_dog(doge)[1])
            print('好像是还没有发布过:'+str(doge['pubDate']))
        else:
            print('好像是已经发布过了:'+str(doge['pubDate']))
            pass
        # sk=input('ss')
        time_dog[dogconf.DogName] = int(doge['pubDate'])+1
        jr = open('last.json', 'w')
        jr.write(json.dumps(time_dog))
        jr.close()


# ssa=post_dog(dogconf,"测试\n由python发送")
# print(ssa)


timef = open('last', 'w')
now_dog = time.gmtime()
now_dog_w = int(time.mktime(now_dog))
timef.write(str(now_dog_w))
timef.close()

jr = open('last.json', 'w')
jr.write(json.dumps(time_dog))
jr.close()

os.system("date > run.log")
