import json

def bpic(picture):
    """
    解析b站API返回图片
    """
    res=[]
    for item in picture:
        res.append(item["img_src"])
    return res

def bcard(type,card):
    """
    解析b站API返回卡片数据
    """
    url=[]
    pic=[]
    if type==1:
        # 转发动态卡片
        raw=json.loads(card)
        rtype=raw["item"]["orig_type"]

        text=raw["item"]["content"]
        orange_text=raw["origin"]
        subres=bcard(rtype,orange_text)
        c=text+"RN:\n"+subres["c"]
        url.extend(subres["url"])
        pic.extend(subres["pic"])
        return {"c":c,"url":url,"pic":pic}
    if type==2:
        # 相册投稿
        raw=json.loads(card)
        text=raw["item"]["description"]
        for pitem in raw["item"]["pictures"]:
            pic.append(pitem["img_src"])
        return {"c":text,"url":url,"pic":pic}
    if type==4:
        # 文字动态
        raw=json.loads(card)
        text=raw["item"]["content"]
        return {"c":text,"url":url,"pic":pic}
    if type==8:
        # 视频动态
        raw=json.loads(card)
        avh=raw["aid"]
        url.append("视频地址: https://api.neko.red/b/av"+str(avh))
        text="【{}】\n{}".format(raw["title"],raw["dynamic"])
        pic.append(raw["pic"])
        return {"c":text,"url":url,"pic":pic}
    if type==64:
        # 专栏动态
        raw=json.loads(card)
        aid=raw["id"]
        text="【{}】\n{}".format(raw["title"],raw['summary'])
        url.append("专栏地址: https://www.bilibili.com/read/cv"+str(aid))
        for pitem in raw["image_urls"]:
            pic.append(pitem)
        return {"c":text,"url":url,"pic":pic}
    if type==256:
        # 音频动态
        raw=json.loads(card)
        auid=raw["id"]
        text="【{}】\n{}".format(raw["title"],raw["intro"])
        url.append("音频地址: https://www.bilibili.com/audio/au"+str(auid))
        pic.append(raw["cover"])
        return {"c":text,"url":url,"pic":pic}

    else:
        raw=json.loads(card)
        print(raw)
        return {"c":"未知类型{}\n需要处理 @dogcraft@m.dogcraft.top".format(type),"url":[],"pic":[]}

    


def bynamic(bdata):
    """
    解析b站动态数据API
    """
    btype=bdata["desc"]["type"]
    pubtime=bdata["desc"]["timestamp"]
    res=bcard(btype,bdata["card"])
    dyid=bdata["desc"]["dynamic_id_str"]
    res["url"].append("https://t.bilibili.com/"+dyid)
    if "orig_dy_id_str" in bdata["desc"]:
        if bdata["desc"]["orig_dy_id_str"]!="0":
            res["url"].append("https://t.bilibili.com/"+bdata["desc"]["orig_dy_id_str"])
    res["time"]=pubtime

    return res
