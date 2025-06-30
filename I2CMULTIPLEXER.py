import smbus
import time

class I2CMultiplexer:
    """
    Klasse zur Steuerung eines I2C-Multiplexers (z.B. TCA9548A).
    Ermöglicht das gezielte Auswählen eines von bis zu 8 I2C-Kanälen.
    """
    def __init__(self, address=0x70, bus_num=1):
        """
        Initialisiert den Multiplexer.
        - address: I2C-Adresse des Multiplexers (Default: 0x70)
        - bus_num: I2C-Busnummer (meistens 1 beim Raspberry Pi)
        """
        self.address = address
        self.bus = smbus.SMBus(bus_num)

        # Initial: Alle Kanäle deaktivieren, um den MUX zu "leeren"
        print("Deaktiviere alle MUX-Kanäle (0x00)")
        self.bus.write_byte(self.address, 0x00)
        time.sleep(0.1)

        # Einmal kurz Kanal 0 aktivieren, dann wieder deaktivieren (zur Initialisierung)
        self.bus.write_byte(self.address, 0x01)
        time.sleep(0.1)

        self.bus.write_byte(self.address, 0x00)
        time.sleep(0.1)

    def select_channel(self, channel):
        """
        Wählt einen der 8 MUX-Kanäle aus (0–7).
        Aktiviert den gewünschten Kanal, indem das entsprechende Bit gesetzt wird.
        """
        if 0 <= channel <= 7:
            try:
                self.bus.write_byte(self.address, 1 << channel)
            except Exception as error:
                # Fehler beim Kanalwechsel, z.B. Sensor nicht erreichbar
                raise RuntimeError(f"Sensor auf Kanal {channel} nicht erreichbar: {error}")
        else:
            raise ValueError("Ungültiger I2C-Kanal: {}".format(channel))

# Beispielcode zum Testen (auskommentiert, kann bei Bedarf aktiviert werden)
"""
if __name__ == "__main__":
    bus = smbus.SMBus(1)
    mux_address = 0x70

    try:
        bus.write_byte(mux_address, 0x01)  # Kanal 0 aktivieren
        print("Kanal 0 aktiviert.")
    except OSError as e:
        print("Fehler:", e)
"""
