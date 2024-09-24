from service.impl.ICreditAccount import ICreditAccount
from entity.creditAccountModel import CreditAccountModel


class CreditAccount(ICreditAccount):
    def __init__(self, connection):
        """
        Инициализация класса CreditAccount. Принимает объект connection для работы с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'credit_accounts' в базе данных. Таблица содержит информацию о кредитных счетах,
        включая: идентификатор пользователя, название банка, дату начала и конца кредита,
        продолжительность кредита в месяцах, сумму кредита, ежемесячные платежи, процентную ставку,
        идентификаторы сотрудника и связанного платежного счета.
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для создания таблицы 'credit_accounts'
            query = '''
            CREATE TABLE credit_accounts (
                credit_account_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор кредитного счета (генерируется автоматически)
                user_id INT NOT NULL,  -- Идентификатор пользователя (внешний ключ)
                bank_name VARCHAR(255) NOT NULL,  -- Название банка
                start_date DATE NOT NULL,  -- Дата начала кредита
                end_date DATE,  -- Дата окончания кредита (может быть NULL для незакрытых счетов)
                loan_duration_months INTEGER NOT NULL,  -- Продолжительность кредита в месяцах
                loan_amount FLOAT NOT NULL,  -- Сумма кредита
                monthly_payment FLOAT NOT NULL,  -- Ежемесячный платеж
                interest_rate FLOAT NOT NULL,  -- Процентная ставка
                employee_id INT NOT NULL,  -- Идентификатор сотрудника, который открыл кредит (внешний ключ)
                payment_account_id INT NOT NULL,  -- Идентификатор связанного платежного счета (внешний ключ)
                FOREIGN KEY (user_id) REFERENCES users(user_id),  -- Ссылка на пользователя
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),  -- Ссылка на сотрудника
                FOREIGN KEY (payment_account_id) REFERENCES payment_accounts(payment_account_id)  -- Ссылка на платежный счет
            );
            '''
            cursor.execute(query)  # Выполняем SQL-запрос для создания таблицы
        self.connection.commit()  # Сохраняем изменения в базе данных

    def drop_table(self):
        """
        Удаляет таблицу 'credit_accounts' вместе с зависимыми объектами.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE credit_accounts CASCADE;
            """
            cursor.execute(query)  # Выполняем SQL-запрос для удаления таблицы
        self.connection.commit()  # Сохраняем изменения

    def create(self, user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount,
               monthly_payment, employee_id, payment_account_id):
        """
        Создает новый кредитный счет и сохраняет его в базе данных.

        :param user_id: Идентификатор пользователя
        :param bank_name: Название банка
        :param start_date: Дата начала кредита
        :param end_date: Дата окончания кредита
        :param loan_duration_months: Продолжительность кредита в месяцах
        :param loan_amount: Сумма кредита
        :param monthly_payment: Ежемесячный платеж
        :param employee_id: Идентификатор сотрудника, который оформил кредит
        :param payment_account_id: Идентификатор связанного платежного счета
        """
        with self.connection.cursor() as cursor:
            # Получаем процентную ставку по названию банка
            query = """
                SELECT interest_rate FROM banks WHERE name = %s
            """
            cursor.execute(query, (bank_name,))
            interest_rate = cursor.fetchone()  # Получаем процентную ставку из запроса

            # Вставляем новую запись о кредитном счете в таблицу 'credit_accounts'
            query = """
                INSERT INTO credit_accounts (user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount, 
                                             monthly_payment, interest_rate, employee_id, payment_account_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING credit_account_id
            """
            cursor.execute(query, (
                user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount,
                monthly_payment, interest_rate, employee_id, payment_account_id))
            credit_accounts_id = cursor.fetchone()[0]
        self.connection.commit()  # Сохраняем изменения
        return CreditAccountModel(credit_accounts_id, user_id, bank_name, start_date, end_date, loan_duration_months,
                                  loan_amount, monthly_payment, interest_rate, employee_id, payment_account_id)

    def read(self, credit_account_id):
        """
        Возвращает данные о кредитном счете по его идентификатору.

        :param credit_account_id: Идентификатор кредитного счета
        :return: Данные о кредитном счете в виде кортежа или None, если счет не найден
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM credit_accounts WHERE credit_account_id = %s"
            cursor.execute(query, (credit_account_id,))
            data = cursor.fetchone()  # Получение первой записи

            if data:
                return CreditAccountModel(*data)
            return None

    def list(self):
        """
        Возвращает список всех кредитных счетов.

        :return: Список всех кредитных счетов в виде кортежей
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM credit_accounts"
            cursor.execute(query)  # Выполняем запрос для получения всех записей из таблицы
            credits_account_data = cursor.fetchall()  # Получение всех записей

            # Возвращаем список экземпляров моделей BankModel для каждого банка
            return [CreditAccountModel(*data) for data in credits_account_data]

    def update(self, credit_account_id, **kwargs):
        """
        Обновляет данные о кредитном счете по его идентификатору. Поля для обновления передаются через kwargs.

        :param credit_account_id: Идентификатор кредитного счета
        :param kwargs: Пары "ключ-значение" для обновляемых полей
        """
        # Формируем строку полей для обновления
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE credit_accounts SET {fields} WHERE credit_account_id = %s"
        params = list(kwargs.values()) + [credit_account_id]  # Параметры для запроса

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполняем запрос на обновление записи
        self.connection.commit()  # Сохраняем изменения

        return self.read(credit_account_id)

    def delete(self, credit_account_id):
        """
        Удаляет кредитный счет по его идентификатору.

        :param credit_account_id: Идентификатор кредитного счета
        """
        with self.connection.cursor() as cursor:
            query = "DELETE FROM credit_accounts WHERE credit_account_id = %s"
            cursor.execute(query, (credit_account_id,))  # Выполняем запрос на удаление записи
        self.connection.commit()  # Сохраняем изменения
        return f"Credit account with ID {credit_account_id} deleted."
