import json

import requests
from bs4 import BeautifulSoup as BS
from pydantic import BaseModel, Field
import aiohttp
import logging
import requests

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')


class Category(BaseModel):
    id: int
    name: str
    url: str


async def gather_data():
    connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        pass


def get_categories_shop():
    with open("static/petrovich/petrovich_api_category.json", encoding="utf=8", mode="r") as infile:
        dict_categories = json.load(infile)
    return dict_categories


def parse_subcategories_shop():
    dict_categories = get_categories_shop()
    with requests.Session() as session:
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/108.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8, '
                      'application/signed-exchange;v=b3;q=0.9 '
        })

        for category in dict_categories:

            session.get(category['url'])


def parse_categories_shop():
    with requests.Session() as session:
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/108.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8, '
                      'application/signed-exchange;v=b3;q=0.9 '
        })
        main_page_url = 'https://moscow.petrovich.ru/'
        request_main_page_site = session.get(main_page_url)
        html_text_main_page_site = BS(request_main_page_site.text, 'html.parser')
        print(html_text_main_page_site)

        list_categories = html_text_main_page_site.find("ul", {"class": "sections-list-item"}).find_all("li")
        dict_categories = {
            category.find("span").text: {
                'id': category.find('a').get('href').split('/')[-2],
                'url': 'https://moscow.petrovich.ru/' + category.find('a').get('href')
            }
            for category in list_categories
        }
        json_object = json.dumps(dict_categories, ensure_ascii=False, indent=True)
        with open("static/petrovich/petrovich_api_category.json", encoding="utf=8", mode="w") as outfile:
            outfile.write(json_object)

def main():
    parse_categories_shop()


if __name__ == '__main__':
    main()
