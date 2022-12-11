import csv
import requests
from _datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re


def get_current_datetime():
    time = datetime.now().strftime('%d.%m.%Y')
    return time

def get_radiator_type(r_name: str) -> str:

    if 'радиатор' and 'стальной' in r_name.lower():
        r_type = 'стальной панельный'
    else:
        if 'радиатор' and 'алюминиевый ' in r_name.lower():
            r_type = 'алюминиевый'
        else:
            if 'радиатор' and 'биметал' in r_name.lower():
                r_type = 'биметаллический'
            else:
                if 'радиатор' and 'чугун' in r_name.lower():
                    r_type = 'чугунный'
                else:
                    r_type = 'комплектующие'

    return r_type

def write_csv(data):
    try:
        with open('catalog_tdstroitel.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow((data['shop_name'],
                             data['current_time'],
                             data['article'],
                             data['name'],
                             data['price'],
                             data['stock'],
                             data['url'],
                             data['item_type'], #радиатор
                             data['radiator_type'], #стальной, биметалл, адюминий, чугун
                             data['power']))
    except Exception as ex:
        print(ex)

#получает ссылку на страницу с нужным типом радиаторов и возвращает список радиаторов с этой страницы
def get_radiator_urls(url: str) -> list:
    with webdriver.Chrome() as browser:
        browser.get(url)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        # получаем url каждого радиатора

        radiator_urls = []
        items = browser.find_elements(By.XPATH, '//*[@id="pagination_contents"]/*/*/div/form/*/a')
        for item in items:
            radiator_urls.append(item.get_attribute('href'))
            print(radiator_urls)
        return list(set(radiator_urls)) #возварщает список урлов каждого радиатора


#получает на вход урл с радиатором и возвращает html код страницы text или ошибку
def get_html(url: list):
    html_list = []
    for rad_url in url:
        headers = {'user_agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36'}
        response = requests.get(rad_url, headers=headers)
        if response.ok: #если ошибок нет т.е. код 200
            html_list.append(response.text)
        else:
            print(response.status_code)
    return html_list



def get_page_data(html: list):
    for rad_html in html:
        soap = BeautifulSoup(rad_html, 'lxml')
        try:
            item_name = soap.find('h1', class_='ty-product-block-title').text
        except Exception as ex:
            print('ex')
        try:
            item_article = soap.find('div', class_='ty-product-block__sku').text.split()[1].strip()
        except Exception as ex:
            print('ex')
        try:
            item_price = float(''.join(soap.find('span', class_='ty-price').text.split()[0:-1]))
        except Exception as ex:
            print('ex')
        try:
            item_stock = sum([int(i.text) for i in soap.find_all('span', class_='ty-wi-warehouse__value')])
        except Exception as ex:
            print('ex')
        try:
            item_type = 'радиатор'
        except Exception as ex:
            print('ex')
        try:
            item_url = soap.find('link', rel='canonical').get('href')
        except Exception as ex:
            print('ex')
        try:
            power = int(re.findall(r'\d+', item_name)[-1])
            print(power)
        except Exception as ex:
            print('ex')
        data = {
            'shop_name': 'https://tdstroitel.ru',
            'current_time': get_current_datetime(),
            'article': item_article,
            'name': item_name,
            'price': item_price,
            'stock': item_stock,
            'url': item_url,
            'power': power,
            'radiator_type': get_radiator_type(item_name),
            'item_type': item_type,
        }
        if data['radiator_type'] == 'комплектующие':
            pass
        else:
            print(data)
            write_csv(data)

def main():
    #список ссылок на каждый тип радиатора
    url_list = ['https://tdstroitel.ru/vodosnabzhenie-otoplenie/radiatory/radiatory-alyuminievye/?features_hash=190-Y',
                'https://tdstroitel.ru/vodosnabzhenie-otoplenie/radiatory/radiatory-stalnye/?features_hash=190-Y',
                'https://tdstroitel.ru/vodosnabzhenie-otoplenie/radiatory/radiatory-bimetallicheskie/?features_hash=190-Y',
                'https://tdstroitel.ru/vodosnabzhenie-otoplenie/radiatory/radiatory-chugunnye/']
    for url in url_list:
        get_page_data(get_html(get_radiator_urls(url)))

if __name__ == '__main__':
    main()
