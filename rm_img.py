import requests as r

def dog_img_rm(url,key,picid):
    """
    删除指定id的图片
    """
    dog_rmpic_json={"i":key,"fileId":picid}
    dog_res=r.post(url,json=dog_rmpic_json)
    # print(dog_res.text)
    return dog_res.text