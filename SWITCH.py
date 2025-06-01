import RPi.GPIO as GPIO
import time
import Parameter as par


class SwitchChecker:
    def __init__(self, pin):
        self.pin = pin
        self.Hf = False
        self.Hr = False
        self.RISING_EDGE = False
        self.FALLING_EDGE = False
        GPIO.setmode(GPIO.BCM)  # BCM-Modus: Pin-Nummerierung nach GPIO
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def pruefe_alle(self):
        zustand = []
        zustand[self.pin] = GPIO.input(self.pin)

        par.S1 = zustand[0]
        par.S2 = zustand[1]

    def pruefe_einzelnen(self):
        return GPIO.input(self.pin)

    def falling_edge(self):
        self.RISING_EDGE = bool(not self.pruefe_einzelnen() and self.Hf)
        self.Hf = self.pruefe_einzelnen()
        return self.RISING_EDGE

    def rising_edge(self, pin):
        self.FALLING_EDGE = bool(self.pruefe_einzelnen() and not self.Hr)
        self.Hr = self.pruefe_einzelnen()
        return self.FALLING_EDGE

    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    schalter = SwitchChecker([16])
    while True:
        schalter.rising_edge(16)
        schalter.falling_edge(16)
        print(schalter.pruefe_einzelnen(16))
        if par.falling_edge:
            print("fällt")
        if par.rising_edge:
            print("steigt")
        time.sleep(1)
