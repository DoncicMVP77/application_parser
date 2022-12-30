import json
import random

from base_parser import BaseParser
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPProxyAuth
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup as BS


class LeroyMerlinParser(BaseParser):

    def __init__(self):
        self.url_category_shop_api = "https://api.leroymerlin.ru/experience/orchestrator/v1/mainpage-mf/getCatalogue" \
                                     "?region=34"
        self.session = requests.Session()
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://leroymerlin.ru",
            "Referer": "https://leroymerlin.ru/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/108.0.0.0 Safari/537.36",
            "sec-ch-ua": '^\^"Not?A_Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"108^\^", ^\^"Google '
                         'Chrome^\^";v=^\^"108^\^"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '^\^"Windows^\^"',
            "x-api-key": 'vaKo7u1tlx3rm1G7YwKMS58CozHIIvgq',
            "x-request-id": ""
        }

    def get_category_shop_response(self):
        proxies = {"https": 'http://wYZG4s:GbxfGs@45.10.248.101:8000'}

        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        with self.session:

            response_category_shop_api = self.session.get('https://stackoverflow.com/questions/40442568/python-requests-http-response-500-site-can-be-reached-in-browser',
                                                          headers=self.headers,
                                                          proxies=proxies)
            return response_category_shop_api.status_code

    def get_category_products_list_response(self):
        pass

    def get_shop_information_response(self):
        pass

    def get_city_shop_response(self):
        pass

    def parse_category_shop_response(self, data):
        pass

    def parse_city_shop_response(self, data):
        pass

    def get_dict_with_category_shop(self) -> dict:
        pass

    def get_random_proxy(self):
        return random.choice([
            'https://wYZG4s:GbxfGs@y45.10.248.101:8000',
            'https://wYZG4s:GbxfGs@y45.10.251.193:8000',
            'https://wYZG4s:GbxfGs@y45.10.249.223:8000',
            'https://wYZG4s:GbxfGs@y45.10.250.15:8000',
        ])

def main():
    leroymarlin_parser = LeroyMerlinParser()
    print(leroymarlin_parser.get_category_shop_response())

if __name__ == '__main__':
    main()
