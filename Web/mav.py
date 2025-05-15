# -------------------------------- #
# Import 
import threading
import random
import math
from pymavlink import mavutil
# -------------------------------- #


class Drone(threading.Thread):
    def __init__(self, name, UDP_IP):
        super().__init__()
        self.name = name
        self.UDP_IP = UDP_IP
        self.master = mavutil.mavlink_connection(UDP_IP)
        
        
    def print_mission_status(self):
        msg = self.master.recv_match(type='MISSION_CURRENT', blocking=True, timeout=5)
        if msg:
            print(f"Mission actuelle: etape {msg.seq}")
        else:
            print("Aucun MISSION_CURRENT recu.")
            
    def print_heartbeat(self):
        msg = self.master.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
        if msg:
            print(f"Heartbeat recu: type {msg.type}, system {msg.get_srcSystem()}, component {msg.get_srcComponent()}")
        else:
            print("Aucun HEARTBEAT recu.")
            
    def monitor_status(self, duration=5):
        start_time = time.time()
        while time.time() - start_time < duration:
            msg = self.master.recv_match(type='STATUSTEXT', blocking=True, timeout=1)
            if msg:
                print(f"Statut: {msg.text}")
            else:
                print("Aucun message de statut recu.")
    
    def clear_mission(self):
        self.master.mav.mission_clear_all_send(self.master.target_system, self.master.target_component)
        print("Mission de " +self.name+ " effacee.")
  
    def move_servo(self, servo_id, position):
        print("Sur " +self.name+ f" deplacement du servo {servo_id} a la position {position}")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0, servo_id, position, 0, 0, 0, 0, 0
        )
        
    def get_current_position(self):
        msg = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if msg:
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.relative_alt / 1000.0
            return lat, lon, alt

    def calculate_offset_coordinates(self, bearing_deg, distance_m):
        lat, lon, _ = self.get_current_position()
        
        lat_rad = math.radians(lat)
        bearing_rad = math.radians(bearing_deg)
        earth_radius = 6371000
        delta_lat = (distance_m / earth_radius) * math.cos(bearing_rad)
        delta_lon = (distance_m / (earth_radius * math.cos(lat_rad))) * math.sin(bearing_rad)
        new_lat = lat + math.degrees(delta_lat)
        new_lon = lon + math.degrees(delta_lon)
        return new_lat, new_lon
    

    


class SubDrone(Drone):
    def __init__(self, name, UDP_IP):
        super().__init__(name, UDP_IP)
        
    def wait_for_ack(self):
        msg = self.master.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
        if msg:
            if msg.type == 0:
                print("MISSION_ACK: mission acceptée.")
                return True
            else:
                print(f"MISSION_ACK reçu mais erreur de type {msg.type}")
        else:
            print("Aucun MISSION_ACK reçu.")
        return False
    
    def lend_with_dolandstart(self, approach_bearing=23):
        lat_touch, lon_touch, _ = self.get_current_position()
    
        cruise_alt = 28
        ground_speed = 16
        final_leg_distance = 250
        descent_rate = 0.5
        descent_time = cruise_alt / descent_rate
        required_leg = ground_speed * descent_time

        print(f"📉 Descente sur {final_leg_distance}m, taux={descent_rate:.2f} m/s")

        wp_final_lat, wp_final_lon = self.calculate_offset_coordinates(lat_touch, lon_touch, (approach_bearing + 180) % 360, final_leg_distance)
        wp_entry_lat, wp_entry_lon = self.calculate_offset_coordinates(wp_final_lat, wp_final_lon, (approach_bearing + 180) % 360, 200)

        mission_items = [
            {"seq": 0, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "lat": wp_entry_lat, "lon": wp_entry_lon, "alt": cruise_alt},
            {"seq": 1, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "lat": wp_final_lat, "lon": wp_final_lon, "alt": cruise_alt},
            {"seq": 2, "cmd": mavutil.mavlink.MAV_CMD_DO_LAND_START, "lat": 0, "lon": 0, "alt": 0},
            {"seq": 3, "cmd": mavutil.mavlink.MAV_CMD_NAV_LAND, "lat": lat_touch, "lon": lon_touch, "alt": 0},
        ]

        self.clear_mission()
        time.sleep(1)
        self.master.mav.mission_count_send(self.master.target_system, self.master.target_component, len(mission_items))

        for item in mission_items:
            while True:
                msg = self.master.recv_match(type='MISSION_REQUEST', blocking=True, timeout=5)
                if msg and msg.seq == item["seq"]:
                    self.master.mav.mission_item_send(
                        self.master.target_system,
                        self.master.target_component,
                        item["seq"],
                        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                        item["cmd"],
                        0, 1, 0, 0, 0, 0,
                        item["lat"], item["lon"], item["alt"]
                    )
                    print(f"✅ Waypoint {item['seq']} envoyé.")
                    break
            time.sleep(0.5)

        return self.wait_for_ack()