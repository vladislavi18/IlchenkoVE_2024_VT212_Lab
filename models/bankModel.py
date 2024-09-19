class BankModel:
    def __init__(self, bank_id=None, name=None, num_offices=0, num_atms=0, num_employees=0, num_clients=0, rating=0,
                 total_money=0, interest_rate=0.0):
        self.bank_id = bank_id
        self.name = name
        self.num_offices = num_offices
        self.num_atms = num_atms
        self.num_employees = num_employees
        self.num_clients = num_clients
        self.rating = rating
        self.total_money = total_money
        self.interest_rate = interest_rate

    def __repr__(self):
        return (
            f"BankModel({self.bank_id}, {self.name}, {self.num_offices}, {self.num_atms}, {self.num_employees}, {self.num_clients}"
            f"{self.rating}, {self.total_money}, {self.interest_rate})")
