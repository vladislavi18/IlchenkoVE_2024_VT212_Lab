class UserModel:
    def __init__(self, user_id=None, full_name=None, birth_date=None, job=None, monthly_income=None,
                 banks=None, credit_rating=None):
        """
        Конструктор класса UserModel.
        Инициализирует объект пользователя с атрибутами:
        :param user_id: Уникальный идентификатор пользователя (по умолчанию None)
        :param full_name: Полное имя пользователя (по умолчанию None)
        :param birth_date: Дата рождения пользователя (по умолчанию None)
        :param job: Должность или работа пользователя (по умолчанию None)
        :param monthly_income: Ежемесячный доход пользователя (по умолчанию None)
        :param banks: Список банков, с которыми связан пользователь (по умолчанию None)
        :param credit_rating: Кредитный рейтинг пользователя (по умолчанию None)
        """
        # Уникальный идентификатор пользователя
        self.user_id = user_id

        # Полное имя пользователя
        self.full_name = full_name

        # Дата рождения пользователя
        self.birth_date = birth_date

        # Должность или работа пользователя
        self.job = job

        # Ежемесячный доход пользователя
        self.monthly_income = monthly_income

        # Список банков, с которыми связан пользователь
        self.banks = banks

        # Кредитный рейтинг пользователя
        self.credit_rating = credit_rating

    def __repr__(self):
        """
        Метод для представления объекта класса в виде строки.
        Используется для удобного вывода и отладки.
        :return: Строковое представление объекта UserModel
        """
        return (
            f"UserModel({self.user_id}, {self.full_name}, {self.birth_date}, {self.job}, "
            f"{self.monthly_income}, {self.banks}, {self.credit_rating})"
        )
