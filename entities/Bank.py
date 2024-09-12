import random


class Bank:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = """
                CREATE TABLE banks (
                    bank_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    num_offices INT DEFAULT 0,
                    num_atms INT DEFAULT 0,
                    num_employees INT DEFAULT 0,
                    num_clients INT DEFAULT 0,
                    rating INT NOT NULL CHECK (rating >= 0 AND rating <= 100),
                    total_money INT NOT NULL CHECK (total_money >= 0 AND total_money <= 1000000),
                    interest_rate FLOAT NOT NULL CHECK (interest_rate >= 0 AND interest_rate <= 20)
                );
            """
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE banks CASCADE;
            """

            cursor.execute(query)
        self.connection.commit()

    def create(self, name):
        rating = random.randint(0, 100)
        total_money = random.randint(0, 1000000)
        interest_rate = random.uniform(0, 20)

        if rating > 80:
            interest_rate *= 0.5
        elif rating > 60:
            interest_rate *= 0.7
        elif rating > 40:
            interest_rate *= 0.9

        with self.connection.cursor() as cursor:
            query = """
                INSERT INTO banks (name, num_offices, num_atms, num_employees, num_clients, rating, total_money, interest_rate)
                VALUES (%s, 0, 0, 0, 0, %s, %s, %s)
            """
            cursor.execute(query, (name, rating, total_money, round(interest_rate, 2)))
        self.connection.commit()

    def read(self, bank_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM banks"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, bank_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE banks SET {fields} WHERE bank_id = %s"
        params = list(kwargs.values()) + [bank_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, bank_id):
        with self.connection.cursor() as cursor:
            query = "DELETE FROM banks WHERE bank_id = %s"
            cursor.execute(query, (bank_id,))
        self.connection.commit()
