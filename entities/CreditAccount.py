class CreditAccount:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = '''
            CREATE TABLE credit_accounts (
                credit_account_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                bank_name VARCHAR(255) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE,
                loan_duration_months INTEGER NOT NULL,
                loan_amount FLOAT NOT NULL,
                monthly_payment FLOAT NOT NULL,
                interest_rate FLOAT NOT NULL,
                employee_id INT NOT NULL,
                payment_account_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
                FOREIGN KEY (payment_account_id) REFERENCES payment_accounts(payment_account_id)
            );
            '''
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE credit_accounts CASCADE;
            """

            cursor.execute(query)
        self.connection.commit()

    def create(self, user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount,
               monthly_payment, employee_id, payment_account_id):
        with self.connection.cursor() as cursor:
            query = """
                SELECT interest_rate FROM banks WHERE name = %s
            """
            cursor.execute(query, (bank_name,))
            interest_rate = cursor.fetchone()

            query = """
                INSERT INTO credit_accounts (user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount, monthly_payment, interest_rate, employee_id, payment_account_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                user_id, bank_name, start_date, end_date, loan_duration_months, loan_amount,
                monthly_payment, interest_rate, employee_id, payment_account_id))
        self.connection.commit()

    def read(self, credit_account_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM credit_accounts WHERE credit_account_id = %s"
            cursor.execute(query, (credit_account_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM credit_accounts"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, credit_account_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE credit_accounts SET {fields} WHERE credit_account_id = %s"
        params = list(kwargs.values()) + [credit_account_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, credit_account_id):
        with self.connection.cursor() as cursor:
            query = "DELETE FROM credit_accounts WHERE credit_account_id = %s"
            cursor.execute(query, (credit_account_id,))
        self.connection.commit()
