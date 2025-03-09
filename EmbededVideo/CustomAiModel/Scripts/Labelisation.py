import os
import subprocess

# Définir le chemin des images et des annotations
IMAGE_DIR = "images"  # Dossier où sont stockées les images
LABEL_DIR = "labels"  # Dossier où seront sauvegardées les annotations
FORMAT = "yolo"  # Choisir entre "yolo" et "pascal"

# Vérifier et installer LabelImg si nécessaire
try:
    import labelImg
except ImportError:
    print("Installation de LabelImg...")
    subprocess.run(["pip", "install", "labelImg"], check=True)

# Créer le dossier de labels s'il n'existe pas
if not os.path.exists(LABEL_DIR):
    os.makedirs(LABEL_DIR)

# Lancer LabelImg avec les bons paramètres
print(f"Ouverture de LabelImg pour annoter les images de {IMAGE_DIR}...")
subprocess.run(["labelImg", IMAGE_DIR, LABEL_DIR, FORMAT])
