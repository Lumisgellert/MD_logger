import matplotlib.pyplot as plt
import time
import Parameter as par
from MPU6050 import MPU6050Sensor
from I2CMULTIPLEXER import I2CMultiplexer

# Puffer vorbereiten
acc_x_vals = []
time_vals = []
pitch_vals = []
roll_vals = []

# Anzahl der Samples & Abtastrate
samples = 500
interval = 0.0001  # 10 ms = 100 Hz

mux = I2CMultiplexer(address=0x70)
sensor = MPU6050Sensor(mux, channel=1)

# Messung starten
start_time = time.time()
for i in range(samples):
    sensor.read(mode="median")  # Medianmodus wie bei dir
    acc_x = sensor.acc_x
    pitch, roll = sensor.get_neigung_acc()

    acc_x_vals.append(acc_x)
    pitch_vals.append(pitch)
    roll_vals.append(roll)
    time_vals.append(time.time() - start_time)

    #time.sleep(interval)  # konstante Abtastrate

# Plot nach der Messung
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
fig.tight_layout(pad=3.0)

ax1.plot(time_vals, acc_x_vals, label="acc_x (g)")
ax1.set_title("Accelerometer X")
ax1.set_ylabel("g")
ax1.grid(True)
ax1.legend()

ax2.plot(time_vals, pitch_vals, label="Pitch (°)", color="orange")
ax2.set_title("Pitch")
ax2.set_ylabel("Grad")
ax2.grid(True)
ax2.legend()

ax3.plot(time_vals, roll_vals, label="Roll (°)", color="green")
ax3.set_title("Roll")
ax3.set_ylabel("Grad")
ax3.set_xlabel("Zeit [s]")
ax3.grid(True)
ax3.legend()

plt.show()
