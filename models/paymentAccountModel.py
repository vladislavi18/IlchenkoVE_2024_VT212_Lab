class PaymentAccountModel:
    def __init__(self, payment_account_id=None, user_id=None, bank_name=None, balance=None):
        self.payment_account_id = payment_account_id
        self.user_id = user_id
        self.bank_name = bank_name
        self.balance = balance
