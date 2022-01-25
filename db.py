import sqlite3


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('account.db')
        self.cur = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts
                (
                    username text PRIMARY KEY,
                    password text
                )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS apps
                (
                    app_name text,
                    username text,
                    FOREIGN KEY(username) REFERENCES accounts(username)
                )
        """)
        self.connection.commit()

    def insert_data(self, table_name: str, list_data: list):
        values = ''
        for data in range(0, len(list_data[0])):
            values += "?"
            if data <= len(list_data)-1:
                values += ", "

        str1 = f"{table_name} VALUES({values})"
        query = "INSERT INTO " + str1
        # print(query)

        try:
            self.cur.executemany(query, list_data)
            self.connection.commit()
            return 0
        except sqlite3.IntegrityError as error:
            # import sys, os
            # print(f"Error occurred! Error msg:\n{error}")
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, file_name, exc_tb.tb_lineno, "\nSaved error in error.log")
            return 1
        except sqlite3.OperationalError as error:
            return 2

    def fetch_data(self, table_name: str):
        query = "SELECT * FROM " + table_name
        self.cur.execute(query)
        return self.cur.fetchall()

    def fetch_account_password(self, account_name: str):
        query = "SELECT * FROM accounts WHERE username=" + '"' + account_name + '"'
        self.cur.execute(query)
        return self.cur.fetchone()

    def delete_data_from_accounts(self, username: str):
        query = 'DELETE FROM accounts WHERE username="' + username + '"'
        print(query)
        self.cur.execute(query)
        self.connection.commit()
        print('Account removed successfully!')

    def close_connection(self):
        self.connection.close()
        print("Connection Closed Successfully")



