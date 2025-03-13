import os
import random

input_folder = "EmbededVideo/CustomAiModel/PreProcess/filtered_images"
output_folder = "EmbededVideo/CustomAiModel/PreProcess/batches"

def batch_creator(input_folder, output_folder, batch_size):
    """
    Crée des lots (batches) contenant chacun 50% de fichiers du sous-dossier 'red'
    et 50% du sous-dossier 'non_red', piochés aléatoirement et sans répétitions.
    Les fichiers sont déplacés (rename) dans les dossiers de batch correspondants.

    :param input_folder: Chemin du dossier qui contient 'red' et 'non_red'
    :param output_folder: Chemin du dossier où créer les batches
    :param batch_size: Taille totale de chaque batch (doit être un nombre pair de préférence)
    """

    # Chemins des sous-dossiers
    red_path = os.path.join(input_folder, "red")
    non_red_path = os.path.join(input_folder, "non_red")

    # Récupération et mélange aléatoire des fichiers
    red_files = os.listdir(red_path)
    non_red_files = os.listdir(non_red_path)
    random.shuffle(red_files)
    random.shuffle(non_red_files)

    # On s'assure que le dossier de sortie existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # On définit combien d'éléments "red" et "non_red" par batch
    half_batch = batch_size // 2  # Par ex si batch_size=100 => 50 "red" et 50 "non_red"

    # Calcul du nombre maximal de batches possibles
    max_batches = min(len(red_files) // half_batch, len(non_red_files) // half_batch)

    # Création des batches
    for i in range(max_batches):
        # Création d'un dossier pour le batch
        batch_folder = os.path.join(output_folder, f"batch_{i}")
        os.makedirs(batch_folder, exist_ok=True)

        # Sélection des fichiers pour ce batch
        red_batch = red_files[i * half_batch : (i + 1) * half_batch]
        non_red_batch = non_red_files[i * half_batch : (i + 1) * half_batch]

        # Déplacement des fichiers "red"
        for f in red_batch:
            src = os.path.join(red_path, f)
            dst = os.path.join(batch_folder, f)
            os.rename(src, dst)

        # Déplacement des fichiers "non_red"
        for f in non_red_batch:
            src = os.path.join(non_red_path, f)
            dst = os.path.join(batch_folder, f)
            os.rename(src, dst)

    print(f"{max_batches} batches créés dans le dossier '{output_folder}'.")


if __name__ == '__main__':
    batch_size = 100  # Exemple : 100 => 50 "red" + 50 "non_red"
    
    batch_creator(input_folder, output_folder, batch_size)
    print("Terminé.")
