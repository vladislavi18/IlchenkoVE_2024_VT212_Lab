from abc import ABC, abstractmethod


class IBankAtm(ABC):
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
    def create(self, name, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money,
               maintenance_cost):
        pass

    @abstractmethod
    def read(self, atm_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, atm_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, atm_id):
        pass
