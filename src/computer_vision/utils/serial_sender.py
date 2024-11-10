import time

import serial

from computer_vision.constants import (COURT_HEIGHT, COURT_WIDTH)


class SerialSender:
    def __init__(self, url, baudrate):
        try:
            self.ser = serial.serial_for_url(url, baudrate=baudrate, timeout=1)
            time.sleep(2)
            print("Serial port connected.")
        except serial.SerialException as e:
            print(f"Could not open serial port: {e}")
            self.ser = None

    def send_current_coordinate(self, x, y):
        if not (0 <= x <= COURT_WIDTH) or not (0 <= y <=  COURT_HEIGHT):
            print("Coordinates are out of range")
            return

        try:
            data = f"{x},{y}\n"
            self.ser.write(data.encode('utf-8'))
            print("Data has been sent")
        except serial.SerialTimeoutException:
            print("Timeout occurred while sending data.")
        except serial.SerialException as e:
            print(f"Error sending data: {e}")

    def close(self):
        if self.ser:
            self.ser.close()
            print("Serial port closed.")
