import cv2
import numpy as np
import torch
import time
import math
from ultralytics import YOLO
from pymavlink import mavutil

# Connexions MAVLink
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
print("✅ Connexion MAVLink principale (master) établie")

phoenix = mavutil.mavlink_connection("udp:127.0.0.1:15550")
phoenix.wait_heartbeat()
print("✅ Connexion MAVLink secondaire (phoenix) établie")

# -------------------------------------------------------
def move_servo(servo_id, position, master):
    print(f"🔧 Déplacement du servo {servo_id} à la position {position}")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0, servo_id, position, 0, 0, 0, 0, 0
    )

def get_current_position():
    while True:
        msg = phoenix.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if msg:
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.relative_alt / 1000.0
            return lat, lon, alt

def calculate_offset_coordinates(lat, lon, bearing_deg, distance_m):
    lat_rad = math.radians(lat)
    bearing_rad = math.radians(bearing_deg)
    earth_radius = 6371000
    delta_lat = (distance_m / earth_radius) * math.cos(bearing_rad)
    delta_lon = (distance_m / (earth_radius * math.cos(lat_rad))) * math.sin(bearing_rad)
    new_lat = lat + math.degrees(delta_lat)
    new_lon = lon + math.degrees(delta_lon)
    return new_lat, new_lon

def clear_mission():
    phoenix.mav.mission_clear_all_send(phoenix.target_system, phoenix.target_component)
    print("🧹 Mission existante effacée.")

def wait_for_ack():
    msg = phoenix.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
    if msg:
        if msg.type == 0:
            print("✅ MISSION_ACK: mission acceptée.")
            return True
        else:
            print(f"⚠️ MISSION_ACK reçu mais erreur de type {msg.type}")
    else:
        print("❌ Aucun MISSION_ACK reçu.")
    return False

def print_mission_status():
    msg = phoenix.recv_match(type='MISSION_CURRENT', blocking=True, timeout=5)
    if msg:
        print(f"📍 MISSION_CURRENT: étape {msg.seq}")
    else:
        print("⛔ Aucun MISSION_CURRENT reçu.")

def print_heartbeat():
    msg = phoenix.recv_match(type='HEARTBEAT', blocking=True, timeout=3)
    if msg:
        armed = (msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
        mode = mavutil.mode_string_v10(msg)
        print(f"🔁 Mode: {mode}, Armé: {armed}")
    else:
        print("❌ Aucun HEARTBEAT reçu")

def monitor_statustext(duration_sec=5):
    print("🛰️ Lecture des STATUSTEXT (messages systèmes)...")
    start_time = time.time()
    while time.time() - start_time < duration_sec:
        msg = phoenix.recv_match(type='STATUSTEXT', blocking=False)
        if msg:
            print(f"[STATUSTEXT] {msg.text}")
        time.sleep(0.2)

def land_with_dolandstart(approach_bearing=23):
    lat_touch, lon_touch, _ = get_current_position()
    
    cruise_alt = 28
    ground_speed = 16
    final_leg_distance = 250
    descent_rate = 0.5
    descent_time = cruise_alt / descent_rate
    required_leg = ground_speed * descent_time

    print(f"📉 Descente sur {final_leg_distance}m, taux={descent_rate:.2f} m/s")

    wp_final_lat, wp_final_lon = calculate_offset_coordinates(lat_touch, lon_touch, (approach_bearing + 180) % 360, final_leg_distance)
    wp_entry_lat, wp_entry_lon = calculate_offset_coordinates(wp_final_lat, wp_final_lon, (approach_bearing + 180) % 360, 200)

    mission_items = [
        {"seq": 0, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "lat": wp_entry_lat, "lon": wp_entry_lon, "alt": cruise_alt},
        {"seq": 1, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "lat": wp_final_lat, "lon": wp_final_lon, "alt": cruise_alt},
        {"seq": 2, "cmd": mavutil.mavlink.MAV_CMD_DO_LAND_START, "lat": 0, "lon": 0, "alt": 0},
        {"seq": 3, "cmd": mavutil.mavlink.MAV_CMD_NAV_LAND, "lat": lat_touch, "lon": lon_touch, "alt": 0},
    ]

    clear_mission()
    time.sleep(1)
    phoenix.mav.mission_count_send(phoenix.target_system, phoenix.target_component, len(mission_items))

    for item in mission_items:
        while True:
            msg = phoenix.recv_match(type='MISSION_REQUEST', blocking=True, timeout=5)
            if msg and msg.seq == item["seq"]:
                phoenix.mav.mission_item_send(
                    phoenix.target_system,
                    phoenix.target_component,
                    item["seq"],
                    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                    item["cmd"],
                    0, 1, 0, 0, 0, 0,
                    item["lat"], item["lon"], item["alt"]
                )
                print(f"✅ Waypoint {item['seq']} envoyé.")
                break
        time.sleep(0.5)

    return wait_for_ack()

# -------------------------------------------------------
model_path = "runs/detect/train/weights/best.pt"
model = YOLO(model_path)
if torch.cuda.is_available():
    model.to("cuda")
    print("✅ Utilisation du GPU pour l'inférence.")
else:
    print("⚠️  Aucun périphérique CUDA trouvé ; utilisation du CPU.")

# -------------------------------------------------------
M1_LOWER_RED = np.array([130, 35, 200])
M1_UPPER_RED = np.array([180, 255, 255])
M2_LOWER_RED = np.array([130, 35, 200])
M2_UPPER_RED = np.array([180, 255, 255])

def filter(image):
    image = cv2.resize(image, (1280, 1280), interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, M1_LOWER_RED, M1_UPPER_RED)
    mask2 = cv2.inRange(hsv, M2_LOWER_RED, M2_UPPER_RED)
    mask = mask1 + mask2
    res = cv2.bitwise_and(image, image, mask=mask)
    return cv2.addWeighted(image, 0.5, res, 0.5, 0)

def predict(image, model):
    results = model.predict(source=image, conf=0.25, verbose=False)
    detections = results[0]
    annotated_frame = image.copy()
    detection_boxes = []

    for box in detections.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = detections.names[cls_id]
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name} {conf:.2f}"
        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        detection_boxes.append((x1, y1, x2, y2))

    return annotated_frame, len(detection_boxes), detection_boxes

# -------------------------------------------------------
def function_de_matheo():
    print("🔄 Démarrage de function_de_matheo")
    lat_touch, lon_touch, _ = get_current_position()
    mission_ready = land_with_dolandstart()

    if mission_ready:
        move_servo(11, 1150, master)
        time.sleep(0.7)
        phoenix.set_mode("AUTO")
        print("🚀 Mode AUTO activé (Phoenix)")
        phoenix.mav.command_long_send(
            phoenix.target_system,
            phoenix.target_component,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        print("📤 MISSION_START envoyé.")
        print("🌀 Changement du mode de master vers LOITER pour 2 minutes...")
        master.set_mode("LOITER")
        time.sleep(120)
        print("🏠 Passage du mode master à RTL (Return To Launch).")
        master.set_mode("RTL")
        monitor_statustext(duration_sec=10)
    else:
        print("❌ La mission n'a pas été acceptée. Servo non activé.")
        print("🏠 Passage du mode master à RTL (Return To Launch).")
        master.set_mode("RTL")
