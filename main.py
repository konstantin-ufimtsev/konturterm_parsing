import requests
from bs4 import BeautifulSoup
import csv
import lxml


def get_html(url):
    r = requests.get(url)
    r.encoding = 'pt-154'
    if r.ok: #если ошибок нет т.е. код 200
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('catalog_kontur.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
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
        item_price = int(item.find('span',class_='price_value').text.replace(' ', ''))

        data = {
            'name': item_name,
            'price': item_price,
            'stock': item_stock,
            'url': item_url
        }
        write_csv(data)

def main():
    url = 'https://www.konturterm.ru/catalog/otoplenie/radiatory/'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()








