import psycopg2
from config import *

def write_postgresql(data):

    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT version();'
            )
            print(f'Server version: {cursor.fetchone()}')

        shop_name = data['shop_name']
        time =  data['current_time']
        article = data['article']
        name = data['name']
        price = data['price']
        stock = data['stock']
        url =  data['url']
        item_type = data['item_type']
        radiator_type = data['radiator_type']
        power = data['power']
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO radiators (time, article, name, price, stock, url, item_type, radiator_type, power, shop_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (time, article, name, price, stock, url, item_type, radiator_type, power, shop_name))
    #
    # (data['shop_name'],
    #  data['current_time'],
    #  data['article'],
    #  data['name'],
    #  data['price'],
    #  data['stock'],
    #  data['url'],
    #  data['item_type'],  # радиатор
    #  data['radiator_type'],  # стальной, биметалл, алюминий, чугун
    #  data['power']))


    except Exception as _ex:
        print('[INFO] Error while workin with PostgreSQL', _ex)

    # finally:
    #     if connection:
    #         connection.close()
    #         print('[INFO] PostgreSQL connection closed')



