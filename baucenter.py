import csv
from selenium import webdriver
from _datetime import datetime
from selenium.webdriver.common.by import By
import time

import write_database
from write_database import write_postgresql

def write_csv(data):
    with open('catalog_baucenter.csv', 'a', newline='') as f:
        try:
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

def get_radiator_type(r_name):
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

def get_page_data(url_list):
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    with webdriver.Chrome(options=options_chrome) as browser:
        for url in url_list:
            browser.get(url)
            browser.find_element(By.ID, 'show-city-tooltip').click()
            time.sleep(2)
            browser.find_element(By.LINK_TEXT, 'Калининград').click()
            time.sleep(2)
            try:
                browser.find_element(By.CLASS_NAME, 'cookie-popup__close').click()
            except:
                pass
            time.sleep(1)
            item_article = browser.find_element(By.CLASS_NAME, 'product-head_right').text.split()[1]
            item_name = browser.find_element(By.TAG_NAME, 'h1').text
            item_url = url
            try:
                item_price = browser.find_element(By.CLASS_NAME, 'totalJsPrice').text
                item_price = round(float(item_price))
            except:
                item_price = 0
            if get_radiator_type(item_name)['radiator_type'] == 'алюминиевый' or get_radiator_type(item_name)['radiator_type'] == 'биметаллический':
                try:
                    power = round(float(browser.find_elements(By.CLASS_NAME, 'description-more_table-cell')[13].text))
                except:
                    power = 0
            else:
                try:
                    power = round(float(browser.find_elements(By.CLASS_NAME, 'description-more_table-cell')[9].text))
                except:
                    power = 0
            stock_list = browser.find_elements(By.CLASS_NAME, 'stock-list_item.green')[1:]
            #остаток
            item_stock = 0
            for i in stock_list:
                try:
                    item_stock += round(float(i.text.split()[1])) #суммируем количество по магазинам
                except:
                    item_stock = 0
            data = {
                'shop_name': 'https://baucenter.ru',
                'current_time': get_current_time(),
                'article': item_article,
                'name': item_name,
                'price': item_price,
                'url': item_url,
                'power': power,
                'stock': item_stock,
                'radiator_type': get_radiator_type(item_name),
            }
            data.update(get_radiator_type(item_name))
            print(data)
            write_database.write_postgresql(data)

def get_radiators_url(url):
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    with webdriver.Chrome(options=options_chrome) as browser:
        browser.get(url)
        browser.find_element(By.ID, 'show-city-tooltip').click()
        time.sleep(3)
        browser.find_element(By.LINK_TEXT, 'Калининград').click()
        time.sleep(3)
        browser.find_element(By.CLASS_NAME, 'cookie-popup__close').click()
        time.sleep(3)

        url_list = []
        while True:
            # собираем все ссылки на радиаторы
            items = browser.find_elements(By.CLASS_NAME, 'catalog_item_main-block')
            for item in items:
                url_list.append(item.get_attribute('href'))
                print(item.get_attribute('href'))
            time.sleep(1)

            # проверка окончания пагинации (проверка равенства двух чисел "Показаны результаты  по 157 из 157"
            if browser.find_element(By.CLASS_NAME, 'pagination_results').text.split()[5] == \
                    browser.find_element(By.CLASS_NAME, 'pagination_results').text.split()[7]:
                break
            else:
                # если пагинация возможна - то клик на следующую страницу
                browser.find_element(By.CLASS_NAME, 'icon-angle-right').click()  # клик на следующую страницу
                time.sleep(1)
    return url_list

def main():

    url = 'https://baucenter.ru/radiatory_otopleniya/?PAGEN_1=1&set_filter=y&arrFilter_5279_2616430844=Y&arrFilter_5279_3516652989=Y&arrFilter_5279_1038747965=Y&arrFilter_5279_3134833003=Y'
    get_page_data(get_radiators_url(url))


if __name__ == '__main__':
    main()





