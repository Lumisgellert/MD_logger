import threading
import os
import GPS
import Parameter
from reboot import reboot
import Parameter as par
from datetime import datetime
from map import show_map, collect_cord
import CSVLogger
from plot import plot
import SWITCH
from save_to_usb import save
from MPU6050 import MPU6050Sensor
import LED
from time import sleep
from I2CMULTIPLEXER import I2CMultiplexer
import RPi.GPIO as GPIO

try:
    led_green = LED.LedSystem(17)
    led_red = LED.LedSystem(27)
    led_green.on()
    led_red.on()

    # Pin für den Reboot-Schalter auf High für Vcc
    PIN_VCC = 6
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_VCC, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(PIN_VCC, GPIO.HIGH)

    gps = GPS.GPS()
    schalter16 = SWITCH.SwitchChecker(23) # Sachalter für loggen
    schalter5 = SWITCH.SwitchChecker(22) # Schalter für Reboot
    # Multiplexer-Instanz
    logger = CSVLogger.CSVLogger()

    try:
        sensor_0 = MPU6050Sensor(address=0x69) # Sensor im Logger
        sensor_1 = MPU6050Sensor(address=0x68) # Sensor am Vorderrad
    except RuntimeError as e:
        raise RuntimeError(e)

    led_green.off()
    led_red.off()
    sleep(0.5)
    led_green.on()

    while True:
        schalter16.rising_edge()
        schalter16.falling_edge()
        schalter5.rising_edge()
        schalter5.falling_edge()
        par.S16 = schalter16.pruefe_einzelnen()
        par.S5 = schalter5.pruefe_einzelnen()

        if schalter5.RISING_EDGE and not par.S16 and not par.check_bit:
            reboot()

        if not par.S16:
            gps.ser.reset_input_buffer()

        if schalter16.RISING_EDGE:
            par.time_start = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            led_green.off()
            led_red.on()
            threading.Thread(target=gps.get_data, daemon=True).start()
            par.check_bit = True
            print(par.time_start)
            sleep(1)

        elif par.S16 == 1 and par.check_bit is True:
            par.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            sensor_0.read(mode="raw")
            sensor_1.read(mode="raw")

            collect_cord(par.lat, par.lon)
            logger.save([
                par.timestamp, par.lat, par.lon, par.altitude, par.speed_kmh,
                par.speed_knts, par.course,
                sensor_0.acc_x, sensor_0.acc_y, sensor_0.acc_z, sensor_0.gyro_x, sensor_0.gyro_y, sensor_0.gyro_z,
                sensor_1.acc_x, sensor_1.acc_y, sensor_1.acc_z, sensor_1.gyro_x, sensor_1.gyro_y, sensor_1.gyro_z,
                sensor_0.temp, sensor_1.temp,
                par.satellites
            ])

        if schalter16.FALLING_EDGE and par.check_bit is True:
            led_green.off()
            led_red.on()
            led_green.on()
            filepath = logger.get_filepath()
            if not os.path.exists(filepath):
                print(f"⚠️ CSV-Datei {filepath} existiert noch nicht – Plot wird übersprungen.")
            else:
                show_map()
                plot(filepath, [
                    "v[kmh]", "alt_GND[m]", "sat[n]", "temp[°C]",
                    "Acc_x0[g]", "Acc_y0[g]", "Acc_z0[g]", "Gyro_x0[deg_s]", "Gyro_y0[deg_s]", "Gyro_z0[deg_s]",
                    "Acc_x1[g]", "Acc_y1[g]", "Acc_z1[g]", "Gyro_x1[deg_s]", "Gyro_y1[deg_s]", "Gyro_z1[deg_s]"
                ])
                save()
            par.check_bit = False
            par.loopBit = False
            led_green.off()
            led_red.off()
            sleep(0.1)
            led_green.on()


except KeyboardInterrupt:
    led_green.off()
    led_red.off()
    print("Programm beendet!")
