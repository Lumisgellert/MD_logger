from mpu6050 import mpu6050
import time
import Parameter as par


class MPU6050Sensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

        self.sensor.set_accel_range(mpu6050.ACCEL_SCALE_MODIFIER_4G)
        self.sensor.set_gyro_range(mpu6050.GYRO_RANGE_250DEG)

    def read(self):
        data = self.sensor.get_all_data()
        print(data)


if __name__ == "__main__":
    while True:
        mpu6050 = MPU6050Sensor()
        mpu6050.read()
