import serial
import pynmea2
import Parameter as par


def calculate_checksum(sentence):
    cs = 0
    for char in sentence:
        cs ^= ord(char)
    return f"{cs:02X}"


class GPS:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, update_rate_hz=5):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=1)
        self.set_update_rate(update_rate_hz)

    def set_update_rate(self, hz):
        # unterstützte Werte: 1, 2, 5, 10 etc.
        interval_ms = int(1000 / hz)
        # PMTK220,<interval>
        pmtk_command = f"$PMTK220,{interval_ms}*{calculate_checksum(f'PMTK220,{interval_ms}')}"

        self.ser.write((pmtk_command + '\r\n').encode('ascii'))
        print(f"Update-Rate gesetzt auf {hz} Hz ({interval_ms} ms)")

    def get_data(self):
        line = self.ser.readline().decode('ascii', errors='ignore')

        if not line.startswith('$GP'):
            return

        try:
            msg = pynmea2.parse(line)
        except pynmea2.nmea.ParseError:
            return

        t = msg.sentence_type

        if t == "GGA":
            par.lat = msg.latitude
            par.lon = msg.longitude
            par.altitude = msg.altitude
            par.satellites = msg.num_sats

        elif t == "RMC":
            par.lat = msg.latitude
            par.lon = msg.longitude
            par.course = msg.true_course
            par.timestamp = msg.datestamp.isoformat() if msg.datestamp else None

        elif t == "VTG":
            par.course = msg.true_track
            par.speed_knts = msg.spd_over_grnd_kts
            par.speed_kmh = msg.spd_over_grnd_kmph

        elif t == "GLL":
            par.lat = msg.latitude
            par.lon = msg.longitude
