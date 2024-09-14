import math


class User:
    def __init__(self, connection):
        """
        Инициализация класса User. Принимает объект connection для работы с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'users' в базе данных. Таблица хранит информацию о пользователях, включая:
        - Идентификатор пользователя (user_id)
        - Полное имя (full_name)
        - Дата рождения (birth_date)
        - Работа (job)
        - Ежемесячный доход (monthly_income), с ограничением не более 10,000
        - Список банков, с которыми связан пользователь (banks)
        - Кредитный рейтинг (credit_rating), который должен быть в пределах от 100 до 1000
        - Уникальное ограничение на сочетание полного имени и даты рождения
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для создания таблицы 'users'
            query = '''
                CREATE TABLE users (
                    user_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор пользователя
                    full_name VARCHAR(255) NOT NULL,  -- Полное имя пользователя
                    birth_date DATE NOT NULL,  -- Дата рождения
                    job VARCHAR(255),  -- Работа
                    monthly_income DECIMAL(10, 2) CHECK (monthly_income <= 10000),  -- Ежемесячный доход (макс. 10,000)
                    banks VARCHAR(255)[],  -- Список банков, связанных с пользователем
                    credit_rating INT CHECK (credit_rating BETWEEN 100 AND 1000),  -- Кредитный рейтинг (от 100 до 1000)
                    UNIQUE(full_name, birth_date)  -- Уникальное ограничение на полное имя и дату рождения
                );
                '''
            cursor.execute(query)  # Выполняем запрос для создания таблицы
        self.connection.commit()  # Сохраняем изменения в базе данных

    def drop_table(self):
        """
        Удаляет таблицу 'users' вместе с зависимыми объектами.
        """
        with self.connection.cursor() as cursor:
            query = """
                    DROP TABLE users CASCADE;
                """
            cursor.execute(query)  # Выполняем запрос для удаления таблицы
        self.connection.commit()  # Сохраняем изменения

    def create(self, full_name, birth_date, job, monthly_income, banks):
        """
        Создает нового пользователя и сохраняет его в базе данных. Кредитный рейтинг рассчитывается
        на основе ежемесячного дохода.

        :param full_name: Полное имя пользователя
        :param birth_date: Дата рождения пользователя
        :param job: Работа пользователя
        :param monthly_income: Ежемесячный доход пользователя
        :param banks: Список банков, с которыми связан пользователь
        """
        # Рассчитываем кредитный рейтинг на основе дохода пользователя (округляем до сотен)
        credit_rating = math.ceil(monthly_income / 1000) * 100

        with self.connection.cursor() as cursor:
            # Вставляем новую запись в таблицу 'users'
            query = """
                INSERT INTO users (full_name, birth_date, job, monthly_income, banks, credit_rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (full_name, birth_date, job, monthly_income, banks, credit_rating))

            # Обновляем информацию о количестве клиентов в каждом банке из списка пользователя
            for bank in banks:
                # Получаем идентификатор банка по его названию
                query = """
                    SELECT bank_id FROM banks WHERE name = %s
                """
                cursor.execute(query, (bank,))
                bank_id = cursor.fetchone()

                # Обновляем количество клиентов банка
                query = """
                    UPDATE banks SET num_clients = num_clients + 1 WHERE bank_id = %s
                """
                cursor.execute(query, (bank_id,))
        self.connection.commit()  # Сохраняем изменения

    def read(self, user_id):
        """
        Возвращает данные о пользователе по его идентификатору.

        :param user_id: Идентификатор пользователя
        :return: Данные о пользователе в виде кортежа или None, если пользователь не найден
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()  # Возвращаем запись о пользователе по его идентификатору

    def list(self):
        """
        Возвращает список всех пользователей.

        :return: Список всех пользователей в виде кортежей
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM users"
            cursor.execute(query)  # Выполняем запрос для получения всех записей из таблицы 'users'
            return cursor.fetchall()  # Возвращаем все записи

    def update(self, user_id, **kwargs):
        """
        Обновляет данные о пользователе по его идентификатору. Поля для обновления передаются через kwargs.

        :param user_id: Идентификатор пользователя
        :param kwargs: Пары "ключ-значение" для обновляемых полей
        """
        # Формируем строку полей для обновления
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE users SET {fields} WHERE user_id = %s"
        params = list(kwargs.values()) + [user_id]  # Параметры для запроса

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполняем запрос на обновление записи
        self.connection.commit()  # Сохраняем изменения

    def delete(self, user_id):
        """
        Удаляет пользователя по его идентификатору. Также обновляет количество клиентов в банках,
        с которыми был связан пользователь.

        :param user_id: Идентификатор пользователя
        """
        with self.connection.cursor() as cursor:
            # Получаем список банков, связанных с пользователем
            query = """
                    SELECT banks FROM users WHERE user_id = %s        
            """
            cursor.execute(query, (user_id,))
            banks = cursor.fetchall()  # Получаем список банков

            # Обновляем количество клиентов в каждом банке
            for bank in banks:
                # Получаем идентификатор банка
                query = """
                    SELECT bank_id FROM banks WHERE name = %s
                """
                bank_id = cursor.execute(query, (bank,))

                # Уменьшаем количество клиентов банка
                query = """
                    UPDATE banks SET num_clients = num_clients - 1 WHERE bank_id = %s
                """
                cursor.execute(query, (bank_id,))

            # Удаляем запись о пользователе
            query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
        self.connection.commit()  # Сохраняем изменения
