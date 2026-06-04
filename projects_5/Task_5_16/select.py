import psycopg2



try:

    # Устанавливаем соединение

    connection = psycopg2.connect(

        host="localhost",          # База в контейнере, но доступна через localhost

        port="5430",               # Порт из секции ports

        user="postgres_user",           # POSTGRES_USER

        password="postgres_password",        # POSTGRES_PASSWORD

        database="postgres_db"          # POSTGRES_DB

    )

    cursor = connection.cursor()



    # 1. Выполняем запрос

    cursor.execute("SELECT product_id, price FROM prices;")



    # 2. Извлекаем все строки

    prices = cursor.fetchall()



    for price in prices:

        print(f"цена: {price[0]} {price[1]}")



    # Не забываем закрыть курсор

    cursor.close()



except Exception as error:

    print(f"Ошибка при подключении: {error}")