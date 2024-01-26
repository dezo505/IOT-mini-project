#!/usr/bin/env python3
from oled_writer import DrawControl
from datetime import datetime
import paho.mqtt.client as mqtt
from database import EmployeeDatabase

broker = "localhost"
client = mqtt.Client()
db = EmployeeDatabase()
db.init_database()


def on_message(client, userdata, message):
    try:
        card_pid = message.payload.decode()

        employee = db.find_employee_by_card_pid(card_pid)

        if employee:
            access_granted = True
            db.add_card_event(card_pid, employee.id, datetime.now(), access_granted)
            client.publish("card/access_response", "access_granted")
            DrawControl.writeMessage("Access granted to", f"{employee.name} {employee.lastname}")
        else:
            access_granted = False
            db.add_card_event(card_pid, None, datetime.now(), access_granted)
            client.publish("card/access_response", "access_denied")
            DrawControl.writeMessage("Access denied!", "")
    except Exception as e:
        print("Error processing message:", e)


def connect_to_broker():
    try:
        client.connect(broker)
        client.subscribe("card/pid")
        client.message_callback_add("card/pid", on_message)
        client.loop_forever()
    except Exception as e:
        print("Error connecting to broker:", e)
        disconnect_from_broker()


def disconnect_from_broker():
    try:
        client.disconnect()
    except Exception as e:
        print("Error disconnecting from broker:", e)


if __name__ == "__main__":
    try:
        connect_to_broker()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, disconnecting from broker and terminating program.")
    finally:
        disconnect_from_broker()
