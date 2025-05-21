import board
import busio


class TCA9548A:
    def __init__(self, i2c, address=0x70):
        self.i2c = i2c
        self.address = address

    def select_channel(self, channel):
        if 0 <= channel <= 7:
            data = bytes([1 << channel])
            while not self.i2c.try_lock():
                pass
            try:
                self.i2c.writeto(self.address, data)
            finally:
                self.i2c.unlock()
        else:
            raise ValueError("Kanal muss zwischen 0 und 7 liegen")


if __name__ == "__main__":
    # Initialisiere I2C mit board-Standard
    i2c = busio.I2C(board.SCL, board.SDA)

    # Erzeuge Multiplexer-Instanz
    mux = TCA9548A(i2c, address=0x70)

    # Kanal 0 aktivieren
    mux.select_channel(0)