from abc import ABC, abstractmethod

from models.bankOfficeModel import BankOfficeModel


class IBankOffice(ABC):
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
    def create(self, name, address, status, can_place_atm, can_provide_credit, dispense_money,
               accept_money, rent_cost, bank_id):
        pass

    @abstractmethod
    def read(self, office_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, office_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, office_id):
        pass
