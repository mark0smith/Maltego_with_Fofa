from __future__ import absolute_import

import codecs
import logging
from base64 import b64encode
from os import getenv

import favicon
import requests
from maltego_trx.entities import URL, Domain, Website
from maltego_trx.maltego import UIM_PARTIAL
from maltego_trx.transform import DiscoverableTransform

import mmh3

from .Fofa_Query_subdomains_with_Domain import FofaApiSearch

requests.urllib3.disable_warnings()



def get_icon_hash(url="https://fofa.so"):
    """计算网页favicon的hash值，如果出错返回False
    - 使用 favicon 库来获取网页favicon的URL
    - 计算hash值算法来自 https://github.com/Becivells/iconhash"""
    try:
        icons = favicon.get(url,verify=False)
        if len(icons) == 0:
            return False
        icon = icons[0]

        icon_content = requests.get(icon.url).content
        return mmh3.hash(codecs.lookup('base64').encode(icon_content)[0])
    except Exception as e:
        logging.exception(e)
        return False

class GetIconHashFromURL(DiscoverableTransform):
    """Look for URLs with given domain in https://fofa.so ."""

    @classmethod
    def create_entities(cls, request, response):
        url = request.Value
        try:
            result = get_icon_hash(url)
            if result:
                iconhash = response.addEntity("mark0smith.WebsiteIconHash")
                iconhash.setValue(result)
        except IOError:
            response.addUIMessage("发生了错误", messageType=UIM_PARTIAL)


if __name__ == "__main__":
    print(get_icon_hash())
