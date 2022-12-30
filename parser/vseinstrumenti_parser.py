import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from base_parser import BaseParser


class VseInstrumentiParser(BaseParser):

    def __init__(self):
        self.url_list_category_shop_api = [
            'https://bff.vseinstrumenti.ru/catalog/categories?id=32&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=13&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=20&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=19&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=26&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=14&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=25&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=16&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=30&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=28&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=21&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=18&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=15&activeRegionId=1',
            'https://bff.vseinstrumenti.ru/catalog/categories?id=22&activeRegionId=1',
        ]
        self.url_subcategory_shop_api = 'https://bff.vseinstrumenti.ru/catalog/child-categories?leftBorder={}&rightBorder={}&activeRegionId=1'
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": 'wucf=7; ab_exps=^%^7B^%^22237^%^22^%^3A6^%^2C^%^22243^%^22^%^3A13^%^2C^%^22245^%^22^%^3A1^%^2C^%^22248^%^22^%^3A2^%^2C^%^22249^%^22^%^3A0^%^2C^%^22260^%^22^%^3A2^%^2C^%^22262^%^22^%^3A2^%^2C^%^22280^%^22^%^3A2^%^2C^%^22362^%^22^%^3A0^%^2C^%^22368^%^22^%^3A1^%^2C^%^22374^%^22^%^3A2^%^2C^%^22380^%^22^%^3A1^%^2C^%^22408^%^22^%^3A2^%^2C^%^22415^%^22^%^3A2^%^2C^%^22438^%^22^%^3A0^%^2C^%^22462^%^22^%^3A0^%^2C^%^22468^%^22^%^3A1^%^2C^%^22474^%^22^%^3A1^%^2C^%^22486^%^22^%^3A11^%^2C^%^22492^%^22^%^3A5^%^2C^%^22505^%^22^%^3A2^%^2C^%^22517^%^22^%^3A1^%^2C^%^22523^%^22^%^3A3^%^7D; cartToken=GKJp8kje1OANcxq0Z4VoznnsNq8oQw1G; _ga=GA1.2.443837103.1671120803; _ym_uid=1671120803230135750; _ym_d=1671120803; _gcl_au=1.1.861777935.1671120806; tmr_lvid=155831903f66d71c66063cfdde88cd21; tmr_lvidTS=1671120806295; popmechanic_sbjs_migrations=popmechanic_1418474375998^%^3D1^%^7C^%^7C^%^7C1471519752600^%^3D1^%^7C^%^7C^%^7C1471519752605^%^3D1; adrcid=A5MELJfJJOupWj7Ed12WA2w; isVueListing=1; pathToProduct=2; goods_per_page=28; favToken=CiMrc3Tl6Vx2nzkRIaAvtoHpk50UnE3N; rrpvid=575553336143445; device_uid=A1P330ObmNfSnKc4UHHhmWQycc3H4kM19fIlg1rGu7DolWJMOCUGAPjc01S1IFGR; rcuid=639a3f4f514016510e303044; contractor_changed=1; vi_represent_type=common; vi_descendant_id=0; vi_represent_approved=1; vi_represent_id=1; rrlevt=1671804310933; _gid=GA1.2.1161220108.1672160657; DCID=3dc-site-u8-app3; _ym_isad=2; mindboxDeviceUUID=f7c3232c-3fd8-413b-aaf2-929c07d58670; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^22f7c3232c-3fd8-413b-aaf2-929c07d58670^%^22^%^7D; acctoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJ2aXRlY2giLCJhdWQiOiJ2c2VpbnN0cnVtZW50aS5ydSIsImlhdCI6MTY3MjMyMTMxOSwiZXhwIjoxNjcyMzI0OTE5LCJkZXZpZCI6ImMyZDM5MTk4LWMzYzAtNWQzMC1iMmYwLWJmZTY3NWVhMGRkMSIsInRpZCI6ImY3OTAyZDRlLThjYmItNDM1Yi1iMGZlLTQ2ODYzODg2OTIzYSJ9.k-wxX1x_CSBYPJoo1_SU4eCI8NVjSaH3i1-SkM70KxfZw_6IZAkCd6Xnr4iBOvlx5-VC9HJbZ77zZ6t1f5rOpw; reftoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJ2aXRlY2giLCJhdWQiOiJ2c2VpbnN0cnVtZW50aS5ydSIsImlhdCI6MTY3MjMyMTMxOSwiZXhwIjoxNjgwOTYxMzE5LCJkZXZpZCI6ImMyZDM5MTk4LWMzYzAtNWQzMC1iMmYwLWJmZTY3NWVhMGRkMSIsInRpZCI6ImY3OTAyZDRlLThjYmItNDM1Yi1iMGZlLTQ2ODYzODg2OTIzYSJ9.7U60H4ViiuFUUQB4F_q30EooeDNXa4ypG7HM724mKqjSppf0KjtHhnuNcgyCNnirg7YUbGhFp2reeOLs78wxdA; _gat=1; _gat_UA-6106715-1=1; __cf_bm=m1YO2m5pzEMHqRGPQYL3UUDwP2C52YHNmVtuj4IG3eA-1672321328-0-AawCEi1NIY5/LnL0VOuCwC6GhcUH7OuDUeUHIE6798zSItLcPGMLasGgEWr3gL8uJBv612VPul1mYHjkdvzdkBXvUZSFUkk5YtUedmAHl7Jpm04kAtQ1frZaQO6q2SJ0lNMh1lBtAgzd+3XjocMGTNe7ibmqRoq6yDmz6Sm6eqluZL3ETlx7QIBhmAR6Km9bbA==" ^/Al9KUL1yFDb73an0c1tHMB/Md2wFSdZz7PDuzPTWwn1C0q6hrSIScZBf98S0kFxTRVLKxXVD9+a7LBGXCtoJl3ET71gGwY26qTcEF9T+npmdw61vPrhBs1vLxS+wKSeZcmWOR+KUJAgjAT8Ugs7CysNSc4mkB+NwomGstL0hfMfdQ6UiSgpEB0AECFVj2g==; _gat=1; _gat_UA-6106715-1=1" ^/r/pWPr8QTVgGkzkqp1cwP26UbYTBMZnm9SDZunObCw==" ^/QGkWdHFCGPQP3H3UQabQhzIsVZ/3ZR7tIrhBwd4mWdE0ozYLe+TqiKFyIUjooL/Z2tP4l4w7xCBH68R6Coor590wZD3TnLtaWj6gusyn5KuZCpIOsbK4hx5qY79sfHJkIsutdA6e/CsiTUo4TVcUQ==; _gat=1; _gat_UA-6106715-1=1; mindboxDeviceUUID=f7c3232c-3fd8-413b-aaf2-929c07d58670; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^22f7c3232c-3fd8-413b-aaf2-929c07d58670^%^22^%^7D; pages_viewed=^%^7B^%^22value^%^22^%^3A6^%^2C^%^22expiration^%^22^%^3A1672315078^%^7D" ^',
            "if-none-match": 'W/^\^"d5b7mt^\^"',
            "origin": "https://www.vseinstrumenti.ru",
            "referer": "https://www.vseinstrumenti.ru/",
            "sec-ch-ua": '^\^"Not?A_Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"108^\^", ^\^"Google '
                         'Chrome^\^";v=^\^"108^\^"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/108.0.0.0 Safari/537.36"
        }

    def get_category_shop_response(self):
        proxies = {"https": 'http://wYZG4s:GbxfGs@45.10.248.101:8000'}
        myDict = {
            "categories": []
        }
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        with self.session:
            for url in self.url_list_category_shop_api:
                response_category_shop_api = self.session.get(
                    url,
                    headers=self.headers,
                    proxies=proxies
                )
                print(response_category_shop_api.status_code)
                dict_parse_category_shop = self.parse_category_shop_response(response_category_shop_api.json())

                myDict['categories'].append(dict_parse_category_shop)
        return myDict

    def get_subcategory_shop_response(self, left_border, right_border):
        proxies = {"https": 'http://wYZG4s:GbxfGs@45.10.248.101:8000'}
        myDict = {
            "categories": []
        }
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        with self.session:
            response_api_subcategories_shop = self.session.get(f'https://bff.vseinstrumenti.ru/catalog/child'
                                                               f'-categories?leftBorder={left_border}&rightBorder={right_border}&activeRegionId=1',
                                                               headers=self.headers,
                                                               proxies=proxies)


            return response_api_subcategories_shop.json()

    def parse_category_shop_response(self, data):
        dict_api_category_shop_api = data[0]
        dict_category_shop = self._parse_json_category_site(dict_api_category_shop_api)


        # category_id = dict_api_category_shop_api['url'].split('/')[-2].split('-')[-1]
        # category_name = dict_api_category_shop_api["name"]
        # category_children = []
        main_subcategories_list = data[0]['children']

        for main_subcategories in main_subcategories_list:
            dict_main_subcategory_shop = self._parse_json_category_site(main_subcategories)

            if main_subcategories['isSubcategoriesExist']:
                list_subcategories = self.get_subcategory_shop_response(main_subcategories['leftBorder'],
                                                                        main_subcategories['rightBorder'])
                list_subcategories = []
                for subcategory in list_subcategories:
                    list_subcategories.append(self._parse_json_category_site(subcategory))
                dict_main_subcategory_shop['categories'] = list_subcategories
            else:
                dict_main_subcategory_shop['categories'] = []

            # dict_main_subcategory_shop = {
            #     'category_id': main_subcategories_id,
            #     'name': main_subcategories_name,
            #     'categories': main_subcategories_children
            # }

            dict_category_shop['categories'].append(dict_main_subcategory_shop)

        return dict_category_shop

    def _parse_json_category_site(self, json_category: dict) -> dict:
        category_id = json_category['url'].split('/')[-2].split('-')[-1]
        category_name = json_category["name"]

        category_dict = {
            'category_id': category_id,
            'name': category_name,
            'url': json_category['url'],
            'categories': []
        }
        return category_dict

    def get_city_shop_response(self):
        pass

    def get_shop_information_response(self):
        pass

    def get_category_products_list_response(self):
        pass





    def parse_city_shop_response(self, data):
        pass

    def get_dict_with_category_shop(self) -> dict:
        pass


def main():
    vseinstrumenti_parser = VseInstrumentiParser()
    dict_categories_shop = vseinstrumenti_parser.get_category_shop_response()
    print(dict_categories_shop)

if __name__ == '__main__':
    main()
