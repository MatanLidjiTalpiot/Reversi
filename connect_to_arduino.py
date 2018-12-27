import serial #Serial imported for Serial communication
import time #Required to use delay functions
arduinoName = 'COM8'
port = 9600
ArduinoSerial = serial.Serial(arduinoName,port)

time.sleep(2)

# code that it's goal is to light a led
while 1:
    var = input()  # get input from user
    ArduinoSerial.write(var.encode())  # send 1
    print("LED turned ON")
    time.sleep(1)
