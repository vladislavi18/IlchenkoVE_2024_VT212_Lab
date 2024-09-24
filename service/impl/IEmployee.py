from abc import ABC, abstractmethod

from entity.employeeModel import EmployeeModel


class IEmployee(ABC):
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
    def create(self, full_name, birth_date, position, bank_id, works_remotely, bank_office_id,
               can_provide_credit, salary):
        pass

    @abstractmethod
    def read(self, employee_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, employee_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, employee_id):
        pass
