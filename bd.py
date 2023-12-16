#!python

import requests as r

from bynamic import bynamic

URL="https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
ua="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36"

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
        if rrr is not None:
            info.append(rrr)
    return info


