import GPS
import Parameter as par
from datetime import datetime
from map import show_map, collect_cord
import CSVLogger
import ACC_GYRO
from plot import plot
import SWITCH

try:
    gps = GPS.GPS()
    logger = CSVLogger.CSVLogger()
    schalter = SWITCH.SwitchChecker([16])
    while True:
        gps.ser.reset_input_buffer()
        if schalter.pruefe_einzelnen(16) == 1:
            par.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            gps.get_data()
            collect_cord(par.lat, par.lon)
            logger.save([par.timestamp,par.lat, par.lon, par.altitude, par.temp, par.speed_kmh, par.speed_knts, par.course, "Acc_x[g]", "Acc_y[g]", "Acc_z[g]", "Gyro_x[deg/s]", "Gyro_y[deg/s]", "Gyro_z[deg/s]", par.satellites])
            print(f"lat: {par.lat}, lon: {par.lon}, sat: {par.satellites}, alt: {par.altitude}, spd_kmh: {par.speed_kmh}, spd_knts: {par.speed_knts}, Kurs: {par.course}")

except KeyboardInterrupt:
    show_map()
    plot(logger.get_filepath(), ["v[kmh]", "alt_GND[m]", "sat[n]"])
    print("Map wurde abgespeichert!")

