import serial #Serial imported for Serial communication
import time #Required to use delay functions
arduinoName = 'COM6'
port = 9600
arduinoSerial = serial.Serial(arduinoName,port)
time.sleep(2)

# code that it's goal is to light a led
while True:
    var = input()  # get input from user
    # board function
    arduinoSerial.write(var.encode())  # send 1
    time.sleep(0.5)
