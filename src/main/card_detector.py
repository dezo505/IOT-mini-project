import time
from collections import namedtuple
from mfrc522 import MFRC522


class CardDetector:
    RFIDResult = namedtuple('RFIDResult', ['result', 'timestamp', 'card_pid'])

    def __init__(self):
        self.card_reader = MFRC522()
        self.last_reading_result = False

    def read_card(self):
        fridRead1 = self._rfid_read()
        fridRead2 = self._rfid_read()

        if fridRead1.result:
            fridRead = fridRead1
        else:
            fridRead = fridRead2

        result = False

        if not self.last_reading_result and fridRead.result:
            result = True

        self.last_reading_result = result

        return self.RFIDResult(result=result, timestamp=fridRead.timestamp, card_pid=fridRead.timestamp)

    def _rfid_read(self):
        card_reader = self.card_reader

        (status, TagType) = card_reader.MFRC522_Request(card_reader.PICC_REQIDL)

        if status == card_reader.MI_OK:
            (status, uid) = card_reader.MFRC522_Anticoll()
            if status == card_reader.MI_OK:
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i * 8)

                return self.RFIDResult(result=True, timestamp=time.time(), card_pid=num)

        return self.RFIDResult(result=False, timestamp=time.time(), card_pid=None)
