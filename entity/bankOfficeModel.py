class BankOfficeModel:

    def __init__(self, bank_office_id=None, name=None, address=None, status=None, can_place_atm=None,
                 num_atms=0, can_provide_credit=None, dispense_money=None, accept_money=None,
                 money_in_office=0, rent_cost=None, bank_id=None):
        """
        Конструктор класса BankOfficeModel.
        Инициализирует экземпляр банковского офиса с атрибутами:
        :param bank_office_id: Уникальный идентификатор офиса банка (по умолчанию None)
        :param name: Название офиса банка (по умолчанию None)
        :param address: Адрес офиса (по умолчанию None)
        :param status: Статус офиса (открыт, закрыт и т.д.) (по умолчанию None)
        :param can_place_atm: Возможность установки банкомата в офисе (по умолчанию None)
        :param num_atms: Количество банкоматов в офисе (по умолчанию 0)
        :param can_provide_credit: Возможность выдачи кредитов в офисе (по умолчанию None)
        :param dispense_money: Возможность выдачи денег в офисе (по умолчанию None)
        :param accept_money: Возможность приёма денег в офисе (по умолчанию None)
        :param money_in_office: Количество денег в офисе (по умолчанию 0)
        :param rent_cost: Стоимость аренды офиса (по умолчанию None)
        :param bank_id: Уникальный идентификатор банка, к которому принадлежит офис (по умолчанию None)
        """
        # Уникальный идентификатор офиса банка
        self.bank_office_id = bank_office_id

        # Название офиса банка
        self.name = name

        # Адрес офиса
        self.address = address

        # Статус офиса (например, открыт, закрыт)
        self.status = status

        # Возможность установки банкоматов в офисе
        self.can_place_atm = can_place_atm

        # Количество банкоматов в офисе
        self.num_atms = num_atms

        # Возможность предоставления кредитов в офисе
        self.can_provide_credit = can_provide_credit

        # Возможность выдачи денег в офисе
        self.dispense_money = dispense_money

        # Возможность приёма денег в офисе
        self.accept_money = accept_money

        # Количество денег в офисе
        self.money_in_office = money_in_office

        # Стоимость аренды офиса
        self.rent_cost = rent_cost

        # Идентификатор банка, к которому относится офис
        self.bank_id = bank_id

    def __repr__(self):
        """
        Метод для представления объекта класса в виде строки.
        Используется для удобного вывода и отладки.
        :return: Строковое представление объекта BankOfficeModel
        """
        return (
            f"BankOfficeModel({self.bank_office_id}, {self.name}, {self.address}, {self.status}, {self.can_place_atm}, "
            f"{self.num_atms}, {self.can_provide_credit}, {self.dispense_money}, {self.accept_money}, "
            f"{self.money_in_office}, {self.rent_cost}, {self.bank_id})"
        )
