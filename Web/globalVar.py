""""

globalVar.py - Ce fichier contient les objets globaux utilisés dans l'application Webb

"""

# -------------------------------- #
from drone.telecom_sim import DroneSimulator
# from drone.mav import Drone, SubDrone
# -------------------------------- #

master_Drone = DroneSimulator()
sub_Drone = DroneSimulator()

# master_Drone = Drone("Master Drone", "udp:127.0.0.1:14550")
# sub_Drone = DroneSimulator() = SubDrone("Sub Drone", "udp:127.0.0.1:15550")