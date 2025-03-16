""""

telecom_sim.py - Module for simulating drone telemetry data

"""

# -------------------------------- #
# Import 
import threading
import random
# -------------------------------- #

class DroneSimulator(threading.Thread):
    def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
          super().__init__(group, target, name, args, kwargs, daemon=daemon)
          self.running = True
    
    def listen_gps():
        latitude = random.uniform(-90.0, 90.0)
        longitude = random.uniform(-180.0, 180.0)
        return latitude, longitude

