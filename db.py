import os
import sqlite3
import sys


def raiseException(err):
    print(err)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, file_name, exc_tb.tb_lineno)


class DB:
    def __init__(self):
        self.cur = None
        self.connection = None
        self.create_table()

    def make_connection(self):
        self.connection = sqlite3.connect('account.db')
        self.cur = self.connection.cursor()

    def create_table(self):
        self.make_connection()
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
                    app_name text PRIMARY KEY,
                    type text,
                    link text,
                    username text,
                    last_content_date text,
                    subscriber_count text,
                    FOREIGN KEY(username) REFERENCES accounts(username)
                )
        """)
        self.connection.commit()
        self.close_connection()

    def insert_data(self, table_name: str, list_data: list):    # Info: list_data is a list of tuples
        self.make_connection()
        values = ''
        for data in range(0, len(list_data[0])):
            values += "?"
            if data <= len(list_data[0])-2:
                values += ", "

        str1 = f"{table_name} VALUES({values})"
        query = "INSERT INTO " + str1
        # print(query, list_data)

        try:
            self.cur.executemany(query, list_data)
            self.connection.commit()
            self.close_connection()
            return 0
        except sqlite3.IntegrityError as error:
            # import sys, os
            # print(f"Error occurred! Error msg:\n{error}")
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, file_name, exc_tb.tb_lineno, "\nSaved error in error.log")
            self.close_connection()
            return 1
        except sqlite3.OperationalError as error:
            self.close_connection()
            raiseException(error)
            return 2

    def fetch_data(self, table_name: str):
        try:
            self.make_connection()
            query = "SELECT * FROM " + table_name
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.close_connection()
            return data
        except Exception as e:
            print(e)

    def fetch_account_password(self, account_name: str):
        self.make_connection()
        query = "SELECT * FROM accounts WHERE username=" + '"' + account_name + '"'
        self.cur.execute(query)
        data = self.cur.fetchone()
        self.close_connection()
        return data

    def fetch_all_apps(self, account_name: str):
        self.make_connection()
        query = "SELECT * FROM apps WHERE username=" + '"' + account_name + '"'
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.close_connection()
        return data

    def delete_data_from_accounts(self, username: str):
        self.make_connection()
        query = 'DELETE FROM accounts WHERE username="' + username + '"'
        print(query)
        try:
            self.cur.execute(query)
            self.connection.commit()
            print('Account removed successfully!')
        except Exception as e:
            print(e)
        self.close_connection()

    def delete_data_from_apps(self, username: str, app_name: str):
        self.make_connection()
        query = 'DELETE FROM apps WHERE username="' + username + '"' + 'AND app_name="' + app_name + '"'
        try:
            self.cur.execute(query)
            self.connection.commit()
            print('App removed successfully!')
            self.close_connection()
            return True
        except Exception as e:
            print("Some error occurred", e)
            self.close_connection()
            return False

    def delete_all_apps(self, username: str):
        query = 'DELETE FROM apps WHERE username="' + username + '"'
        self.make_connection()
        try:
            self.cur.execute(query)
            self.connection.commit()
            print('All Apps were removed successfully!')
            self.close_connection()
            return True
        except Exception as e:
            print("Some error occurred", e)
            self.close_connection()
            return False

    def update_app_link(self, data):
        self.make_connection()
        query = f'UPDATE apps SET link="{data[1]}" WHERE app_name="{data[0]}"'
        try:
            self.cur.execute(query)
            self.connection.commit()
            self.close_connection()
            return 0
        except sqlite3.OperationalError:
            self.close_connection()
            return -1
        except Exception as e:
            self.close_connection()
            print(f"This '{e}' error occurred!")

    def update_app_detail(self, data: dict):
        self.make_connection()
        print(data)
        try:
            data_app_name = list(data.keys())[0]
            data_field = data[data_app_name][0]
            data_value = data[data_app_name][1]

            query = f'UPDATE apps SET {data_field}="{data_value}" WHERE app_name="{data_app_name}"'

            self.cur.execute(query)
            self.connection.commit()
            self.close_connection()
            return 0
        except sqlite3.OperationalError:
            self.close_connection()
            return -1
        except Exception as e:
            self.close_connection()
            print(f"This '{e}' error occurred!")

    def close_connection(self):
        self.connection.close()



