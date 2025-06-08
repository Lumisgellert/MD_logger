import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import Parameter as par
from ACC_GYRO import MPU6050Sensor
from I2CMULTIPLEXER import I2CMultiplexer

# Puffer für die letzten N Werte
history_length = 100
acc_x_vals = []
time_vals = []
pitch_vals = []
roll_vals = []

mux = I2CMultiplexer(address=0x70)
# Sensor vorbereiten (angenommen `sensor` ist dein MPU6050Sensor-Objekt)
sensor = MPU6050Sensor(mux, channel=0)


def update(frame):
    global acc_x_vals, time_vals, pitch_vals, roll_vals

    # Sensor lesen
    sensor.read(0)  # oder direkt: acc = sensor.get_filtered_acc()
    acc_x = par.acc_x[0]

    # Zeit holen
    t = time.time()

    # Werte hinzufügen
    time_vals.append(t)
    acc_x_vals.append(acc_x)

    #pitch, roll = sensor.get_gyro_orientation_only()
    pitch, roll = sensor.get_neigung(0.05)

    pitch_vals.append(pitch)
    roll_vals.append(roll)

    if len(pitch_vals) > history_length:
        pitch_vals = pitch_vals[-history_length:]
        roll_vals = roll_vals[-history_length:]

    # Länge begrenzen
    if len(time_vals) > history_length:
        time_vals = time_vals[-history_length:]
        acc_x_vals = acc_x_vals[-history_length:]

    # Plot 1: acc_x
    ax1.clear()
    ax1.plot(time_vals, acc_x_vals, label="acc_x (g)")
    ax1.set_title("Accelerometer X")
    ax1.set_ylabel("g")
    ax1.grid(True)
    ax1.legend()

    # Plot 2: Pitch
    ax2.clear()
    ax2.plot(time_vals, pitch_vals, label="Pitch (°)", color="orange")
    ax2.set_title("Pitch")
    ax2.set_ylabel("Grad")
    ax2.grid(True)
    ax2.legend()

    # Plot 3: Roll
    ax3.clear()
    ax3.plot(time_vals, roll_vals, label="Roll (°)", color="green")
    ax3.set_title("Roll")
    ax3.set_ylabel("Grad")
    ax3.set_xlabel("Zeit [s]")
    ax3.grid(True)
    ax3.legend()


# Matplotlib vorbereiten
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
fig.tight_layout(pad=3.0)

ani = FuncAnimation(fig, update, interval=50)
plt.show()

