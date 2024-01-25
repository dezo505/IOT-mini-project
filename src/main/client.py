#!/usr/bin/env python3
from time import sleep

import paho.mqtt.client as mqtt
from src.main.card_detector import CardDetector
from src.main.utils import blink_red, blink_green

terminal_id = "T0"
broker = "localhost"
client = mqtt.Client()


def call_card_detection(card_pid):
    client.publish("card/pid", card_pid)


def connect_to_broker():
    try:
        client.connect(broker)
    except Exception as e:
        print("Error connecting to broker:", e)


def disconnect_from_broker():
    try:
        client.disconnect()
    except Exception as e:
        print("Error disconnecting from broker:", e)


def on_access_response(client, userdata, message):
    try:
        message_data = message.payload.decode()
        if message_data == "access_granted":
            print("Access granted!")
            blink_green(0.5)
        elif message_data == "access_denied":
            print("Access denied!")
            blink_red(0.5)
        else:
            print("Unknown response:", message_data)
            blink_red(0.1)
            sleep(0.1)
            blink_red(0.1)
            sleep(0.1)
            blink_red(0.1)
    except Exception as e:
        print("Error processing message:", e)


def run_sender():
    connect_to_broker()

    try:
        client.message_callback_add("card/access_response", on_access_response)
        client.loop_start()

        cardDetector = CardDetector()

        while True:
            try:
                cardReading = cardDetector.read_card()

                if cardReading["result"]:
                    call_card_detection(cardReading["card_pid"])

            except Exception as e:
                print("Error reading card:", e)

    except Exception as e:
        print("Error:", e)

    finally:
        disconnect_from_broker()
        print("Program terminated.")


if __name__ == "__main__":
    run_sender()
