import threading

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

try:
    gps = GPS.GPS()
    schalter = SWITCH.SwitchChecker([16])
    mpu = ACC_GYRO.MPU6050Sensor()
    logger = CSVLogger.CSVLogger()
    led_blue = LED.LedSystem(17)
    led_red = LED.LedSystem(27)
    led_blue.on()
    sleep(1)

    while True:
        schalter.falling_edge(16)
        schalter.rising_edge(16)
        par.S16 = schalter.pruefe_einzelnen(16)
        gps.ser.reset_input_buffer()
        sleep(0.1)

        if par.rising_edge:
            par.time_start = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            led_blue.off()
            led_red.on()
            print(par.time_start)

        if par.S16 == 1:
            par.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            gps.get_data()
            mpu.read()
            collect_cord(par.lat, par.lon)
            logger.save([
                par.timestamp,par.lat, par.lon, par.altitude, par.temp, par.speed_kmh,
                par.speed_knts, par.course, par.acc_x, par.acc_y, par.acc_z, par.gyro_x,
                par.gyro_y, par.gyro_z, par.satellites
            ])
            print(
                f"lat: {par.lat}, lon: {par.lon}, sat: {par.satellites}, alt: {par.altitude}, "
                f"spd_kmh: {par.speed_kmh}, spd_knts: {par.speed_knts}, Kurs: {par.course}"
            )
            schalter.falling_edge(16)
            schalter.rising_edge(16)

        if par.falling_edge:
            threading.Thread(target=led_blue.blink_fast, daemon=True).start()
            show_map()
            plot(logger.get_filepath(), [
                "v[kmh]", "alt_GND[m]", "sat[n]", "Acc_x[g]", "Acc_y[g]", "Acc_z[g]",
                "Gyro_x[deg_s]", "Gyro_y[deg_s]", "Gyro_z[deg_s]"
            ])
            save()
            del logger
            logger = CSVLogger.CSVLogger()
            led_blue.off()
            led_red.off()
            sleep(0.5)
            led_blue.on()


except KeyboardInterrupt:
    print("Programm beendet!")
