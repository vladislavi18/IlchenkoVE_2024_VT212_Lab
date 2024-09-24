class CreditAccountModel:
    def __init__(self, credit_account_id=None, user_id=None, bank_name=None, start_date=None, end_date=None,
                 loan_duration_months=None, loan_amount=None, monthly_payment=None, interest_rate=None,
                 employee_id=None, payment_account_id=None):
        self.credit_account_id = credit_account_id
        self.user_id = user_id
        self.bank_name = bank_name
        self.start_date = start_date
        self.end_date = end_date
        self.loan_duration_months = loan_duration_months
        self.loan_amount = loan_amount
        self.monthly_payment = monthly_payment
        self.interest_rate = interest_rate
        self.employee_id = employee_id
        self.payment_account_id = payment_account_id
