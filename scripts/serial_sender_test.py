import serial
import serial.tools.list_ports
import time

MAX_X = 600.0
MAX_Y = 346.0

def list_com_ports():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No COM ports available. Please connect your Arduino.")
        return None

    print("Available COM Ports:")
    for i, port in enumerate(ports):
        print(f"{i + 1}: {port.device} - {port.description}")

    return ports


# Function to allow the user to select a COM port
def select_com_port():
    ports = list_com_ports()
    if not ports:
        return None

    while True:
        try:
            choice = int(input("Select a COM port by entering the corresponding number: ")) - 1
            if 0 <= choice < len(ports):
                return ports[choice].device
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(ports)}.")
        except ValueError:
            print("Please enter a valid number.")


def connect_serial(port, baudrate=9600, timeout=2):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)
        print(f"Serial port '{port}' connected.")
        return ser
    except serial.SerialException:
        print(f"Could not open serial port '{port}'. Please check the connection and port.")
        return None


def get_valid_input(prompt, max_value):
    while True:
        try:
            value = float(input(f"{prompt} (max {max_value}): "))
            if 0 <= value <= max_value:
                return value
            else:
                print(f"Value should be between 0 and {max_value}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def send_data(ser, x, y):
    if ser:
        try:
            data = f"{x},{y}\n"
            ser.write(data.encode('utf-8'))
            print("Data has been sent.")
        except serial.SerialException:
            print("Failed to send data. Serial connection might be lost.")

def main():
    selected_port = select_com_port()
    if not selected_port:
        print("No valid COM port selected. Exiting...")
        return

    ser = connect_serial(selected_port)
    if not ser:
        return

    try:
        while True:
            x = get_valid_input("Enter the value for X", MAX_X)
            y = get_valid_input("Enter the value for Y", MAX_Y)
            send_data(ser, x, y)
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        if ser:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()

