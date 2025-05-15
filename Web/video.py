""""

video.py - Module for video capture and processing

"""

# -------------------------------- #
# Import 
import cv2
import threading
import numpy as np
import time
import torch
from ultralytics import YOLO
from collections import deque
# -------------------------------- #


# -------------------------------------------------------
from model import model
# -------------------------------------------------------

cap = cv2.VideoCapture(0)


##### Video Capture and Processing #####

class Video(threading.Thread):
    def __init__(self, mod, cam_index=0):
        super().__init__()
        self.cap = cv2.VideoCapture(cam_index)
        self.running = self.cap.isOpened()
        
        self.frame = None
        self.f_frame = None
        self.d_frame = None
        
        self.detected = False
        self.beacons = 0
        self.mod = mod
        
        # 🔧 Historique des détections sur 6 frames
        self.detection_history = deque(maxlen=6)
        self.detection_triggered = False

        self.M1_LOWER_RED = np.array([130, 35, 200])
        self.M1_UPPER_RED = np.array([180, 255, 255])
        self.M2_LOWER_RED = np.array([130, 35, 200])
        self.M2_UPPER_RED = np.array([180, 255, 255])
        
        self.min_area = 500
        
        
    def stop(self):
        self.running = False
        self.cap.release()  # libère la caméra


    def update(self):
        success, frame = self.cap.read()
        if success:
            self.frame = frame


    def get_frame(self):
        if self.frame is not None:
            success, buffer = cv2.imencode('.jpg', self.frame)
            if success:
                return buffer.tobytes()
        return None
    
    
    def get_f_frame(self):
        if self.f_frame is not None:
            success, buffer = cv2.imencode('.jpg', self.f_frame)
            if success:
                return buffer.tobytes()
        return None
    
    
    def get_d_frame(self):
        if self.d_frame is not None:
            success, buffer = cv2.imencode('.jpg', self.d_frame)
            if success:
                return buffer.tobytes()
        return None
    
    
    def filter(self):
            self.frame = cv2.resize(self.frame, (1280, 1280), interpolation=cv2.INTER_CUBIC)
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, self.M1_LOWER_RED, self.M1_UPPER_RED)
            mask2 = cv2.inRange(hsv, self.M2_LOWER_RED, self.M2_UPPER_RED)
            mask = mask1 + mask2
            res = cv2.bitwise_and(self.frame, self.frame, mask=mask)
            self.f_frame = cv2.addWeighted(self.frame, 0.5, res, 0.5, 0)
    
    def predict(self):
        results = self.mod.predict(source=self.f_frame, conf=0.25, verbose=False)
        detections = results[0]
        annotated_frame = self.f_frame.copy()
        
        for box in detections.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            class_name = detections.names[cls_id]
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} {conf:.2f}"
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        self.beacons = len(detections.boxes)
        self.d_frame = annotated_frame.copy()

        # Mise à jour de l'historique
        self.detection_history.append(self.beacons > 0)

        # Déclenchement uniquement si 4+ détections sur les 6 dernières frames
        if not self.detection_triggered and self.detection_history.count(True) >= 4:
            self.detection_triggered = True
            threading.Thread(target=self.on_object_detected, daemon=True).start()


    def on_object_detected(self):
        print("🚨 Objet détecté ! Traitement dans un thread séparé...")
        time.sleep(10)  # À remplacer par l'action réelle à effectuer
        print("✅ Traitement terminé.")
        self.detection_triggered = False

##### Fonction génératrice pour le streaming vidéo #####

def loop_video():
    video_thread = Video(model)
    video_thread.start()
    
    while video_thread.running:
        video_thread.update()
        video_thread.filter()
        video_thread.predict()
        frame = video_thread.get_d_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video_thread.stop()