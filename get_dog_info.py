#!python3

import requests

# uid="https://rsshub.app/bilibili/user/dynamic/228832527"


def get_dog(url_dog):
    res_dog=requests.get(url_dog)
    xml_dog=res_dog.text
    return xml_dog
# su=get_dog(uid)

# f=open('dog.xml','a')

# f.write(su)

# f.close()

