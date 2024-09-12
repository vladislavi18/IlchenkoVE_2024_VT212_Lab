class BankOffice:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = """
                    CREATE TABLE bank_offices (
                        bank_office_id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        address VARCHAR(255) NOT NULL,
                        status VARCHAR(50) NOT NULL,
                        can_place_atm BOOLEAN NOT NULL,
                        num_atms INT DEFAULT 0,
                        can_provide_credit BOOLEAN NOT NULL,
                        dispense_money BOOLEAN NOT NULL,
                        accept_money BOOLEAN NOT NULL,
                        money_in_office INT DEFAULT 0,
                        rent_cost FLOAT NOT NULL,
                        bank_id INT NOT NULL,
                        FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE
                    );

                """
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE bank_offices CASCADE;
            """

            cursor.execute(query)
        self.connection.commit()

    def create(self, name, address, status, can_place_atm, can_provide_credit, dispense_money,
               accept_money, rent_cost, bank_id):
        with self.connection.cursor() as cursor:
            query = """
                        SELECT total_money FROM banks WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))
            total_money = cursor.fetchone()

            query = """
                INSERT INTO bank_offices (name, address, status, can_place_atm, num_atms, can_provide_credit, dispense_money, accept_money, money_in_office, rent_cost, bank_id)
                VALUES (%s, %s, %s, %s, 0, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, address, status, can_place_atm, can_provide_credit, dispense_money, accept_money,
                total_money, rent_cost, bank_id))

            query = """
                    UPDATE banks SET num_offices = num_offices + 1 WHERE bank_id = %s
                    """
            cursor.execute(query, (bank_id,))

        self.connection.commit()

    def read(self, office_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (office_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM bank_offices"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, office_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE bank_offices SET {fields} WHERE bank_office_id = %s"
        params = list(kwargs.values()) + [office_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, office_id):
        with self.connection.cursor() as cursor:
            query = "SELECT bank_id FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (office_id,))
            bank_id = cursor.fetchone()

            query = """
                        UPDATE banks SET num_offices = num_offices - 1 WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))

            query = "DELETE FROM bank_offices WHERE bank_office_id = %s"
            cursor.execute(query, (office_id,))
        self.connection.commit()
