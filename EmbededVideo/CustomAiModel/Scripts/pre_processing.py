import os
import cv2
import numpy as np

from charging_bar import ChargingBar
        

def process_all_image(input_folder, output_folder):
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
    # Charger l'image
    image = cv2.imread(image_path)

    # Vérifier si l'image est chargée correctement
    if image is None:
        print(f"Erreur : impossible de charger l'image {image_path}")
        return

    # Redimensionnement en 1280x1280 (avec padding si nécessaire pour conserver le ratio)
    image = cv2.resize(image, (1280, 1280), interpolation=cv2.INTER_CUBIC) 
    
    # Ajouter un filtrage sur l'image pour détecter le rouge
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([150, 127, 120])
    upper_red = np.array([255, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([130, 35, 200])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    mask = mask1 + mask2
    
    # Produire l'image filtrée
    res = cv2.bitwise_and(image, image, mask=mask)
    
    # Produit enntre le résultat et l'image originale
    res = cv2.addWeighted(image, 0.3, res, 0.7, 0)
    
    # Sauvegarde de l'image traitée
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, res)
 
 
if __name__ == '__main__':
    input_folder = "EmbededVideo/CustomAiModel/RawData/mini_batch"
    output_folder = "EmbededVideo/CustomAiModel/PreProcess/images1s"
    process_all_image(input_folder, output_folder)

    