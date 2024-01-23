from datetime import datetime

from main.database import EmployeeDatabase


def example_usage():
    # Create a new instance of the EmployeeDatabase
    employee_db = EmployeeDatabase()

    # Initialize and clear the database
    employee_db.init_database()
    employee_db.clear_database()

    # Adding employees
    employee_db.add_employee("John", "Doe", card_pid=12345)
    employee_db.add_employee("Jake", "Smith", card_pid=12346)
    employee_db.add_employee("Olivia", "Hart", card_pid=12347)

    # Adding card events
    employee_db.add_card_event(card_pid=12345, employee_id=1, timestamp="2024-01-23 11:00:00", access_granted=True)
    employee_db.add_card_event(card_pid=12346, employee_id=2, timestamp=datetime(2024, 1, 23, 13, 0, 0), access_granted=True)
    employee_db.add_card_event(card_pid=12347, employee_id=3, timestamp="2024-01-23 14:00:00", access_granted=False)
    employee_db.add_card_event(card_pid=12348, employee_id=None, timestamp="2024-01-23 15:00:00", access_granted=False)

    # Finding an employee by card pid
    card_pid_to_find = 12346
    result_employee_by_card_pid = employee_db.find_employee_by_card_pid(card_pid_to_find)
    print(f"Found Employee with Card PID {card_pid_to_find}:", result_employee_by_card_pid)

    # Finding all card events between two timestamps
    all_card_events_between_timestamps = employee_db.find_all_card_events_between(datetime(2024, 1, 23, 12, 0, 0),
                                                                                  datetime(2024, 1, 23, 14, 30, 0))
    print("All Card Events Between Timestamps:", all_card_events_between_timestamps)

    # Finding all card events after timestamp
    all_card_events_after_timestamp = employee_db.find_all_card_events_after("2024-01-23 12:00:00")
    print("All Card Events after Timestamp:", all_card_events_between_timestamps)

    # Finding an employee
    result_employee = employee_db.find_employee(employee_id=1)
    print("Found Employee:", result_employee)

    # Finding all employees
    all_employees = employee_db.find_all_employees()
    print("All Employees:", all_employees)


if __name__ == "__main__":
    example_usage()
