import os
import cv2
import numpy as np
from charging_bar import ChargingBar

# Paramètres du filtre pour la détection de la couleur rouge
M1_LOWER_RED = np.array([130, 35, 200])
M1_UPPER_RED = np.array([180, 255, 255])
M2_LOWER_RED = np.array([130, 35, 200])
M2_UPPER_RED = np.array([180, 255, 255])

# Dossiers d'entrée et de sortie
input_folder = "EmbededVideo/CustomAiModel/RawData/images1s"
output_folder = "EmbededVideo/CustomAiModel/PreProcess/filtered_images"

def process_all_image(input_folder, output_folder):
    """
    Traite toutes les images d'un dossier en les filtrant et en les classant
    en fonction de la présence de rouge.

    :param input_folder: Chemin du dossier contenant les images à traiter
    :param output_folder: Chemin du dossier où enregistrer les images filtrées
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    bar = ChargingBar(len(os.listdir(input_folder)))
    bar.show()
    
    for image_name in os.listdir(input_folder):
        if image_name.lower().endswith('.jpg'):
            image_path = os.path.join(input_folder, image_name)
            process_image(image_path, output_folder)
            bar.update()

def process_image(image_path, output_folder):
    """
    Charge, filtre et enregistre une image dans le bon dossier selon
    la présence de la couleur rouge.
    
    :param image_path: Chemin de l'image à traiter
    :param output_folder: Dossier où stocker l'image filtrée
    """
    # Charger l'image
    image = cv2.imread(image_path)

    # Vérifier si l'image est correctement chargée
    if image is None:
        print(f"Erreur : impossible de charger l'image {image_path}")
        return
    
    # Appliquer le filtre
    image = filter(image)
    
    # Vérifier la présence de rouge et trier l'image
    if detect_red(image):
        red_output_folder = os.path.join(output_folder, "red")
        os.makedirs(red_output_folder, exist_ok=True)
        image_name = f"r_{os.path.basename(image_path)}"
        output_path = os.path.join(red_output_folder, image_name)
    else:
        non_red_output_folder = os.path.join(output_folder, "non_red")
        os.makedirs(non_red_output_folder, exist_ok=True)
        output_path = os.path.join(non_red_output_folder, os.path.basename(image_path))
    
    # Sauvegarde de l'image traitée
    cv2.imwrite(output_path, image)

def filter(image):
    """
    Applique un redimensionnement et un filtre détectant la couleur rouge.
    
    :param image: Image originale à traiter
    :return: Image filtrée
    """
    image = cv2.resize(image, (1280, 1280), interpolation=cv2.INTER_CUBIC) 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, M1_LOWER_RED, M1_UPPER_RED)
    mask2 = cv2.inRange(hsv, M2_LOWER_RED, M2_UPPER_RED)
    mask = mask1 + mask2
    res = cv2.bitwise_and(image, image, mask=mask)
    return cv2.addWeighted(image, 0.5, res, 0.5, 0)

def detect_red(image):
    """
    Détecte si une image contient une quantité significative de rouge.
    
    :param image: Image à analyser
    :return: Booléen indiquant la présence de rouge
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, M1_LOWER_RED, M1_UPPER_RED)
    mask2 = cv2.inRange(hsv, M2_LOWER_RED, M2_UPPER_RED)
    mask = mask1 + mask2
    red_pixels = cv2.countNonZero(mask)
    return red_pixels > 400

if __name__ == '__main__':
    process_all_image(input_folder, output_folder)
