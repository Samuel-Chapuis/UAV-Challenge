import time
from pymavlink import mavutil

master = mavutil.mavlink_connection('com5', 57600)

master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (master.target_system, master.target_component))


while True:
    msg = master.recv_match(type ="GLOBAL_POSITION_INT",blocking=True)
    print(msg)