from mpu6050 import mpu6050
import time
import Parameter as par


class MPU6050Sensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

        self.sensor.set_accel_range(0x08)
        self.sensor.set_gyro_range(0x00)

    def read(self):
        par.acc_x = self.sensor.get_accel_data(g=True)["x"]
        par.acc_y = self.sensor.get_accel_data(g=True)["y"]
        par.acc_z = self.sensor.get_accel_data(g=True)["z"]

        par.gyro_x = self.sensor.get_gyro_data()["x"]
        par.gyro_y = self.sensor.get_gyro_data()["y"]
        par.gyro_z = self.sensor.get_gyro_data()["z"]
        print(par.acc_x)
        print(par.acc_y)
        print(par.acc_z)
        print(par.gyro_x)
        print(par.gyro_y)
        print(par.gyro_z)


if __name__ == "__main__":
    while True:
        mpu = MPU6050Sensor()
        mpu.read()
        time.sleep(0.25)
