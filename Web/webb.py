""""

webb.py - Cette partie du code gère l'application webb

"""

# -------------------------------- #
# Import 
from flask import Flask, render_template, jsonify, Response
import cv2

# Imports locaux
from video import loop_video
import globalVar
# -------------------------------- #

app = Flask(__name__)

##### Routes ###################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # On encode l’image stockée dans la variable globale
    return Response(
        cv2.imencode('.png', globalVar.video_image)[1].tobytes(),
        mimetype='image/png'
    )

@app.route('/gps')
def gps():
    # Obtention des coordonnées simulées pour les 2 drones
    lat1, lon1 = globalVar.mother_drone.listen_gps()
    lat2, lon2 = globalVar.second_drone.listen_gps()
    return jsonify(
        drone1={'latitude': lat1, 'longitude': lon1},
        drone2={'latitude': lat2, 'longitude': lon2}
    )

# Fonctions associées aux boutons du panneau gauche
@app.route('/start')
def start():
    print("Fonction Start déclenchée")
    return jsonify(success=True, action="start")

@app.route('/stop')
def stop():
    print("Fonction Stop déclenchée")
    return jsonify(success=True, action="stop")

@app.route('/left_change_view')
def left_change_view():
    print("Changement de vue (panneau gauche) déclenché")
    return jsonify(success=True, action="left_change_view")

@app.route('/screenshot')
def screenshot():
    print("Capture d'écran déclenchée")
    return jsonify(success=True, action="screenshot")

@app.route('/reload')
def reload_():
    print("Recharge déclenchée")
    return jsonify(success=True, action="reload")

# Fonctions associées aux boutons du panneau droit
@app.route('/add_waypoint')
def add_waypoint():
    print("Ajout de waypoint déclenché")
    return jsonify(success=True, action="add_waypoint")

@app.route('/export_pos')
def export_pos():
    print("Export des positions déclenché")
    return jsonify(success=True, action="export_pos")

@app.route('/right_change_view')
def right_change_view():
    print("Changement de vue (panneau droit) déclenché")
    return jsonify(success=True, action="right_change_view")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)