#!python

import re

adi = re.compile('\n(\n)?')  # 匹配多个br标签超过两个就继续换行

dog_img = re.compile('<img src="(.*?)"')
aid_dog = re.compile('https://www.bilibili.com/video/')
dog_rm_band = re.compile('<.*>')
dog_re_title = re.compile('\n')
dog_re_j = re.compile('#(.*?)#')


def add_jing(matched):
    print(matched)
    dog_str = matched.group()
    dog_str = str(dog_str)
    # intValue[:-1]=' '
    dog_str = dog_str[:-1]+' '
    return dog_str


def core_dog(dog_cont):
    dog_url = []
    dog_neirong = dog_cont['c']
    # 去除<br>
    dog_neirong2 = adi.sub('\n', dog_neirong)
    # dog_img1 = dog_img.findall(dog_neirong)
    # print(dog_img1)
    # 提取视频aid(如果有)
    # dog_aid = aid_dog.findall(dog_neirong)
    # dog_title = dog_re_title.sub(' ', dog_cont['title'])
    # if len(dog_title) >= 30:
    #     dog_title_r = dog_title[0:30]+"..."
    # else:
    #     dog_title_r = dog_title
    # if dog_aid != []:
    #     dog_url.append('https://www.bilibili.com/video/av'+dog_aid[0]+'/')
    # dog_url.append(dog_cont['link'])
    dog_neirong3 = dog_rm_band.sub('', dog_neirong2)
    dog_neirong4 = dog_re_j.sub(add_jing, dog_neirong3)
    dog_neirong5 = aid_dog.sub('https://api.neko.red/b/',dog_neirong4)
    # dog_title_r2 = dog_re_j.sub(add_jing, dog_title_r)
    dog_url_str = ''
    for item in dog_cont['url']:
        dog_url_str = dog_url_str+'\n'+item
    dog_res_str = dog_neirong5+'\n'+dog_url_str
    dog_res_str2 = adi.sub('\n', dog_res_str)

    return [dog_res_str2, dog_cont['pic']]
