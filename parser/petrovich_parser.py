import json
import random
import time
from typing import List, Dict
import asyncio
import aiohttp
from aiohttp.client_exceptions import ClientOSError, ClientConnectorError
from fake_useragent import UserAgent
import aiofiles

from base_parser import BaseParser
import requests
from bs4 import BeautifulSoup as BS


class PetrovichParser(BaseParser):

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
                'authority': 'api.petrovich.ru',
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'u__geoCityGuid=b835705e-037e-11e4-9b63-00259038e9f2; u__geoUserChoose=1; SIK=fQAAAKYhHituULgSbicIAA; SIV=1; C_2orUj4RbWJX-j2qd_tb1pLl3dQo=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAMDNDdbpQaaI-PDrj_mr1rceKGwUuUI; _gcl_au=1.1.950704639.1671053130; tmr_lvid=c1484313d2acd33489116f19f69906d0; tmr_lvidTS=1671053131274; _ym_uid=1671053131251279816; _ym_d=1671053131; UIN=fQAAANTnQkHYek8WOeKdXFnIYEdHgoQXcVC4Et5JBwA; ssaid=d7c99630-7bf5-11ed-aadc-4bf072c36bf8; rrpvid=267247304460759; rcuid=639a3f4f514016510e303044; adrcid=A5MELJfJJOupWj7Ed12WA2w; dd_user.isReturning=true; aplaut_distinct_id=g5sySwa7vGYM; FPID=FPID1.2.PfCLw4RysDx667ur652PCTYaDnrReTXNLTDkHK2lzx0^%^3D.1671053131; popmechanic_sbjs_migrations=popmechanic_1418474375998^%^3D1^%^7C^%^7C^%^7C1471519752600^%^3D1^%^7C^%^7C^%^7C1471519752605^%^3D1; _gid=GA1.2.1527413864.1671442360; SNK=121; u__typeDevice=desktop; _ym_isad=2; FPLC=lfT0K3lNPAiWZnyJlyCS4W6XvGKmWK484TGFWOKtDtE3lHLx^%^2Fm17AAI7XMZbsGBV^%^2Fl7hdkvu9TvQ8OngLRM6KwEX^%^2BaG3u^%^2FlCOI^%^2F9pKquYU2kRnTOieFH4UGda^%^2FT80A^%^3D^%^3D; _ym_visorc=b; dd__persistedKeys=^[^%^22custom.lastViewedProductImages^%^22^%^2C^%^22user.isReturning^%^22^%^2C^%^22custom.lt13^%^22^%^2C^%^22custom.ts14^%^22^%^2C^%^22custom.ts12^%^22^%^2C^%^22custom.lt11^%^22^%^2C^%^22custom.productsViewed^%^22^]; rrviewed=603404; dd_custom.lastViewedProductImages=^[^%^22^%^22^%^2C^%^223520^%^22^%^2C^%^22^%^22^]; dd_custom.productsViewed=3; dd_custom.ts12=^{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:^{^%^221671148800^%^22:6^%^2C^%^221671408000^%^22:11^%^2C^%^221671494400^%^22:3^}^}; dd_custom.lt11=2022-12-20T10:24:21.796Z; rrlevt=1671531865183; _ga=GA1.2.1499298080.1671053131; _dc_gtm_UA-23479690-1=1; qrator_msid=1671530183.342.NdAyVGFujXMSY3y1-6n5q5ip51qrne20r9cn24o4krqu8173i; _gat_ddl=1; dd_custom.lt13=2022-12-20T10:35:58.593Z; dd_custom.ts14=^{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:^{^%^221671062400^%^22:1^%^2C^%^221671148800^%^22:10^%^2C^%^221671408000^%^22:7^%^2C^%^221671494400^%^22:15^}^}; __tld__=null; _dc_gtm_UA-23479690-19=1; dd__lastEventTimestamp=1671532558637; digi_uc=W1sidiIsIjYwMzQwNCIsMTY3MTUzMTg2Mzk2OV0sWyJ2IiwiMTAzMzUzIiwxNjcxNDY5Mzk1NzY0XSxbInYiLCIxMzk0MTYiLDE2NzE0NjIzNTExMTBdLFsidiIsIjEyNjkxNiIsMTY3MTQ0MzE4NzgxMV0sWyJjdiIsIjE0MDIxNiIsMTY3MTUzMTk1NzQ5M10sWyJjdiIsIjEwNTUyOSIsMTY3MTUzMTc4NTU4Nl0sWyJjdiIsIjEyNjkxNiIsMTY3MTUzMjU1NzA2NF0sWyJjdiIsIjY3OTIxNSIsMTY3MTEzMDcyOTY1MV1d; mindboxDeviceUUID=f7c3232c-3fd8-413b-aaf2-929c07d58670; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^22f7c3232c-3fd8-413b-aaf2-929c07d58670^%^22^%^7D; _gat_popmechanicManualTracker=1; _ga_XW7S332S1N=GS1.1.1671531492.16.1.1671532573.43.0.0" ^',
                'referer': 'https://moscow.petrovich.ru/catalog/1557/',
                'sec-ch-ua': '^\^"Not?A_Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"108^\^", ^\^"Google Chrome^\^";v=^\^"108^\^"',
                'sec-ch-ua-platform': '^\^"Windows^\^"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            })
        self.headers = {'authority': 'api.petrovich.ru',
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'u__geoCityGuid=b835705e-037e-11e4-9b63-00259038e9f2; u__geoUserChoose=1; SIK=fQAAAKYhHituULgSbicIAA; SIV=1; C_2orUj4RbWJX-j2qd_tb1pLl3dQo=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAMDNDdbpQaaI-PDrj_mr1rceKGwUuUI; _gcl_au=1.1.950704639.1671053130; tmr_lvid=c1484313d2acd33489116f19f69906d0; tmr_lvidTS=1671053131274; _ym_uid=1671053131251279816; _ym_d=1671053131; UIN=fQAAANTnQkHYek8WOeKdXFnIYEdHgoQXcVC4Et5JBwA; ssaid=d7c99630-7bf5-11ed-aadc-4bf072c36bf8; rrpvid=267247304460759; rcuid=639a3f4f514016510e303044; adrcid=A5MELJfJJOupWj7Ed12WA2w; dd_user.isReturning=true; aplaut_distinct_id=g5sySwa7vGYM; FPID=FPID1.2.PfCLw4RysDx667ur652PCTYaDnrReTXNLTDkHK2lzx0^%^3D.1671053131; popmechanic_sbjs_migrations=popmechanic_1418474375998^%^3D1^%^7C^%^7C^%^7C1471519752600^%^3D1^%^7C^%^7C^%^7C1471519752605^%^3D1; _gid=GA1.2.1527413864.1671442360; SNK=121; u__typeDevice=desktop; _ym_isad=2; FPLC=lfT0K3lNPAiWZnyJlyCS4W6XvGKmWK484TGFWOKtDtE3lHLx^%^2Fm17AAI7XMZbsGBV^%^2Fl7hdkvu9TvQ8OngLRM6KwEX^%^2BaG3u^%^2FlCOI^%^2F9pKquYU2kRnTOieFH4UGda^%^2FT80A^%^3D^%^3D; _ym_visorc=b; dd__persistedKeys=^[^%^22custom.lastViewedProductImages^%^22^%^2C^%^22user.isReturning^%^22^%^2C^%^22custom.lt13^%^22^%^2C^%^22custom.ts14^%^22^%^2C^%^22custom.ts12^%^22^%^2C^%^22custom.lt11^%^22^%^2C^%^22custom.productsViewed^%^22^]; rrviewed=603404; dd_custom.lastViewedProductImages=^[^%^22^%^22^%^2C^%^223520^%^22^%^2C^%^22^%^22^]; dd_custom.productsViewed=3; dd_custom.ts12=^{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:^{^%^221671148800^%^22:6^%^2C^%^221671408000^%^22:11^%^2C^%^221671494400^%^22:3^}^}; dd_custom.lt11=2022-12-20T10:24:21.796Z; rrlevt=1671531865183; _ga=GA1.2.1499298080.1671053131; _dc_gtm_UA-23479690-1=1; qrator_msid=1671530183.342.NdAyVGFujXMSY3y1-6n5q5ip51qrne20r9cn24o4krqu8173i; _gat_ddl=1; dd_custom.lt13=2022-12-20T10:35:58.593Z; dd_custom.ts14=^{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:^{^%^221671062400^%^22:1^%^2C^%^221671148800^%^22:10^%^2C^%^221671408000^%^22:7^%^2C^%^221671494400^%^22:15^}^}; __tld__=null; _dc_gtm_UA-23479690-19=1; dd__lastEventTimestamp=1671532558637; digi_uc=W1sidiIsIjYwMzQwNCIsMTY3MTUzMTg2Mzk2OV0sWyJ2IiwiMTAzMzUzIiwxNjcxNDY5Mzk1NzY0XSxbInYiLCIxMzk0MTYiLDE2NzE0NjIzNTExMTBdLFsidiIsIjEyNjkxNiIsMTY3MTQ0MzE4NzgxMV0sWyJjdiIsIjE0MDIxNiIsMTY3MTUzMTk1NzQ5M10sWyJjdiIsIjEwNTUyOSIsMTY3MTUzMTc4NTU4Nl0sWyJjdiIsIjEyNjkxNiIsMTY3MTUzMjU1NzA2NF0sWyJjdiIsIjY3OTIxNSIsMTY3MTEzMDcyOTY1MV1d; mindboxDeviceUUID=f7c3232c-3fd8-413b-aaf2-929c07d58670; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^22f7c3232c-3fd8-413b-aaf2-929c07d58670^%^22^%^7D; _gat_popmechanicManualTracker=1; _ga_XW7S332S1N=GS1.1.1671531492.16.1.1671532573.43.0.0" ^',
                'referer': 'https://moscow.petrovich.ru/catalog/1557/',
                'sec-ch-ua': '^\^"Not?A_Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"108^\^", ^\^"Google Chrome^\^";v=^\^"108^\^"',
                'sec-ch-ua-platform': '^\^"Windows^\^"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        self.url_category_shop_api = 'https://api.petrovich.ru/catalog/v2.3/sections/tree/3?city_code=msk&' \
                                     'client_id=pet_site'
        self.url_city_shop_api = 'https://api.petrovich.ru/geobase/v1.1/cities?city_code=msk&client_id=pet_site'
        self.url_main_shop_page = 'https://rf.petrovich.ru/'
        self.url_list_product_shop_api = 'https://api.petrovich.ru/catalog/v2.3/sections/10169?offset=0&path' \
                                         '=%2Fcatalog%2F10169%2F&city_code=msk&client_id=pet_site'
        self.count = 0

    def get_dict_with_category_shop(self) -> dict:
        with open('static/petrovich_category.json', "r", encoding="utf-8") as outfile:
            dict_category_shop = json.loads(outfile.read())
        return dict_category_shop

    def get_dict_with_city_shop(self) -> dict:
        with open('static/petrovich_city.json', "r", encoding="utf-8") as outfile:
            dict_city_shop = json.loads(outfile.read())
        return dict_city_shop

    def get_list_subcategories(self) -> Dict[str, List]:
        dict_categories_shop = self.get_dict_with_category_shop()
        dict_subcategories_shop = {"subcategories": []}
        for main_category in dict_categories_shop['categories']:
            for main_subcategory in main_category['categories']:
                if main_subcategory['categories'] is not []:
                    for subcategory in main_subcategory['categories']:
                        dict_subcategories_shop['subcategories'].append({
                            'category_id': subcategory['category_id'],
                            'name': subcategory['name']
                        })
                else:
                    dict_subcategories_shop["subcategories"].append({
                        'category_id': main_subcategory['category_id'],
                        'name': main_subcategory['name']
                    })

        return dict_subcategories_shop

    def make_urls_list_for_get_products(self):
        my_list = []
        dict_subcategories_shop = self.get_list_subcategories()
        dict_city_shop = self.get_dict_with_city_shop()
        url_list_product_shop_api = 'https:{}catalog/v2.3/sections/{}?offset=0&path' \
        '=%2Fcatalog%2F10169%2F&city_code={}&client_id=pet_site'

        for city in dict_city_shop['objects']:
            for category in dict_subcategories_shop['subcategories']:
                url = url_list_product_shop_api.format(city['url'], category['category_id'], city['id'])
                my_list.append(url)
        return my_list

    def parse_category_shop_response(self, body):
        myDict = {
            'categories': []
        }
        list_categories = body['data']
        list_main_category = self._parse_json_category_site(list_categories)
        for main_category in list_categories['sections']:
            main_category_dict = self._parse_json_category_site(main_category)

            for main_subcategory in main_category['sections']:
                main_subcategory_dict = self._parse_json_category_site(main_subcategory)

                if main_subcategory['sections'] is not None:
                    for subcategory in main_subcategory['sections']:
                        subcategory_dict = self._parse_json_category_site(subcategory)
                        main_subcategory_dict['categories'].append(subcategory_dict)

                main_category_dict['categories'].append(main_subcategory_dict)

            myDict['categories'].append(main_category_dict)
        return myDict

    def parse_city_shop_response(self, body):
        list_city = body['data']['commonCities']
        city_dict = {
            'objects': []
        }
        for city in list_city:
            object_id = city['code']
            object_name = city['title']
            object_url = city['url']


            city_dict['objects'].append({
                'id': object_id,
                'name': object_name,
                'url': object_url
            })

        print(city_dict)
        return city_dict

    def _parse_json_category_site(self, json_category:dict) -> dict:
        category_id = json_category.get('code', None)
        name = json_category.get('title', None)

        category_dict = {
            'category_id': category_id,
            'name': name,
            'categories': []
        }
        return category_dict

    def get_category_site_response(self):
        with self.session:
            response_category_shop_api = self.session.get(self.url_category_shop_api)
            return response_category_shop_api.json()

    def get_category_products_list_response(self):
        pass


    def get_shop_information_response(self):
        print(self.session)
        with self.session:
            response_main_shop_page_text = self.session.get(self.url_main_shop_page)
            return response_main_shop_page_text

    def get_city_shop_response(self):
        with self.session:
            response_city_shop_api = self.session.get(self.url_city_shop_api)
            return response_city_shop_api.json()

    def write_dict_to_json_file(self, shop_dict, path_file):
        category_json_object = json.dumps(shop_dict, ensure_ascii=False, indent=True)
        with open(path_file, "w", encoding="utf-8") as outfile:
            outfile.write(category_json_object)

    async def get_product_data(self, session, url):
        headers = self.headers
        headers['user-agent'] = self.get_user_agent()
        proxy = self.get_random_proxy()
        try:
            async with session.get(url=url, headers=headers, proxy=proxy) as response:
                response_text = await response.text()
                self.count += 1
                print(print(f"[INFO] page {url}, number {self.count}"))
        except (ClientOSError, ClientConnectorError) as ex:
            await asyncio.sleep(10 + random.randint(0, 9))
            async with session.get(url=url, headers=self.headers) as response:
                response_text = await response.text()
            print(ex)

    def get_random_proxy(self):
        return random.choice([
            'http://wYZG4s:GbxfGs@y45.10.248.101:8000',
            'http://wYZG4s:GbxfGs@y45.10.251.193:8000',
            'http://wYZG4s:GbxfGs@y45.10.249.223:8000',
            'http://wYZG4s:GbxfGs@y45.10.250.15:8000',
        ])

    def get_user_agent(self):
        return UserAgent(verify_ssl=False).random

    async def gather_data(self):
        urls = self.make_urls_list_for_get_products()
        # urls = [
        #     "https://petrovich.ru/catalog/v2.3/sections/1557?offset=0&path=%2Fcatalog%2F10169%2F&city_code=spb&client_id=pet_site",
        #     "https://petrovich.ru/catalog/v2.3/sections/1573?offset=0&path=%2Fcatalog%2F10169%2F&city_code=spb&client_id=pet_site",
        #
        # ]
        tasks = []
        connector = aiohttp.TCPConnector(force_close=True, limit=40)
        timeout = aiohttp.ClientTimeout(total=600)
        dummy_jar = aiohttp.DummyCookieJar()
        async with aiohttp.ClientSession(connector=connector, cookie_jar=dummy_jar, timeout=timeout, trust_env=True) \
                as session:
            for url in urls:
                task = asyncio.create_task(self.get_product_data(session, url))
                tasks.append(task)
            await asyncio.gather(*tasks)


def main():
    petrovich_site = PetrovichParser()

    # json_category_shop_response = petrovich_site.get_category_site_response()
    # dict_category_shop_parse = petrovich_site.parse_category_shop_response(json_category_shop_response)
    # petrovich_site.write_dict_to_json_file(dict_category_shop_parse, 'static/petrovich_category.json')

    # json_city_shop_response = petrovich_site.get_city_shop_response()
    # dict_city_shop_parse = petrovich_site.parse_city_shop_response(json_city_shop_response)
    # petrovich_site.write_dict_to_json_file(dict_city_shop_parse, 'static/petrovich_city.json')

    # petrovich_site.make_urls_list_for_get_products()
    # dict_subcategory_shop = petrovich_site.get_list_subcategories()
    # petrovich_site.write_dict_to_json_file(dict_subcategory_shop, 'static/petrovich_subcategory.json')
    # url_list = petrovich_site.make_urls_list_for_get_products()
    # petrovich_site.write_dict_to_json_file(url_list, 'static/petrovich_url_product_list.json')

    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(petrovich_site.gather_data())
    finish_time = time.time()


if __name__ == '__main__':
    main()
