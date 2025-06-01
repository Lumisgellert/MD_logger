import os
import time


def reboot():
    print("Neustart wird ausgeführt...")
    os.system('sudo reboot')
    time.sleep(0.1)


if __name__ == "__main__":
    print("Neustart wird ausgeführt...")
    os.system('sudo reboot')
    time.sleep(0.1)
