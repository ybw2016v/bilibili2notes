from core import core_dog
from xml_dog import dog_p
from get_dog_info import get_dog
from par_dog_conf import Pardogconf
from post_notes import post_dog
import time
import os




timef=open('./last','r')
dogtime=int(timef.read())
timef.close()

dog_conf_files=os.listdir('conf')

for conf_file in dog_conf_files:
    conf_file_path=os.path.join('conf',conf_file)
    dogconf=Pardogconf(conf_file_path)
    # print(dogconf.DogName)
    dogxml=get_dog(dogconf.SouUrl)
    doglist=dog_p(dogxml)
    for doge in doglist:
        if int(doge['pubDate'])>dogtime:
            post_dog(dogconf,(str(dogconf.Pex)+core_dog(doge)+str(dogconf.Afr)))
            # print('好像是还没有发布过:'+str(doge['pubDate']))
        else:
            # print('好像是已经发布过了:'+str(doge['pubDate']))
            pass




# ssa=post_dog(dogconf,"测试\n由python发送")
# print(ssa)





timef=open('last','w')
now_dog=time.gmtime()
now_dog_w=int(time.mktime(now_dog))
timef.write(str(now_dog_w))
timef.close()
os.system("date > run.log")