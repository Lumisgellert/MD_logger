import smbus


class I2CMultiplexer:
    def __init__(self, address=0x70, bus_num=1):
        self.address = address
        self.bus = smbus.SMBus(bus_num)

    def select_channel(self, channel):
        if 0 <= channel <= 7:
            self.bus.write_byte(self.address, 1 << channel)
        else:
            raise ValueError("Ungültiger I2C-Kanal: {}".format(channel))
