import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath('DFROBOT_MPX5700.py')))))
from DFRobot_MPX5700 import *
mpx5700 = DFRobot_MPX5700_I2C (0x01 ,0x16) # bus default use I2C1 , iic address is 0x16

def setup():
  mpx5700.set_mean_sample_size(5)
  mpx5700.calibration_kpa(101.3)
  
def loop():
  press = mpx5700.get_pressure_value_kpa(1)
  print ("Pressure : " + str(press) + " kPA")
  time.sleep(1)
  
if __name__ == "__main__":
  setup()
  while True:
    loop()



