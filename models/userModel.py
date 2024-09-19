class UserModel:
    def __init__(self, user_id=None, full_name=None, birth_date=None, job=None, monthly_income=None,
                 banks=None, credit_rating=None):
        self.user_id = user_id
        self.full_name = full_name
        self.birth_date = birth_date
        self.job = job
        self.monthly_income = monthly_income
        self.banks = banks
        self.credit_rating = credit_rating
