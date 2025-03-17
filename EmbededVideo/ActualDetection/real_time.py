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
    Exécute l'inférence sur l'image à l'aide du modèle YOLO et retourne une image annotée.
    
    Étapes :
      - Exécution du modèle sur l'image pour obtenir des détections.
      - Parcours des détections pour dessiner des rectangles et ajouter des étiquettes avec le nom de la classe et la confiance.
    
    Args:
        image (numpy.ndarray): L'image d'entrée sur laquelle réaliser la prédiction.
        model (YOLO): Le modèle YOLO utilisé pour la détection.
    
    Returns:
        numpy.ndarray: L'image annotée avec les détections.
    """
    # Exécuter l'inférence
    results = model.predict(source=image, conf=0.25, verbose=False)
    beacons = 0
    detections = results[0]
    annotated_frame = image.copy()
    for box in detections.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = detections.names[cls_id]
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name} {conf:.2f}"
        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    beacons = len(detections.boxes)  # Compter le nombre de détections (beacons)
    
    return annotated_frame, beacons  # Retourner aussi l'état du beacon (détection d'objet)

# -------------------------------------------------------

def load_video(input_file):
    """
    Charge une vidéo depuis un fichier et retourne l'objet VideoCapture.
    
    Args:
        input_file (str): Le chemin vers le fichier vidéo.
    
    Returns:
        cv2.VideoCapture ou None: L'objet VideoCapture si la vidéo est chargée avec succès, sinon None.
    """
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print(f"❌ Impossible d'ouvrir le fichier vidéo : {input_file}")
        return None
    print(f"✅ Fichier vidéo chargé : {input_file}")
    return cap

# -------------------------------------------------------

def video_player(cap, model, target_fps=30):
    """
    Joue une vidéo avec les détections en temps réel du modèle YOLO.
    
    Contrôles utilisateur :
      - 'q' : Quitter la lecture.
      - 'w' : Augmenter la vitesse de lecture.
      - 's' : Diminuer la vitesse de lecture.
      - 'p' ou 'space' : Mettre en pause ou reprendre la lecture.
      - 'a' : Reculer de 30 images.
      - 'd' : Avancer de 30 images.
    
    Args:
        cap (cv2.VideoCapture): L'objet VideoCapture de la vidéo.
        model (YOLO): Le modèle YOLO pour la détection d'objets.
        target_fps (int, optionnel): Le nombre d'images par seconde visé. Par défaut à 30.
    """
    # Affichage des commandes utilisateur
    print("Contrôles:")
    print("  'q' - Quitter")
    print("  'w' - Augmenter la vitesse de lecture")
    print("  's' - Diminuer la vitesse de lecture")
    print("  'p' ou 'space' - Mettre en pause/Reprendre")
    print("  'a' - Reculer (30 images)")
    print("  'd' - Avancer (30 images)")
    
    # Définir le nombre d'images à sauter lors des opérations d'avance/recul
    jump_frames = 30  # par exemple, sauter ~1 seconde à 30 FPS
    
    paused = False
    annotated_frame = None  # Initialisation de la frame annotée pour le mode pause
    while True:
        start_time = time.time()
        
        # Si la lecture n'est pas en pause, lire la frame suivante
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Plus de frames ou lecture impossible du flux vidéo.")
                break

            # Appliquer le filtrage et la détection avec YOLO
            filtered_frame = filter(frame)
            annotated_frame = predict(filtered_frame, model)
        # Si la vidéo est en pause, on réaffiche simplement la dernière frame annotée
        
        # Afficher la vitesse de lecture actuelle (FPS) sur la frame
        cv2.putText(
            annotated_frame,
            f"FPS: {target_fps}" + (" [PAUSE]" if paused else ""),
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Vidéo (Appuyez sur 'q' pour quitter)", annotated_frame)

        # Capturer les entrées utilisateur (délai de 1 ms)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Lecture vidéo arrêtée par l'utilisateur.")
            break
        elif key == ord('w'):
            # Augmenter la vitesse de lecture
            target_fps += 5
            print(f"Vitesse de lecture augmentée : {target_fps} FPS")
        elif key == ord('s'):
            # Diminuer la vitesse de lecture
            target_fps = max(1, target_fps - 5)
            print(f"Vitesse de lecture diminuée : {target_fps} FPS")
        elif key == ord('p') or key == 32:
            # Basculer entre pause et reprise
            paused = not paused
            print("Pause" if paused else "Reprise")
        elif key == ord('a'):
            # Reculer de jump_frames images
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            new_frame = max(0, current_frame - jump_frames)
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            print(f"Recul de la vidéo jusqu'à la frame {new_frame}")
        elif key == ord('d'):
            # Avancer de jump_frames images
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            new_frame = min(total_frames - 1, current_frame + jump_frames)
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            print(f"Avance de la vidéo jusqu'à la frame {new_frame}")

        # Maintenir le target_fps en ajoutant une pause si nécessaire
        if not paused:
            frame_time = 1.0 / target_fps
            elapsed_time = time.time() - start_time
            sleep_time = frame_time - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    cap.release()
    cv2.destroyAllWindows()


# -------------------------------------------------------

if __name__ == "__main__":
    input_file = "EmbededVideo/CustomAiModel/RawData/video/video1.mp4"

    cap = load_video(input_file)
    if cap:
        video_player(cap, model, target_fps=30)
