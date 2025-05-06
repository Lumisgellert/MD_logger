import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import Parameter as par


def plot(filepath, columns_to_plot, output_dir="plots"):
    # CSV einlesen
    df = pd.read_csv(filepath)

    # Zeitspalte in datetime umwandeln
    df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%d_%H-%M-%S", errors='coerce')
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
        plt.plot(df['time'], df[col], marker='o')
        plt.xlabel("Zeit")
        plt.ylabel(col)
        plt.title(f"{col} über Zeit")
        plt.grid(True)
        plt.tight_layout()

        # PNG-Dateiname
        filename = f"{output_dir}/{col}_{par.timestamp}.png"
        plt.savefig(filename)
        plt.close()
        print(f"✅ Plot gespeichert: {filename}")

# Beispielaufruf:
# plot_and_save_csv_data("deine_daten.csv", ["v[km/h]", "alt_GND[m]", "sat[n]"])
