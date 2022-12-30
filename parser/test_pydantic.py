from pydantic import BaseModel, ValidationError, Field
import logging
from typing import Any, Union, List
import requests
from selenium import webdriver

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

# with requests.Session() as session:
#     session.headers.update({
#         'authority': 'api.petrovich.ru',
#         'accept': '*/*',
#         'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#         'cookie': 'u__geoCityGuid=b835705e-037e-11e4-9b63-00259038e9f2; u__geoUserChoose=1; SIK=fQAAAKYhHituULgSbicIAA; SIV=1; C_2orUj4RbWJX-j2qd_tb1pLl3dQo=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAMDNDdbpQaaI-PDrj_mr1rceKGwUuUI; _gcl_au=1.1.950704639.1671053130; tmr_lvid=c1484313d2acd33489116f19f69906d0; tmr_lvidTS=1671053131274; _ym_uid=1671053131251279816; _ym_d=1671053131; UIN=fQAAANTnQkHYek8WOeKdXFnIYEdHgoQXcVC4Et5JBwA; ssaid=d7c99630-7bf5-11ed-aadc-4bf072c36bf8; rrpvid=267247304460759; rcuid=639a3f4f514016510e303044; adrcid=A5MELJfJJOupWj7Ed12WA2w; dd_user.isReturning=true; aplaut_distinct_id=g5sySwa7vGYM; FPID=FPID1.2.PfCLw4RysDx667ur652PCTYaDnrReTXNLTDkHK2lzx0^%^3D.1671053131; popmechanic_sbjs_migrations=popmechanic_1418474375998^%^3D1^%^7C^%^7C^%^7C1471519752600^%^3D1^%^7C^%^7C^%^7C1471519752605^%^3D1; _gid=GA1.2.1527413864.1671442360; SNK=121; u__typeDevice=desktop; _ym_isad=2; FPLC=lfT0K3lNPAiWZnyJlyCS4W6XvGKmWK484TGFWOKtDtE3lHLx^%^2Fm17AAI7XMZbsGBV^%^2Fl7hdkvu9TvQ8OngLRM6KwEX^%^2BaG3u^%^2FlCOI^%^2F9pKquYU2kRnTOieFH4UGda^%^2FT80A^%^3D^%^3D; _ym_visorc=b; dd__persistedKeys=^[^%^22custom.lastViewedProductImages^%^22^%^2C^%^22user.isReturning^%^22^%^2C^%^22custom.lt13^%^22^%^2C^%^22custom.ts14^%^22^%^2C^%^22custom.ts12^%^22^%^2C^%^22custom.lt11^%^22^%^2C^%^22custom.productsViewed^%^22^]; rrviewed=603404; dd_custom.lastViewedProductImages=^[^%^22^%^22^%^2C^%^223520^%^22^%^2C^%^22^%^22^]; dd_custom.productsViewed=3; dd_custom.ts12=^{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:^{^%^221671148800^%^22:6^%^2C^%^221671408000^%^22:11^%^2C^%^221671494400^%^22:3^}^}; dd_custom.lt11=2022-12-20T10:24:21.796Z; rrlevt=1671531865183; _ga=GA1.2.1499298080.1671053131; _dc_gtm_UA-23479690-1=1; qrator_msid=1671530183.342.NdAyVGFujXMSY3y1-6n5q5ip51qrne20r9cn24o4krqu8173i; _gat_ddl=1; dd_custom.lt13=2022-12-20T10:35:58.593Z; dd_custom.ts14=^{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:^{^%^221671062400^%^22:1^%^2C^%^221671148800^%^22:10^%^2C^%^221671408000^%^22:7^%^2C^%^221671494400^%^22:15^}^}; __tld__=null; _dc_gtm_UA-23479690-19=1; dd__lastEventTimestamp=1671532558637; digi_uc=W1sidiIsIjYwMzQwNCIsMTY3MTUzMTg2Mzk2OV0sWyJ2IiwiMTAzMzUzIiwxNjcxNDY5Mzk1NzY0XSxbInYiLCIxMzk0MTYiLDE2NzE0NjIzNTExMTBdLFsidiIsIjEyNjkxNiIsMTY3MTQ0MzE4NzgxMV0sWyJjdiIsIjE0MDIxNiIsMTY3MTUzMTk1NzQ5M10sWyJjdiIsIjEwNTUyOSIsMTY3MTUzMTc4NTU4Nl0sWyJjdiIsIjEyNjkxNiIsMTY3MTUzMjU1NzA2NF0sWyJjdiIsIjY3OTIxNSIsMTY3MTEzMDcyOTY1MV1d; mindboxDeviceUUID=f7c3232c-3fd8-413b-aaf2-929c07d58670; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^22f7c3232c-3fd8-413b-aaf2-929c07d58670^%^22^%^7D; _gat_popmechanicManualTracker=1; _ga_XW7S332S1N=GS1.1.1671531492.16.1.1671532573.43.0.0" ^',
#         'referer': 'https://moscow.petrovich.ru/catalog/1557/',
#         'sec-ch-ua': '^\^"Not?A_Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"108^\^", ^\^"Google Chrome^\^";v=^\^"108^\^"',
#         'sec-ch-ua-platform': '^\^"Windows^\^"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-site',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
#     })
#     main_page_url = 'https://api.petrovich.ru/catalog/v2.3/sections/tree/3?city_code=msk&client_id=pet_site'
#     # params = {
#     #     'section_code': 1557,
#     #     'city_mode': 'msk',
#     #     'client_id': 'pet_site'
#     # }
#
#     request_main_page_site = session.get(main_page_url)
#     print(request_main_page_site.text)


class Category(BaseModel):
    category_id: int
    name: str
    categories: Union["list[Category]", list[None]] = Field(alias='children')


myDict = {
    "category_id": 102,
    "name": "hello_1",
    "children": [{
        "category_id": 103,
        "name": "hello_2",
        "children": []
    }]
}

category_response = Category.parse_obj(myDict)
print(category_response.json(by_alias=True))
