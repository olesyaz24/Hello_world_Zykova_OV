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

    print("Подключение к базе данных прошло успешно!")



except Exception as error:

    print(f"Ошибка при подключении: {error}")