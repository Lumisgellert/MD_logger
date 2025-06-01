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
from ACC_GYRO import MPU6050Sensor
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
    schalter16 = SWITCH.SwitchChecker(16)
    schalter5 = SWITCH.SwitchChecker(5)
    # Multiplexer-Instanz
    mux = I2CMultiplexer(address=0x70)
    logger = CSVLogger.CSVLogger()

    sensors = []  # Liste mit (kanalnummer, sensorobjekt)

    for i in range(5):
        print(f"Kanal {i} aktivieren")
        try:
            sensor = MPU6050Sensor(mux, channel=i)
            sensors.append((i, sensor))
            sleep(0.1)
        except RuntimeError as e:
            print(e)
            continue

    print(sensors)

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

        elif par.S16 == 1 and par.check_bit is True:
            par.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            for kanal, sensor in sensors:
                sensor.read(index=kanal)
                sleep(1/10000)

            collect_cord(par.lat, par.lon)
            logger.save([
                par.timestamp, par.lat, par.lon, par.altitude, par.speed_kmh,
                par.speed_knts, par.course,
                par.acc_x[0], par.acc_y[0], par.acc_z[0], par.gyro_x[0], par.gyro_y[0], par.gyro_z[0],
                par.acc_x[1], par.acc_y[1], par.acc_z[1], par.gyro_x[1], par.gyro_y[1], par.gyro_z[1],
                par.acc_x[2], par.acc_y[2], par.acc_z[2], par.gyro_x[2], par.gyro_y[2], par.gyro_z[2],
                par.acc_x[3], par.acc_y[3], par.acc_z[3], par.gyro_x[3], par.gyro_y[3], par.gyro_z[3],
                par.acc_x[4], par.acc_y[4], par.acc_z[4], par.gyro_x[4], par.gyro_y[4], par.gyro_z[4],
                par.temp[0], par.temp[1], par.temp[2], par.temp[3], par.temp[4],
                par.satellites
            ])

        if schalter16.FALLING_EDGE and par.check_bit is True:
            filepath = logger.get_filepath()
            if not os.path.exists(filepath):
                print(f"⚠️ CSV-Datei {filepath} existiert noch nicht – Plot wird übersprungen.")
            else:
                threading.Thread(target=led_green.blink_fast, daemon=True).start()
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
            par.loopBit = False
            led_green.off()
            led_red.off()
            sleep(1)
            led_green.on()


except KeyboardInterrupt:
    led_green.off()
    led_red.off()
    print("Programm beendet!")
