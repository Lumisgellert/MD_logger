import folium

waypoints = []
last_lat = 0
last_lon = 0

def collect_cord(lat, lon):
    global last_lat, last_lon  # Zugriff auf die globalen Variablen

    if lat > 0.0 and lon > 0.0:
        if lat != last_lat or lon != last_lon:
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                waypoints.append((lat, lon))
                #print("Gespeicherte Waypoints:", waypoints)
                last_lat = lat
                last_lon = lon


def show_map():
    if not waypoints:
        print("Keine gÃ¼ltigen Wegpunkte vorhanden.")
        return

    # Erste Koordinate als Startpunkt
    start_lat, start_lon = waypoints[0]
    m = folium.Map(location=[start_lat, start_lon], zoom_start=15)

    for coord in waypoints:
        if isinstance(coord, tuple) and len(coord) == 2:
            folium.Marker(location=coord).add_to(m)

    folium.PolyLine(waypoints, color='blue').add_to(m)
    m.save("gps_karte.html")
    print("Karte gespeichert als gps_karte.html")
