from abc import ABC, abstractmethod

from entity.creditAccountModel import CreditAccountModel


class ICreditAccount(ABC):
    @abstractmethod
    def __init__(self, connection):
        pass

    @abstractmethod
    def create_table(self):
        pass
    @abstractmethod
    def drop_table(self):
        pass

    @abstractmethod
    def create(self, user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount,
               monthly_payment, employee_id, payment_account_id):
        pass

    @abstractmethod
    def read(self, credit_account_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, credit_account_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, credit_account_id):
        pass
