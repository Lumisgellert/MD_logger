class SimpleKalman:
    def __init__(self, q=0.01, r=0.1):
        """
        Initialisiert einen einfachen 1D-Kalman-Filter.
        q: Prozessrauschen (Q) – wie stark der Wert zwischen den Messungen schwanken kann (Modellunschärfe)
        r: Messrauschen (R) – wie stark einzelne Messwerte schwanken dürfen (Sensorsignal-Rauschen)
        """
        self.Q = q  # Prozessrauschen
        self.R = r  # Messrauschen
        self.x = 0.0   # Aktueller Zustandsschätzer
        self.P = 1.0   # Aktuelle Fehlerkovarianz

    def update(self, measurement):
        """
        Nimmt eine neue Messung entgegen und gibt den gefilterten Wert zurück.
        """
        self.P += self.Q   # Prozessrauschen zum Fehler hinzufügen
        K = self.P / (self.P + self.R)   # Kalman-Gain berechnen
        self.x += K * (measurement - self.x)  # Schätzwert mit Messwert korrigieren
        self.P *= (1 - K)  # Fehlerkovarianz aktualisieren
        return self.x      # Gefilterter Wert
