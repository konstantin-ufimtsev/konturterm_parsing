import requests
from bs4 import BeautifulSoup
import csv
from _datetime import datetime
import lxml

#функция вывода времени и даты
def get_current_datetime():
    time = datetime.now().strftime('%H.%M-%d.%m.%Y')
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
        writer.writerow((data['current_time'],
                         data['article'],
                         data['name'],
                         data['price'],
                         data['stock'],
                         data['url']))

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
            'current_time': get_current_datetime(),
            'article': article,
            'name': item_name,
            'price': item_price,
            'stock': item_stock,
            'url': item_url
        }
        print(data)
        write_csv(data)

def main():
    url = 'https://www.konturterm.ru/catalog/otoplenie/radiatory/?SHOWALL_1=1'
    try:
        get_page_data(get_html(url))
    except:
        pass

if __name__ == '__main__':
    main()








