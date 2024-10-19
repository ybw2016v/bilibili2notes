#!/usr/bin/env python3

import time
from functools import reduce
from hashlib import md5
import hmac
import hashlib
import json
import urllib.parse
import requests as r


# import requests


def hmac_sha256(key, message):
    """
    使用HMAC-SHA256算法对给定的消息进行加密
    :param key: 密钥
    :param message: 要加密的消息
    :return: 加密后的哈希值
    """
    # 将密钥和消息转换为字节串
    key = key.encode("utf-8")
    message = message.encode("utf-8")

    # 创建HMAC对象，使用SHA256哈希算法
    hmac_obj = hmac.new(key, message, hashlib.sha256)

    # 计算哈希值
    hash_value = hmac_obj.digest()

    # 将哈希值转换为十六进制字符串
    hash_hex = hash_value.hex()

    return hash_hex


mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


def getMixinKey(orig: str):
    "对 imgKey 和 subKey 进行字符顺序打乱编码"
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]


def encWbi(params: dict, img_key: str, sub_key: str):
    "为请求参数进行 wbi 签名"
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params["wts"] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params["w_rid"] = wbi_sign
    return params


URL1 = "https://www.bilibili.com/"
URL2 = "https://api.bilibili.com/x/frontend/finger/spi"
URL4 = "https://api.bilibili.com/bapis/bilibili.api.ticket.v1.Ticket/GenWebTicket"

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36"

# URL3='https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space'


class Bubi(object):
    img_key = None
    sub_key = None

    def __init__(self):
        self.jar = r.cookies.RequestsCookieJar()
        ck = self.getcookfromfile()
        if "buvid4" not in ck or "buvid3" not in ck:
            ck = self.getcookfromweb()
        # ck = self.getcookfromweb()
        self.jar.set("buvid4", ck["buvid4"])
        self.jar.set("buvid3", ck["buvid3"])
        self.getubikey()

    def getcookfromfile(self):
        """
        从文件中获取buvid2 buvid4
        """
        with open("key.json", "r", encoding="utf-8") as f:
            cookies = json.loads(f.read())
        return cookies

    def getcookfromweb(self):
        """
        从网页获取buvid2 buvid4
        """
        hd = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
        r1 = r.get(URL1, headers=hd)
        self.jar = r1.cookies
        r2 = r.get(URL2, headers=hd, cookies=self.jar)
        ppu = r2.json()["data"]["b_4"]
        self.jar.set("buvid4", ppu)
        buvid4 = self.jar.get("buvid4")
        with open("key.json", "w") as f:
            f.write(json.dumps({"buvid3": self.jar.get("buvid3"), "buvid4": buvid4}))
        return {"buvid4": buvid4, "buvid3": self.jar.get("buvid3")}

    def getubikey(self):
        """
        获取密钥
        """
        o = hmac_sha256("XgwSnGZ1p",f"ts{int(time.time())}")
        # url = "https://api.bilibili.com/bapis/bilibili.api.ticket.v1.Ticket/GenWebTicket"
        lparams = {
            "key_id":"ec02",
            "hexsign":o,
            "context[ts]":f"{int(time.time())}",
            "csrf": ''
        }
        hd = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
        ress = r.post(URL4, params=lparams, headers=hd, cookies=self.jar)
        resjson = ress.json()
        # print(resjson)
        tk = ress.json()["data"]["ticket"]
        exptime = resjson["data"]["ttl"] + resjson["data"]["created_at"]
        img_url = resjson["data"]["nav"]["img"]
        sub_url = resjson["data"]["nav"]["sub"]
        self.img_key = img_url.rsplit("/", 1)[1].split(".")[0]
        self.sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
        self.jar.set("bili_ticket", tk)
        self.jar.set("bili_ticket_expires", str(exptime))

    def ubisign(self, pma):
        """
        签名
        """
        sig_pm = encWbi(pma, self.img_key, self.sub_key)
        return sig_pm, self.jar
