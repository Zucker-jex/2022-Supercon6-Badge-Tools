# By Jex Zucker
import serial
import time
import os
from tqdm import tqdm


def send_file_via_serial(port, baudrate, filename):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

        file_size = os.path.getsize(filename)

        with open(filename, "rb") as f:
            with tqdm(
                total=file_size, unit="B", unit_scale=True, desc=filename
            ) as pbar:
                while True:
                    block = f.read(1024)
                    if not block:
                        break
                    ser.write(block)
                    pbar.update(len(block))

        print("File sent successfully.")
        ser.close()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python win_flash.py <file>")
        sys.exit(1)

    file_to_send = sys.argv[1]
    serial_port = "COM18"
    baud_rate = 9600

    send_file_via_serial(serial_port, baud_rate, file_to_send)
