import requests
from bs4 import BeautifulSoup
import csv
from _datetime import datetime
import re

#функция вывода времени и даты
def get_current_datetime():
    time = datetime.now().strftime('%d.%m.%Y')
    return time

def get_html(url):
    r = requests.get(url)
    r.encoding = 'pt-154'
    if r.ok: #если ошибок нет т.е. код 200
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('catalog_kontur.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['shop_name'],
                         data['current_time'],
                         data['article'],
                         data['name'],
                         data['price'],
                         data['stock'],
                         data['url'],
                         data['item_type'],
                         data['radiator_type'],
                         data['power']))

def get_item_properties(item_name):

    if 'радиатор' and 'стальной' and 'панельный' in item_name.lower():
        item_type = 'радиатор'
        radiator_type = 'стальной панельный'
        power = int(re.findall(r'\d+', item_name)[-1])
    else:
        if 'радиатор' and 'schulter' in item_name.lower():
            item_type = 'радиатор'
            radiator_type = 'стальной панельный'
            power = int(re.findall(r'\d+', item_name)[-1])
        else:

            if 'радиатор' and 'алюминиевый ' in item_name.lower():
                item_type = 'радиатор'
                radiator_type = 'алюминиевый'
                power = int(re.findall(r'\d+', item_name)[-2]) * int(re.findall(r'\d+', item_name)[-1])
            else:
                if 'радиатор' and 'биметал' in item_name.lower():
                    item_type = 'радиатор'
                    radiator_type = 'биметаллический'
                    power = int(re.findall(r'\d+', item_name)[-2]) * int(re.findall(r'\d+', item_name)[-1])
                else:
                    if 'конвектор' in item_name.lower():
                        item_type = 'конвектор'
                        radiator_type = 'внутрипольный'
                        power = int(re.findall(r'\d+', item_name)[-1])
                    else:
                        if 'радиатор' and 'чугун' in item_name.lower():
                            item_type = 'радиатор'
                            radiator_type = 'чугунный'
                            power = int(re.findall(r'\d+', item_name)[-2]) * int(re.findall(r'\d+', item_name)[-1])
                        else:
                            if 'радиатор' in item_name.lower() and ('конвектор' not in item_name.lower()) and ('стальной' not in item_name.lower()) and ('биметал' not in item_name.lower()) and ('алюмини' not in item_name.lower()) and ('чугун' not in item_name.lower()):
                                item_type = 'радиатор'
                                radiator_type = 'стальной трубчатый'
                                power = int(re.findall(r'\d+', item_name)[-1])
                            else:
                                item_type = 'комплектующие'
                                radiator_type = '-'
                                power = '-'

    data = {
            'item_type': item_type, #радиатор, комплектующие
            'radiator_type': radiator_type, ##конвектор, биметаллчиеский,алюминиевый , стальной панельный, стальбной трубчатый, чугунный,
            'power': power, #тепловая мощность
        }

    return data



def get_page_data(html):
    
    soap = BeautifulSoup(html, 'lxml')
    items = soap.find_all('div', class_='item_info')

    for item in items:
        item_name = item.find('div', class_='item-title').text.strip()
        item_url = 'https://www.konturterm.ru' + item.find('a').get('href')
        item_stock = int(item.find('span', class_='value font_sxs').text.split(':')[1].strip())
        item_price = int(item.find('span', class_='price_value').text.replace(' ', ''))

        # проваливаемся в карточку и забираем артикул
        soap_item = BeautifulSoup(get_html(item_url), 'lxml')
        article = soap_item.find('span', class_='article__value').text.strip()



        data = {
            'shop_name' : 'www.konturterm.ru',
            'current_time': get_current_datetime(),
            'article': article,
            'name': item_name,
            'price': item_price,
            'stock': item_stock,
            'url': item_url,
        }
        data.update(get_item_properties(item_name))

        if data['item_type'] == 'комплектующие':
            pass
        else:
            print(data)
            write_csv(data)

def main():
    url_list = ['https://www.konturterm.ru/catalog/otoplenie/radiatory/bimetallicheskie/filter/in_stock-is-y/apply/?SHOWALL_1=1',
                'https://www.konturterm.ru/catalog/otoplenie/radiatory/panelnye/filter/in_stock-is-y/apply/?SHOWALL_1=1,',
                'https://www.konturterm.ru/catalog/otoplenie/radiatory/stalnye_trubchatye/filter/in_stock-is-y/apply/?SHOWALL_1=1',
                'https://www.konturterm.ru/catalog/otoplenie/radiatory/alyuminievye/filter/in_stock-is-y/apply/?SHOWALL_1=1',
                'https://www.konturterm.ru/catalog/otoplenie/radiatory/chugunnye/filter/in_stock-is-y/apply/?SHOWALL_1=1',
                'https://www.konturterm.ru/catalog/otoplenie/radiatory/vnutripolnye_konvektory/filter/in_stock-is-y/apply/?SHOWALL_1=1']


    for url in url_list:
        try:
            get_page_data(get_html(url))
        except:
            print('ошибка получения данных со страницы')

if __name__ == '__main__':
    main()








