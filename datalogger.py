import serial_manager
import time

def datalog(port):
    """Logs data from a port"""
    ser = serial.Serial(port)
    while True:
        ser_bytes = ser.readline()
        with open("Data.txt", "w") as file:
            file.write(time.time(), ser_bytes, "\n")
            
