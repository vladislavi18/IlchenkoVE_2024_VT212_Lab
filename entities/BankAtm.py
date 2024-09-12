class BankAtm:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = """
                CREATE TABLE atms (
                    atm_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    bank_id INT NOT NULL,
                    bank_office_id INT NOT NULL,
                    employee_id INT NOT NULL,
                    dispense_money BOOLEAN NOT NULL,
                    accept_money BOOLEAN NOT NULL,
                    money_in_atm INT DEFAULT 0,
                    maintenance_cost FLOAT NOT NULL,
                    FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE,
                    FOREIGN KEY (bank_office_id) REFERENCES bank_offices(bank_office_id) ON DELETE CASCADE
                );
            """
                    # FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
            cursor.execute(query)
        self.connection.commit()

    def drop_table(self):
        with self.connection.cursor() as cursor:
            query = """
                DROP TABLE atms CASCADE;
            """

            cursor.execute(query)
        self.connection.commit()

    def create(self, name, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money,
               maintenance_cost):
        with self.connection.cursor() as cursor:
            query = """
            SELECT address FROM bank_offices WHERE bank_office_id = %s
            """
            cursor.execute(query, (bank_office_id,))
            address = cursor.fetchone()

            query = """
                        SELECT total_money FROM banks WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))
            total_money = cursor.fetchone()

            query = """
                INSERT INTO atms (name, address, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money, money_in_atm, maintenance_cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, address, status, bank_id, bank_office_id, employee_id, dispense_money, accept_money, total_money,
                maintenance_cost))

            query = """
                        UPDATE banks SET num_atms = num_atms + 1 WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))

            query = """
                        UPDATE bank_offices SET num_atms = num_atms + 1 WHERE bank_office_id = %s
                        """
            cursor.execute(query, (bank_office_id,))
        self.connection.commit()

    def read(self, atm_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms WHERE atm_id = %s"
            cursor.execute(query, (atm_id,))
            return cursor.fetchone()

    def list(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM atms"
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, atm_id, **kwargs):
        fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE atms SET {fields} WHERE atm_id = %s"
        params = list(kwargs.values()) + [atm_id]

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def delete(self, atm_id):
        with self.connection.cursor() as cursor:
            query = "SELECT bank_id, bank_office_id FROM atms WHERE atm_id=%s"
            cursor.execute(query, (atm_id,))
            bank_id, bank_office_id = cursor.fetchone()

            query = """
                        UPDATE banks SET num_atms = num_atms - 1 WHERE bank_id = %s
                        """
            cursor.execute(query, (bank_id,))

            query = """
                        UPDATE bank_offices SET num_atms = num_atms - 1 WHERE bank_office_id = %s
                        """
            cursor.execute(query, (bank_office_id,))
            query = "DELETE FROM atms WHERE atm_id = %s"

            cursor.execute(query, (atm_id,))
        self.connection.commit()
