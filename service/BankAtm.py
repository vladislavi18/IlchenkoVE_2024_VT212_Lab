from service.impl.IBankAtm import IBankAtm
from entity.bankAtmModel import BankAtmModel


class BankAtm(IBankAtm):
    def __init__(self, connection):
        """
        Инициализация класса BankAtm. Принимает объект connection для взаимодействия с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'atms' в базе данных для хранения информации о банкоматах.
        """
        with self.connection.cursor() as cursor:
            query = """
                CREATE TABLE atms (
                    atm_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    bank_id INT NOT NULL,
                    bank_office_id INT NOT NULL,
                    employee_id INT NOT NULL,
                    dispense_money BOOLEAN NOT NULL,
                    accept_money BOOLEAN NOT NULL,
                    money_in_atm INT DEFAULT 0,
                    maintenance_cost FLOAT NOT NULL,
                    FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE,
                    FOREIGN KEY (bank_office_id) REFERENCES bank_offices(bank_office_id) ON DELETE CASCADE,
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
                );
            """
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        """
        Удаляет таблицу 'atms' вместе с её зависимостями.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE atms CASCADE;
            """
            cursor.execute(query)
        self.connection.commit()

    def create(self, name, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money,
               maintenance_cost):
        """
        Создает новый банкомат, добавляет его в базу данных и возвращает объект модели AtmModel.
        """
        with self.connection.cursor() as cursor:
            # Получаем адрес офиса банка
            query = "SELECT address FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (bank_office_id,))
            address = cursor.fetchone()[0]

            # Получаем количество денег в банке
            query = "SELECT total_money FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
            total_money = cursor.fetchone()[0]

            # Вставляем данные банкомата
            query = """
                INSERT INTO atms (name, address, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money, money_in_atm, maintenance_cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING atm_id
            """
            cursor.execute(query, (
                name, address, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money, total_money,
                maintenance_cost))
            atm_id = cursor.fetchone()[0]

            # Обновляем количество банкоматов в банке и офисе
            cursor.execute("UPDATE banks SET num_atms = num_atms + 1 WHERE bank_id = %s", (bank_id,))
            cursor.execute("UPDATE bank_offices SET num_atms = num_atms + 1 WHERE bank_office_id = %s",
                           (bank_office_id,))

        self.connection.commit()

        # Возвращаем экземпляр модели с данными нового банкомата
        return BankAtmModel(atm_id, name, address, status, bank_id, bank_office_id, employee_id, dispense_money,
                            accept_money, total_money, maintenance_cost)

    def read(self, atm_id):
        """
        Возвращает данные о банкомате в виде объекта модели AtmModel по его идентификатору.
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms WHERE atm_id = %s"
            cursor.execute(query, (atm_id,))
            data = cursor.fetchone()

            if data:
                return BankAtmModel(*data)  # Возвращаем объект модели с данными банкомата
            return None

    def list(self):
        """
        Возвращает список всех банкоматов в виде объектов модели AtmModel.
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms"
            cursor.execute(query)
            atms_data = cursor.fetchall()

            # Возвращаем список объектов модели
            return [BankAtmModel(*data) for data in atms_data]

    def update(self, atm_id, **kwargs):
        """
        Обновляет данные банкомата по его идентификатору и возвращает обновленный объект модели AtmModel.
        """
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE atms SET {fields} WHERE atm_id = %s"
        params = list(kwargs.values()) + [atm_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

        # Возвращаем обновленный объект модели после обновления
        return self.read(atm_id)

    def delete(self, atm_id):
        """
        Удаляет банкомат по его идентификатору и обновляет информацию о количестве банкоматов в банке и офисе.
        """
        with self.connection.cursor() as cursor:
            # Получаем идентификаторы банка и офиса
            query = "SELECT bank_id, bank_office_id FROM atms WHERE atm_id=%s"
            cursor.execute(query, (atm_id,))
            bank_id, bank_office_id = cursor.fetchone()

            # Обновляем количество банкоматов в банке и офисе
            cursor.execute("UPDATE banks SET num_atms = num_atms - 1 WHERE bank_id = %s", (bank_id,))
            cursor.execute("UPDATE bank_offices SET num_atms = num_atms - 1 WHERE bank_office_id = %s",
                           (bank_office_id,))

            # Удаляем банкомат
            cursor.execute("DELETE FROM atms WHERE atm_id = %s", (atm_id,))
        self.connection.commit()

        # Возвращаем подтверждение удаления
        return f"ATM with ID {atm_id} deleted."
