import folium
import os
import Parameter as par
from datetime import datetime

waypoints = []
last_lat = 0
last_lon = 0


def collect_cord(lat, lon):
    global last_lat, last_lon

    if lat > 0.0 and lon > 0.0:
        if lat != last_lat or lon != last_lon:
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                waypoints.append((lat, lon))
                last_lat = lat
                last_lon = lon


def show_map():
    if not waypoints:
        print("Keine gültigen Wegpunkte vorhanden.")
        return

    # Zielordner
    folder_name = "GPS-Maps"
    os.makedirs(folder_name, exist_ok=True)

    # Zeitstempel für Dateinamen
    file_name = f"GPS-Map_{par.time_start}.html"
    file_path = os.path.join(folder_name, file_name)

    # Karte erzeugen
    start_lat, start_lon = waypoints[0]
    m = folium.Map(location=[start_lat, start_lon], zoom_start=15)

    for coord in waypoints:
        if isinstance(coord, tuple) and len(coord) == 2:
            folium.Marker(location=coord).add_to(m)

    folium.PolyLine(waypoints, color='blue').add_to(m)
    m.save(file_path)
    print(f"Karte gespeichert als {file_path}")
