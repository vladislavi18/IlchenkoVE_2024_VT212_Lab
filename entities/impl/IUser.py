import math
from abc import ABC, abstractmethod

from models.userModel import UserModel


class IUser(ABC):
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
    def create(self, full_name, birth_date, job, monthly_income, banks):
        pass

    @abstractmethod
    def read(self, user_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, user_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
