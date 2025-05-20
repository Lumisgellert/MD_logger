from mpu6050 import mpu6050
import time
import Parameter as par


class MPU6050Sensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

        self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
        self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
        self.sensor.set_filter_range(filter_range=self.sensor.FILTER_BW_5)

    def read(self, index):
        par.acc_x[index] = self.sensor.get_accel_data(g=True)["x"] + 0.006
        par.acc_y[index] = self.sensor.get_accel_data(g=True)["y"] + 0.003
        par.acc_z[index] = self.sensor.get_accel_data(g=True)["z"] + 0.012

        par.gyro_x[index] = self.sensor.get_gyro_data()["x"] + 1.52
        par.gyro_y[index] = self.sensor.get_gyro_data()["y"] - 1.30
        par.gyro_z[index] = self.sensor.get_gyro_data()["z"] - 2.19

        par.temp[index] = self.sensor.get_temp()