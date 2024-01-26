#!/usr/bin/env python3
from time import sleep

import paho.mqtt.client as mqtt
from card_detector import CardDetector
from led_control import *
from buzzer_control import BuzzerControl

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
            LedControl.turnOnColor(LedControl.GREEN)
            BuzzerControl.changeBuzzerState(True)
            time.sleep(0.5)
            BuzzerControl.changeBuzzerState(False)
            LedControl.turnOffLed()
            #LedControl.blink_green(0.5)
        elif message_data == "access_denied":
            print("Access denied!")
            LedControl.turnOnColor(LedControl.RED)
            BuzzerControl.changeBuzzerState(True)
            time.sleep(0.2)
            BuzzerControl.changeBuzzerState(False)
            time.sleep(0.1)
            BuzzerControl.changeBuzzerState(True)
            time.sleep(0.25)
            BuzzerControl.changeBuzzerState(False)

            LedControl.turnOffLed()
        else:
            print("Unknown response:", message_data)
            LedControl.blink_red(0.1)
            sleep(0.1)
            LedControl.blink_red(0.1)
            sleep(0.1)
            LedControl.blink_red(0.1)
    except Exception as e:
        print("Error processing message:", e)


def run_sender():
    connect_to_broker()

    try:
        client.subscribe("card/access_response")
        client.message_callback_add("card/access_response", on_access_response)
        client.loop_start()

        cardDetector = CardDetector()

        while True:
            try:
                cardReading = cardDetector.read_card()

                if cardReading.result:
                    call_card_detection(cardReading.card_pid)

            except Exception as e:
                print("Error reading card:", e)

    except Exception as e:
        print("Error:", e)

    finally:
        disconnect_from_broker()
        print("Program terminated.")


if __name__ == "__main__":
    run_sender()
