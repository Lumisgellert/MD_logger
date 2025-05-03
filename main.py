import GPS
import Parameter as par
import time

if __name__ == "__main__":
    gps = GPS.GPS()
    now = time.time()
    while True:
        gps.get_data()
        print(par.lat, par.lon, par.satellites, par.altitude, par.speed_kmh, par.speed_knts)
        if time.time() - now > 1.0:
            print("hallo")
            now = time.time()
