class BankAtm:
    def __init__(self, connection):
        """
        Инициализация класса BankAtm. Принимает объект connection для взаимодействия с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'atms' в базе данных. Таблица содержит информацию о банкоматах, таких как:
        название, адрес, статус, наличие возможности выдачи и приема денег, количество денег в банкомате,
        затраты на обслуживание и ссылки на связанные таблицы банка, офисов и сотрудников.
        """
        with self.connection.cursor() as cursor:
            # SQL запрос для создания таблицы 'atms'
            query = """
                CREATE TABLE atms (
                    atm_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор банкомата (генерируется автоматически)
                    name VARCHAR(255) NOT NULL,  -- Название банкомата
                    address VARCHAR(255) NOT NULL,  -- Адрес банкомата (получается из офиса банка)
                    status VARCHAR(50) NOT NULL,  -- Текущий статус банкомата (например, работает или не работает)
                    bank_id INT NOT NULL,  -- Идентификатор банка (ссылка на таблицу 'banks')
                    bank_office_id INT NOT NULL,  -- Идентификатор офиса банка (ссылка на таблицу 'bank_offices')
                    employee_id INT NOT NULL,  -- Идентификатор сотрудника, обслуживающего банкомат (ссылка на таблицу 'employees')
                    dispense_money BOOLEAN NOT NULL,  -- Возможность выдачи денег (True или False)
                    accept_money BOOLEAN NOT NULL,  -- Возможность приема денег (True или False)
                    money_in_atm INT DEFAULT 0,  -- Количество денег в банкомате (по умолчанию 0)
                    maintenance_cost FLOAT NOT NULL,  -- Затраты на обслуживание банкомата
                    FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE,  -- Внешний ключ на банк
                    FOREIGN KEY (bank_office_id) REFERENCES bank_offices(bank_office_id) ON DELETE CASCADE,  -- Внешний ключ на офис банка
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE  -- Внешний ключ на сотрудника
                );
            """
            cursor.execute(query)  # Выполнение запроса на создание таблицы
        self.connection.commit()  # Применение изменений

    def drop_table(self):
        """
        Удаляет таблицу 'atms' вместе с её зависимостями.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE atms CASCADE;
            """
            cursor.execute(query)  # Выполнение запроса на удаление таблицы
        self.connection.commit()  # Применение изменений

    def create(self, name, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money,
               maintenance_cost):
        """
        Создает новый банкомат и сохраняет его в базе данных. Адрес банкомата берется из информации об офисе,
        а количество денег в банкомате берется из информации о банке.

        :param name: Название банкомата
        :param status: Статус банкомата
        :param bank_id: Идентификатор банка
        :param bank_office_id: Идентификатор офиса банка
        :param employee_id: Идентификатор сотрудника
        :param dispense_money: Возможность выдачи денег (True или False)
        :param accept_money: Возможность приема денег (True или False)
        :param maintenance_cost: Затраты на обслуживание банкомата
        """
        with self.connection.cursor() as cursor:
            # Получаем адрес офиса банка по его идентификатору
            query = """
                SELECT address FROM bank_offices WHERE bank_office_id = %s
            """
            cursor.execute(query, (bank_office_id,))
            address = cursor.fetchone()  # Получаем результат запроса

            # Получаем количество денег в банке по идентификатору банка
            query = """
                SELECT total_money FROM banks WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))
            total_money = cursor.fetchone()  # Получаем результат запроса

            # Вставляем новую запись о банкомате в таблицу 'atms'
            query = """
                INSERT INTO atms (name, address, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money, money_in_atm, maintenance_cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, address, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money, total_money,
                maintenance_cost))

            # Обновляем количество банкоматов в банке
            query = """
                UPDATE banks SET num_atms = num_atms + 1 WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))

            # Обновляем количество банкоматов в офисе банка
            query = """
                UPDATE bank_offices SET num_atms = num_atms + 1 WHERE bank_office_id = %s
            """
            cursor.execute(query, (bank_office_id,))
        self.connection.commit()  # Применение изменений

    def read(self, atm_id):
        """
        Возвращает данные о банкомате по его идентификатору.

        :param atm_id: Идентификатор банкомата
        :return: Данные о банкомате в виде кортежа или None, если банкомат не найден
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms WHERE atm_id = %s"
            cursor.execute(query, (atm_id,))
            return cursor.fetchone()  # Возвращает первую запись

    def list(self):
        """
        Возвращает список всех банкоматов.

        :return: Список всех банкоматов в виде кортежей
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms"
            cursor.execute(query)  # Выполнение запроса для получения всех банкоматов
            return cursor.fetchall()  # Возвращает все записи

    def update(self, atm_id, **kwargs):
        """
        Обновляет данные о банкомате по его идентификатору. Обновляемые поля передаются как ключ-значение через kwargs.

        :param atm_id: Идентификатор банкомата
        :param kwargs: Пары "ключ-значение" для обновляемых полей
        """
        # Формируем строку полей для обновления
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE atms SET {fields} WHERE atm_id = %s"
        params = list(kwargs.values()) + [atm_id]  # Параметры для запроса

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполнение запроса на обновление
        self.connection.commit()  # Применение изменений

    def delete(self, atm_id):
        """
        Удаляет банкомат по его идентификатору. Также обновляет информацию о количестве банкоматов в банке и офисе.

        :param atm_id: Идентификатор банкомата
        """
        with self.connection.cursor() as cursor:
            # Получаем идентификаторы банка и офиса банка, к которым привязан банкомат
            query = "SELECT bank_id, bank_office_id FROM atms WHERE atm_id=%s"
            cursor.execute(query, (atm_id,))
            bank_id, bank_office_id = cursor.fetchone()  # Получаем результат запроса

            # Уменьшаем количество банкоматов в банке
            query = """
                UPDATE banks SET num_atms = num_atms - 1 WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))

            # Уменьшаем количество банкоматов в офисе банка
            query = """
                UPDATE bank_offices SET num_atms = num_atms - 1 WHERE bank_office_id = %s
            """
            cursor.execute(query, (bank_office_id,))

            # Удаляем банкомат
            query = "DELETE FROM atms WHERE atm_id = %s"
            cursor.execute(query, (atm_id,))
        self.connection.commit()  # Применение изменений
