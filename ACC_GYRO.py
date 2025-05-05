from mpu6050 import mpu6050
import time
import Parameter as par


class MPU6050Sensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

    def read(self):
        data = self.sensor.get_accel_data()
        print(data)


if __name__ == "__main__":
    while True:
        mpu6050 = MPU6050Sensor()
        mpu6050.read()