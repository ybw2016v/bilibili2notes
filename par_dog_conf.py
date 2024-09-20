#!python3
import configparser


class Pardogconf(object):
    ApiKey = ''
    PostUrl = ''
    Uid = ''
    Pex = ''
    Afr = ''
    DogName = ''
    Extime = ''
    Cookie = ''

    def __init__(self, ini_dog_file):
        conf_dog = configparser.ConfigParser(interpolation = None)
        conf_dog.read(ini_dog_file, encoding="utf-8")
        self.DogName = conf_dog.sections()[0]
        conf_dog_items = conf_dog[self.DogName]
        self.ApiKey = conf_dog_items.get('ApiKey')
        self.PostUrl = conf_dog_items.get('PostUrl')
        self.Uid = conf_dog_items.get('Uid')
        self.Pex = conf_dog_items.get('Pex')
        self.Afr = conf_dog_items.get('Afr')
        self.Extime = conf_dog_items.get('Extime')
        self.Cookie = conf_dog_items.get('Cookie')
    pass
