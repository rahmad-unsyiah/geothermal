import board
import busio
import adafruit_sht31d
import time
import adafruit_mlx90614
import sys
import os
import serial
import binascii

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath('DFROBOT_MPX5700.py')))))
from DFRobot_MPX5700 import *
mpx5700 = DFRobot_MPX5700_I2C (0x01 ,0x16) # bus default use I2C1 , iic address is 0x16

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c, 0x45)
mlx = adafruit_mlx90614.MLX90614(i2c)
press = mpx5700.get_pressure_value_kpa(1)

def setup():
  mpx5700.set_mean_sample_size(5)
  mpx5700.calibration_kpa(101.3)

def verify_checksum(bytes):
  if len(bytes) != 9:
    return False
  sum = 0
  for i in range(1, 8):
    sum += bytes[i]
  sum = sum % 256
  checksum = 255 - sum + 1

  return bytes[8] == checksum

def get_co2(con):
  con.write(bytearray(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79'))
  rcv = con.read(9)
  if not verify_checksum(rcv):
    print("Checksum error from received: `{}'".format(binascii.hexlify(rcv)), file=sys.stderr)
    return -1
  return rcv[2] * 256 + rcv[3]

def calibrate_span(con):
  con.write(bytearray(b'\xff\x01\x88\x07\xd0\x00\x00\x00\xa0'))

def calibrate_zero(con):
  con.write(bytearray(b'\xff\x01\x87\x00\x00\x00\x00\x00\x78'))

if __name__ == "__main__":
  setup()
  while True:
    con = serial.Serial("/dev/ttyAMA0", 9600, timeout=5)
    co2 = get_co2(con)
    con.close()
    
    if co2 < 100 or co2 > 6000:
        print("CO2 concentration {} is out of range".format(co2), file=sys.stderr)
        exit(1)
    else:
        print("\nTemperature \t: %0.1f C" % sensor.temperature)
        print("Humidity \t: %0.1f %%" % sensor.relative_humidity)
        print("Ambient Temp \t:", mlx.ambient_temperature)
        print("Object Temp \t:", mlx.object_temperature)
        print("Pressure \t: " + str(press) + " kPA")
        print("Gas concentration :", co2, "PPM")
        co2=co2+1
        time.sleep(2)
