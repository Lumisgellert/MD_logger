import RPi.GPIO as GPIO
from time import sleep
import Parameter as par
import threading

class LedSystem:
    """
    Klasse zur Steuerung einer einzelnen LED am Raspberry Pi über einen GPIO-Pin.
    Unterstützt An, Aus und Blinken (schnell/langsam).
    """
    def __init__(self, pin):
        """
        Konstruktor. Setzt den Pin als Ausgang und initialisiert ihn als AUS.
        Wenn der GPIO-Modus noch nicht gesetzt ist, wird BCM gewählt.
        """
        self.pin = pin
        if not GPIO.getmode():  # Prüft, ob ein GPIO-Modus gesetzt wurde
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        """
        Schaltet die LED ein (Pin auf HIGH).
        """
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        """
        Schaltet die LED aus (Pin auf LOW).
        Setzt auch den Blink-State in den Parametern auf False, damit Blink-Loops beendet werden.
        """
        par.led_blink_state = False
        GPIO.output(self.pin, GPIO.LOW)

    def blink_fast(self):
        """
        Lässt die LED schnell (0,5 s an / 0,5 s aus) blinken.
        Die Methode läuft in einer Endlosschleife, solange led_blink_state True ist.
        """
        self.off()  # Sicherstellen, dass vorherige Blink-Schleifen gestoppt werden
        par.led_blink_state = True
        while par.led_blink_state:
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(0.5)   # LED 0,5 Sekunden an
            GPIO.output(self.pin, GPIO.LOW)
            sleep(0.5)   # LED 0,5 Sekunden aus

    def blink_slow(self):
        """
        Lässt die LED langsam (1 s an / 1 s aus) blinken.
        Die Methode läuft in einer Endlosschleife, solange led_blink_state True ist.
        """
        par.led_blink_state = True
        while par.led_blink_state:
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(1)   # LED 1 Sekunde an
            GPIO.output(self.pin, GPIO.LOW)
            sleep(1)   # LED 1 Sekunde aus

    def __del__(self):
        """
        Destruktor: Wird aufgerufen, wenn das Objekt gelöscht wird.
        Führt ein GPIO.cleanup() durch, um alle GPIO-Pins freizugeben.
        """
        # self
