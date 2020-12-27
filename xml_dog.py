#!python3
import time
import xml.etree.ElementTree as ET


def dog_cov_time(dog_time_str):
    dog_time_array = time.strptime(dog_time_str, '%a, %d %b %Y %H:%M:%S GMT')
    dog_time_chuo = int(time.mktime(dog_time_array))
    return dog_time_chuo


def dog_p(dog_xml_str):
    dog_res = []
    dog_doc = ET.fromstring(dog_xml_str)
    dog_cd = dog_doc.find('channel')
    dog_items = dog_cd.findall('item')
    for dog_item in dog_items:
        dog_item_title = dog_item.findtext('title')
        dog_item_description = dog_item.findtext('description')
        dog_item_pubDate = dog_cov_time(dog_item.findtext('pubDate'))
        dog_item_guid = dog_item.findtext('guid')
        dog_item_link = dog_item.findtext('link')
        dog_item_res = {'title': dog_item_title, 'description': dog_item_description,
                        'pubDate': dog_item_pubDate, 'guid': dog_item_guid, 'link': dog_item_link}
        dog_res.append(dog_item_res)
    return dog_res
