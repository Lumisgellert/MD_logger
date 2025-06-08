from mpu6050 import mpu6050
import time
import numpy as np
from Kalman import SimpleKalman
from collections import deque


class MPU6050Sensor:
    def __init__(self, mux=None, channel=None, address=0x68):
        self.mux = mux
        self.channel = channel
        self.address = address
        self.sensor = None

        # Variablen für Beschleunigung, Drehrate und Temperatur
        self.acc_x = 0.0
        self.acc_y = 0.0
        self.acc_z = 0.0

        self.gyro_x = 0.0
        self.gyro_y = 0.0
        self.gyro_z = 0.0

        self.temp = 0.0

        # Variablen für den Selbst test
        self.acc_x_offset = 0.0
        self.acc_y_offset = 0.0
        self.acc_z_offset = 0.0

        self.gyro_x_offset = 0.0
        self.gyro_y_offset = 0.0
        self.gyro_z_offset = 0.0

        # Variablen für Pitch und Roll Gyro
        self.pitch_gyro = 0.0
        self.roll_gyro = 0.0
        self.last_time = time.time()

        # Variablen für Pitch und Roll Acc
        self.pitch_acc = 0.0
        self.roll_acc = 0.0

        # Variablen für den Median Filter
        self.acc_x_buffer = deque(maxlen=5)
        self.acc_y_buffer = deque(maxlen=5)
        self.acc_z_buffer = deque(maxlen=5)

        self.gyro_x_buffer = deque(maxlen=5)
        self.gyro_y_buffer = deque(maxlen=5)
        self.gyro_z_buffer = deque(maxlen=5)

        # Kalman Objekte mit Parametern Q und R
        # Q groß --> Empfindlicher | R groß --> Träger
        self.kalman_acc_x = SimpleKalman(q=0.05, r=0.05)
        self.kalman_acc_y = SimpleKalman(q=0.05, r=0.05)
        self.kalman_acc_z = SimpleKalman(q=0.05, r=0.05)

        self.kalman_gyro_x = SimpleKalman(q=0.05, r=0.05)
        self.kalman_gyro_y = SimpleKalman(q=0.05, r=0.05)
        self.kalman_gyro_z = SimpleKalman(q=0.05, r=0.05)

        if self.init_sensor() is False:
            raise RuntimeError(f"Sensor auf Kanal {channel} nicht erreichbar")

    def init_sensor(self):
        try:
            if self.mux is not None:
                self.mux.select_channel(self.channel)
                time.sleep(0.1)

            self.sensor = mpu6050(self.address)

            # Sensor konfigurieren
            self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
            self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
            self.sensor.set_filter_range(filter_range=self.sensor.FILTER_BW_5)

            # Sensor Kalibrieren im stillstand
            self.kalibrieren()

            print(f"✅ Sensor auf Kanal {self.channel} initialisiert")
            return True
        except Exception as e:
            print(f"⚠️  Fehler beim Initialisieren des Sensors auf Kanal {self.channel}: {e}")
            return False

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

    def get_kalman_acc(self):
        acc = self.sensor.get_accel_data(g=True)
        acc = {
            "x": self.kalman_acc_x.update(acc["x"] - self.acc_x_offset),
            "y": self.kalman_acc_y.update(acc["y"] - self.acc_y_offset),
            "z": self.kalman_acc_z.update(acc["z"] - self.acc_z_offset + 1),
        }
        return acc

    def get_kalman_gyro(self):
        gyro = self.sensor.get_gyro_data()
        gyro = {
            "x": self.kalman_gyro_x.update(gyro["x"] - self.gyro_x_offset),
            "y": self.kalman_gyro_y.update(gyro["y"] - self.gyro_y_offset),
            "z": self.kalman_gyro_z.update(gyro["z"] - self.gyro_z_offset),
        }
        return gyro

    def get_median_acc(self):
        acc = self.sensor.get_accel_data(g=True)
        self.acc_x_buffer.append(acc["x"])
        self.acc_y_buffer.append(acc["y"])
        self.acc_z_buffer.append(acc["z"])

        acc = {
            "x": np.median(self.acc_x_buffer),
            "y": np.median(self.acc_y_buffer),
            "z": np.median(self.acc_z_buffer)
        }
        return acc

    def get_median_gyro(self):
        gyro = self.sensor.get_gyro_data()
        self.gyro_x_buffer.append(gyro["x"])
        self.gyro_y_buffer.append(gyro["y"])
        self.gyro_z_buffer.append(gyro["z"])

        gyro = {
            "x": np.median(self.gyro_x_buffer),
            "y": np.median(self.gyro_y_buffer),
            "z": np.median(self.gyro_z_buffer)
        }
        return gyro

    def get_neigung_acc(self):
        acc = self.get_kalman_acc()

        # Berechne Pitch und Roll aus Accelerometer
        self.pitch_acc = np.arctan2(acc["y"], acc["z"]) * 180 / np.pi
        self.roll_acc = np.arctan2(acc["x"], acc["z"]) * 180 / np.pi

        return self.pitch_acc, self.roll_acc

    def get_neigung_gyro(self):
        gyro = self.get_kalman_gyro()

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

    def read(self, mode="raw"):
        try:
            if self.channel is not None:
                self.mux.select_channel(self.channel)

            if mode == "raw":
                acc_raw = self.sensor.get_accel_data(g=True)
                gyro_raw = self.sensor.get_gyro_data()

                self.acc_x = acc_raw["x"] - self.acc_x_offset
                self.acc_y = acc_raw["y"] - self.acc_y_offset
                self.acc_z = acc_raw["z"] - self.acc_z_offset + 1

                self.gyro_x = gyro_raw["x"] - self.gyro_x_offset
                self.gyro_y = gyro_raw["y"] - self.gyro_y_offset
                self.gyro_z = gyro_raw["z"] - self.gyro_z_offset

            if mode == "kalman":
                acc = self.get_kalman_acc()
                gyro = self.get_kalman_gyro()
                self.acc_x = acc["x"] - self.acc_x_offset
                self.acc_y = acc["y"] - self.acc_y_offset
                self.acc_z = acc["z"] - self.acc_z_offset + 1

                self.gyro_x = gyro["x"] - self.gyro_x_offset
                self.gyro_y = gyro["y"] - self.gyro_y_offset
                self.gyro_z = gyro["z"] - self.gyro_z_offset

            if mode == "median":
                acc = self.get_median_acc()
                gyro = self.get_median_gyro()
                self.acc_x = acc["x"] - self.acc_x_offset
                self.acc_y = acc["y"] - self.acc_y_offset
                self.acc_z = acc["z"] - self.acc_z_offset + 1

                self.gyro_x = gyro["x"] - self.gyro_x_offset
                self.gyro_y = gyro["y"] - self.gyro_y_offset
                self.gyro_z = gyro["z"] - self.gyro_z_offset

            self.temp = self.sensor.get_temp()

        except OSError as e:
            print(f"[WARN] I2C-Fehler bei Channel {self.channel}: {e}")
        except Exception as e:
            print(f"[ERROR] Unerwarteter Fehler in read(): {e}")

