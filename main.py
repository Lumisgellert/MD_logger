import threading
import os
import GPS
import Parameter as par
from datetime import datetime
from map import show_map, collect_cord
import CSVLogger
from plot import plot
import SWITCH
from save_to_usb import save
import ACC_GYRO
import LED
from time import sleep
import time
from MUX import TCA9548A

try:
    gps = GPS.GPS()
    schalter = SWITCH.SwitchChecker([16])
    mpu = ACC_GYRO.MPU6050Sensor()
    logger = CSVLogger.CSVLogger()
    led_blue = LED.LedSystem(17)
    led_red = LED.LedSystem(27)
    led_blue.on()

    mux = TCA9548A(bus=1)
    sensors = []

    for i in range(5):
        mux.select_channel(i)
        time.sleep(0.1)
        sensors.append(ACC_GYRO.MPU6050Sensor())

    sleep(1)

    while True:
        par.rising_edge = schalter.rising_edge(16)
        par.falling_edge = schalter.falling_edge(16)
        par.S16 = schalter.pruefe_einzelnen(16)
        if not par.S16:
            gps.ser.reset_input_buffer()

        if par.rising_edge:
            par.time_start = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            led_blue.off()
            led_red.on()
            par.check_bit = True
            print(par.time_start)

        elif par.S16 == 1 and par.check_bit is True:
            par.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            gps.get_data()
            mpu.read(0)
            for i, sensor in enumerate(sensors):
                mux.select_channel(i)
                time.sleep(0.05)
                sensor.read(i)

            collect_cord(par.lat, par.lon)
            logger.save([
                par.timestamp,par.lat, par.lon, par.altitude, par.temp[0], par.speed_kmh,
                par.speed_knts, par.course,
                par.acc_x[0], par.acc_y[0], par.acc_z[0], par.gyro_x[0], par.gyro_y[0], par.gyro_z[0],
                par.acc_x[1], par.acc_y[1], par.acc_z[1], par.gyro_x[1], par.gyro_y[1], par.gyro_z[1],
                par.acc_x[2], par.acc_y[2], par.acc_z[2], par.gyro_x[2], par.gyro_y[2], par.gyro_z[2],
                par.acc_x[3], par.acc_y[3], par.acc_z[3], par.gyro_x[3], par.gyro_y[3], par.gyro_z[3],
                par.acc_x[4], par.acc_y[4], par.acc_z[4], par.gyro_x[4], par.gyro_y[4], par.gyro_z[4],
                par.satellites
            ])
            print(
                f"lat: {par.lat}, lon: {par.lon}, sat: {par.satellites}, alt: {par.altitude}, "
                f"spd_kmh: {par.speed_kmh}, spd_knts: {par.speed_knts}, Kurs: {par.course}"
            )

        if schalter.falling_edge(16) and par.check_bit is True:
            filepath = logger.get_filepath()
            if not os.path.exists(filepath):
                print(f"⚠️ CSV-Datei {filepath} existiert noch nicht – Plot wird übersprungen.")
            else:
                threading.Thread(target=led_blue.blink_fast, daemon=True).start()
                show_map()
                plot(filepath, [
                    "v[kmh]", "alt_GND[m]", "sat[n]", "temp[°C]",
                    "Acc_x0[g]", "Acc_y0[g]", "Acc_z0[g]", "Gyro_x0[deg_s]", "Gyro_y0[deg_s]", "Gyro_z0[deg_s]",
                    "Acc_x1[g]", "Acc_y1[g]", "Acc_z1[g]", "Gyro_x1[deg_s]", "Gyro_y1[deg_s]", "Gyro_z1[deg_s]",
                    "Acc_x2[g]", "Acc_y2[g]", "Acc_z2[g]", "Gyro_x2[deg_s]", "Gyro_y2[deg_s]", "Gyro_z2[deg_s]",
                    "Acc_x3[g]", "Acc_y3[g]", "Acc_z3[g]", "Gyro_x3[deg_s]", "Gyro_y3[deg_s]", "Gyro_z3[deg_s]",
                    "Acc_x4[g]", "Acc_y4[g]", "Acc_z4[g]", "Gyro_x4[deg_s]", "Gyro_y4[deg_s]", "Gyro_z4[deg_s]",
                ])
                save()
            par.check_bit = False
            led_blue.off()
            led_red.off()
            sleep(1)
            led_blue.on()


except KeyboardInterrupt:
    print("Programm beendet!")
