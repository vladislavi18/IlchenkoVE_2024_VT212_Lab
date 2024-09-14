import random  # Импортируем модуль random для генерации случайных значений


class Bank:
    def __init__(self, connection):
        """
        Инициализация класса Bank. Принимает объект connection, который используется для
        подключения к базе данных
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'banks' в базе данных. Таблица включает поля для информации о банке,
        такие как количество офисов, банкоматов, сотрудников, клиентов, рейтинг, общая сумма денег
        и процентная ставка
        """
        with self.connection.cursor() as cursor:
            # SQL запрос для создания таблицы
            query = """
                CREATE TABLE banks (
                    bank_id SERIAL PRIMARY KEY,  -- Идентификатор банка (генерируется автоматически)
                    name VARCHAR(255) NOT NULL,  -- Название банка (обязательное поле)
                    num_offices INT DEFAULT 0,  -- Количество офисов (по умолчанию 0)
                    num_atms INT DEFAULT 0,  -- Количество банкоматов (по умолчанию 0)
                    num_employees INT DEFAULT 0,  -- Количество сотрудников (по умолчанию 0)
                    num_clients INT DEFAULT 0,  -- Количество клиентов (по умолчанию 0)
                    rating INT NOT NULL CHECK (rating >= 0 AND rating <= 100),  -- Рейтинг банка (0-100)
                    total_money INT NOT NULL CHECK (total_money >= 0 AND total_money <= 1000000),  -- Общая сумма денег (0-1 000 000)
                    interest_rate FLOAT NOT NULL CHECK (interest_rate >= 0 AND interest_rate <= 20)  -- Процентная ставка (0-20%)
                );
            """
            cursor.execute(query)  # Выполнение SQL-запроса
        self.connection.commit()  # Применение изменений в базе данных

    def drop_table(self):
        """
        Удаляет таблицу 'banks' из базы данных
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE banks CASCADE;
            """
            cursor.execute(query)  # Выполнение SQL-запроса на удаление таблицы
        self.connection.commit()  # Применение изменений в базе данных

    def create(self, name):
        """
        Добавляет новый банк в таблицу 'banks'. Процентная ставка корректируется на основе рейтинга:
        чем выше рейтинг, тем ниже процентная ставка.

        :param name: Название банка
        """
        rating = random.randint(0, 100)  # Случайный рейтинг банка (0-100)
        total_money = random.randint(0, 1000000)  # Случайная сумма денег (0-1 000 000)
        interest_rate = random.uniform(0, 20)  # Случайная процентная ставка (0-20%)

        # Коррекция процентной ставки в зависимости от рейтинга
        if rating > 80:
            interest_rate *= 0.5
        elif rating > 60:
            interest_rate *= 0.7
        elif rating > 40:
            interest_rate *= 0.9

        with self.connection.cursor() as cursor:
            # SQL запрос для вставки данных о банке
            query = """
                INSERT INTO banks (name, num_offices, num_atms, num_employees, num_clients, rating, total_money, interest_rate)
                VALUES (%s, 0, 0, 0, 0, %s, %s, %s)
            """
            cursor.execute(query, (name, rating, total_money, round(interest_rate, 2)))  # Вставка данных в таблицу
        self.connection.commit()  # Применение изменений в базе данных

    def read(self, bank_id):
        """
        Возвращает данные о банке по его ID.

        :param bank_id: ID банка
        :return: Данные о банке в виде кортежа или None, если банк не найден.
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))  # Получение данных о банке с указанным ID
            return cursor.fetchone()  # Возвращение первой записи

    def list(self):
        """
        Возвращает список всех банков из таблицы 'banks'.

        :return: Список всех банков в виде кортежей.
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM banks"
            cursor.execute(query)  # Получение всех записей из таблицы
            return cursor.fetchall()  # Возвращение всех записей

    def update(self, bank_id, **kwargs):
        """
        Обновляет данные банка по его ID.

        :param bank_id: ID банка, который нужно обновить.
        :param kwargs: Данные для обновления (передаются в формате ключ-значение).
        """
        # Формирование строки для обновления полей (key = value)
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE banks SET {fields} WHERE bank_id = %s"
        params = list(kwargs.values()) + [bank_id]  # Параметры для обновления

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполнение запроса на обновление
        self.connection.commit()  # Применение изменений в базе данных

    def delete(self, bank_id):
        """
        Удаляет банк из таблицы по его ID.

        :param bank_id: ID банка, который нужно удалить.
        """
        with self.connection.cursor() as cursor:
            query = "DELETE FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))  # Удаление банка с указанным ID
        self.connection.commit()  # Применение изменений в базе данных
