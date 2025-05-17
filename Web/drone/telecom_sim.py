""""

telecom_sim.py - Module for simulating drone telemetry data

"""

# -------------------------------- #
# Import 
import threading
import random
# -------------------------------- #



class DroneSimulator(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.running = True
        
        self.current_lat = 48.8566
        self.current_lon = 2.3522
          
            
    
    def listen_gps(self):
        global current_lat, current_lon
        # Ajout d'une petite variation pour simuler le mouvement
        delta_lat = random.uniform(-0.0005, 0.0005)
        delta_lon = random.uniform(-0.0005, 0.0005)
        self.current_lat += delta_lat
        self.current_lon += delta_lon
        return self.current_lat, self.current_lon
    
    def get_battery_voltage(self):
        # Simule une tension de batterie entre 3.7V et 4.2V
        voltage = random.uniform(3.7, 4.2)
        return voltage

