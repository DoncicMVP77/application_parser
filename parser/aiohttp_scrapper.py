import requests
from bs4 import BeautifulSoup as BS
import aiohttp
import logging
import requests

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')


def get_main_shop_category():
    pass

url = 'https://api.petrovich.ru/catalog/v2.3/sections/tree/3?city_code=msk&client_id=pet_site'

def main():
    pass


if __name__ == '__main__':
    main()
