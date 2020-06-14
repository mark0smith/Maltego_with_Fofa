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


def FofaApiSearch(searchtype,value,api_field):
    """使用fofa的api进行搜索
    - searchtype 和 value 相当于在搜索框里面输入的内容，目前只支持单个搜素语句
    - api_field是对应的api里面的字段，参看 https://beta.fofa.so/static_pages/api_help """
    fofa_email = getenv("fofa_email")
    fofa_token = getenv("fofa_token")
    fofa_api_url = "https://beta.fofa.so/api/v1/search/all"

    query = f'{searchtype}="{value}"'
    qbase64_query = b64encode(query.encode())
    params = {
        "email":fofa_email,
        "key":fofa_token,
        "qbase64":qbase64_query,
        "full":True,
        "fields":f"{api_field}",
    }
    response = requests.get(fofa_api_url,params=params,timeout=10)
    return response.json()["results"]
    


class Fofa_Query_subdomains_with_Domain(DiscoverableTransform):
    """Lookup the domain name in https://fofa.so ."""

    @classmethod
    def create_entities(cls, request, response):
        domain = request.Value
        try:
            subdomains = cls.get_subdomains(domain)
            for subdomain in subdomains:
                response.addEntity(Domain, subdomain)
        except IOError:
            response.addUIMessage("发生了错误", messageType=UIM_PARTIAL)

    @staticmethod
    def get_subdomains(domain):
        domains = FofaApiSearch("domain",domain,"hosts")
        domains_list = []
        for domain in domains:
            if "://" in domain:
                domain = domain.split("://")[-1]
            if domain not in domains_list:
                domains_list.append(domain)
        return domains_list

class FofaURL(DiscoverableTransform):
    """Look for URLs with given domain in https://fofa.so ."""

    @classmethod
    def create_entities(cls, request, response):
        domain = request.Value
        try:
            subdomains = cls.get_urls(domain)
            for subdomain in subdomains:
                response.addEntity(URL, subdomain)
        except IOError:
            response.addUIMessage("发生了错误", messageType=UIM_PARTIAL)

    @staticmethod
    def get_urls(domain):
        domains = FofaApiSearch("domain",domain,"hosts")
        domains_list = []
        for domain in domains:
            if "://" not in domain:
                domain = "http://" + domain
            if domain not in domains_list:
                domains_list.append(domain)
        return domains_list


if __name__ == "__main__":
    print(Fofa_Query_URLs_with_Domain.get_subdomains("fofa.so"))
    