class BankOfficeModel:
    """
    Модель для представления офисов банка. Содержит атрибуты, соответствующие столбцам таблицы 'bank_offices'.
    """

    def __init__(self, bank_office_id=None, name=None, address=None, status=None, can_place_atm=None,
                 num_atms=0, can_provide_credit=None, dispense_money=None, accept_money=None,
                 money_in_office=0, rent_cost=None, bank_id=None):
        self.bank_office_id = bank_office_id
        self.name = name
        self.address = address
        self.status = status
        self.can_place_atm = can_place_atm
        self.num_atms = num_atms
        self.can_provide_credit = can_provide_credit
        self.dispense_money = dispense_money
        self.accept_money = accept_money
        self.money_in_office = money_in_office
        self.rent_cost = rent_cost
        self.bank_id = bank_id
