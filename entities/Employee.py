class Employee:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = '''
                CREATE TABLE employees (
                employee_id SERIAL PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                birth_date DATE NOT NULL,
                position VARCHAR(255) NOT NULL,
                bank_id INT NOT NULL,
                works_remotely BOOLEAN NOT NULL,
                bank_office_id INT NOT NULL,
                can_provide_credit BOOLEAN NOT NULL,
                salary DECIMAL(7, 2) NOT NULL,
                FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE,
                FOREIGN KEY (bank_office_id) REFERENCES bank_offices(bank_office_id) ON DELETE SET NULL
            );
                '''
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                    DROP TABLE employees CASCADE;
                """

            cursor.execute(query)
        self.connection.commit()

    def create(self, full_name, birth_date, position, bank_id, works_remotely, bank_office_id,
               can_provide_credit, salary):
        with self.connection.cursor() as cursor:
            query = """
                INSERT INTO employees (full_name, birth_date, position, bank_id, works_remotely, bank_office_id, can_provide_credit, salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                full_name, birth_date, position, bank_id, works_remotely, bank_office_id, can_provide_credit,
                salary))

            query = """
                        UPDATE banks SET num_employees = num_employees + 1 WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))
        self.connection.commit()

    def read(self, employee_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM employees"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, employee_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE employees SET {fields} WHERE employee_id = %s"
        params = list(kwargs.values()) + [employee_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, employee_id):
        with self.connection.cursor() as cursor:
            query = "SELECT bank_id FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            bank_id = cursor.fetchone()

            query = """
                        UPDATE banks SET num_employees = num_employees - 1 WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))

            query = "DELETE FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
        self.connection.commit()
