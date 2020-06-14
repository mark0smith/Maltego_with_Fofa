from __future__ import absolute_import
from maltego_trx.entities import Domain,Website,URL
from maltego_trx.maltego import UIM_PARTIAL
from maltego_trx.transform import DiscoverableTransform

from os import getenv
from base64 import b64encode
import requests
import favicon
import mmh3
import codecs
requests.urllib3.disable_warnings()


from .Fofa_Query_subdomains_with_Domain import FofaApiSearch

class Fofa_Query_URLs_with_Domain(DiscoverableTransform):
    """Look for URLs with given domain in https://fofa.so ."""

    @classmethod
    def create_entities(cls, request, response):
        domain = request.Value
        try:
            results_list = cls.get_urls(domain)
            for info in results_list:
                url = response.addEntity(URL)
                url.addProperty("url",value=info[0])
                url.addProperty("short-title",value=info[1])
                url.addProperty("title",value=info[1])
        except IOError:
            response.addUIMessage("发生了错误", messageType=UIM_PARTIAL)

    @staticmethod
    def get_urls(domain):
        results = FofaApiSearch("domain",domain,"host,title")
        results_list = []
        for info in results:
            if "://" not in info[0]:
                info[0] = "http://" + info[0]
            if info[1] == "":
                info[1] = info[0]
                
            if info not in results_list:
                results_list.append(info)
        return results_list


if __name__ == "__main__":
    print(FofaURL.get_urls("fofa.so"))