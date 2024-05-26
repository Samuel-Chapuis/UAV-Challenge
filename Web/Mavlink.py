import serial
from pymavlink import mavutil
import serial.tools.list_ports
import time

# Fonction pour envoyer une commande pour actionner un servo
# def set_servo(servo_number, pwm_value):
#     master.mav.command_long_send(
#         master.target_system, 
#         master.target_component,
#         mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
#         0,                # confirmation
#         servo_number,     # numéro du servo (de 1 à 8 en général)
#         pwm_value,        # valeur PWM à envoyer au servo (en microsecondes, typiquement entre 1000 et 2000)
#         0, 0, 0, 0, 0, 0  # paramètres non utilisés
#     )
    
def close_existing_connections(port_name):
    # Liste tous les ports série disponibles
    available_ports = serial.tools.list_ports.comports()
    for port in available_ports:
        if port.device == port_name:
            try:
                ser = serial.Serial(port.device)
                ser.close()
                print(f"Connexion fermée sur le port {port.device}")
            except Exception as e:
                print(f"Erreur en fermant le port {port.device}: {e}")

def larguer():
	# Connexion au drone
	#close_existing_connections('com5')
	master = mavutil.mavlink_connection('com3', 57600)

	# Attendre un signal heartbeat pour vérifier la connexion
	print("Attente du signal heartbeat...")
	master.wait_heartbeat()
	print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

	# Commande le servo 10 à 3000, LIBERE LE MINI DRONE
	master.mav.command_long_send(
        master.target_system, 
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,                # confirmation
        10,     # numéro du servo (de 1 à 8 en général)
        2000,        # valeur PWM à envoyer au servo (en microsecondes, typiquement entre 1000 et 2000)
        0, 0, 0, 0, 0, 0  # paramètres non utilisés
    )
	print("Mini drone largué !")
 
def resetServo():
	# Connexion au drone
	#close_existing_connections('com5')
	master = mavutil.mavlink_connection('com3', 57600)

	# Attendre un signal heartbeat pour vérifier la connexion
	print("Attente du signal heartbeat...")
	master.wait_heartbeat()
	print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

	# Commande le servo 10 à 3000, LIBERE LE MINI DRONE
	master.mav.command_long_send(
        master.target_system, 
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,                # confirmation
        10,     # numéro du servo (de 1 à 8 en général)
        1500,        # valeur PWM à envoyer au servo (en microsecondes, typiquement entre 1000 et 2000)
        0, 0, 0, 0, 0, 0  # paramètres non utilisés
    )
	print("Mini drone largué !")
 
def armer():
	master = mavutil.mavlink_connection('com3', 57600)
	print("Attente du signal heartbeat...")
	master.wait_heartbeat()
	print("Heartbeat from system (system %u component %u)"
		(master.target_system, master.target_component))
	master.mav.command_long_send(
		master.target_system, master.target_component,
		mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
 
 
 
 
 
 
 
 