import GPS
import Parameter as par
import time

if __name__ == "__main__":
    gps = GPS.GPS()
    now = time.time()
    while True:
        gps.get_data()
        print(f"lat: {par.lat}, lon: {par.lon}, sat: {par.satellites}, alt: {par.altitude}, spd_kmh: {par.speed_kmh}, spd_knts: {par.speed_knts}, Kurs: {par.course}")
