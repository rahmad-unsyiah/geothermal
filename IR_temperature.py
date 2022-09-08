import board
import time
import adafruit_mlx90614

# The MLX90614 only works at the default I2C bus speed of 100kHz.
# A higher speed, such as 400kHz, will not work.
i2c = board.I2C()
mlx = adafruit_mlx90614.MLX90614(i2c)

# temperature results in celsius
while True:
    print("Ambient Temp: ", mlx.ambient_temperature)
    print("Object Temp: ", mlx.object_temperature)
    time.sleep(2)

