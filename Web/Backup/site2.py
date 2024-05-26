from flask import Flask, render_template, Response, jsonify
import cv2
import folium

app = Flask(__name__)

# Générer la carte avec Folium
def generate_map():
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    folium.Marker([45.5236, -122.6750], popup='Location').add_to(m)
    return m._repr_html_()

# Capture vidéo avec OpenCV
def gen_frames():
    cap = cv2.VideoCapture(1)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', map=generate_map())

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Actions des boutons
@app.route('/action/<int:action_id>', methods=['POST'])
def action(action_id):
    if action_id == 1:
        print("Action 1 exécutée")
        return jsonify(result="Action 1 exécutée")
    elif action_id == 2:
        print("Action 2 exécutée")
        return jsonify(result="Action 2 exécutée")
    elif action_id == 3:
        print("Action 3 exécutée")
        return jsonify(result="Action 3 exécutée")
    elif action_id == 4:
        print("Action 4 exécutée")
        return jsonify(result="Action 4 exécutée")
    elif action_id == 5:
        print("Action 5 exécutée")
        return jsonify(result="Action 5 exécutée")
    elif action_id == 6:
        print("Action 6 exécutée")
        return jsonify(result="Action 6 exécutée")
    else:
        return jsonify(result="Action inconnue")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
