import pandas as pd
import matplotlib.pyplot as plt
import os
import Parameter as par

def plot(filepath, columns_to_plot, output_dir=None):
    """
    Erstellt Zeitreihen-Plots für die angegebenen Spalten einer CSV-Datei.
    Die Plots werden als PNG-Dateien gespeichert.

    :param filepath: Pfad zur CSV-Datei mit den Messdaten
    :param columns_to_plot: Liste der zu plottenden Spaltennamen
    :param output_dir: Zielverzeichnis für die Plots (optional)
    """

    # Sicherstellen, dass ein Messungs-Zeitpunkt vorhanden ist
    if not par.time_start:
        raise ValueError("time_start wurde noch nicht gesetzt!")

    # Standard-Ausgabeverzeichnis dynamisch auf Basis des Messungszeitpunkts
    if output_dir is None:
        output_dir = f"plots/Messung {par.time_start}"

    # CSV einlesen
    df = pd.read_csv(filepath)

    # Zeitspalte in datetime-Objekte umwandeln (Format beachten!)
    df['time'] = pd.to_datetime(df['time'], format="%d.%m.%Y %H:%M:%S.%f", errors='coerce')
    df = df.dropna(subset=['time'])  # Zeilen ohne gültigen Zeitstempel entfernen

    # Alle Spalten (außer 'time') als numerisch interpretieren, Fehler werden zu NaN
    for col in df.columns:
        if col != 'time':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Zielverzeichnis für die Plots erstellen (falls nicht vorhanden)
    os.makedirs(output_dir, exist_ok=True)

    # Für jede gewünschte Spalte...
    for col in columns_to_plot:
        # Prüfen, ob die Spalte überhaupt in der CSV existiert
        if col not in df.columns:
            print(f"Spalte '{col}' nicht gefunden – wird übersprungen.")
            continue
        # Prüfen, ob die Spalte gültige Werte enthält
        if df[col].dropna().empty:
            print(f"Spalte '{col}' enthält keine gültigen Werte – wird übersprungen.")
            continue

        # Plot erstellen
        plt.figure(figsize=(12, 6))
        plt.plot(df['time'], df[col])
        plt.xlabel("Zeit")
        plt.ylabel(col)
        plt.title(f"{col} über Zeit")
        plt.grid(True)
        plt.tight_layout()

        # Dateiname für den Plot (PNG)
        filename = f"{output_dir}/plot_{col}_{par.time_start}.png"
        print(filename)
        plt.savefig(filename)
        plt.close()
        print(f"✅ Plots gespeichert: {filename}")

if __name__ == "__main__":
    # Testaufruf für ein einzelnes Beispiel (wird nur ausgeführt, wenn das Skript direkt gestartet wird)
    plot("CSV-Datein/Messdaten_2025-05-06_14-10-06.csv", ["v[kmh]", "alt_GND[m]", "sat[n]"])
