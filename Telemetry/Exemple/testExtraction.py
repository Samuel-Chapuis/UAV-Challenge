import re
import time
from pymavlink import mavutil

def extract_lat_lon(data):
    lat_match = re.search(r'lat\s*:\s*(-?\d+)', data)
    lon_match = re.search(r'lon\s*:\s*(-?\d+)', data)

    if lat_match and lon_match:
        lat = float(lat_match.group(1)) / 1e7
        lon = float(lon_match.group(1)) / 1e7
        return lat, lon
    else:
        raise ValueError("lat or lon not found in the data")


msg = "GLOBAL_POSITION_INT {time_boot_ms : 383712, lat : 487874080, lon : 20416098, alt : 177160, relative_alt : -39, vx : 4, vy : 17, vz : 28, hdg : 25507}"
lat, lon = extract_lat_lon(str(msg))
print(f"Latitude: {lat}, Longitude: {lon}")


