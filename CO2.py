import time
import serial
import binascii
import sys

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

while True:
    con = serial.Serial("/dev/ttyAMA0", 9600, timeout=5)
    co2 = get_co2(con)
    con.close()
    if co2 < 100 or co2 > 6000:
        print("CO2 concentration {} is out of range".format(co2), file=sys.stderr)
        exit(1)
    else:
        print("Gas concentration :", co2, "PPM")
        co2=co2+1
        time.sleep(1)
