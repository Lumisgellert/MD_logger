import folium
import os
import Parameter as par

# Globale Liste zum Speichern aller Wegpunkte (GPS-Koordinaten)
waypoints = []
last_lat = 0
last_lon = 0

def collect_cord(lat, lon):
    """
    Fügt einen neuen Wegpunkt (lat, lon) zu der globalen waypoints-Liste hinzu,
    wenn sich die Koordinate geändert hat und beide Werte > 0.0 sind.
    Dadurch werden nur sinnvolle und neue GPS-Punkte gespeichert.
    """
    global last_lat, last_lon

    if lat > 0.0 and lon > 0.0:  # Nur gültige Werte speichern
        if lat != last_lat or lon != last_lon:  # Nur wenn es eine Änderung gab
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                waypoints.append((lat, lon))
                last_lat = lat
                last_lon = lon

def show_map(output_dir=None):
    """
    Erstellt eine HTML-Karte mit allen gespeicherten Wegpunkten und speichert sie im Zielordner.
    Jeder Wegpunkt bekommt einen Marker und die Strecke wird als blaue Linie eingezeichnet.

    :param output_dir: Optionaler Zielordner für die HTML-Datei (Default basiert auf time_start)
    """
    if not par.time_start:
        raise ValueError("time_start wurde noch nicht gesetzt!")

    if not waypoints:
        print("Keine gültigen Wegpunkte vorhanden.")
        return

    # Standard-Ausgabeverzeichnis (z.B. "GPS-Maps/Map_2024-07-01_12-45-00")
    if output_dir is None:
        output_dir = f"GPS-Maps/Map_{par.time_start}"

    # Ordner anlegen, falls noch nicht vorhanden
    os.makedirs(output_dir, exist_ok=True)

    # Name und Pfad der HTML-Datei bestimmen
    file_name = f"GPS-Map_{par.time_start}.html"
    file_path = os.path.join(output_dir, file_name)

    # Karte erzeugen, Startpunkt ist der erste gespeicherte Wegpunkt
    start_lat, start_lon = waypoints[0]
    m = folium.Map(location=[start_lat, start_lon], zoom_start=15)

    # Jeden Wegpunkt als Marker einzeichnen
    for coord in waypoints:
        folium.Marker(location=coord).add_to(m)

    # Die Route als blaue Linie verbinden
    folium.PolyLine(waypoints, color='blue').add_to(m)

    # Karte als HTML speichern
    m.save(file_path)
    print(f"✅ Karte gespeichert als {file_path}")
