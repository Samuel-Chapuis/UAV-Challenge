# Utilisation des scripts

Les scripts de ce dossier sont à utiliser pour prétraiter des vidéos afin d'entraîner un modèle d'IA de reconnaissance d'image.

## Chemin à suivre 

1. **Échantillonnage de la vidéo**  
   Les modèles actuels ne prennent pas en compte les vidéos. Il est donc nécessaire d'extraire des images à partir de la vidéo source.  
   **Script :** `split_video_to_images.py`

2. **Prétraitement des images**  
   Pour améliorer la compréhension des images par le modèle, une phase de "préprocessing" est nécessaire.  
   - Les modèles d'IA utilisant des tenseurs réguliers, les images doivent être de format carré.  
   - L'application de certains filtres (couleur, bordures) peut améliorer la convergence du modèle.  
   **Script :** `pre_processing.py`

3. **Création de batches**  
   Afin d'éviter de traiter toutes les images en une seule fois, la création de batches permet de répartir le travail.  
   - Dans notre cas, nous créons des batches de 100 images, composés de 50 % d’images contenant un élément rouge détecté et 50 % sans.  
   - `batche_maker` : Génère des batches en triant les images.  
   - `naive_batche_maker` : Découpe les images en batches sans effectuer de tri.

4. **Labélisation**  
   La labélisation des images est nécessaire pour l'entraînement du modèle. Pour cela, nous utilisons le logiciel **LabelImg**.

5. **Organisation des fichiers**  
   LabelImg génère des fichiers texte associés aux images, mais tous sont placés dans un même répertoire. Or, l’objectif est d’arriver à une architecture organisée comme suit :

   ```
   /dataset
   ├── images
   │    ├── train
   │    │    ├── img_1.jpg
   │    │    ├── img_2.jpg
   │    │    ├── ...
   │    ├── val
   │         ├── img_51.jpg
   │         ├── img_52.jpg
   │         ├── ...
   ├── labels
   │    ├── train
   │    │    ├── img_1.txt
   │    │    ├── img_2.txt
   │    │    ├── ...
   │    ├── val
   │         ├── img_51.txt
   │         ├── img_52.txt
   │         ├── ...
   ├── data.yaml  (fichier de configuration)
   ```

   Pour réaliser cette séparation entre fichiers texte et images, utilisez le script suivant :  
   **Script :** `text_jpg_separator.py`
