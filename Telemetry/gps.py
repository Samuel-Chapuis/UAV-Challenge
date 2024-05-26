import time
from pymavlink import mavutil

def extract_lat_lon(data):
    lat = data.lat
    lon = data.lon

    lat = float(lat) / 1e7
    lon = float(lon) / 1e7
    return lat, lon

# Connexion MAVLink
master = mavutil.mavlink_connection('com3', 57600)

# Attendre le heartbeat
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" 
      % (master.target_system, master.target_component))

start_time = time.time()
lat_values = []
lon_values = []

# Collecter les données pendant t secondes
t = 1

while time.time() - start_time < t:
    data = master.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
    if data:
        lat, lon = extract_lat_lon(data)
        lat_values.append(lat)
        lon_values.append(lon)
        print(f"Latitude: {lat}, Longitude: {lon}")

# Calculer la moyenne des valeurs collectées
if lat_values and lon_values:
    avg_lat = sum(lat_values) / len(lat_values)
    avg_lon = sum(lon_values) / len(lon_values)
    print(f"Average Latitude: {avg_lat}, Average Longitude: {avg_lon}")
else:
    print("No data collected")