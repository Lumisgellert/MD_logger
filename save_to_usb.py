import os
import shutil
import time

# Basispfad relativ zum Speicherort des Skripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Relativ benannte Ordner
ORDNER_NAMEN = ["plots", "CSV-Datein", "GPS-Maps"]
QUELL_ORDNER = [os.path.join(SCRIPT_DIR, name) for name in ORDNER_NAMEN]

# Optional: nur bestimmter USB-Stick
USB_NAME = ""  # z. B. "MY_USB", oder leer für beliebigen


def finde_usb_laufwerk(basis="/media/Data"):
    if not os.path.exists(basis):
        return None
    for eintrag in os.listdir(basis):
        voller_pfad = os.path.join(basis, eintrag)
        if os.path.ismount(voller_pfad):
            if not USB_NAME or eintrag == USB_NAME:
                return voller_pfad
    return None


def kopiere_daten_nicht_ueberschreiben(quellordner, zielbasis):
    zielordner = os.path.join(zielbasis, os.path.basename(quellordner))
    os.makedirs(zielordner, exist_ok=True)

    for wurzel, verzeichnisse, dateien in os.walk(quellordner):
        rel_pfad = os.path.relpath(wurzel, quellordner)
        ziel_wurzel = os.path.join(zielordner, rel_pfad)

        os.makedirs(ziel_wurzel, exist_ok=True)

        for datei in dateien:
            quell_datei = os.path.join(wurzel, datei)
            ziel_datei = os.path.join(ziel_wurzel, datei)

            # Kopiere Datei nur, wenn sie noch nicht existiert oder neuer ist
            if not os.path.exists(ziel_datei) or os.path.getmtime(quell_datei) > os.path.getmtime(ziel_datei):
                shutil.copy2(quell_datei, ziel_datei)
                print(f"📁 {quell_datei} → {ziel_datei}")


def save():
    print("⏳ Warte auf USB-Stick...")
    delay = 20  # Sekunden
    start = time.time()
    while time.time() - start < delay:
        usb_pfad = finde_usb_laufwerk()
        if usb_pfad:
            print(f"💾 USB-Stick erkannt: {usb_pfad}")
            for ordner in QUELL_ORDNER:
                if os.path.exists(ordner):
                    kopiere_daten_nicht_ueberschreiben(ordner, usb_pfad)
                    shutil.rmtree(ordner)  # Quellordner löschen
                    print(f"✅ {ordner} erfolgreich gelöscht")
                else:
                    print(f"⚠️ Ordner nicht gefunden: {ordner}")
            print("✅ Übertragung abgeschlossen.")
            return
        time.sleep(0.5)
    print("⚠️ Es wurde kein USB-Stick eingesteckt!")



if __name__ == "__main__":
    save()
