import serial
import pynmea2
import Parameter as par


def parse_nmea_line(line):
    try:
        msg = pynmea2.parse(line)
        return msg
    except pynmea2.nmea.ParseError:
        return None


class GPS:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            timeout=1
        )

    def get_data(self):
        line = self.ser.readline().decode('ascii', errors='ignore')
        msg = parse_nmea_line(line)

        if msg is None:
            return  # oder alternativ: print("Ungültige Zeile")

        if msg.sentence_type == "GGA":
            par.lat = msg.latitude
            par.lon = msg.longitude
            par.altitude = msg.altitude
            par.satellites = msg.num_sats

        elif msg.sentence_type == "RMC":
            par.lat = msg.latitude
            par.lon = msg.longitude
            par.course = msg.true_course
            par.timestamp = msg.datestamp.isoformat() if msg.datestamp else None

        elif msg.sentence_type == "VTG":
            par.course = msg.true_track
            par.speed_knts = msg.spd_over_grnd_kts
            par.speed_kmh = msg.spd_over_grnd_kmph

        elif msg.sentence_type == "GLL":
            par.lat = msg.latitude
            par.lon = msg.longitude
            #par.timestamp = msg.timestamp.isoformat() if msg.timestamp else None
