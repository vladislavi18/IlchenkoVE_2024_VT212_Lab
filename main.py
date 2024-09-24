import psycopg2

from service.Bank import Bank
from service.BankAtm import BankAtm
from service.BankOffice import BankOffice
from service.CreditAccount import CreditAccount
from service.Employee import Employee
from service.PaymentAccount import PaymentAccount
from service.User import User

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="root1324",
    host="localhost",
    port="5432"
)

bank = Bank(connection)
bank_office = BankOffice(connection)
bank_atm = BankAtm(connection)
credit_account = CreditAccount(connection)
employee = Employee(connection)
payment_account = PaymentAccount(connection)
user = User(connection)

bank.drop_table()
bank.create_table()
bank.create("Sberbank")

bank_office.drop_table()
bank_office.create_table()
bank_office.create("office", "ul puskina dom kolotushkina", "working", True, True, True, True, 10.0, 1)
bank_office.create("office", "ul puskina dom kolotushkina", "working", True, True, True, True, 10.0, 1)

bank_atm.drop_table()
bank_atm.create_table()
bank_atm.create("Ya", "working", 1, 1, 1, True, True, 11.0)
bank_atm.create("Ya", "working", 1, 1, 1, True, True, 11.0)

user.drop_table()
user.create_table()
user.create("full name", '2023-03-22', "job", 7500, ["Sberbank"])
user.create("full name", '2023-03-22', "job", 7500, ["Sberbank"])

employee.drop_table()
employee.create_table()
employee.create("full name", '2023-03-22', "job", 1, True, 1, True, 10000)
employee.create("full name", '2023-03-22', "job", 1, True, 1, True, 10000)

payment_account.drop_table()
payment_account.create_table()
payment_account.create(1, "Sberbank", 0)
payment_account.create(1, "Sberbank", 0)

credit_account.drop_table()
credit_account.create_table()
credit_account.create(1, "Sberbank", "2023-03-22", "2023-03-24", 10, 1000000, 100000, 1, 1)
credit_account.create(1, "Sberbank", "2023-03-22", "2023-03-24", 10, 1000000, 100000, 1, 1)

print("Bank", bank.list())
print("BankOffice", bank_office.list())
print("BankAtm", bank_atm.list())
print("CreditAccount", credit_account.list())
print("Employee", employee.list())
print("PaymentAccount", payment_account.list())
print("User", user.list())
connection.close()
