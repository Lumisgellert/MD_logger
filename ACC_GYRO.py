from mpu6050 import mpu6050
import Parameter as par
import time
import numpy as np


class MPU6050Sensor:
    def __init__(self, mux, channel, address=0x68):
        self.mux = mux
        self.channel = channel
        self.address = address
        self.sensor = None

        # Variablen für den Selbst test
        self.acc_x_offset = 0.0
        self.acc_y_offset = 0.0
        self.acc_z_offset = 0.0

        self.gyro_x_offset = 0.0
        self.gyro_y_offset = 0.0
        self.gyro_z_offset = 0.0

        if self.init_sensor() is False:
            raise RuntimeError(f"Sensor auf Kanal {channel} nicht erreichbar")

    def kalibrieren(self, werte=50):
        accX = np.zeros(werte)
        accY = np.zeros(werte)
        accZ = np.zeros(werte)

        gyroX = np.zeros(werte)
        gyroY = np.zeros(werte)
        gyroZ = np.zeros(werte)

        for i in range(werte):
            acc = self.sensor.get_accel_data(g=True)
            gyro = self.sensor.get_gyro_data()
            accX[i] = acc["x"]
            accY[i] = acc["y"]
            accZ[i] = acc["z"]

            gyroX[i] = gyro["x"]
            gyroY[i] = gyro["y"]
            gyroZ[i] = gyro["z"]

        self.acc_x_offset = accX.mean()
        self.acc_y_offset = accY.mean()
        self.acc_z_offset = accZ.mean()

        self.gyro_x_offset = gyroX.mean()
        self.gyro_y_offset = gyroY.mean()
        self.gyro_z_offset = gyroZ.mean()
        print(f"Kalibrieren für Sensor {self.channel} erfolgreich")

    def init_sensor(self):
        try:
            self.mux.select_channel(self.channel)
            time.sleep(0.1)
            self.sensor = mpu6050(self.address)

            # Sensor konfigurieren
            self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
            self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
            self.sensor.set_filter_range(filter_range=self.sensor.FILTER_BW_5)

            self.kalibrieren()

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

            # Da beim Sensor 0, welcher im Logger selbst ist, die Z-Achse verdreht ist, wird diese mit -1 umgedreht.
            if index == 0:
                par.acc_x[index] = acc["x"] - self.acc_x_offset
                par.acc_y[index] = acc["y"] - self.acc_y_offset
                par.acc_z[index] = (acc["z"] - self.acc_z_offset - 1) * -1

                par.gyro_x[index] = gyro["x"] - self.gyro_x_offset
                par.gyro_y[index] = gyro["y"] - self.gyro_y_offset
                par.gyro_z[index] = (gyro["z"] - self.gyro_z_offset) * -1
            else:
                par.acc_x[index] = acc["x"] - self.acc_x_offset
                par.acc_y[index] = acc["y"] - self.acc_y_offset
                par.acc_z[index] = acc["z"] - self.acc_z_offset + 1

                par.gyro_x[index] = gyro["x"] - self.gyro_x_offset
                par.gyro_y[index] = gyro["y"] - self.gyro_y_offset
                par.gyro_z[index] = gyro["z"] - self.gyro_z_offset

            par.temp[index] = self.sensor.get_temp()

        except OSError as e:
            print(f"[WARN] I2C-Fehler bei Channel {self.channel}: {e}")
            # → Kein neuer Wert geschrieben = alter bleibt erhalten

        except Exception as e:
            print(f"[ERROR] Unerwarteter Fehler in read(): {e}")
            # Auch hier: nichts überschreiben, damit alter Wert bleibt
