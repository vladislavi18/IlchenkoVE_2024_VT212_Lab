class PaymentAccount:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = '''
                CREATE TABLE payment_accounts (
                payment_account_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                bank_name VARCHAR(255) NOT NULL,
                balance DECIMAL(10, 2) DEFAULT 0.00,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
                '''
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                    DROP TABLE payment_accounts CASCADE;
                """

            cursor.execute(query)
        self.connection.commit()

    def create(self, user_id, bank_name, balance=0):
        with self.connection.cursor() as cursor:
            query = """
                INSERT INTO payment_accounts (user_id, bank_name, balance)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, bank_name, balance))
        self.connection.commit()

    def read(self, account_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM payment_accounts WHERE account_id = %s"
            cursor.execute(query, (account_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM payment_accounts"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, account_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE payment_accounts SET {fields} WHERE account_id = %s"
        params = list(kwargs.values()) + [account_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, account_id):
        with self.connection.cursor() as cursor:
            query = "DELETE FROM payment_accounts WHERE account_id = %s"
            cursor.execute(query, (account_id,))
        self.connection.commit()
