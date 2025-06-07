import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from ACC_GYRO import MPU6050Sensor
from I2CMULTIPLEXER import I2CMultiplexer

# Puffer für die letzten N Werte
history_length = 100
acc_x_vals = []
time_vals = []


mux = I2CMultiplexer(address=0x70)
# Sensor vorbereiten (angenommen `sensor` ist dein MPU6050Sensor-Objekt)
sensor = MPU6050Sensor(mux, channel=0)


def update(frame):
    global acc_x_vals, time_vals

    # Sensor lesen
    sensor.read(0)  # oder direkt: acc = sensor.get_filtered_acc()
    acc_x = par.acc_x[0]

    # Zeit holen
    t = time.time()

    # Werte hinzufügen
    time_vals.append(t)
    acc_x_vals.append(acc_x)

    # Länge begrenzen
    if len(time_vals) > history_length:
        time_vals = time_vals[-history_length:]
        acc_x_vals = acc_x_vals[-history_length:]

    # Plot leeren & neu zeichnen
    ax.clear()
    ax.plot(time_vals, acc_x_vals, label="acc_x (gefiltert)")
    ax.set_title("Live MPU6050 acc_x")
    ax.set_ylabel("g")
    ax.set_xlabel("Zeit [s]")
    ax.legend()
    ax.grid(True)


# Matplotlib vorbereiten
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, interval=50)  # alle 50 ms updaten
plt.show()
