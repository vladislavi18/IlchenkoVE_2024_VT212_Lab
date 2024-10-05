class EmployeeModel:
    def __init__(self, employee_id=None, full_name=None, birth_date=None, position=None, bank_id=None,
                 works_remotely=None, bank_office_id=None, can_provide_credit=None, salary=None):
        """
        Конструктор класса EmployeeModel.
        Инициализирует объект работника банка с атрибутами:
        :param employee_id: Уникальный идентификатор работника (по умолчанию None)
        :param full_name: Полное имя работника (по умолчанию None)
        :param birth_date: Дата рождения работника (по умолчанию None)
        :param position: Должность работника (по умолчанию None)
        :param bank_id: Идентификатор банка, в котором работает работник (по умолчанию None)
        :param works_remotely: Признак, работающий ли работник удаленно (по умолчанию None)
        :param bank_office_id: Идентификатор офиса банка, в котором работает работник (по умолчанию None)
        :param can_provide_credit: Признак, может ли работник предоставлять кредиты (по умолчанию None)
        :param salary: Зарплата работника (по умолчанию None)
        """
        # Уникальный идентификатор работника
        self.employee_id = employee_id

        # Полное имя работника
        self.full_name = full_name

        # Дата рождения работника
        self.birth_date = birth_date

        # Должность работника в банке
        self.position = position

        # Идентификатор банка, в котором работает работник
        self.bank_id = bank_id

        # Признак, работает ли работник удаленно
        self.works_remotely = works_remotely

        # Идентификатор банка, где работает работник
        self.bank_office_id = bank_office_id

        # Признак, может ли работник предоставлять кредиты
        self.can_provide_credit = can_provide_credit

        # Зарплата работника
        self.salary = salary

    def __repr__(self):
        """
        Метод для представления объекта класса в виде строки.
        Используется для удобного вывода и отладки.
        :return: Строковое представление объекта EmployeeModel
        """
        return (
            f"EmployeeModel({self.employee_id}, {self.full_name}, {self.birth_date}, {self.position}, "
            f"{self.bank_id}, {self.works_remotely}, {self.bank_office_id}, {self.can_provide_credit}, "
            f"{self.salary})"
        )

