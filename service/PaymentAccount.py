from service.impl.IPaymentAccount import IPaymentAccount
from entity.paymentAccountModel import PaymentAccountModel


class PaymentAccount(IPaymentAccount):
    def __init__(self, connection):
        """
        Инициализация класса PaymentAccount. Принимает объект connection для работы с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'payment_accounts' в базе данных. Таблица хранит информацию о платежных счетах, включая:
        - Идентификатор пользователя (user_id)
        - Название банка (bank_name)
        - Баланс счета
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для создания таблицы 'payment_accounts'
            query = '''
                CREATE TABLE payment_accounts (
                payment_account_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор платежного счета (генерируется автоматически)
                user_id INT NOT NULL,  -- Идентификатор пользователя (внешний ключ)
                bank_name VARCHAR(255) NOT NULL,  -- Название банка
                balance DECIMAL(10, 2) DEFAULT 0.00,  -- Баланс счета, по умолчанию 0.00
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE  -- Ссылка на таблицу 'users', удаление с каскадом
            );
            '''
            cursor.execute(query)  # Выполняем SQL-запрос для создания таблицы
        self.connection.commit()  # Сохраняем изменения в базе данных

    def drop_table(self):
        """
        Удаляет таблицу 'payment_accounts' вместе с зависимыми объектами.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE payment_accounts CASCADE;
            """
            cursor.execute(query)  # Выполняем SQL-запрос для удаления таблицы
        self.connection.commit()  # Сохраняем изменения

    def create(self, user_id, bank_name, balance=0):
        """
        Создает новый платежный счет для пользователя и сохраняет его в базе данных.

        :param user_id: Идентификатор пользователя
        :param bank_name: Название банка
        :param balance: Начальный баланс счета, по умолчанию 0
        """
        with self.connection.cursor() as cursor:
            # Вставляем новую запись о платёжном счете в таблицу 'payment_accounts'
            query = """
                INSERT INTO payment_accounts (user_id, bank_name, balance)
                VALUES (%s, %s, %s)
                RETURNING payment_account_id
            """
            cursor.execute(query, (user_id, bank_name, balance))
            payment_account_id = cursor.fetchone()[0]
        self.connection.commit()  # Сохраняем изменения

        return PaymentAccountModel(payment_account_id, user_id, bank_name, balance)

    def read(self, account_id):
        """
        Возвращает данные о платежном счете по его идентификатору.

        :param account_id: Идентификатор платежного счета
        :return: Данные о счете в виде кортежа или None, если счет не найден
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM payment_accounts WHERE payment_account_id = %s"
            cursor.execute(query, (account_id,))
            data = cursor.fetchone()  # Получение первой записи

            if data:
                return PaymentAccountModel(*data)
            return None

    def list(self):
        """
        Возвращает список всех платежных счетов.

        :return: Список всех платежных счетов в виде кортежей
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM payment_accounts"
            cursor.execute(query)
            payment_accounts_data = cursor.fetchall()

            return [PaymentAccountModel(*data) for data in payment_accounts_data]

    def update(self, account_id, **kwargs):
        """
        Обновляет данные о платежном счете по его идентификатору. Поля для обновления передаются через kwargs.

        :param account_id: Идентификатор платежного счета
        :param kwargs: Пары "ключ-значение" для обновляемых полей
        """
        # Формируем строку полей для обновления
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE payment_accounts SET {fields} WHERE payment_account_id = %s"
        params = list(kwargs.values()) + [account_id]  # Параметры для запроса

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполняем запрос на обновление записи
        self.connection.commit()  # Сохраняем изменения

        return self.read(account_id)

    def delete(self, account_id):
        """
        Удаляет платежный счет по его идентификатору.

        :param account_id: Идентификатор платежного счета
        """
        with self.connection.cursor() as cursor:
            # Удаляем запись о платежном счете из таблицы 'payment_accounts'
            query = "DELETE FROM payment_accounts WHERE payment_account_id = %s"
            cursor.execute(query, (account_id,))
        self.connection.commit()  # Сохраняем изменения

        return f"Paymeny Account with ID {account_id} deleted."
