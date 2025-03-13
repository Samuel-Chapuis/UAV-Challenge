import cv2
import numpy as np
import time

"""
Ce script capture la vidéo depuis la webcam et détecte les zones de couleur rouge.
Pour ce faire, il convertit chaque image en espace HSV, applique des seuils de couleur,
crée un masque combiné et détecte les contours. Lorsque des contours d'une surface minimale
sont présents de manière continue pendant 0.5 seconde, ils sont encadrés et un message est affiché.
"""

# Initialisation de la capture vidéo via la webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam")
    exit()

detected = False
detection_start_time = 0
min_area = 100  # Taille minimale (en pixels) requise pour considérer un contour comme valide

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire la vidéo")
        break
    
    # Conversion de l'image capturée en espace de couleurs HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Définition des seuils de couleur pour détecter le rouge (première plage)
    lower_red = np.array([0, 100, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    # Définition d'une seconde plage pour le rouge
    lower_red = np.array([170, 110, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    # Combinaison des deux masques pour obtenir l'ensemble des zones rouges
    mask = mask1 + mask2
    
    # Application du masque sur l'image d'origine pour filtrer les zones rouges
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Détection des contours dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrage des contours selon la taille minimale définie
    valid_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
    
    if valid_contours:
        if not detected:
            detection_start_time = time.time()  # Démarrage du chronomètre de détection
            detected = True
        else:
            # Vérification que la détection rouge persiste depuis au moins 0.5 seconde
            if time.time() - detection_start_time >= 0.5:
                # Pour chaque contour valide, dessiner un rectangle autour de la zone détectée
                for contour in valid_contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                print("Tache rouge détectée pendant 1 seconde")
    else:
        detected = False  # Réinitialisation si aucune détection n'est présente
    
    # Affichage de l'image filtrée (zones rouges détectées)
    cv2.imshow('Detected Red', res)
    
    # Affichage de l'image originale avec les éventuels encadrements
    cv2.imshow('Webcam', frame)
    
    # Quitter le programme si la touche 'Echap' (ESC) est appuyée
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
