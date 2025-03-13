import os
import cv2
import numpy as np

from charging_bar import ChargingBar
        
# FILTER PARAMS
M1_LOWER_RED = np.array([130, 35, 200])
M1_UPPER_RED = np.array([180, 255, 255])        
M2_LOWER_RED = np.array([130, 35, 200])
M2_UPPER_RED = np.array([180, 255, 255])

input_folder = "EmbededVideo/CustomAiModel/RawData/images1s"
# input_folder = "EmbededVideo/CustomAiModel/RawData/mini_batch"
output_folder = "EmbededVideo/CustomAiModel/PreProcess/filtered_images"



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
    
    # Appliquer le filtre
    image = filter(image)
    
    if detect_red(image):
        # Ajouter un tag au nom de l'image 'r_' au début
        red_output_folder = os.path.join(output_folder, "red")
        if not os.path.exists(red_output_folder):
            os.makedirs(red_output_folder)
        image_name = os.path.basename(image_path)
        image_name = f"r_{image_name}"
        output_path = os.path.join(red_output_folder, image_name)
    else:
        non_red_output_folder = os.path.join(output_folder, "non_red")
        if not os.path.exists(non_red_output_folder):
            os.makedirs(non_red_output_folder)
        output_path = os.path.join(non_red_output_folder, os.path.basename(image_path))
    
    # Sauvegarde de l'image traitée
    cv2.imwrite(output_path, image)



def filter(image):
    # Redimensionnement en 1280x1280 (avec padding si nécessaire pour conserver le ratio)
    image = cv2.resize(image, (1280, 1280), interpolation=cv2.INTER_CUBIC) 
    
    # Ajouter un filtrage sur l'image pour détecter le rouge
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv, M1_LOWER_RED, M1_UPPER_RED)
    mask2 = cv2.inRange(hsv, M2_LOWER_RED, M2_UPPER_RED)
    mask = mask1 + mask2
    
    # Produire l'image filtrée
    res = cv2.bitwise_and(image, image, mask=mask)
    
    # Produit enntre le résultat et l'image originale
    res = cv2.addWeighted(image, 0.5, res, 0.5, 0)
    
    return res



def detect_red(image):
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv, M1_LOWER_RED, M1_UPPER_RED)
    mask2 = cv2.inRange(hsv, M2_LOWER_RED, M2_UPPER_RED)
    mask = mask1 + mask2
    
    # Count the number of non-zero (red) pixels
    red_pixels = cv2.countNonZero(mask)

    # You can set the threshold based on experimentation or your needs:
    # Here we use a simple fixed threshold of 3,000 pixels.
    # Alternatively, you could use a ratio (e.g. ratio = red_pixels / mask.size)
    # and compare it to a fraction to detect how much red is in the image.
    threshold = 400
    return red_pixels > threshold

    
 
if __name__ == '__main__':
    process_all_image(input_folder, output_folder)

    