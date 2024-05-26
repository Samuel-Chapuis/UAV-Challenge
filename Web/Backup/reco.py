import cv2
import numpy as np
import time
import serial
from pymavlink import mavutil
import serial.tools.list_ports

from Mavlink import larguer

def reco(cap):
# Initialisation de la capture vidéo
	# cap = cv2.VideoCapture(1)

	if not cap.isOpened():
		print("Erreur : Impossible d'ouvrir la webcam")
		exit()

	detected = False
	detection_start_time = 0
	min_area = 100  # Seuil minimum de taille en pixels pour les contours

	while True:
		ret, frame = cap.read()
		if not ret:
			print("Erreur : Impossible de lire la vidéo")
			break
		
		# Conversion de l'image en espace de couleurs HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		# Définition des seuils de couleur pour détecter le rouge
		lower_red = np.array([0, 100, 70])
		upper_red = np.array([10, 255, 255])
		mask1 = cv2.inRange(hsv, lower_red, upper_red)
		
		lower_red = np.array([170, 110, 70])
		upper_red = np.array([180, 255, 255])
		mask2 = cv2.inRange(hsv, lower_red, upper_red)
		
		# Combinaison des deux masques
		mask = mask1 + mask2
		
		# Application du masque
		res = cv2.bitwise_and(frame, frame, mask=mask)
		
		# Détection des contours
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		valid_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
		
		if valid_contours:
			if not detected:
				detection_start_time = time.time()
				detected = True
			else:
				if time.time() - detection_start_time >= 0.5:
					# Dessiner les contours et afficher le message
					for contour in valid_contours:
						x, y, w, h = cv2.boundingRect(contour)
						cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
					print("Tache rouge détectée pendant 1 seconde")
					master = mavutil.mavlink_connection('com3', 57600)
					print("Attente du signal heartbeat...")
					master.wait_heartbeat()
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
					return
     
		else:
			detected = False
		
		# Affichage de l'image filtrée
		cv2.imshow('Detected Red', res)
		
		# Affichage de l'image originale
		cv2.imshow('Webcam', frame)
		
		if cv2.waitKey(1) & 0xFF == 27:
			break

	cap.release()
	cv2.destroyAllWindows()