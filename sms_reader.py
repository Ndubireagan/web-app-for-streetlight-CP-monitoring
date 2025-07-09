import serial
import time
import re
import sqlite3
from datetime import datetime

SERIAL_PORT = 'COM3'  # Update as needed for your system
BAUDRATE = 9600
DB_FILE = 'sensor_readings.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sms_text TEXT,
            voltage REAL,
            current REAL,
            power REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_reading(sms_text, voltage, current, power):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO readings (sms_text, voltage, current, power, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (sms_text, voltage, current, power, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def send_at_command(ser, command, delay=1):
    ser.write((command + '\r').encode())
    time.sleep(delay)
    response = b""
    while ser.in_waiting:
        response += ser.read(ser.in_waiting)
        time.sleep(0.1)
    return response.decode(errors='ignore')

def parse_sensor_sms(sms_text):
    pattern = r"V:(\d+\.?\d*)\s+I:(\d+\.?\d*)\s+P:(\d+\.?\d*)"
    match = re.search(pattern, sms_text)
    if match:
        voltage = float(match.group(1))
        current = float(match.group(2))
        power = float(match.group(3))
        return voltage, current, power
    else:
        return None, None, None

def extract_sms_bodies(response):
    bodies = []
    lines = response.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("+CMGL:"):
            if i + 1 < len(lines):
                bodies.append(lines[i + 1])
    return bodies

def main():
    init_db()
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=5)
    time.sleep(2)  # Wait for modem to initialize

    print("Setting SMS text mode...")
    print(send_at_command(ser, "AT+CMGF=1"))

    print("Reading unread SMS...")
    response = send_at_command(ser, 'AT+CMGL="REC UNREAD"', delay=3)
    print(response)

    sms_bodies = extract_sms_bodies(response)
    for sms_text in sms_bodies:
        voltage, current, power = parse_sensor_sms(sms_text)
        if voltage is not None:
            print(f"Parsed Sensor Data - Voltage: {voltage} V, Current: {current} A, Power: {power} W")
            store_reading(sms_text, voltage, current, power)
        else:
            print("Could not parse sensor data from SMS:", sms_text)
            store_reading(sms_text, None, None, None)


    ser.close()

if __name__ == "__main__":
    main()