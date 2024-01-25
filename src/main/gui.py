import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import paho.mqtt.client as mqtt

from src.main.database import EmployeeDatabase

db = EmployeeDatabase()
db.init_database()


class AddEmployeeWindow:
    def __init__(self, master, callback, mqtt_client):
        self.master = master
        self.master.title("Dodaj pracownika")

        # Callback to the main window
        self.callback = callback

        # MQTT Client
        self.mqtt_client = mqtt_client

        # Frame
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        # Label i Entry dla imienia
        self.name_label = tk.Label(self.frame, text="Imię:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label i Entry dla nazwiska
        self.lastname_label = tk.Label(self.frame, text="Nazwisko:")
        self.lastname_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
        self.lastname_entry = tk.Entry(self.frame)
        self.lastname_entry.grid(row=1, column=1, padx=10, pady=5)

        # Label i Entry dla numeru karty
        self.card_pid_label = tk.Label(self.frame, text="Numer karty:")
        self.card_pid_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.card_pid_entry = tk.Entry(self.frame)
        self.card_pid_entry.grid(row=2, column=1, padx=10, pady=5)

        # Przycisk "Dodaj pracownika"
        self.add_employee_button = tk.Button(self.frame, text="Dodaj pracownika", command=self.add_employee)
        self.add_employee_button.grid(row=3, columnspan=2, pady=10)

        # Subskrybuj temat MQTT
        self.mqtt_client.subscribe("numer_karty")

        # Przypisz funkcję do obsługi nowych wiadomości MQTT
        self.mqtt_client.message_callback_add("numer_karty", self.on_card_number_received)

    def on_card_number_received(self, client, userdata, message):
        # Funkcja wywołana po odebraniu nowej wiadomości MQTT
        card_number = message.payload.decode("utf-8")
        self.card_pid_entry.delete(0, tk.END)  # Wyczyść aktualny numer karty
        self.card_pid_entry.insert(0, card_number)  # Wstaw nowy numer karty

    def add_employee(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        card_pid = self.card_pid_entry.get()

        if name and lastname and card_pid:
            # Wywołanie funkcji zwrotnej z danymi pracownika
            self.callback(name, lastname, card_pid)
            # Zamknięcie okna
            self.master.destroy()
        else:
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane.")


class EmployeeLogWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Logi pracowników")

        # Employee Database
        self.employee_db = db

        # Frame
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        # Treeview do wyświetlania logów
        self.log_treeview = ttk.Treeview(self.frame, columns=("Timestamp", "Numer Karty", "Status Dostępu"),
                                         show="headings")
        self.log_treeview.grid(row=0, column=0, padx=10, pady=10)

        # Ustaw nagłówki kolumn
        self.log_treeview.heading("Timestamp", text="Timestamp")
        self.log_treeview.heading("Numer Karty", text="Numer Karty")
        self.log_treeview.heading("Status Dostępu", text="Status Dostępu")

        # Przycisk "Zamknij"
        self.close_button = tk.Button(self.frame, text="Zamknij", command=self.master.destroy)
        self.close_button.grid(row=1, column=0, pady=5)

        # Wypełnij Treeview logami
        self.populate_logs()

    def populate_logs(self):
        # Pobierz wszystkie logi z bazy danych
        card_events = self.employee_db.get_all_card_events()

        # Wypełnij Treeview danymi
        for event in card_events:
            self.log_treeview.insert("", "end", values=(
                event.timestamp, event.card_pid, 'odczytana' if event.access_granted else 'odmowa dostępu'))


class EmployeeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Pracownicy")

        # Employee Database
        self.employee_db = db

        # Frame
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        # Treeview do wyświetlania pracowników
        self.employee_treeview = ttk.Treeview(self.frame, columns=("ID", "Imię", "Nazwisko", "Numer Karty"),
                                              show="headings")
        self.employee_treeview.grid(row=0, column=0, padx=10, pady=10)

        # Ustaw nagłówki kolumn
        self.employee_treeview.heading("ID", text="ID")
        self.employee_treeview.heading("Imię", text="Imię")
        self.employee_treeview.heading("Nazwisko", text="Nazwisko")
        self.employee_treeview.heading("Numer Karty", text="Numer Karty")

        # Przycisk "Zamknij"
        self.close_button = tk.Button(self.frame, text="Zamknij", command=self.master.destroy)
        self.close_button.grid(row=1, column=0, pady=5)

        # Wypełnij Treeview pracownikami
        self.populate_employees()

    def populate_employees(self):
        # Pobierz wszystkich pracowników z bazy danych
        employees = self.employee_db.find_all_employees()

        # Wypełnij Treeview danymi
        for employee in employees:
            self.employee_treeview.insert("", "end",
                                          values=(employee.id, employee.name, employee.lastname, employee.card_pid))


class EmployeeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Database App")
        self.master.geometry("400x300")

        # Frame na przyciski
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        # Przycisk "Dodaj pracownika"
        self.add_employee_button = tk.Button(self.frame, text="Dodaj pracownika", command=self.open_add_employee_window)
        self.add_employee_button.grid(row=0, column=0, pady=5)

        # Przycisk "Wyświetl logi"
        self.show_logs_button = tk.Button(self.frame, text="Wyświetl logi", command=self.open_log_window)
        self.show_logs_button.grid(row=1, column=0, pady=5)

        # Przycisk "Wyświetl pracowników"
        self.show_employees_button = tk.Button(self.frame, text="Wyświetl pracowników",
                                               command=self.open_employees_window)
        self.show_employees_button.grid(row=2, column=0, pady=5)

        # Przycisk "Wyjście z programu"
        self.exit_button = tk.Button(self.frame, text="Wyjście z programu", command=self.master.destroy)
        self.exit_button.grid(row=3, column=0, pady=5)

        # Inicjalizacja klienta MQTT
        self.mqtt_client = mqtt.Client()
        # self.mqtt_client.connect("localhost", 1883, 60)
        # self.mqtt_client.loop_start()  # Rozpocznij pętlę MQTT

        # Inicjalizacja bazy danych
        self.employee_db = db

    def open_add_employee_window(self):
        # Otwórz okno do dodawania pracownika
        add_employee_window = tk.Toplevel(self.master)
        add_employee_window.grab_set()  # Zablokuj główne okno
        AddEmployeeWindow(add_employee_window, self.add_employee, self.mqtt_client)

    def open_log_window(self):
        # Otwórz okno z logami
        log_window = tk.Toplevel(self.master)
        log_window.grab_set()  # Zablokuj główne okno
        EmployeeLogWindow(log_window)

    def open_employees_window(self):
        # Otwórz okno z pracownikami
        employees_window = tk.Toplevel(self.master)
        employees_window.grab_set()  # Zablokuj główne okno
        EmployeeWindow(employees_window)

    def add_employee(self, name, lastname, card_pid):
        # Tutaj możesz dodać kod do obsługi dodawania pracownika do bazy danych
        self.employee_db.add_employee(name, lastname, card_pid)
        messagebox.showinfo("Sukces", f"Dodano pracownika: {name} {lastname}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()