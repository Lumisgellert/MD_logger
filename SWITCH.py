import RPi.GPIO as GPIO
import time
import Parameter as par

class SwitchChecker:
    def __init__(self, pins):
        self.pins = pins
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

    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    while True:
        schalter = SwitchChecker([16])
        print(schalter.pruefe_einzelnen(16))
