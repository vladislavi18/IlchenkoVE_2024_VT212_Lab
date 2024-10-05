class PaymentAccountModel:
    def __init__(self, payment_account_id=None, user_id=None, bank_name=None, balance=None):
        """
        Конструктор класса PaymentAccountModel.
        Инициализирует объект платежного аккаунта с атрибутами:
        :param payment_account_id: Уникальный идентификатор платежного аккаунта (по умолчанию None)
        :param user_id: Идентификатор пользователя, которому принадлежит аккаунт (по умолчанию None)
        :param bank_name: Название банка, в котором открыт аккаунт (по умолчанию None)
        :param balance: Баланс платежного аккаунта (по умолчанию None)
        """
        # Уникальный идентификатор платежного аккаунта
        self.payment_account_id = payment_account_id

        # Идентификатор пользователя, которому принадлежит аккаунт
        self.user_id = user_id

        # Название банка, в котором открыт аккаунт
        self.bank_name = bank_name

        # Баланс платежного аккаунта
        self.balance = balance

    def __repr__(self):
        """
        Метод для представления объекта класса в виде строки.
        Используется для удобного вывода и отладки.
        :return: Строковое представление объекта PaymentAccountModel
        """
        return (
            f"PaymentAccountModel({self.payment_account_id}, {self.user_id}, "
            f"{self.bank_name}, {self.balance})"
        )
