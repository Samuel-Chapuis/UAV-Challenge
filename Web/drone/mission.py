# -------------------------------- #
# Import 
from globalVar import master_Drone, sub_Drone

import time
from pymavlink import mavutil
# -------------------------------- #

def mission():
    master_Drone.print_heartbeat()
    sub_Drone.print_heartbeat()
    
    lat_touch, lon_touch, _ = master_Drone.get_current_position()
    mission_ready = land_with_dolandstart()
    
    if mission_ready:
        master_Drone.move_servo(11, 1150)
        time.sleep(0.7)
        sub_Drone.set_mode("AUTO")
        sub_Drone.mav.command_long_send(
            sub_Drone.target_system,
            sub_Drone.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MODE,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        master_Drone.set_mode("LOITER")
        time.sleep(120)
        master_Drone.set_mode("RTL")
        sub_Drone.monitor_statustext(duration_sec=10)
    else:
        master_Drone.set_mopde("RTL")
        
        
def return_to_launch(drone = 0):
    if drone == 0:
        master_Drone.set_mode("RTL")
    elif drone == 1:
        sub_Drone.set_mode("RTL")
        
