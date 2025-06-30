import threading
import os
import GPS
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
import RPi.GPIO as GPIO

try:
    # Pin-Definitionen (BCM-Nummern)
    PIN_VCC = 6             # Versorgungsspannung VCC Schalter
    PIN_LOGGEN = 23         # Logging-Schalter
    PIN_REBOOT = 22         # Reboot-Schalter
    PIN_LED_GREEN = 17      # Grüne LED
    PIN_LED_RED = 27        # Rote LED
    ADRESSE_SENSOR_0 = 0x69 # I2C-Adresse für Sensor 0 (Logger)
    ADRESSE_SENSOR_1 = 0x68 # I2C-Adresse für Sensor 1 (Vorderrad)
    ADRESSE_I2C = 0x00 # I2C-Adresse für zusätzliches I2C-Gerät (noch frei)

    # LED-Objekte initialisieren
    led_green = LED.LedSystem(PIN_LED_GREEN)
    led_red = LED.LedSystem(PIN_LED_RED)
    led_green.on()  # Grüne LED an
    led_red.on()    # Rote LED an

    # Pin für VCC setzen (Schalter mit Strom versorgen)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_VCC, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(PIN_VCC, GPIO.HIGH)

    # GPS-Modul initialisieren
    gps = GPS.GPS()
    # Schalter-Objekte initialisieren
    schalter16 = SWITCH.SwitchChecker(PIN_LOGGEN) # Schalter für Logging
    schalter5 = SWITCH.SwitchChecker(PIN_REBOOT)  # Schalter für Reboot

    # Logger initialisieren
    logger = CSVLogger.CSVLogger()

    # MPU6050-Sensoren initialisieren
    try:
        sensor_0 = MPU6050Sensor(address=ADRESSE_SENSOR_0) # Sensor im Logger
        sensor_1 = MPU6050Sensor(address=ADRESSE_SENSOR_1) # Sensor am Vorderrad
    except RuntimeError as e:
        # Fehler beim Initialisieren der Sensoren wird weitergereicht
        raise RuntimeError(e)

    # LEDs kurz durchschalten, um Status zu signalisieren
    led_green.off()
    led_red.off()
    sleep(0.5)
    led_green.on()

    # Hauptloop
    while True:
        # Schalter-Events abfragen
        schalter16.rising_edge()
        schalter16.falling_edge()
        schalter5.rising_edge()
        schalter5.falling_edge()
        par.S16 = schalter16.pruefe_einzelnen() # Status Schalter 16 (Logging)
        par.S5 = schalter5.pruefe_einzelnen()   # Status Schalter 5 (Reboot)

        # Reboot auslösen, wenn Schalter 5 gedrückt wird und Logging AUS ist
        if schalter5.RISING_EDGE and not par.S16 and not par.check_bit:
            reboot()

        # Input-Buffer des GPS zurücksetzen, wenn Logging AUS ist
        if not par.S16:
            gps.ser.reset_input_buffer()

        # Start Logging: Schalter 16 gedrückt
        if schalter16.RISING_EDGE:
            # Startzeit für Logging merken
            par.time_start = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            led_green.off()
            led_red.on()
            # GPS-Datenabfrage in separatem Thread starten
            threading.Thread(target=gps.get_data, daemon=True).start()
            par.check_bit = True
            print(par.time_start)
            sleep(1) # Kurze Pause zum Stabilisieren

        # Während Logging aktiv ist (Schalter 16 gedrückt)
        elif par.S16 == 1 and par.check_bit is True:
            # Zeitstempel generieren
            par.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            # Sensorwerte auslesen (beide MPU6050)
            sensor_0.read(mode="raw")
            sensor_1.read(mode="raw")
            # GPS-Koordinaten speichern
            collect_cord(par.lat, par.lon)
            # Alle Werte in CSV schreiben
            logger.save([
                par.timestamp, par.lat, par.lon, par.altitude, par.speed_kmh,
                par.speed_knts, par.course,
                sensor_0.acc_x, sensor_0.acc_y, sensor_0.acc_z, sensor_0.gyro_x, sensor_0.gyro_y, sensor_0.gyro_z,
                sensor_1.acc_x, sensor_1.acc_y, sensor_1.acc_z, sensor_1.gyro_x, sensor_1.gyro_y, sensor_1.gyro_z,
                sensor_0.temp, sensor_1.temp,
                par.satellites
            ])

        # Stop Logging: Schalter 16 losgelassen
        if schalter16.FALLING_EDGE and par.check_bit is True:
            led_green.off()
            led_red.on()
            led_green.on()
            filepath = logger.get_filepath()
            # Prüfen, ob CSV existiert, sonst kein Plot
            if not os.path.exists(filepath):
                print(f"⚠️ CSV-Datei {filepath} existiert noch nicht – Plot wird übersprungen.")
            else:
                # Karte und Plot anzeigen, Daten auf USB speichern
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
    # Bei STRG+C LEDs ausschalten und sauber beenden
    led_green.off()
    led_red.off()
    print("Programm beendet!")
