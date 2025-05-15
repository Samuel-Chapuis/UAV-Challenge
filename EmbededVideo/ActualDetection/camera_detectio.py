import cv2
import numpy as np
import torch
import time
from ultralytics import YOLO

# Définition des plages de couleurs pour filtrer le rouge dans l'espace HSV
M1_LOWER_RED = np.array([130, 35, 200])
M1_UPPER_RED = np.array([180, 255, 255])
M2_LOWER_RED = np.array([130, 35, 200])
M2_UPPER_RED = np.array([180, 255, 255])

# -------------------------------------------------------
# Chargement du modèle une seule fois, en le plaçant sur le GPU si possible
model_path = "runs/detect/train/weights/best.pt"  # Chemin vers vos poids personnalisés
model = YOLO(model_path)
if torch.cuda.is_available():
    model.to("cuda")
    print("✅ Utilisation du GPU pour l'inférence.")
else:
    print("⚠️  Aucun périphérique CUDA trouvé ; utilisation du CPU.")
# -------------------------------------------------------

def filter(image):
    """
    Applique un redimensionnement et un filtrage de l'image pour isoler les zones rouges.
    
    Étapes :
      - Redimensionnement de l'image à 1280x1280 en utilisant une interpolation cubique.
      - Conversion de l'image du format BGR à l'espace de couleurs HSV.
      - Création de deux masques pour détecter le rouge selon des plages de valeurs définies.
      - Combinaison des masques et application d'un filtrage bit-à-bit pour extraire les zones ciblées.
      - Fusion de l'image originale et de l'image filtrée pour un rendu final.
    
    Args:
        image (numpy.ndarray): L'image d'entrée en format BGR.
    
    Returns:
        numpy.ndarray: L'image filtrée avec une superposition du masque.
    """
    image = cv2.resize(image, (1280, 1280), interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, M1_LOWER_RED, M1_UPPER_RED)
    mask2 = cv2.inRange(hsv, M2_LOWER_RED, M2_UPPER_RED)
    mask = mask1 + mask2
    res = cv2.bitwise_and(image, image, mask=mask)
    return cv2.addWeighted(image, 0.5, res, 0.5, 0)

# -------------------------------------------------------

def predict(image, model):
    """
    Exécute l'inférence sur l'image à l'aide du modèle YOLO et retourne une image annotée, le nombre de détections
    et la liste de rectangles (x1, y1, x2, y2) pour chaque détection.
    
    Args:
        image (numpy.ndarray): L'image d'entrée sur laquelle réaliser la prédiction.
        model (YOLO): Le modèle YOLO utilisé pour la détection.
    
    Returns:
        tuple: (annotated_frame, beacons, detection_boxes)
            annotated_frame (numpy.ndarray): L'image annotée.
            beacons (int): Nombre de détections.
            detection_boxes (list): Liste de tuples pour les coordonnées des boîtes détectées.
    """
    # Exécuter l'inférence
    results = model.predict(source=image, conf=0.25, verbose=False)
    detections = results[0]
    annotated_frame = image.copy()
    detection_boxes = []
    
    for box in detections.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = detections.names[cls_id]
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name} {conf:.2f}"
        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
        detection_boxes.append((x1, y1, x2, y2))
    
    beacons = len(detection_boxes)  # Compter le nombre de détections (beacons)
    
    return annotated_frame, beacons, detection_boxes

# -------------------------------------------------------

def function_de_Matheo():
    """
    Fonction de démonstration pour illustrer l'utilisation de la fonction de détection.
    
    Cette fonction est un exemple et peut être modifiée selon les besoins spécifiques.
    """
    print("Fonction de Matheo exécutée.")

# -------------------------------------------------------

if __name__ == "__main__":
    stream = 0 
    cap = cv2.VideoCapture(stream)
    if not cap.isOpened():
        print("Erreur lors de l'ouverture du flux vidéo.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Impossible de lire une image depuis le flux vidéo.")
            break

        # Appliquer le filtre sur l'image pour isoler les zones rouges
        filtered_frame = filter(frame)

        # Détecter les beacons dans l'image filtrée
        annotated_frame, beacon_count, boxes = predict(filtered_frame, model)

        # Si des beacons ont été détectés, dessiner une boîte englobante autour de toutes les détections
        if boxes:
            
            function_de_Matheo()
            
            x1_list, y1_list, x2_list, y2_list = zip(*boxes)
            x1_group = min(x1_list)
            y1_group = min(y1_list)
            x2_group = max(x2_list)
            y2_group = max(y2_list)
            # Dessiner la boîte englobante en bleu
            cv2.rectangle(annotated_frame, (x1_group, y1_group), (x2_group, y2_group), (255, 0, 0), 2)
            cv2.putText(annotated_frame, f"Beacons: {beacon_count}", (x1_group, y1_group - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

