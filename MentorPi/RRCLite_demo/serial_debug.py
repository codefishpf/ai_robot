#!/usr/bin/env python3
import serial
import time

# 根据实际串口号修改，比如 /dev/ttyUSB0 或 /dev/ttyAMA0
PORT = "/dev/rrc"
BAUD = 115200  # 波特率看板子文档，常见有 115200 / 460800

def main():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print(f"Opened serial port {PORT} at {BAUD} baud")
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return

    try:
        while True:
            line = ser.readline()
            if line:
                print("RAW (hex):", line.hex())
                # try:
                #     print("RAW:", line.decode("utf-8", errors="replace").strip())
                # except:
                #     print("RAW (hex):", line.hex())
            else:
                print("No data...")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exit by user")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
