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


def kopiere_daten(quellpfad, zielbasis):
    zielpfad = os.path.join(zielbasis, os.path.basename(quellpfad))
    try:
        if os.path.exists(zielpfad):
            shutil.rmtree(zielpfad)
        shutil.copytree(quellpfad, zielpfad)
        print(f"✅ {quellpfad} → {zielpfad}")
    except Exception as e:
        print(f"❌ Fehler beim Kopieren von {quellpfad}: {e}")


def save():
    print("⏳ Warte auf USB-Stick...")
    while True:
        usb_pfad = finde_usb_laufwerk()
        if usb_pfad:
            print(f"💾 USB-Stick erkannt: {usb_pfad}")
            for ordner in QUELL_ORDNER:
                if os.path.exists(ordner):
                    kopiere_daten(ordner, usb_pfad)
                else:
                    print(f"⚠️ Ordner nicht gefunden: {ordner}")
            print("✅ Übertragung abgeschlossen.")
            break
        time.sleep(5)


if __name__ == "__main__":
    save()
