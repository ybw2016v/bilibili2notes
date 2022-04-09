#!python

import requests as r

from bynamic import bynamic

URL="https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

def getdynamic(uid):
    """
    获取用户动态
    """
    info=[]
    print(uid)
    pm={"host_uid": str(uid), "offset_dynamic_id":0,"need_top":False}
    res=r.get(URL,params=pm,headers={"User-Agent":ua})
    res_text=res.json()

    for itemdog in res_text["data"]["cards"]:
        rrr=bynamic(itemdog)
        info.append(rrr)
    return info


