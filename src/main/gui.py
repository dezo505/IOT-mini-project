from config import *

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from card_detector import CardDetector
from database import EmployeeDatabase

import RPi.GPIO as GPIO

db = EmployeeDatabase()
db.init_database()

cancel = False

def buttonPressedCallback(channel):
    global cancel
    cancel = True

GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)

class AddEmployeeWindow:
    def __init__(self, master, callback):
        self.master = master
        self.master.title("Dodaj pracownika")
        self.card_detector = CardDetector()

        self.callback = callback

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.name_label = tk.Label(self.frame, text="Imię:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.lastname_label = tk.Label(self.frame, text="Nazwisko:")
        self.lastname_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
        self.lastname_entry = tk.Entry(self.frame)
        self.lastname_entry.grid(row=1, column=1, padx=10, pady=5)

        self.card_pid_label = tk.Label(self.frame, text="Numer karty:")
        self.card_pid_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.card_pid_entry = tk.Entry(self.frame)
        self.card_pid_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_employee_button = tk.Button(self.frame, text="Dodaj pracownika", command=self.add_employee)
        self.add_employee_button.grid(row=3, column=1, columnspan=2, pady=10)

        self.read_card_button = tk.Button(self.frame, text="Czytaj kartę", command=self.read_card)
        self.read_card_button.grid(row=4, column=1, columnspan=2, pady=10)

    def read_card(self):
        global cancel
        cancel = False
        card_detector = CardDetector()

        messagebox.showinfo("Information","Przyłóż kartę lub wciśnij czerwony przycisk, aby anulować")

        reading = card_detector.read_card()

        while not reading.result and not cancel:
            reading = card_detector.read_card()

        if cancel:
            cancel = False
            return

        self.card_pid_entry.insert(0, reading.card_pid)
        

    def add_employee(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        card_pid = self.card_pid_entry.get()

        if name and lastname and card_pid:
            self.callback(name, lastname, card_pid)
            self.master.destroy()
        else:
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane.")



class EmployeeLogWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Logi pracowników")

        self.employee_db = db

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.log_treeview = ttk.Treeview(self.frame, columns=("Timestamp", "Numer Karty", "Status Dostępu"),
                                         show="headings")
        self.log_treeview.grid(row=0, column=0, padx=10, pady=10)

        self.log_treeview.heading("Timestamp", text="Timestamp")
        self.log_treeview.heading("Numer Karty", text="Numer Karty")
        self.log_treeview.heading("Status Dostępu", text="Status Dostępu")

        self.close_button = tk.Button(self.frame, text="Zamknij", command=self.master.destroy)
        self.close_button.grid(row=1, column=0, pady=5)

        self.populate_logs()

    def populate_logs(self):
        card_events = self.employee_db.get_all_card_events()

        for event in card_events:
            self.log_treeview.insert("", "end", values=(
                event.timestamp, event.card_pid, 'Przyznano dostęp' if event.access_granted else 'odmowa dostępu'))


class EmployeeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Pracownicy")

        self.employee_db = db

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.employee_treeview = ttk.Treeview(self.frame, columns=("ID", "Imię", "Nazwisko", "Numer Karty"),
                                              show="headings")
        self.employee_treeview.grid(row=0, column=0, padx=10, pady=10)

        self.employee_treeview.heading("ID", text="ID")
        self.employee_treeview.heading("Imię", text="Imię")
        self.employee_treeview.heading("Nazwisko", text="Nazwisko")
        self.employee_treeview.heading("Numer Karty", text="Numer Karty")

        self.close_button = tk.Button(self.frame, text="Zamknij", command=self.master.destroy)
        self.close_button.grid(row=1, column=0, pady=5)

        self.populate_employees()

    def populate_employees(self):
        employees = self.employee_db.find_all_employees()

        for employee in employees:
            self.employee_treeview.insert("", "end",
                                          values=(employee.id, employee.name, employee.lastname, employee.card_pid))


class EmployeeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Database App")
        self.master.geometry("400x300")

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.add_employee_button = tk.Button(self.frame, text="Dodaj pracownika", command=self.open_add_employee_window)
        self.add_employee_button.grid(row=0, column=0, pady=5)

        self.show_logs_button = tk.Button(self.frame, text="Wyświetl logi", command=self.open_log_window)
        self.show_logs_button.grid(row=1, column=0, pady=5)

        self.show_employees_button = tk.Button(self.frame, text="Wyświetl pracowników",
                                               command=self.open_employees_window)
        self.show_employees_button.grid(row=2, column=0, pady=5)

        self.exit_button = tk.Button(self.frame, text="Wyjście z programu", command=self.master.destroy)
        self.exit_button.grid(row=3, column=0, pady=5)

        self.employee_db = db

    def open_add_employee_window(self):
        add_employee_window = tk.Toplevel(self.master)
        add_employee_window.grab_set()
        AddEmployeeWindow(add_employee_window, self.add_employee)

    def open_log_window(self):
        log_window = tk.Toplevel(self.master)
        log_window.grab_set()
        EmployeeLogWindow(log_window)

    def open_employees_window(self):
        employees_window = tk.Toplevel(self.master)
        employees_window.grab_set()
        EmployeeWindow(employees_window)

    def add_employee(self, name, lastname, card_pid):
        result = self.employee_db.add_employee(name, lastname, card_pid)
        if result:
            messagebox.showinfo("Sukces", f"Dodano pracownika: {name} {lastname}, pid: {card_pid}")
        else:
            messagebox.showwarning("Błąd", f"Nie udało dodać się pracownika: {name} {lastname}, pid: {card_pid}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()
