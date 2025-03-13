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

    # Appliquer un filtre CLAHE pour améliorer le contraste
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # Convertir en LAB
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)  # Améliorer la luminosité
    lab = cv2.merge((l, a, b))
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # Reconvertir en BGR

    # Augmenter la saturation du rouge
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.addWeighted(s, 5, np.zeros_like(s), 0, 0)  # Augmenter la saturation
    hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Sauvegarde de l'image traitée
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, image)
 
 
if __name__ == '__main__':
	input_folder = "EmbededVideo/CustomAiModel/RawData/images1s"
	output_folder = "EmbededVideo/CustomAiModel/PreProcess/mini_batch"
	process_all_image(input_folder, output_folder)

	