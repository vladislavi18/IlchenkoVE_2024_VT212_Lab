import random  # Импортируем модуль random для генерации случайных значений

from entity.bankAtmModel import BankAtmModel
from entity.bankOfficeModel import BankOfficeModel
from entity.employeeModel import EmployeeModel
from entity.userModel import UserModel
from service.impl.IBank import IBank
from entity.bankModel import BankModel


class Bank(IBank):
    def __init__(self, connection):
        """
        Инициализация класса Bank. Принимает объект connection, который используется для
        подключения к базе данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'banks' в базе данных с полями для хранения информации о банках,
        включая идентификатор банка, название, количество офисов, банкоматов, сотрудников,
        клиентов, рейтинг, общую сумму денег и процентную ставку.
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для создания таблицы
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
            cursor.execute(query)  # Выполнение SQL-запроса на создание таблицы
        self.connection.commit()  # Применение изменений в базе данных

    def drop_table(self):
        """
        Удаляет таблицу 'banks' из базы данных, если она существует.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE IF EXISTS banks CASCADE;
            """
            cursor.execute(query)  # Выполнение SQL-запроса на удаление таблицы
        self.connection.commit()  # Применение изменений в базе данных

    def create(self, name):
        """
        Создает новый банк с заданным именем и случайными значениями для рейтинга, общей суммы денег
        и процентной ставки. Процентная ставка корректируется в зависимости от рейтинга.

        :param name: Название банка.
        :return: Возвращает экземпляр модели BankModel с данными нового банка.
        """
        # Генерация случайных значений для рейтинга, общей суммы денег и процентной ставки
        rating = random.randint(0, 100)
        total_money = random.randint(0, 1000000)
        interest_rate = random.uniform(0, 20)

        # Корректировка процентной ставки в зависимости от рейтинга
        if rating > 80:
            interest_rate *= 0.5
        elif rating > 60:
            interest_rate *= 0.7
        elif rating > 40:
            interest_rate *= 0.9

        with self.connection.cursor() as cursor:
            # SQL-запрос для вставки нового банка
            query = """
                INSERT INTO banks (name, num_offices, num_atms, num_employees, num_clients, rating, total_money, interest_rate)
                VALUES (%s, 0, 0, 0, 0, %s, %s, %s)
                RETURNING bank_id
            """
            cursor.execute(query, (name, rating, total_money, round(interest_rate, 2)))  # Вставка данных в таблицу
            bank_id = cursor.fetchone()[0]  # Получение идентификатора нового банка
        self.connection.commit()  # Применение изменений в базе данных

        # Возвращаем экземпляр модели BankModel с данными о новом банке
        return BankModel(bank_id, name, 0, 0, 0, 0, rating, total_money, round(interest_rate, 2))

    def read(self, bank_id):
        """
        Получает информацию о банке по его ID.

        :param bank_id: Идентификатор банка.
        :return: Экземпляр модели BankModel с данными банка или None, если банк не найден.
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для получения данных банка по его ID
            query = "SELECT * FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
            data = cursor.fetchone()  # Получение первой записи

            # Если банк найден, возвращаем экземпляр модели BankModel
            if data:
                return BankModel(*data)
            return None  # Если банк не найден, возвращаем None

    def list(self):
        """
        Возвращает список всех банков, хранящихся в базе данных.

        :return: Список объектов BankModel для каждого банка.
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для получения всех данных о банках
            query = "SELECT * FROM banks"
            cursor.execute(query)
            banks_data = cursor.fetchall()  # Получение всех записей

            # Возвращаем список экземпляров моделей BankModel для каждого банка
            return [BankModel(*data) for data in banks_data]

    def update(self, bank_id, **kwargs):
        """
        Обновляет информацию о банке по его ID. Передаваемые параметры задают поля для обновления.

        :param bank_id: Идентификатор банка, который нужно обновить.
        :param kwargs: Поля, которые нужно обновить (в формате ключ-значение).
        :return: Возвращает экземпляр модели BankModel с обновленными данными банка.
        """
        # Формирование строки для обновления полей (ключ = значение)
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE banks SET {fields} WHERE bank_id = %s"
        params = list(kwargs.values()) + [bank_id]  # Параметры для обновления

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполнение запроса на обновление
        self.connection.commit()  # Применение изменений в базе данных

        # Получаем обновленные данные после изменения и возвращаем обновленную модель
        return self.read(bank_id)

    def delete(self, bank_id):
        """
        Удаляет банк из базы данных по его ID.

        :param bank_id: Идентификатор банка, который нужно удалить.
        :return: Сообщение, подтверждающее удаление банка.
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для удаления банка по его ID
            query = "DELETE FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
        self.connection.commit()  # Применение изменений в базе данных

        # Возвращаем подтверждение удаления банка
        return f"Bank with ID {bank_id} deleted."

    def __get_all_bankATMs_from_banks(self, bank_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
            atms_data = cursor.fetchall()
        self.connection.commit()

        return [BankAtmModel(*data) for data in atms_data]

    def __get_all_bankOffices_from_banks(self, bank_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM bank_offices WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
            banks_office_data = cursor.fetchall()
        self.connection.commit()

        return [BankOfficeModel(*data) for data in banks_office_data]

    def __get_all_employees_from_banks(self, bank_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM employees WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
            employees_data = cursor.fetchall()
        self.connection.commit()

        return [EmployeeModel(*data) for data in employees_data]

    def __get_all_users_from_banks(self, bank_id):
        with self.connection.cursor() as cursor:
            query = """SELECT name FROM banks WHERE bank_id = %s"""
            cursor.execute(query, (bank_id,))
            bank_name = cursor.fetchone()[0]

            query = "SELECT * FROM users WHERE banks @> %s::varchar[]"
            cursor.execute(query, (f'{{{bank_name}}}',))
            user_data = cursor.fetchall()

        self.connection.commit()

        return [UserModel(*data) for data in user_data]

    def get_all_info_about_bank(self, bank_id):
        bank_atms = self.__get_all_bankATMs_from_banks(bank_id)
        bank_offices = self.__get_all_bankOffices_from_banks(bank_id)
        employees = self.__get_all_employees_from_banks(bank_id)
        users = self.__get_all_users_from_banks(bank_id)

        print("bank_atms:", bank_atms, "\nbank_offices:", bank_offices, "\nemployees:", employees, "\nusers:", users)
