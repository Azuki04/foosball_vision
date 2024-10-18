import serial
import time

MAX_X = 600.0
MAX_Y = 346.0

try:
    ser = serial.Serial('COM3', 9600)
    time.sleep(2)
    print("Serial port connected.")
except serial.SerialException:
    print("Could not open serial port.")
    exit()


def get_valid_input(prompt, max_value):
    while True:
        user_input = input(f"{prompt} (max {max_value}): ")
        try:
            value = float(user_input)
            if value > max_value:
                print(f"Value should not exceed {max_value}. Please try again.")
            else:
                return value
        except ValueError:
            print("Please enter a numeric value.")


while True:
    x = get_valid_input("Enter the value for x", MAX_X)
    y = get_valid_input("Enter the value for y", MAX_Y)

    data = f"{x},{y}\n"
    ser.write(data.encode('utf-8'))
    print("Data has been sent")
