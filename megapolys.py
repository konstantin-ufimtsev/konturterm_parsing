import csv
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from _datetime import datetime
from selenium.webdriver.common.by import By
import time

def write_csv(data):
    try:
        with open('catalog_megapolys.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow((data['shop_name'],
                             data['current_time'],
                             data['article'],
                             data['name'],
                             data['price'],
                             data['stock'],
                             data['url'],
                             data['item_type'],  # радиатор
                             data['radiator_type'],  # стальной, биметалл, алюминий, чугун
                             data['power']))
    except Exception as ex:
        print(ex)

def get_current_time():
    time = datetime.now().strftime('%d.%m.%Y')
    return time


def get_html(urls):
    html_list = []
    for url in urls:
        r = requests.get(url)
        if r.ok:
            html_list.append(r.text)
        else:
            print(r.status_code)
    return html_list

def get_radiator_type(r_name):
    item_type = ''
    radiator_type = ''
    if 'радиатор' and 'стальной' in r_name.lower():
        item_type = 'радиатор'
        radiator_type = 'стальной панельный'
    else:
        if 'радиатор' and 'алюминиевый ' in r_name.lower():
            item_type = 'радиатор'
            radiator_type = 'алюминиевый'
        else:
            if 'радиатор' and 'биметал' in r_name.lower():
                item_type = 'радиатор'
                radiator_type = 'биметаллический'
            else:
                if 'радиатор' and 'чугун' in r_name.lower():
                    item_type = 'радиатор'
                    radiator_type = 'чугунный'
                else:
                    if 'конвектор' in r_name.lower():
                        item_type = 'конвектор'
                        radiator_type = 'внутрипольный'
                    else:
                        item_type = 'комплектующие'

    data = {
        'item_type': item_type,  # радиатор, комплектующие
        'radiator_type': radiator_type,
    }

    return data



def get_radiator_urls(url):
    radiator_urls = []
    with webdriver.Chrome() as browser:
        browser.get(url)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(7)
        items = browser.find_elements(By.CLASS_NAME, 'dark_link.js-notice-block__title')
        for item in items:
            radiator_urls.append(item.get_attribute('href'))
    return list(set(radiator_urls))

def get_page_data(html_list):

    for html in html_list:
        soap = BeautifulSoup(html, 'lxml')
        item_name = soap.find('h1', id='pagetitle').text
        item_article = soap.find_all('span', class_='value')[2].text
        item_price = int(soap.find('span', class_='price_value').text.replace(' ', ''))
        item_stock = sum([int(i.text) for i in (soap.find_all('span', class_='value')[4:])])
        #item_stock = soap.find('span', class_='store_view').text.strip(')').strip('(')
        item_url = soap.find('link', rel='alternate').get('href')
        try:
            power = int(item_name.split('(')[1].split('Вт)')[0].strip(''))
        except:
            power = 0
        data = {
            'shop_name': 'https://www.megapolys.com',
            'current_time': get_current_time(),
            'article': item_article,
            'name': item_name,
            'price': item_price,
            'stock': item_stock,
            'url': item_url,
            'power': power,
            'radiator_type': get_radiator_type(item_name),
        }
        data.update(get_radiator_type(item_name))
        if data['power'] == 0:
            pass
        else:
            print(data)
            write_csv(data)

def main():
    urls = ['https://www.megapolys.com/catalog/otoplenie_vodosnabzhenie_i_ventilyatsiya/otoplenie/radiatory_otopleniya/radiatory_alyuminievye/',
            'https://www.megapolys.com/catalog/otoplenie_vodosnabzhenie_i_ventilyatsiya/otoplenie/radiatory_otopleniya/radiatory_bimetallicheskie/',
            'https://www.megapolys.com/catalog/otoplenie_vodosnabzhenie_i_ventilyatsiya/otoplenie/radiatory_otopleniya/radiatory_stalnye/',
            'https://www.megapolys.com/catalog/otoplenie_vodosnabzhenie_i_ventilyatsiya/otoplenie/radiatory_otopleniya/radiatory_chugunnye/',
            'https://www.megapolys.com/catalog/otoplenie_vodosnabzhenie_i_ventilyatsiya/otoplenie/radiatory_otopleniya/radiatory_konvektory_vnutripolnye/'
            ]

  #  urls = ['https://www.megapolys.com/catalog/otoplenie_vodosnabzhenie_i_ventilyatsiya/otoplenie/radiatory_otopleniya/radiatory_stalnye/']


    for url in urls:
        get_page_data(get_html(get_radiator_urls(url)))




if __name__ == '__main__':
    main()