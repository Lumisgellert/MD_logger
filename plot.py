import pandas as pd
import matplotlib.pyplot as plt
import os
import Parameter as par


def plot(filepath, columns_to_plot, output_dir=None):
    if not par.time_start:
        raise ValueError("time_start wurde noch nicht gesetzt!")

    # Output-Dir bei jedem Aufruf neu setzen
    if output_dir is None:
        output_dir = f"plots/Messung {par.time_start}"
    # CSV einlesen
    df = pd.read_csv(filepath)

    # Zeitspalte in datetime umwandeln (korrektes Format!)
    df['time'] = pd.to_datetime(df['time'], format="%d.%m.%Y %H:%M:%S.%f", errors='coerce')
    df = df.dropna(subset=['time'])

    # Versuche alle Spalten numerisch zu interpretieren
    for col in df.columns:
        if col != 'time':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Erstelle Ausgabeordner (falls nicht vorhanden)
    os.makedirs(output_dir, exist_ok=True)

    for col in columns_to_plot:
        if col not in df.columns:
            print(f"Spalte '{col}' nicht gefunden – wird übersprungen.")
            continue
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

        # PNG-Dateiname
        filename = f"{output_dir}/plot_{col}_{par.time_start}.png"
        print(filename)
        plt.savefig(filename)
        plt.close()
        print(f"✅ Plots gespeichert: {filename}")

if __name__ == "__main__":
    plot("CSV-Datein/Messdaten_2025-05-06_14-10-06.csv", ["v[kmh]", "alt_GND[m]", "sat[n]"])
