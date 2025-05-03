import GPS
import Parameter as par

if __name__ == "__main__":
    gps = GPS.GPS()
    while True:
        gps.get_data()
        print(par.lat, par.lon, par.satellites)
