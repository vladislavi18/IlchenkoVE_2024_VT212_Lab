class EmployeeModel:
    def __init__(self, employee_id=None, full_name=None, birth_date=None, position=None, bank_id=None,
                 works_remotely=None, bank_office_id=None, can_provide_credit=None, salary=None):
        self.employee_id = employee_id
        self.full_name = full_name
        self.birth_date = birth_date
        self.position = position
        self.bank_id = bank_id
        self.works_remotely = works_remotely
        self.bank_office_id = bank_office_id
        self.can_provide_credit = can_provide_credit
        self.salary = salary
