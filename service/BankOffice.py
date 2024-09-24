from service.impl.IBankOffice import IBankOffice
from entity.bankOfficeModel import BankOfficeModel


class BankOffice(IBankOffice):
    def __init__(self, connection):
        """
        Инициализация класса BankOffice. Принимает объект connection для взаимодействия с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'bank_offices' в базе данных. Таблица содержит информацию о банковских офисах,
        такие как: название, адрес, статус, возможность установки банкомата, количество банкоматов,
        возможность выдачи кредита, выдачи и приема денег, аренда офиса и ссылка на таблицу банка.
        """
        with self.connection.cursor() as cursor:
            # SQL запрос для создания таблицы 'bank_offices'
            query = """
                    CREATE TABLE bank_offices (
                        bank_office_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор офиса банка (генерируется автоматически)
                        name VARCHAR(255) NOT NULL,  -- Название офиса
                        address VARCHAR(255) NOT NULL,  -- Адрес офиса
                        status VARCHAR(50) NOT NULL,  -- Текущий статус офиса (например, работает или закрыт)
                        can_place_atm BOOLEAN NOT NULL,  -- Возможность установки банкомата (True или False)
                        num_atms INT DEFAULT 0,  -- Количество банкоматов в офисе (по умолчанию 0)
                        can_provide_credit BOOLEAN NOT NULL,  -- Возможность предоставления кредита (True или False)
                        dispense_money BOOLEAN NOT NULL,  -- Возможность выдачи денег (True или False)
                        accept_money BOOLEAN NOT NULL,  -- Возможность приема денег (True или False)
                        money_in_office INT DEFAULT 0,  -- Количество денег в офисе (по умолчанию 0)
                        rent_cost FLOAT NOT NULL,  -- Затраты на аренду офиса
                        bank_id INT NOT NULL,  -- Идентификатор банка (ссылка на таблицу 'banks')
                        FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE  -- Внешний ключ на банк
                    );
                """
            cursor.execute(query)  # Выполнение запроса на создание таблицы
        self.connection.commit()  # Применение изменений

    def drop_table(self):
        """
        Удаляет таблицу 'bank_offices' вместе с её зависимостями.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE bank_offices CASCADE;
            """
            cursor.execute(query)  # Выполнение запроса на удаление таблицы
        self.connection.commit()  # Применение изменений

    def create(self, name, address, status, can_place_atm, can_provide_credit, dispense_money,
               accept_money, rent_cost, bank_id):
        """
        Создает новый офис банка и сохраняет его в базе данных. Количество денег в офисе берется из информации о банке.

        :param name: Название офиса
        :param address: Адрес офиса
        :param status: Статус офиса
        :param can_place_atm: Возможность установки банкомата (True или False)
        :param can_provide_credit: Возможность предоставления кредита (True или False)
        :param dispense_money: Возможность выдачи денег (True или False)
        :param accept_money: Возможность приема денег (True или False)
        :param rent_cost: Затраты на аренду офиса
        :param bank_id: Идентификатор банка
        """
        with self.connection.cursor() as cursor:
            # Получаем количество денег в банке по идентификатору банка
            query = """
                SELECT total_money FROM banks WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))
            total_money = cursor.fetchone()  # Получаем результат запроса

            # Вставляем новую запись об офисе в таблицу 'bank_offices'
            query = """
                INSERT INTO bank_offices (name, address, status, can_place_atm, num_atms, can_provide_credit, dispense_money, accept_money, money_in_office, rent_cost, bank_id)
                VALUES (%s, %s, %s, %s, 0, %s, %s, %s, %s, %s, %s)
                RETURNING bank_office_id
            """
            cursor.execute(query, (
                name, address, status, can_place_atm, can_provide_credit, dispense_money, accept_money, total_money,
                rent_cost, bank_id))
            bank_office_id = cursor.fetchone()[0]

            # Обновляем количество офисов в банке
            query = """
                UPDATE banks SET num_offices = num_offices + 1 WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))
        self.connection.commit()  # Применение изменений

        return BankOfficeModel(bank_office_id, name, address, status, can_place_atm, can_provide_credit,
                               dispense_money, accept_money, total_money, rent_cost, bank_id)

    def read(self, office_id):
        """
        Возвращает данные об офисе банка по его идентификатору.

        :param office_id: Идентификатор офиса
        :return: Данные об офисе в виде кортежа или None, если офис не найден
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (office_id,))
            data = cursor.fetchone()  # Получение первой записи

            # Если банк найден, возвращаем экземпляр модели BankModel
            if data:
                return BankOfficeModel(*data)
            return None

    def list(self):
        """
        Возвращает список всех офисов банка.

        :return: Список всех офисов банка в виде кортежей
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM bank_offices"
            cursor.execute(query)  # Выполнение запроса для получения всех офисов
            banks_office_data = cursor.fetchall()  # Получение всех записей

            # Возвращаем список экземпляров моделей BankOfficeModel для каждого банка
            return [BankOfficeModel(*data) for data in banks_office_data]

    def update(self, office_id, **kwargs):
        """
        Обновляет данные об офисе банка по его идентификатору. Обновляемые поля передаются как ключ-значение через kwargs.

        :param office_id: Идентификатор офиса
        :param kwargs: Пары "ключ-значение" для обновляемых полей
        """
        # Формируем строку полей для обновления
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE bank_offices SET {fields} WHERE bank_office_id = %s"
        params = list(kwargs.values()) + [office_id]  # Параметры для запроса

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполнение запроса на обновление
        self.connection.commit()  # Применение изменений

        return self.read(office_id)

    def delete(self, office_id):
        """
        Удаляет офис банка по его идентификатору. Также обновляет информацию о количестве офисов в банке.

        :param office_id: Идентификатор офиса
        """
        with self.connection.cursor() as cursor:
            # Получаем идентификатор банка, к которому привязан офис
            query = "SELECT bank_id FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (office_id,))
            bank_id = cursor.fetchone()  # Получаем результат запроса

            # Уменьшаем количество офисов в банке
            query = """
                UPDATE banks SET num_offices = num_offices - 1 WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))

            # Удаляем офис
            query = "DELETE FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (office_id,))
        self.connection.commit()  # Применение изменений

        return f"Office with ID {office_id} deleted."
