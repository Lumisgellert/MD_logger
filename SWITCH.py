import RPi.GPIO as GPIO
import time
import Parameter as par

class SwitchChecker:
    """
    Klasse zum Überwachen eines Tasters oder Schalters an einem GPIO-Pin.
    Erkennt Rising-Edge (flanke steigt) und Falling-Edge (flanke fällt).
    """
    def __init__(self, pin):
        self.pin = pin
        self.Hf = False  # Merker für Falling-Edge (Letzter Status)
        self.Hr = False  # Merker für Rising-Edge (Letzter Status)
        self.RISING_EDGE = False   # Wird True, wenn eine positive Flanke erkannt wird
        self.FALLING_EDGE = False  # Wird True, wenn eine negative Flanke erkannt wird
        GPIO.setmode(GPIO.BCM)  # BCM-Modus: Pin-Nummerierung nach GPIO
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Interner Pull-Down-Widerstand

    def pruefe_einzelnen(self):
        """
        Gibt den aktuellen Schalterstatus zurück (0 = aus, 1 = an).
        """
        return GPIO.input(self.pin)

    def falling_edge(self):
        """
        Erkennt eine fallende Flanke (1 → 0).
        Setzt self.FALLING_EDGE kurzzeitig auf True, wenn erkannt.
        """
        self.FALLING_EDGE = bool(not self.pruefe_einzelnen() and self.Hf)
        self.Hf = self.pruefe_einzelnen()
        return self.FALLING_EDGE

    def rising_edge(self):
        """
        Erkennt eine steigende Flanke (0 → 1).
        Setzt self.RISING_EDGE kurzzeitig auf True, wenn erkannt.
        """
        self.RISING_EDGE = bool(self.pruefe_einzelnen() and not self.Hr)
        self.Hr = self.pruefe_einzelnen()
        return self.RISING_EDGE

    def cleanup(self):
        """
        Gibt alle verwendeten GPIO-Ressourcen wieder frei.
        """
        GPIO.cleanup()

if __name__ == "__main__":
    # Beispiel zum Testen:
    schalter = SwitchChecker(16)  # Pin 16 überwachen
    while True:
        schalter.rising_edge()
        schalter.falling_edge()
        print(schalter.pruefe_einzelnen())
        if schalter.FALLING_EDGE:
            print("fällt")
        if schalter.RISING_EDGE:
            print("steigt")
        time.sleep(1)
