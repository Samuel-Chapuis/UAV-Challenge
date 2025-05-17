""""

webb.py - Cette partie du code gère l'application webb

"""

# -------------------------------- #
# Import 
from flask import Flask, render_template, jsonify, Response

# Imports locaux
from video.video import loop_video
from globalVar import master_Drone, sub_Drone
# -------------------------------- #

app = Flask(__name__)

##### Routes ###################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(loop_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gps')
def gps():
    # Obtention des coordonnées simulées pour les 2 drones
    lat1, lon1 = master_Drone.get_current_position()
    lat2, lon2 = sub_Drone.get_current_position()
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

@app.route('/displays')
def displays():
    """
    Retourne un JSON : {disp1: ..., disp2: ..., disp3: ...}
    Chaque champ est calculé par sa fonction dédiée.
    En cas d'erreur on renvoie 'N/A' au lieu d'un 500.
    """
    try:
        disp1 = get_disp1()
    except Exception as e:
        print("[/displays] erreur disp1 :", e)
        disp1 = "Master : N/A"

    try:
        disp2 = get_disp2()
    except Exception as e:
        print("[/displays] erreur disp2 :", e)
        disp2 = "Phoenix : N/A"

    return jsonify(disp1=disp1,
                   disp2=disp2,
                   disp3="-")      # provisoire
    
def get_disp1():
    """
    Tension batterie du drone maître, formatée « 12.3 V ».
    La méthode peut :
      - renvoyer un float
      - ou un tuple (voltage, percent, …)
    On normalise dans tous les cas.
    """
    v = master_Drone.get_battery_voltage()   # ← votre API
    if isinstance(v, (list, tuple)):
        v = v[0]
    return f"Master : {float(v):.1f} V"

def get_disp2():
    """
    Tension batterie du drone esclave.
    Même logique que ci-dessus.
    """
    v = sub_Drone.get_battery_voltage()
    if isinstance(v, (list, tuple)):
        v = v[0]
    return f"Phoenix : {float(v):.1f} V"



if __name__ == '__main__':
    app.run(debug=True, threaded=True)