""""

telecom_sim.py - Module for simulating drone telemetry data

"""

# -------------------------------- #
# Import 
import threading
import random
# -------------------------------- #

current_lat = 48.8566
current_lon = 2.3522

class DroneSimulator(threading.Thread):
    def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
          super().__init__(group, target, name, args, kwargs, daemon=daemon)
          self.running = True
    
    def listen_gps():
        global current_lat, current_lon
        # Ajout d'une petite variation pour simuler le mouvement
        delta_lat = random.uniform(-0.0005, 0.0005)
        delta_lon = random.uniform(-0.0005, 0.0005)
        current_lat += delta_lat
        current_lon += delta_lon
        return current_lat, current_lon

