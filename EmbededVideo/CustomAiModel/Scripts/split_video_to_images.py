import cv2
import os
from charging_bar import ChargingBar

def extract_frames(video_folder, output_folder, interval=5):
    """
    Extrait des images des vidéos à intervalles réguliers.
    
    :param video_folder: Chemin du dossier contenant les vidéos
    :param output_folder: Chemin du dossier où enregistrer les images extraites
    :param interval: Intervalle de temps entre chaque image extraite (en secondes)
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_frames = 0
    
    # Calcul du nombre total d'images à extraire
    for video_name in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_name)
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_frames += frame_count // (fps * interval)
        cap.release()

    # Initialisation de la barre de progression
    bar = ChargingBar(total_frames)
    bar.show()

    video_number = 0
    for video_name in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_name)
        extract_frames_from_video(video_path, output_folder, interval, video_number, bar)
        video_number += 1

def extract_frames_from_video(video_path, output_folder, interval, number_name, bar):
    """
    Extrait les images d'une vidéo donnée à intervalles définis et les enregistre.
    
    :param video_path: Chemin de la vidéo source
    :param output_folder: Chemin du dossier où enregistrer les images
    :param interval: Intervalle de temps entre chaque image extraite (en secondes)
    :param number_name: Numéro de la vidéo pour nommer les images extraites
    :param bar: Barre de progression pour visualiser l'avancement
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{number_name}_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            bar.update()  # Mise à jour de la barre pour chaque image sauvegardée

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_folder = "EmbededVideo/CustomAiModel/RawData/video"
    interval = 1  # Intervalle en secondes
    output_folder = f"EmbededVideo/CustomAiModel/RawData/images{interval}s"
    extract_frames(video_folder, output_folder, interval)
