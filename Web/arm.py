from pymavlink import mavutil

master = mavutil.mavlink_connection('com3', 57600)

master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)"
	(master.target_system, master.target_component))

master.mav.command_long_send(
	master.target_system, master.target_component,
	mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
