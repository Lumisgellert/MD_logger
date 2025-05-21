import smbus


class I2CMultiplexer:
    def __init__(self, address=0x70, bus_num=1):
        self.address = address
        self.bus = smbus.SMBus(bus_num)

    def select_channel(self, channel):
        if 0 <= channel <= 7:
            try:
                self.bus.write_byte(self.address, 1 << channel)
            except Exception as error:
                print(f"❌ Sensor auf Kanal {channel} konnte nicht initialisiert werden: {error}")
        else:
            raise ValueError("Ungültiger I2C-Kanal: {}".format(channel))


if __name__ == "__main__":
    bus = smbus.SMBus(1)
    mux_address = 0x70

    try:
        bus.write_byte(mux_address, 0x01)  # Kanal 0 aktivieren
        print("Kanal 0 aktiviert.")
    except OSError as e:
        print("Fehler:", e)
