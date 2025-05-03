import GPS
import Parameter as par
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
z = 0

gps = GPS.GPS()
now = time.time()
while True:
    while GPIO.input(17) == GPIO.LOW:
        z += 1
        gps.get_data()
        print(f"lat: {par.lat}, lon: {par.lon}, sat: {par.satellites}, alt: {par.altitude}, spd_kmh: {par.speed_kmh}, spd_knts: {par.speed_knts}, Kurs: {par.course}")
        print(z)

GPIO.cleanup()
