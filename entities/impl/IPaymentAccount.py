from abc import ABC, abstractmethod

from models.paymentAccountModel import PaymentAccountModel


class IPaymentAccount(ABC):
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
    def create(self, user_id, bank_name, balance=0):
        pass

    @abstractmethod
    def read(self, account_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, account_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, account_id):
        pass