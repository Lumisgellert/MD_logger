import RPi.GPIO as GPIO
import time
import Parameter as par


class SwitchChecker:
    def __init__(self, pins):
        self.pins = pins
        self.Hf = False
        self.Hr = False
        GPIO.setmode(GPIO.BCM)  # BCM-Modus: Pin-Nummerierung nach GPIO
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def pruefe_alle(self):
        zustand = {}
        for pin in self.pins:
            zustand[pin] = GPIO.input(pin)

        par.S1 = zustand[0]
        par.S2 = zustand[1]

    def pruefe_einzelnen(self, pin):
        if pin in self.pins:
            return GPIO.input(pin)
        else:
            raise ValueError("Pin nicht in der Liste!")

    def falling_edge(self, pin):
        par.falling_edge = bool(not self.pruefe_einzelnen(pin) and self.Hf)
        self.Hf = self.pruefe_einzelnen(pin)
        return par.falling_edge

    def rising_edge(self, pin):
        par.rising_edge = bool(self.pruefe_einzelnen(pin) and not self.Hr)
        self.Hr = self.pruefe_einzelnen(pin)
        return par.rising_edge

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
