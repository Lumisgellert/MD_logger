from mpu6050 import mpu6050
import Parameter as par
import time


class MPU6050Sensor:
    def __init__(self, mux, channel, address=0x68):
        self.mux = mux
        self.channel = channel
        self.address = address
        self.sensor = None

        if self.init_sensor() is False:
            raise RuntimeError(f"Sensor auf Kanal {channel} nicht erreichbar")

    def init_sensor(self):
        try:
            self.mux.select_channel(self.channel)
            time.sleep(0.1)
            self.sensor = mpu6050(self.address)
            # Sensor konfigurieren
            self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
            self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
            self.sensor.set_filter_range(filter_range=self.sensor.FILTER_BW_5)
            print(f"✅ Sensor auf Kanal {self.channel} initialisiert")
            return True
        except Exception as e:
            print(f"⚠️  Fehler beim Initialisieren des Sensors auf Kanal {self.channel}: {e}")
            return False

    def read(self, index):
        try:
            self.mux.select_channel(self.channel)
            acc = self.sensor.get_accel_data(g=True)
            gyro = self.sensor.get_gyro_data()

            par.acc_x[index] = acc["x"]
            par.acc_y[index] = acc["y"]
            par.acc_z[index] = acc["z"]

            par.gyro_x[index] = gyro["x"]
            par.gyro_y[index] = gyro["y"]
            par.gyro_z[index] = gyro["z"]
            """
            par.acc_x[index] = acc["x"] + 0.006
            par.acc_y[index] = acc["y"] + 0.003
            par.acc_z[index] = acc["z"] + 0.012
    
            par.gyro_x[index] = gyro["x"] + 1.52
            par.gyro_y[index] = gyro["y"] - 1.30
            par.gyro_z[index] = gyro["z"] - 2.19
            """
            par.temp[index] = self.sensor.get_temp()
        except Exception as e:
            raise RuntimeError(e)
