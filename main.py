import random
import psycopg2
from data import *
from entity.employeeModel import EmployeeModel
from service.Bank import Bank
from service.BankAtm import BankAtm
from service.BankOffice import BankOffice
from service.CreditAccount import CreditAccount
from service.Employee import Employee
from service.PaymentAccount import PaymentAccount
from service.User import User


class BankDataFiller:
    def __init__(self, connection_params):
        self.connection = psycopg2.connect(**connection_params)
        self.banks = []
        self.bank_offices = []
        self.bank_atms = []
        self.employees = []
        self.users = []
        self.payment_accounts = []
        self.credit_accounts = []

        # Сервисы
        self.bank = Bank(self.connection)
        self.bank_office = BankOffice(self.connection)
        self.bank_atm = BankAtm(self.connection)
        self.credit_account = CreditAccount(self.connection)
        self.employee = Employee(self.connection)
        self.payment_account = PaymentAccount(self.connection)
        self.user = User(self.connection)

        # Параметры
        self.count_bank_offices = 3
        self.count_bank_atms = 3
        self.count_employees = 5
        self.count_fill_users = 5
        self.count_credit_payments_accounts = 2
        self.count_users = 0

        # Создание и очистка таблиц
        self._init_db()

    def _init_db(self):
        """
        Инициализация базы данных: создание и очистка таблиц.
        """
        self.bank.drop_table()
        self.bank.create_table()

        self.bank_office.drop_table()
        self.bank_office.create_table()

        self.bank_atm.drop_table()
        self.bank_atm.create_table()

        self.user.drop_table()
        self.user.create_table()

        self.employee.drop_table()
        self.employee.create_table()

        self.payment_account.drop_table()
        self.payment_account.create_table()

        self.credit_account.drop_table()
        self.credit_account.create_table()

    def fill_bank_offices(self, bank_id, bank_office_id):
        address = random.choice(addresses)
        self.bank_offices.append(
            self.bank_office.create(
                f"office{self.count_bank_offices * bank_id + bank_office_id}",
                address,
                random.choice(["working", "not working"]),
                random.choice([True, False]), random.choice([True, False]),
                random.choice([True, False]), random.choice([True, False]),
                random.uniform(10.0, 100.0), self.banks[bank_id].bank_id
            )
        )
        addresses.remove(address)

    def fill_employees(self, bank_id, bank_office_id):
        positions_copy = positions.copy()
        full_names_copy = full_names.copy()
        birth_dates_copy = birth_dates.copy()

        for k in range(self.count_employees):
            full_name = random.choice(full_names_copy)
            birth_date = random.choice(birth_dates_copy)
            position = random.choice(positions_copy)

            self.employees.append(
                self.employee.create(
                    full_name, birth_date, position, self.banks[bank_id].bank_id,
                    random.choice([True, False]), self.bank_offices[bank_office_id].bank_office_id,
                    random.choice([True, False]), random.randint(10000, 100000)
                )
            )

            full_names_copy.remove(full_name)
            birth_dates_copy.remove(birth_date)
            positions_copy.remove(position)

    def fill_bank_atms(self, bank_id, bank_office_id, empl):
        self.bank_atms.append(
            self.bank_atm.create(
                f"BankATM{bank_office_id}",
                random.choice(["working", "not working", "no money"]),
                self.banks[bank_id].bank_id, self.bank_offices[bank_office_id].bank_office_id,
                empl.employee_id, random.choice([True, False]), random.choice([True, False]),
                random.uniform(1.0, 10.0)
            )
        )

    def fill_users(self, bank_id, empl):
        for k in range(self.count_fill_users):
            self.users.append(self.user.create(
                f"User{self.count_users}", '1987-03-22', f"job{self.count_users}",
                random.randint(0, 10000), [banks_str[bank_id]]
            ))
            self.count_users += 1

            for m in range(self.count_credit_payments_accounts):
                self.payment_accounts.append(
                    self.payment_account.create(self.count_users, banks_str[bank_id], random.randint(0, 100000))
                )
                self.credit_accounts.append(
                    self.credit_account.create(
                        self.count_users, banks_str[bank_id], "2023-03-22", "2024-03-24",
                        random.randint(2, 20), random.randint(100000, 10000000),
                        random.randint(1000, 100000), empl.employee_id,
                        self.payment_accounts[m].payment_account_id
                    )
                )
        self.employees.remove(empl)

    def fill_models(self):
        for i in range(len(banks_str)):
            self.banks.append(self.bank.create(banks_str[i]))
            for j in range(self.count_bank_offices):
                self.fill_bank_offices(i, j)
                self.fill_employees(i, j)

                empl: EmployeeModel = random.choice(self.employees)  # Используем явно, чтобы взять ID сотрудника

                self.fill_bank_atms(i, j, empl)
                self.fill_users(i, empl)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    connection_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "root1324",
        "host": "localhost",
        "port": "5432"
    }

    filler = BankDataFiller(connection_params)
    filler.fill_models()
    filler.bank.get_all_info_about_bank(1)
    filler.user.get_all_info_about_user(1)
    filler.close_connection()
