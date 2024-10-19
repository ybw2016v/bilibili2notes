#!python

import requests as r

from bynamic import bynamic

URL = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
ua = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36"
dm_img_list = "[]"
dm_img_str = "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ=="
dm_cover_img_str = "QU5HTEUgKEdvb2dsZSwgVnVsa2FuIDEuMy4wIChTd2lmdFNoYWRlciBEZXZpY2UgKFN1Ynplcm8pICgweDAwMDBDMERFKSksIFN3aWZ0U2hhZGVyIGRyaXZlcik="

def getdynamic(uid, cookie):
    """
    获取用户动态
    """
    info = []
    print(uid)
    pm = { "host_mid": str(uid), "dm_img_list": dm_img_list, "dm_img_str": dm_img_str, "dm_cover_img_str": dm_cover_img_str }
    
    headers = {
        "User-Agent": ua,
        "Cookie": cookie,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    
    try:
        res = r.get(URL, params = pm, headers = headers)
        res.raise_for_status()
        res_text = res.json()
    except (r.exceptions.HTTPError, ValueError) as e:
        print(f"Req Failed: {e}")
        return info

    for index, itemdog in enumerate(res_text.get("data", {}).get("items", [])):
        if itemdog is None:
            print("Card's value is null, break")
            break
        rrr = bynamic(index, itemdog)
        if rrr is not None:
            info.append(rrr)
    
    return info

def getdynamic_wbi(uid, bubi):
    """
    使用wbi签名在未登录情况下获取用户动态
    """
    info = []
    print(uid)
    pm = { "host_mid": str(uid), "dm_img_list": dm_img_list, "dm_img_str": dm_img_str, "dm_cover_img_str": dm_cover_img_str }
    pms,jar = bubi.ubisign(pm)
    headers = {
        "User-Agent": ua,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    
    try:
        res = r.get(URL, params=pms, headers=headers,cookies=jar)
        res.raise_for_status()
        res_text = res.json()
    except (r.exceptions.HTTPError, ValueError) as e:
        print(f"Req Failed: {e}")
        return info

    for index, itemdog in enumerate(res_text.get("data", {}).get("items", [])):
        if itemdog is None:
            print("Card's value is null, break")
            break
        rrr = bynamic(index, itemdog)
        if rrr is not None:
            info.append(rrr)
    
    return info

