import serial
import pynmea2
import Parameter as par

def calculate_checksum(sentence):
    """
    Berechnet die NMEA-Checksumme für einen gegebenen Befehlssatz (ohne $ und ohne *).
    Das Ergebnis wird als zweistelliger Hex-String zurückgegeben.
    """
    cs = 0
    for char in sentence:
        cs ^= ord(char)
    return f"{cs:02X}"

class GPS:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, update_rate_hz=5):
        """
        Initialisiert die serielle Verbindung zum GPS-Modul.
        port: Geräteschnittstelle (z.B. '/dev/ttyAMA0')
        baudrate: Übertragungsgeschwindigkeit
        update_rate_hz: Aktualisierungsrate der GPS-Daten (Hz)
        """
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=1)
        self.set_update_rate(update_rate_hz)

    def set_update_rate(self, hz):
        """
        Stellt die Ausgabe-Rate des GPS-Moduls auf hz Hertz ein.
        Sendet dazu einen speziellen PMTK-Befehl an das Modul.
        """
        interval_ms = int(1000 / hz)  # Intervall in Millisekunden berechnen
        # PMTK220,<interval> Befehl (Herstellerspezifisch)
        pmtk_command = f"$PMTK220,{interval_ms}*{calculate_checksum(f'PMTK220,{interval_ms}')}"
        self.ser.write((pmtk_command + '\r\n').encode('ascii'))
        print(f"Update-Rate gesetzt auf {hz} Hz ({interval_ms} ms)")

    def get_data(self):
        """
        Endlosschleife zum Einlesen und Parsen von GPS-Daten.
        Erkennt verschiedene NMEA-Sätze und schreibt die Werte in das Parameter-Modul.
        Wird in der Regel in einem separaten Thread aufgerufen.
        """
        par.loopBit = True
        while par.loopBit is True:
            # Zeile von der seriellen Schnittstelle lesen (NMEA-Satz)
            line = self.ser.readline().decode('ascii', errors='ignore')
            # Nur Sätze, die mit '$GP' beginnen, verarbeiten (GPS-relevant)
            if not line.startswith('$GP'):
                continue

            try:
                # Satz mit pynmea2 parsen
                msg = pynmea2.parse(line)
            except pynmea2.nmea.ParseError:
                # Falls Parsing fehlschlägt, Satz ignorieren
                continue

            t = msg.sentence_type  # Typ des NMEA-Satzes (z.B. GGA, RMC, VTG, GLL)

            # Auswertung je nach Satztyp:
            if t == "GGA":
                # GGA liefert Position, Höhe und Satellitenanzahl
                par.lat = msg.latitude
                par.lon = msg.longitude
                par.altitude = msg.altitude
                par.satellites = msg.num_sats

            elif t == "RMC":
                # RMC liefert u.a. Position und Kurs
                par.lat = msg.latitude
                par.lon = msg.longitude
                par.course = msg.true_course

            elif t == "VTG":
                # VTG liefert Kurs und Geschwindigkeit
                par.course = msg.true_track
                par.speed_knts = msg.spd_over_grnd_kts
                par.speed_kmh = msg.spd_over_grnd_kmph

            elif t == "GLL":
                # GLL liefert nur Position
                par.lat = msg.latitude
                par.lon = msg.longitude
