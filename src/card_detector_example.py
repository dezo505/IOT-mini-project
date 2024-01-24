from main.card_detector import CardDetector


def example_usage():
    card_detector = CardDetector()

    while True:

        card_reading = card_detector.read_card()

        if card_reading.result:
            print("Card detected!")
        else:
            print("No card detected.")

        print("Card pid: " + card_reading.card_pid)
        print("timestamp: " + card_reading.timestamp)


if __name__ == "__main__":
    example_usage()
