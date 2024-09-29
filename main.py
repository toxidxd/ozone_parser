import json
import time
from loguru import logger
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from functions import page_down
from functions import collect_product_info


def get_products_list(item_name='headphones hyperx'):
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(3)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    time.sleep(3)
    find_input.send_keys(item_name)
    time.sleep(3)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = f'{driver.current_url}&sorting=rating'
    driver.get(url=current_url)
    time.sleep(3)

    # page_down(driver=driver)
    # time.sleep(10)

    driver.close()
    driver.quit()
    try:
        find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))
        logger.info('links collected')

        products_urls_dict = {}

        for k, v in enumerate(products_urls):
            products_urls_dict.update({k: v})

        with open('products_urls_dict.json', 'w', encoding='utf-8') as f:
            json.dump(products_urls_dict, f, indent=4, ensure_ascii=False)

        time.sleep(2)

        products_data = []

        for url in products_urls[:3]:
            data = collect_product_info(driver=driver, url=url)
            logger.info(f'get product data id: {data.get("product_id")}')
            time.sleep(2)
            products_data.append(data)

        with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
            json.dump(products_data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        logger.error(f'cant collect links, {e}')


def main():
    logger.add('log.log', format="{time} {level} {message}", level='INFO',
               rotation='10 KB', compression='zip')
    logger.info('start collect data')
    get_products_list(item_name='notebooks')
    logger.info('data collected')


if __name__ == '__main__':
    main()
