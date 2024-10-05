class CreditAccountModel:
    def __init__(self, credit_account_id=None, user_id=None, bank_name=None, start_date=None, end_date=None,
                 loan_duration_months=None, loan_amount=None, monthly_payment=None, interest_rate=None,
                 employee_id=None, payment_account_id=None):
        """
        Конструктор класса CreditAccountModel.
        Инициализирует объект кредитного счета с атрибутами:
        :param credit_account_id: Уникальный идентификатор кредитного счета (по умолчанию None)
        :param user_id: Идентификатор пользователя, владеющего кредитом (по умолчанию None)
        :param bank_name: Название банка, выдавшего кредит (по умолчанию None)
        :param start_date: Дата начала кредита (по умолчанию None)
        :param end_date: Дата окончания кредита (по умолчанию None)
        :param loan_duration_months: Продолжительность кредита в месяцах (по умолчанию None)
        :param loan_amount: Сумма кредита (по умолчанию None)
        :param monthly_payment: Ежемесячный платеж по кредиту (по умолчанию None)
        :param interest_rate: Процентная ставка по кредиту (по умолчанию None)
        :param employee_id: Идентификатор сотрудника, оформившего кредит (по умолчанию None)
        :param payment_account_id: Идентификатор расчетного счета, связанного с кредитом (по умолчанию None)
        """
        # Уникальный идентификатор кредитного счета
        self.credit_account_id = credit_account_id

        # Идентификатор пользователя (владельца кредитного счета)
        self.user_id = user_id

        # Название банка, предоставившего кредит
        self.bank_name = bank_name

        # Дата начала кредита
        self.start_date = start_date

        # Дата окончания кредита
        self.end_date = end_date

        # Продолжительность кредита в месяцах
        self.loan_duration_months = loan_duration_months

        # Сумма кредита
        self.loan_amount = loan_amount

        # Ежемесячный платеж по кредиту
        self.monthly_payment = monthly_payment

        # Процентная ставка по кредиту
        self.interest_rate = interest_rate

        # Идентификатор сотрудника, оформившего кредит
        self.employee_id = employee_id

        # Идентификатор расчетного счета, связанного с кредитом
        self.payment_account_id = payment_account_id

    def __repr__(self):
        """
        Метод для представления объекта класса в виде строки.
        Используется для удобного вывода и отладки.
        :return: Строковое представление объекта CreditAccountModel
        """
        return (
            f"CreditAccountModel({self.credit_account_id}, {self.user_id}, {self.bank_name}, {self.start_date}, {self.end_date}, "
            f"{self.loan_duration_months}, {self.loan_amount}, {self.monthly_payment}, {self.interest_rate}, "
            f"{self.employee_id}, {self.payment_account_id})"
        )
