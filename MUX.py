import smbus2


class TCA9548A:
    def __init__(self, bus=1, address=0x70):
        self.bus = smbus2.SMBus(bus)
        self.address = address

    def select_channel(self, channel):
        if 0 <= channel <= 7:
            self.bus.write_byte(self.address, 1 << channel)
        else:
            raise ValueError("Kanal muss zwischen 0 und 7 liegen")
