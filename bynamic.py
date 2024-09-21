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
    if type == "DYNAMIC_TYPE_FORWARD":
        # 转发动态卡片
        raw=json.loads(card)
        rtype=raw["item"]["orig_type"]
        text=raw["item"]["content"]
        orange_text = raw.get("origin")

        if orange_text is not None:
            subres = bcard(rtype, orange_text)
            if subres is not None:
                c = text + "RN:\n" + subres.get("c", "Nothing")
                url.extend(subres.get("url", []))
                pic.extend(subres.get("pic", []))
            else:
                c = text + "RN:\n(转发内容不支持解析)"
        else:
            c = text + "RN:\n(原始内容为空或不支持解析)"

        print("1")

        return {"c":c,"url":url,"pic":pic}
    if type == "DYNAMIC_TYPE_DRAW":
        # 相册投稿
        raw=json.loads(card)
        text=raw["item"]["description"]
        for pitem in raw["item"]["pictures"]:
            pic.append(pitem["img_src"])
        print("2")
        return {"c":text,"url":url,"pic":pic}
    if type == "DYNAMIC_TYPE_WORD":
        # 文字动态
        raw=json.loads(card)
        text=raw["item"]["content"]
        print("4")
        return {"c":text,"url":url,"pic":pic}
    if type == "DYNAMIC_TYPE_AV11":
        # 视频动态
        raw=json.loads(card)
        avh=raw["aid"]
        url.append("视频地址: https://www.bilibili.com/video/av"+str(avh))
        text="【{}】\n{}".format(raw["title"],raw["dynamic"])
        pic.append(raw["pic"])
        print("8")
        return {"c":text,"url":url,"pic":pic}
    if type == "DYNAMIC_TYPE_ARTICLE":
        # 专栏动态
        raw=json.loads(card)
        aid=raw["id"]
        text="【{}】\n{}".format(raw["title"],raw['summary'])
        url.append("专栏地址: https://www.bilibili.com/read/cv"+str(aid))
        for pitem in raw["image_urls"]:
            pic.append(pitem)
        print("64")
        return {"c":text,"url":url,"pic":pic}
    if type == "DYNAMIC_TYPE_MUSIC":
        # 音频动态
        raw=json.loads(card)
        auid=raw["id"]
        text="【{}】\n{}".format(raw["title"],raw["intro"])
        url.append("音频地址: https://www.bilibili.com/audio/au"+str(auid))
        pic.append(raw["cover"])
        print("256")
        return {"c":text,"url":url,"pic":pic}
    if "DYNAMIC_TYPE_LIVE" in type or type == "DYNAMIC_TYPE_NONE":
        # 直播动态
        # 应该忽略
        print("4308")
        return None

    else:
        raw=json.loads(card)
        print(raw)
        print("Unknown")
        return {"c":"未知类型{}\n请反馈至 https://github.com/ybw2016v/bilibili2notes/issues".format(type),"url":[],"pic":[]}

    


def bynamic(bdata):
    """
    解析b站动态数据API
    """
    if "module_tag" in bdata.get("modules", {}) or not bdata["modules"]["visible"]:
        btype=bdata["type"]
        pubtime=bdata["modules"]["module_author"]["pub_ts"]
        res=bcard(btype,bdata["modules"]["module_dynamic"])
        if res is None:
            return None
        dyid=bdata["id_str"]
        res["url"].append("https://t.bilibili.com/"+dyid)
        if "id_str" in bdata.get("orig", {}):
            if bdata["orig"]["id_str"]!="0":
                res["url"].append("https://t.bilibili.com/"+bdata["orig"]["id_str"])
        res["time"]=pubtime

        return res

    else:
        print("置顶或不可见")