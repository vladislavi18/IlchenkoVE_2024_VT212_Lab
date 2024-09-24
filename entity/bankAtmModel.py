class BankAtmModel:
    def __init__(self, atm_id, name, address, status, bank_id, bank_office_id, employee_id, dispense_money,
                 accept_money, money_in_atm, maintenance_cost):
        """
        Инициализация модели AtmModel, которая представляет собой объект данных банкомата.

        :param atm_id: Идентификатор банкомата
        :param name: Название банкомата
        :param address: Адрес банкомата
        :param status: Статус банкомата
        :param bank_id: Идентификатор банка
        :param bank_office_id: Идентификатор офиса банка
        :param employee_id: Идентификатор сотрудника, ответственного за банкомат
        :param dispense_money: Возможность выдачи денег (True или False)
        :param accept_money: Возможность приема денег (True или False)
        :param money_in_atm: Количество денег в банкомате
        :param maintenance_cost: Затраты на обслуживание банкомата
        """
        self.atm_id = atm_id
        self.name = name
        self.address = address
        self.status = status
        self.bank_id = bank_id
        self.bank_office_id = bank_office_id
        self.employee_id = employee_id
        self.dispense_money = dispense_money
        self.accept_money = accept_money
        self.money_in_atm = money_in_atm
        self.maintenance_cost = maintenance_cost

    def __repr__(self):
        return (f'<BankAtmModel: {self.atm_id}, {self.name}, {self.address}, {self.status}, {self.bank_id}, '
                f'{self.bank_office_id}, {self.employee_id}, {self.dispense_money}, {self.accept_money}, '
                f'{self.money_in_atm}, {self.maintenance_cost}>')
