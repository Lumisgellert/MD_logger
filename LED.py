import RPi.GPIO as GPIO
from time import sleep
import Parameter as par
import threading


class LedSystem:
    def __init__(self, pin):
        self.pin = pin
        if not GPIO.getmode():  # Überprüfen, ob der Modus bereits gesetzt wurde
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    # Schaltet die LED an. Weiß ist als default Wert hinterlegt
    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print(par.led_blink_state)

    # Schaltet die LED aus
    def off(self):
        par.led_blink_state = False
        GPIO.output(self.pin, GPIO.LOW)
        print(par.led_blink_state)

    def blink_fast(self):
        self.off()
        par.led_blink_state = True
        while par.led_blink_state:
            GPIO.output(self.pin, GPIO.HIGH)
            print(par.led_blink_state)
            sleep(1/2)
            GPIO.output(self.pin, GPIO.LOW)
            print(par.led_blink_state)
            sleep(1/2)

    def blink_slow(self):
        par.led_blink_state = True
        while par.led_blink_state:
            GPIO.output(self.pin, GPIO.HIGH)
            print(par.led_blink_state)
            sleep(1/1)
            GPIO.output(self.pin, GPIO.LOW)
            print(par.led_blink_state)
            sleep(1/1)

    def __del__(self):
        # Aufräumen der GPIOs, wenn das Objekt gelöscht wird
        self.off()
        GPIO.cleanup()
