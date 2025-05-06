from mpu6050 import mpu6050
import time
import Parameter as par


class MPU6050Sensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

        self.sensor.set_accel_range(0x08)
        self.sensor.set_gyro_range(0x00)

    def read(self):
        data = self.sensor.get_accel_data(g=True)[1]
        print(data)


if __name__ == "__main__":
    while True:
        mpu = MPU6050Sensor()
        mpu.read()
        time.sleep(0.25)
