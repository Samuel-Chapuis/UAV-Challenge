import cv2
import os

class ChargingBar:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.bar_length = 50

    def show(self):
        progress = self.current / self.total
        bar = "=" * int(progress * self.bar_length)
        space = " " * (self.bar_length - len(bar))
        print(f"\r[{bar}{space}] {progress * 100:.2f}%", end="")

    def update(self, step=1):
        self.current += step
        self.show()

def extract_frames(video_folder, output_folder, interval=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_frames = 0
    for video_name in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_name)
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_frames += frame_count // (fps * interval)  # Nombre d'images prévues
        cap.release()

    bar = ChargingBar(total_frames)
    bar.show()

    video_number = 0
    for video_name in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_name)
        extract_frames_from_video(video_path, output_folder, interval, video_number, bar)
        video_number += 1

def extract_frames_from_video(video_path, output_folder, interval, number_name, bar):
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
            bar.update()  # Mise à jour de la barre seulement pour les images sauvegardées

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_folder = "EmbededVideo/CustomAiModel/RawData/video"
    interval = 1 # in seconds
    output_folder = "EmbededVideo/CustomAiModel/RawData/images" + str(interval) + "s"
    
    extract_frames(video_folder, output_folder, interval)