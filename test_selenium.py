from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("general.useragent.override")
options.add_argument(" Chrome/102.0.5005.115 Mobile")
#options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('--ignore-certificate-errors-spki-list')


with webdriver.Chrome(ChromeDriverManager().install(), options=options) as webdriver:
    response = webdriver.get("https://api.petrovich.ru/catalog/v2.3/products/103353?section_code=1557&city_code=msk&client_id=pet_site",
                             )
    print(webdriver.page_source)
