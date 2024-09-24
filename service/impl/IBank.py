import random  # Импортируем модуль random для генерации случайных значений
from abc import ABC, abstractmethod

from entity.bankModel import BankModel


class IBank(ABC):
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
    def create(self, name):
        pass

    @abstractmethod
    def read(self, bank_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self, bank_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, bank_id):
        pass
