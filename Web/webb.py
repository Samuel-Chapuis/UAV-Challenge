""""

webb.py - Cette partie du code gère l'application webb

"""

# -------------------------------- #
# Import 
from flask import Flask, render_template, jsonify, Response

# Imports locaux
from video import loop_video
# -------------------------------- #

app = Flask(__name__)

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
