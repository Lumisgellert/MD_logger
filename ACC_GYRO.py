from mpu6050 import mpu6050
import time
import Parameter as par


class MPU6050Sensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

        self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
        self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
        self.sensor.set_filter_range(filter_range=self.sensor.FILTER_BW_5)

    def read(self):
        par.acc_x[0] = self.sensor.get_accel_data(g=True)["x"]
        par.acc_y[0] = self.sensor.get_accel_data(g=True)["y"]
        par.acc_z[0] = self.sensor.get_accel_data(g=True)["z"]

        par.gyro_x[0] = self.sensor.get_gyro_data()["x"]
        par.gyro_y[0] = self.sensor.get_gyro_data()["y"]
        par.gyro_z[0] = self.sensor.get_gyro_data()["z"]

        par.temp[0] = self.sensor.get_temp()