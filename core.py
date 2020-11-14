#!python

import re

adi=re.compile('<br>(<br>)?')#匹配多个br标签超过两个就继续换行
dog_img=re.compile('<img src="(.*?)"')
aid_dog=re.compile('aid=([0-9]*)')
dog_rm_band=re.compile('<.*>')
dog_re_title=re.compile('\n')

def core_dog(dog_cont):
    dog_url=[]
    dog_neirong=dog_cont['description']
    # 去除<br>
    dog_neirong2= adi.sub('\n',dog_neirong)
    dog_img1=dog_img.findall(dog_neirong)
    # print(dog_img1)
    # 提取视频aid(如果有)
    dog_aid=aid_dog.findall(dog_neirong)
    dog_title=dog_re_title.sub(' ',dog_cont['title'])
    if len(dog_title)>=30:
        dog_title_r=dog_title[0:30]+"..."
    else:
        dog_title_r=dog_title
    if dog_aid!=[]:
        dog_url.append('https://www.bilibili.com/video/av'+dog_aid[0]+'/')
    dog_url.append(dog_cont['link'])
    dog_neirong3=dog_rm_band.sub('',dog_neirong2)
    dog_url_str=''
    for item in dog_url:
        dog_url_str=dog_url_str+'\n'+item
    dog_res_str='【'+dog_title_r+'】\n'+dog_neirong3+dog_url_str
    
    return [dog_res_str,dog_img1]
    pass