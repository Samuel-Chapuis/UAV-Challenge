from flask import Flask, render_template, jsonify, Response
import cv2
import threading
import numpy as np
import time

################################

app = Flask(__name__)

###### Variables globales ######

cap = cv2.VideoCapture(0)

##### Programme principal #####

class Video(threading.Thread):
    def __init__(self, cam_index=0):
        super().__init__()
        self.cap = cv2.VideoCapture(cam_index)
        self.running = self.cap.isOpened()  # vérifie si la caméra est ouverte
        self.frame = None
        self.detected = False
        self.min_area = 500  # aire minimale pour la détection de contours

    def stop(self):
        self.running = False
        self.cap.release()  # libère la caméra

    def update_frame(self):
        success, frame = self.cap.read()
        if success:
            self.frame = frame

    def get_jpg(self):
        if self.frame is not None:
            success, buffer = cv2.imencode('.jpg', self.frame)
            if success:
                return buffer.tobytes()
        return None
    
    def detect(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        lower_red = np.array([0, 100, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([170, 110, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = mask1 + mask2
        res = cv2.bitwise_and(self.frame, self.frame, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [contour for contour in contours if cv2.contourArea(contour) >= self.min_area]
        
        if valid_contours:
            if not self.detected:
                self.detection_start_time = time.time()  # start timer
                self.detected = True
            else:
                if time.time() - self.detection_start_time >= 0.5:
                    for contour in valid_contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    print("Tache rouge détectée pendant 1 seconde")
        else:
            self.detected = False

def loop_video():
    video_thread = Video()
    video_thread.start()
    
    while video_thread.running:
        video_thread.update_frame()
        video_thread.detect()
        frame = video_thread.get_jpg()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video_thread.stop()

##### Routes ###################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(loop_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Fonctions associées aux boutons du panneau gauche
@app.route('/start')
def start():
    print("Fonction Start déclenchée")
    # Insérez ici votre code pour démarrer le drone
    return jsonify(success=True, action="start")

@app.route('/stop')
def stop():
    print("Fonction Stop déclenchée")
    # Insérez ici votre code pour arrêter le drone
    return jsonify(success=True, action="stop")

@app.route('/left_change_view')
def left_change_view():
    print("Changement de vue (panneau gauche) déclenché")
    # Insérez ici votre code pour changer la vue du panneau gauche
    return jsonify(success=True, action="left_change_view")

@app.route('/screenshot')
def screenshot():
    print("Capture d'écran déclenchée")
    # Insérez ici votre code pour réaliser une capture d'écran
    return jsonify(success=True, action="screenshot")

@app.route('/reload')
def reload_():
    print("Recharge déclenchée")
    # Insérez ici votre code pour recharger l'affichage ou réinitialiser
    return jsonify(success=True, action="reload")

# Fonctions associées aux boutons du panneau droit
@app.route('/add_waypoint')
def add_waypoint():
    print("Ajout de waypoint déclenché")
    # Insérez ici votre code pour ajouter un waypoint
    return jsonify(success=True, action="add_waypoint")

@app.route('/export_pos')
def export_pos():
    print("Export des positions déclenché")
    # Insérez ici votre code pour exporter les positions
    return jsonify(success=True, action="export_pos")

@app.route('/right_change_view')
def right_change_view():
    print("Changement de vue (panneau droit) déclenché")
    # Insérez ici votre code pour changer la vue du panneau droit
    return jsonify(success=True, action="right_change_view")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
