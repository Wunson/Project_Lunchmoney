import serial
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4'

ser.open()
while True:
  h1=ser.readline()
  if h1:
      print(int(h1))
