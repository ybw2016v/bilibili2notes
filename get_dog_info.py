#!python3

import requests


def get_dog(url_dog):
    res_dog = requests.get(url_dog)
    xml_dog = res_dog.text
    return xml_dog
