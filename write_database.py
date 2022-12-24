import psycopg2

try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='1234',
        database='radiators',
        port='5432'
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT version();'
        )
        print(f'Server version: {cursor.fetchone()}')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO radiators (time, article, name, price, stock, url, item_type, radiator_type, power, shop_name) 
            VALUES ('24.12.22', '123456789', 'Радиатор Хер', 6000, 50, 'www.ru', 'Радиатор', 'стальной панельный', 1550, 'www.baucenter.ru');
            """
        )

    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM radiators""")
        print(cursor.fetchall())

except Exception as _ex:
    print('[INFO] Error while workin with PostgreSQL', _ex)

finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')



