class BankModel:
    def __init__(self, bank_id=None, name=None, num_offices=0, num_atms=0, num_employees=0, num_clients=0, rating=0,
                 total_money=0, interest_rate=0.0):
        """
        Конструктор класса BankModel.
        Инициализирует экземпляр банка с атрибутами:
        :param bank_id: Уникальный идентификатор банка (по умолчанию None)
        :param name: Название банка (по умолчанию None)
        :param num_offices: Количество офисов банка (по умолчанию 0)
        :param num_atms: Количество банкоматов банка (по умолчанию 0)
        :param num_employees: Количество сотрудников банка (по умолчанию 0)
        :param num_clients: Количество клиентов банка (по умолчанию 0)
        :param rating: Рейтинг банка (по умолчанию 0)
        :param total_money: Общая сумма денег в банке (по умолчанию 0)
        :param interest_rate: Процентная ставка банка (по умолчанию 0.0)
        """
        # Уникальный идентификатор банка
        self.bank_id = bank_id

        # Название банка
        self.name = name

        # Количество офисов
        self.num_offices = num_offices

        # Количество банкоматов
        self.num_atms = num_atms

        # Количество сотрудников банка
        self.num_employees = num_employees

        # Количество клиентов банка
        self.num_clients = num_clients

        # Рейтинг банка
        self.rating = rating

        # Общая сумма денег в банке
        self.total_money = total_money

        # Процентная ставка банка
        self.interest_rate = interest_rate

    def __repr__(self):
        """
        Метод для представления объекта класса в виде строки.
        Используется для удобного вывода и отладки.
        :return: Строковое представление объекта BankModel
        """
        # Форматированная строка с перечислением всех атрибутов объекта
        return (
            f"BankModel({self.bank_id}, {self.name}, {self.num_offices}, {self.num_atms}, {self.num_employees}, {self.num_clients}, "
            f"{self.rating}, {self.total_money}, {self.interest_rate})"
        )



