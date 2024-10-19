import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from core import core_dog
from par_dog_conf import Pardogconf
from post_notes import *
from rm_img import rm_exp_pic
from bd import getdynamic,getdynamic_wbi
from bubi import Bubi

bubi = Bubi()
def read_time_file(dog_name):
    try:
        with open(f'./last_{dog_name}', 'r') as timef:
            return int(timef.read())
    except FileNotFoundError:
        return int(time.mktime(time.gmtime()) - 86400)


def read_json_file(file_path, default_value):
    try:
        with open(file_path, 'r') as json_file:
            return json.loads(json_file.read())
    except (FileNotFoundError, json.JSONDecodeError):
        return default_value


def write_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json_file.write(json.dumps(data))


def process_dogconf(conf_file):
    conf_file_path = os.path.join('conf', conf_file)
    dogconf = Pardogconf(conf_file_path)

    dogtime = read_time_file(dogconf.DogName)
    time_dog = read_json_file(f'./last_{dogconf.DogName}.json', {})
    pic_time_dog = read_json_file(f'./db_{dogconf.DogName}.json', {})

    if dogconf.DogName not in time_dog:
        time_dog[dogconf.DogName] = dogtime
    if dogconf.DogName not in pic_time_dog:
        pic_time_dog[dogconf.DogName] = {}
        write_json_file(f'./db_{dogconf.DogName}.json', pic_time_dog)

    print(f">>> {dogconf.DogName}\nExtime: {dogconf.Extime}")
    if int(dogconf.Extime) > 0:
        print('Checking……')
        rm_exp_pic(dogconf)

    last_dog_time = int(time_dog[dogconf.DogName])
    new_max_time = last_dog_time

    if dogconf.Cookie:
        doglist = getdynamic(dogconf.Uid, dogconf.Cookie)
    else:
        doglist = getdynamic_wbi(dogconf.Uid,bubi)

    # for doge in doglist:
    #     if int(doge['time']) > last_dog_time or int(doge['time']) not in pic_time_dog[dogconf.DogName]:
    #         text, pic = core_dog(doge)
    #         new_post_dog(dogconf, f"{dogconf.Pex}{text}{dogconf.Afr}", pic)
    #         print(f'好像是还没有发布过: {doge["time"]}')
    #     else:
    #         print(f'好像是已经发布过了: {doge["time"]}')
    #     time_dog[dogconf.DogName] = int(doge['time']) + 1

    doge_times = []

    for doge in doglist:
        doge_time = int(doge['time'] - 28800)
        doge_times.append(doge_time)

        # print(doge_time, "+",last_dog_time, "+", int(time.mktime(time.gmtime())), "+", int(time.time()))
        # print(doge_time < last_dog_time)

        # Check if the doge time is already published
        if doge_time <= last_dog_time or doge_time in pic_time_dog[dogconf.DogName]:
            print(f'好像是已经发布过了: {doge["time"]}')
            continue  # Skip to the next iteration if already published

        # If not published, process the new doge
        elif doge_time > last_dog_time:
            text, pic = core_dog(doge)

            # Call new_post_dog only if the ID is not already stored
            new_post_dog(dogconf, f"{dogconf.Pex}{text}{dogconf.Afr}", pic)  # Get the ID
            print(f'好像是还没有发布过: {doge["time"]}')

    new_max_time = max(new_max_time, max(doge_times))
    # print(max(doge_times), "+", new_max_time)

    time_dog[dogconf.DogName] = new_max_time
    write_json_file(f'./last_{dogconf.DogName}.json', time_dog)

    now_dog = time.gmtime()
    now_dog_w = int(time.mktime(now_dog))
    with open(f'last_{dogconf.DogName}', 'w') as timef:
        timef.write(str(now_dog_w))

    with open(f'run_{dogconf.DogName}.log', 'w') as log_file:
        log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", now_dog))

    os.system(f"date > run_{dogconf.DogName}.log")


with ThreadPoolExecutor(max_workers = 3) as executor:
    for conf_file in os.listdir('conf'):
        executor.submit(partial(process_dogconf, conf_file))
        time.sleep(5)
