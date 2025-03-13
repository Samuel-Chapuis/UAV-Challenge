import os
from charging_bar import ChargingBar

def batch_creator(input_folder, output_folder, size):
    """
    Crée des lots (batches) de fichiers en les regroupant par taille définie.
    Les fichiers sont déplacés dans des dossiers de batch correspondants.

    :param input_folder: Chemin du dossier contenant les fichiers à batcher
    :param output_folder: Chemin du dossier où stocker les batches
    :param size: Nombre de fichiers par batch
    """

    # Vérifie et crée le dossier de sortie si nécessaire
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Liste des fichiers à traiter
    files = os.listdir(input_folder)
    batch_number = 0  # Compteur de batchs
    
    # Barre de progression pour visualiser l'avancement
    bar = ChargingBar(len(files))
    bar.show()

    # Création des batches
    for i in range(0, len(files), size):
        batch = files[i:i + size]
        batch_folder = os.path.join(output_folder, f'batch_{batch_number}')
        os.makedirs(batch_folder, exist_ok=True)

        # Déplacement des fichiers dans le batch correspondant
        for file in batch:
            src = os.path.join(input_folder, file)
            dst = os.path.join(batch_folder, file)
            os.rename(src, dst)
            bar.update()
        
        batch_number += 1

if __name__ == '__main__':
    input_folder = "EmbededVideo/CustomAiModel/PreProcess/square_high_red"
    output_folder = "EmbededVideo/CustomAiModel/PreProcess/batches"
    batch_creator(input_folder, output_folder, 100)
