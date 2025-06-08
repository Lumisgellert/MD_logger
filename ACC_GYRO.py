from MPU6050 import mpu6050
import Parameter as par
import time
import numpy as np
from Kalman import SimpleKalman


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

        self.pitch_gyro = 0.0
        self.roll_gyro = 0.0
        self.last_time = time.time()

        self.kalman_acc_x = SimpleKalman(q=0.05, r=0.05)
        self.kalman_acc_y = SimpleKalman(q=0.05, r=0.05)
        self.kalman_acc_z = SimpleKalman(q=0.05, r=0.05)

        self.kalman_gyro_x = SimpleKalman(q=0.05, r=0.05)
        self.kalman_gyro_y = SimpleKalman(q=0.05, r=0.05)
        self.kalman_gyro_z = SimpleKalman(q=0.05, r=0.05)

        if self.init_sensor() is False:
            raise RuntimeError(f"Sensor auf Kanal {channel} nicht erreichbar")

    def kalibrieren(self, werte=100):
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

    def get_filtered_acc(self):
        acc = self.sensor.get_accel_data(g=True)
        return {
            "x": self.kalman_acc_x.update(acc["x"]),
            "y": self.kalman_acc_y.update(acc["y"]),
            "z": self.kalman_acc_z.update(acc["z"]),
        }

    def get_filtered_gyro(self):
        gyro = self.sensor.get_gyro_data()
        return {
            "x": self.kalman_gyro_x.update(gyro["x"]),
            "y": self.kalman_gyro_y.update(gyro["y"]),
            "z": self.kalman_gyro_z.update(gyro["z"]),
        }

    def get_neigung(self, channel):
        self.read(channel)

        # Berechne Pitch und Roll aus Accelerometer
        pitch_acc = np.arctan2(par.acc_y[channel], par.acc_z[channel]) * 180 / np.pi
        roll_acc = np.arctan2(par.acc_x[channel], par.acc_z[channel]) * 180 / np.pi

        roll_acc = roll_acc
        pitch_acc = pitch_acc

        return pitch_acc, roll_acc

    def get_gyro_orientation_only(self):
        gyro = self.sensor.get_gyro_data()

        # Zeit seit letztem Aufruf
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0 or dt > 1:
            dt = 0.02  # Fallback
        self.last_time = current_time

        # Winkelgeschwindigkeit in °/s → integrieren
        gyro_x = gyro["x"] - self.gyro_x_offset  # Roll
        gyro_y = gyro["y"] - self.gyro_y_offset  # Pitch

        self.roll_gyro += gyro_x * dt
        self.pitch_gyro += gyro_y * dt

        return self.pitch_gyro, self.roll_gyro

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
            acc_raw = self.sensor.get_accel_data(g=True)
            acc = {
                "x": self.kalman_acc_x.update(acc_raw["x"]),
                "y": self.kalman_acc_y.update(acc_raw["y"]),
                "z": self.kalman_acc_z.update(acc_raw["z"]),
            }

            gyro_raw = self.sensor.get_gyro_data()
            gyro = {
                "x": self.kalman_gyro_x.update(gyro_raw["x"]),
                "y": self.kalman_gyro_y.update(gyro_raw["y"]),
                "z": self.kalman_gyro_z.update(gyro_raw["z"]),
            }

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
        except Exception as e:
            print(f"[ERROR] Unerwarteter Fehler in read(): {e}")
