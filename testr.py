#!/usr/bin/env python3
import requests as r
import hmac
import hashlib
# import requests
import time
from functools import reduce
from hashlib import md5
import urllib.parse

# import time
# import requests
def hmac_sha256(key, message):
    """
    使用HMAC-SHA256算法对给定的消息进行加密
    :param key: 密钥
    :param message: 要加密的消息
    :return: 加密后的哈希值
    """
    # 将密钥和消息转换为字节串
    key = key.encode('utf-8')
    message = message.encode('utf-8')

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
    '对 imgKey 和 subKey 进行字符顺序打乱编码'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    '为请求参数进行 wbi 签名'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time                                   # 添加 wts 字段
    params = dict(sorted(params.items()))                       # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k : ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v 
        in params.items()
    }
    query = urllib.parse.urlencode(params)                      # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params



ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
hd={'User-Agent':ua,
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}

url1='https://www.bilibili.com/'

url2="https://api.bilibili.com/x/frontend/finger/spi"

url3='https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space'

pma={
    "host_mid": ,
    "dm_img_list": "[]",
    "dm_img_str": "V2ViR0wgMS4wIChQ",
    "dm_cover_img_str": "QU5HTEUgKE5WSURJQSBDb3Jwb3JhdGlvbiwgTlZJRElBIEdlRm9yY2UgR1RYIDk1ME0vUENJZS9TU0UyLCBPcGVuR0wgNC49vZ2xlIEluYy4gKE5WSURJQSBDb3Jwb3JhdGlvbi9"
    }



r1=r.get(url1,headers=hd)
print(r1.cookies)
jar=r1.cookies

r2=r.get(url2,headers=hd,cookies=jar)
print(r2.json())
ppu=r2.json()['data']['b_4']
jar.set('buvid4', ppu)

o = hmac_sha256("XgwSnGZ1p",f"ts{int(time.time())}")
url4 = "https://api.bilibili.com/bapis/bilibili.api.ticket.v1.Ticket/GenWebTicket"
lparams = {
    "key_id":"ec02",
    "hexsign":o,
    "context[ts]":f"{int(time.time())}",
    "csrf": ''
}
ress = r.post(url4, params=lparams,headers=hd,cookies=jar)
    # print(indexrequest.cookies)
resjson=ress.json()
print(resjson)
tk=ress.json()['data']['ticket']
exptime=resjson['data']['ttl']+resjson['data']['created_at']
img_url=resjson['data']['nav']['img']
sub_url=resjson['data']['nav']['sub']
img_key = img_url.rsplit('/', 1)[1].split('.')[0]
sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]

sig_pm=encWbi(pma,img_key,sub_key)

jar.set('bili_ticket',tk)
jar.set('bili_ticket_expires',str(exptime))

for cookie in jar:
    print(f"{cookie.name}={cookie.value}")
r3=r.get(url3,params=sig_pm,headers={'User-Agent':ua,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'},cookies=jar)
print(r3.url)
# print(r3.json())