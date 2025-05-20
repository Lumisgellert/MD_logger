import time
from smbus2 import SMBus


class DOGS164Display:
    I2C_ADDR =0x78   # oder 0x3C oder, je nach SA0-Pin
    COMMAND = 0x00
    DATA = 0x40

    def __init__(self, bus=1):
        self.bus = SMBus(bus)
        self._init_display()

    def _send(self, control, data):
        self.bus.write_i2c_block_data(self.I2C_ADDR, control, [data])

    def _send_command(self, cmd):
        self._send(self.COMMAND, cmd)

    def _send_data(self, data):
        self._send(self.DATA, data)

    def _init_display(self):
        cmds = [
            0x3A,  # Function set: 8 bit, RE=1
            0x09,  # 4-line mode
            0x06,  # Entry mode: BDC=0, BDS=1 (bottom view)
            0x1E,  # Bias setting
            0x39,  # Function set: 8 bit, RE=0, IS=1
            0x1B,  # Internal OSC
            0x6C,  # Follower control
            0x56,  # Power control
            0x7A,  # Contrast
            0x38,  # Function set: normal instruction set
            0x0C,  # Display on, cursor off, blink off
        ]
        for cmd in cmds:
            self._send_command(cmd)
            time.sleep(0.01)

    def clear(self):
        self._send_command(0x01)
        time.sleep(0.01)

    def set_cursor(self, line, pos):
        # DDRAM Adressen laut Datenblatt (Bottom View)
        line_offsets = [0x00, 0x20, 0x40, 0x60]
        address = line_offsets[line] + pos
        self._send_command(0x80 | address)

    def write(self, text, line=0):
        self.set_cursor(line, 0)
        for char in text.ljust(16)[:16]:  # max 16 Zeichen pro Zeile
            self._send_data(ord(char))

# Beispielanwendung:
if __name__ == "__main__":
    display = DOGS164Display()
    display.clear()
    display.write("Hallo Welt!", line=0)
    display.write("Zeile 2", line=1)