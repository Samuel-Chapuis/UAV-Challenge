import os

input_folder = "EmbededVideo/CustomAiModel/PreProcess/batches/batch_3"

def separator(input_folder):
    """
    Sépare les images et les fichiers textes dans des dossiers différents.

    Les images (extensions : .jpg, .jpeg, .png, .gif, .bmp, .tiff) sont déplacées dans un sous-dossier "images".
    Les fichiers textes (extensions : .txt, .doc, .docx, .pdf) sont déplacés dans un sous-dossier "texts".
    
    :param input_folder: Chemin du dossier contenant les fichiers à séparer
    """
    # Définir les dossiers de destination
    images_folder = os.path.join(input_folder, "images")
    texts_folder = os.path.join(input_folder, "texts")
    
    # Créer les dossiers s'ils n'existent pas
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(texts_folder, exist_ok=True)
    
    # Listes des extensions à traiter
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    text_extensions = {".txt", ".doc", ".docx", ".pdf"}
    
    # Parcourir tous les fichiers du dossier
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        
        # Vérifier que c'est bien un fichier (et éviter de traiter les dossiers nouvellement créés)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_name)[1].lower()
            if ext in image_extensions:
                dest_path = os.path.join(images_folder, file_name)
                os.rename(file_path, dest_path)
            elif ext in text_extensions:
                dest_path = os.path.join(texts_folder, file_name)
                os.rename(file_path, dest_path)

# Exemple d'appel à la fonction
separator(input_folder)
