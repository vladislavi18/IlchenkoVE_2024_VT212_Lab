import math


class User:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = '''
                CREATE TABLE users (
                    user_id SERIAL PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    birth_date DATE NOT NULL,
                    job VARCHAR(255),
                    monthly_income DECIMAL(10, 2) CHECK (monthly_income <= 10000),
                    banks VARCHAR(255)[],
                    credit_rating INT CHECK (credit_rating BETWEEN 100 AND 1000),
                    UNIQUE(full_name, birth_date)
                );
                '''
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                    DROP TABLE users CASCADE;
                """

            cursor.execute(query)
        self.connection.commit()

    def create(self, full_name, birth_date, job, monthly_income, banks):
        credit_rating = math.ceil(monthly_income / 1000) * 100

        with self.connection.cursor() as cursor:
            query = """
                INSERT INTO users (full_name, birth_date, job, monthly_income, banks, credit_rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                full_name, birth_date, job, monthly_income, banks, credit_rating))

            for bank in banks:
                query = """
                            SELECT bank_id FROM banks WHERE name = %s
                            """
                cursor.execute(query, (bank,))
                bank_id = cursor.fetchone()

                query = """
                            UPDATE banks SET num_clients = num_clients + 1 WHERE bank_id = %s
                            """
                cursor.execute(query, (bank_id,))
        self.connection.commit()

    def read(self, user_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM users"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, user_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE users SET {fields} WHERE user_id = %s"
        params = list(kwargs.values()) + [user_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, user_id):
        with self.connection.cursor() as cursor:
            query = """
                    SELECT banks FROM users WHERE user_id = %s        
            """
            cursor.execute(query, (user_id,))
            banks = cursor.fetchall()

            for bank in banks:
                query = """
                            SELECT * FROM banks WHERE name = %s
                            """
                bank_id = cursor.execute(query, (bank,))

                query = """
                            UPDATE banks SET num_clients = num_clients - 1 WHERE bank_id = %s
                            """
                cursor.execute(query, (bank_id,))

            query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
        self.connection.commit()
