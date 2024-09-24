from service.impl.IEmployee import IEmployee
from entity.employeeModel import EmployeeModel


class Employee(IEmployee):
    def __init__(self, connection):
        """
        Инициализация класса Employee. Принимает объект connection для работы с базой данных.
        """
        self.connection = connection

    def create_table(self):
        """
        Создает таблицу 'employees' в базе данных. Таблица содержит информацию о сотрудниках, включая:
        - ФИО
        - Дату рождения
        - Должность
        - Связанный банк (bank_id)
        - Признак удаленной работы
        - Связанный банк/офис (bank_office_id)
        - Возможность предоставления кредита
        - Зарплату
        """
        with self.connection.cursor() as cursor:
            # SQL-запрос для создания таблицы 'employees'
            query = '''
                CREATE TABLE employees (
                employee_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор сотрудника (генерируется автоматически)
                full_name VARCHAR(255) NOT NULL,  -- Полное имя сотрудника
                birth_date DATE NOT NULL,  -- Дата рождения сотрудника
                position VARCHAR(255) NOT NULL,  -- Должность сотрудника
                bank_id INT NOT NULL,  -- Идентификатор банка, где работает сотрудник (внешний ключ)
                works_remotely BOOLEAN NOT NULL,  -- Флаг удаленной работы
                bank_office_id INT NOT NULL,  -- Идентификатор банковского офиса (внешний ключ)
                can_provide_credit BOOLEAN NOT NULL,  -- Флаг возможности выдачи кредита
                salary DECIMAL(7, 2) NOT NULL,  -- Зарплата сотрудника
                FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE,  -- Ссылка на таблицу 'banks', удаление с каскадом
                FOREIGN KEY (bank_office_id) REFERENCES bank_offices(bank_office_id) ON DELETE SET NULL  -- Ссылка на офис банка
            );
            '''
            cursor.execute(query)  # Выполняем SQL-запрос для создания таблицы
        self.connection.commit()  # Сохраняем изменения в базе данных

    def drop_table(self):
        """
        Удаляет таблицу 'employees' вместе с зависимыми объектами.
        """
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE employees CASCADE;
            """
            cursor.execute(query)  # Выполняем SQL-запрос для удаления таблицы
        self.connection.commit()  # Сохраняем изменения

    def create(self, full_name, birth_date, position, bank_id, works_remotely, bank_office_id,
               can_provide_credit, salary):
        """
        Создает нового сотрудника и сохраняет его в базе данных.

        :param full_name: Полное имя сотрудника
        :param birth_date: Дата рождения
        :param position: Должность сотрудника
        :param bank_id: Идентификатор банка, где работает сотрудник
        :param works_remotely: Флаг удаленной работы (True/False)
        :param bank_office_id: Идентификатор офиса банка
        :param can_provide_credit: Возможность предоставления кредита (True/False)
        :param salary: Зарплата сотрудника
        """
        with self.connection.cursor() as cursor:
            # Вставляем новую запись о сотруднике в таблицу 'employees'
            query = """
                INSERT INTO employees (full_name, birth_date, position, bank_id, works_remotely, bank_office_id, can_provide_credit, salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING employee_id
            """
            cursor.execute(query, (
                full_name, birth_date, position, bank_id, works_remotely, bank_office_id, can_provide_credit,
                salary))
            employee_id = cursor.fetchone()[0]

            # Обновляем количество сотрудников в таблице 'banks'
            query = """
                UPDATE banks SET num_employees = num_employees + 1 WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))
        self.connection.commit()  # Сохраняем изменения

        return EmployeeModel(employee_id, full_name, birth_date, position, bank_id, works_remotely, bank_office_id,
                             can_provide_credit, salary)

    def read(self, employee_id):
        """
        Возвращает данные о сотруднике по его идентификатору.

        :param employee_id: Идентификатор сотрудника
        :return: Данные о сотруднике в виде кортежа или None, если сотрудник не найден
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            data = cursor.fetchone()  # Получение первой записи

            # Если банк найден, возвращаем экземпляр модели BankModel
            if data:
                return EmployeeModel(*data)
            return None

    def list(self):
        """
        Возвращает список всех сотрудников.

        :return: Список всех сотрудников в виде кортежей
        """
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM employees"
            cursor.execute(query)  # Выполняем запрос для получения всех записей из таблицы 'employees'
            employees_data = cursor.fetchall()  # Получение всех записей

            # Возвращаем список экземпляров моделей BankModel для каждого банка
            return [EmployeeModel(*data) for data in employees_data]

    def update(self, employee_id, **kwargs):
        """
        Обновляет данные о сотруднике по его идентификатору. Поля для обновления передаются через kwargs.

        :param employee_id: Идентификатор сотрудника
        :param kwargs: Пары "ключ-значение" для обновляемых полей
        """
        # Формируем строку полей для обновления
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE employees SET {fields} WHERE employee_id = %s"
        params = list(kwargs.values()) + [employee_id]  # Параметры для запроса

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполняем запрос на обновление записи
        self.connection.commit()  # Сохраняем изменения

        return self.read(employee_id)

    def delete(self, employee_id):
        """
        Удаляет сотрудника по его идентификатору.

        :param employee_id: Идентификатор сотрудника
        """
        with self.connection.cursor() as cursor:
            # Получаем идентификатор банка, к которому относится сотрудник
            query = "SELECT bank_id FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            bank_id = cursor.fetchone()

            # Обновляем количество сотрудников в банке, уменьшая на 1
            query = """
                UPDATE banks SET num_employees = num_employees - 1 WHERE bank_id = %s
            """
            cursor.execute(query, (bank_id,))

            # Удаляем запись о сотруднике из таблицы 'employees'
            query = "DELETE FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
        self.connection.commit()  # Сохраняем изменения

        return f"Employee with ID {employee_id} deleted."
