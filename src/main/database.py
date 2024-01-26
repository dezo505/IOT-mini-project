import sqlite3
from collections import namedtuple
from datetime import datetime


class EmployeeDatabase:

    Employee = namedtuple('Employee', ['id', 'name', 'lastname', 'card_pid'])
    CardEvent = namedtuple('CardEvent', ['card_pid', 'employee_id', 'timestamp', 'access_granted'])

    def __init__(self, db_file='employee_database.db'):
        self.db_file = db_file

    def init_database(self):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS EMPLOYEES (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        lastname TEXT,
                        card_pid INTEGER UNIQUE
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS CARD_EVENTS (
                        card_pid INTEGER,
                        employee_id INTEGER,
                        timestamp DATETIME,
                        access_granted BOOLEAN,
                        FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(id),
                        PRIMARY KEY (card_pid, timestamp)
                    )
                ''')

                connection.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def add_employee(self, name, lastname, card_pid=None):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    INSERT INTO EMPLOYEES (name, lastname, card_pid)
                    VALUES (?, ?, ?)
                ''', (name, lastname, card_pid))

                connection.commit()
                print("Employee added successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error adding employee: {e}")
            return False

    def add_card_event(self, card_pid, employee_id=None, timestamp=None, access_granted=False):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                if isinstance(timestamp, datetime):
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute('''
                    INSERT INTO CARD_EVENTS (card_pid, employee_id, timestamp, access_granted)
                    VALUES (?, ?, ?, ?)
                ''', (card_pid, employee_id, timestamp, access_granted))

                connection.commit()
                print("Card event added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding card event: {e}")

    def update_employee(self, employee_id, name=None, lastname=None, card_pid=None):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                update_query = 'UPDATE EMPLOYEES SET '
                update_params = []

                if name is not None:
                    update_query += 'name=?, '
                    update_params.append(name)

                if lastname is not None:
                    update_query += 'lastname=?, '
                    update_params.append(lastname)

                if card_pid is not None:
                    update_query += 'card_pid=?, '
                    update_params.append(card_pid)

                update_query = update_query.rstrip(', ')
                update_query += ' WHERE id=?'
                update_params.append(employee_id)

                cursor.execute(update_query, tuple(update_params))
                connection.commit()

                print("Employee updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating employee: {e}")

    def find_employee(self, employee_id):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT * FROM EMPLOYEES
                    WHERE id=?
                ''', (employee_id,))

                result = cursor.fetchone()
                return self.Employee(*result) if result else None
        except sqlite3.Error as e:
            print(f"Error finding employee: {e}")

    def find_all_employees(self):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT * FROM EMPLOYEES
                ''')

                result = cursor.fetchall()
                return [self.Employee(*row) for row in result]
        except sqlite3.Error as e:
            print(f"Error finding all employees: {e}")

    def find_all_card_events_after(self, timestamp):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                if isinstance(timestamp, datetime):
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute('''
                    SELECT * FROM CARD_EVENTS
                    WHERE timestamp > ?
                ''', (timestamp,))

                result = cursor.fetchall()
                return [self.CardEvent(*row) for row in result]
        except sqlite3.Error as e:
            print(f"Error finding card events after {timestamp}: {e}")

    def find_all_card_events_between(self, start_timestamp, finish_timestamp):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                if isinstance(start_timestamp, datetime):
                    start_timestamp = start_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                if isinstance(finish_timestamp, datetime):
                    finish_timestamp = finish_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute('''
                    SELECT * FROM CARD_EVENTS
                    WHERE timestamp BETWEEN ? AND ?
                ''', (start_timestamp, finish_timestamp))

                result = cursor.fetchall()
                return [self.CardEvent(*row) for row in result]
        except sqlite3.Error as e:
            print(f"Error finding card events between {start_timestamp} and {finish_timestamp}: {e}")

    def get_all_card_events(self):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT * FROM CARD_EVENTS
                ''')

                result = cursor.fetchall()
                return [self.CardEvent(*row) for row in result]
        except sqlite3.Error as e:
            print(f"Error getting all card events: {e}")

    def find_employee_by_card_pid(self, card_pid):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT * FROM EMPLOYEES
                    WHERE card_pid=?
                ''', (card_pid,))

                result = cursor.fetchone()
                return self.Employee(*result) if result else None
        except sqlite3.Error as e:
            print(f"Error finding employee by card pid {card_pid}: {e}")

    def clear_database(self):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()

                cursor.execute('DELETE FROM EMPLOYEES')

                cursor.execute('DELETE FROM CARD_EVENTS')

                connection.commit()

            print("Database reset successfully.")
        except sqlite3.Error as e:
            print(f"Error resetting database: {e}")
