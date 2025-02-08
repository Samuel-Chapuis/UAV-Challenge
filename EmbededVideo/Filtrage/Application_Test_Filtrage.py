import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas

def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s) / 255.0
    v = float(v) / 255.0
    hi = int(h / 60.0) % 6
    f = (h / 60.0) - hi
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)

def update_image():
    try:
        # Obtenez les valeurs des entrées
        lower_h1 = int(hue_low1.get())
        lower_s1 = int(sat_low1.get())
        lower_v1 = int(val_low1.get())
        upper_h1 = int(hue_high1.get())
        upper_s1 = int(sat_high1.get())
        upper_v1 = int(val_high1.get())
        
        lower_h2 = int(hue_low2.get())
        lower_s2 = int(sat_low2.get())
        lower_v2 = int(val_low2.get())
        upper_h2 = int(hue_high2.get())
        upper_s2 = int(sat_high2.get())
        upper_v2 = int(val_high2.get())

        # Conversion de l'image en espace de couleurs HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Définition des seuils de couleur pour le premier filtre
        lower_color1 = np.array([lower_h1, lower_s1, lower_v1])
        upper_color1 = np.array([upper_h1, upper_s1, upper_v1])
        
        # Définition des seuils de couleur pour le deuxième filtre
        lower_color2 = np.array([lower_h2, lower_s2, lower_v2])
        upper_color2 = np.array([upper_h2, upper_s2, upper_v2])
        
        # Création des masques
        mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
        
        # Application des masques
        res1 = cv2.bitwise_and(frame, frame, mask=mask1)
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)
        
        # Affichage des images
        cv2.imshow('Original', frame)
        cv2.imshow('Filtered 1', res1)
        cv2.imshow('Filtered 2', res2)
        
        # Mise à jour des couleurs affichées
        lower_rgb1 = hsv_to_rgb(lower_h1, lower_s1, lower_v1)
        upper_rgb1 = hsv_to_rgb(upper_h1, upper_s1, upper_v1)
        lower_rgb2 = hsv_to_rgb(lower_h2, lower_s2, lower_v2)
        upper_rgb2 = hsv_to_rgb(upper_h2, upper_s2, upper_v2)
        
        canvas1_lower.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % lower_rgb1, outline="")
        canvas1_upper.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % upper_rgb1, outline="")
        canvas2_lower.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % lower_rgb2, outline="")
        canvas2_upper.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % upper_rgb2, outline="")
    except ValueError:
        pass  # Ignore invalid inputs

def capture_frame():
    global frame
    ret, frame = cap.read()
    if ret:
        update_image()
    root.after(10, capture_frame)

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam")
    exit()

# Initialisation de l'interface Tkinter
root = tk.Tk()
root.title("HSV Color Filter")

# Créer des zones de texte pour le premier filtre
tk.Label(root, text="Filter 1").grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Hue Low").grid(row=1, column=0)
hue_low1 = tk.Entry(root)
hue_low1.insert(0, "0")
hue_low1.grid(row=1, column=1)
canvas1_lower = Canvas(root, width=50, height=50)
canvas1_lower.grid(row=1, column=2)

tk.Label(root, text="Saturation Low").grid(row=2, column=0)
sat_low1 = tk.Entry(root)
sat_low1.insert(0, "120")
sat_low1.grid(row=2, column=1)

tk.Label(root, text="Value Low").grid(row=3, column=0)
val_low1 = tk.Entry(root)
val_low1.insert(0, "70")
val_low1.grid(row=3, column=1)

tk.Label(root, text="Hue High").grid(row=4, column=0)
hue_high1 = tk.Entry(root)
hue_high1.insert(0, "10")
hue_high1.grid(row=4, column=1)
canvas1_upper = Canvas(root, width=50, height=50)
canvas1_upper.grid(row=4, column=2)

tk.Label(root, text="Saturation High").grid(row=5, column=0)
sat_high1 = tk.Entry(root)
sat_high1.insert(0, "255")
sat_high1.grid(row=5, column=1)

tk.Label(root, text="Value High").grid(row=6, column=0)
val_high1 = tk.Entry(root)
val_high1.insert(0, "255")
val_high1.grid(row=6, column=1)

# Créer des zones de texte pour le deuxième filtre
tk.Label(root, text="Filter 2").grid(row=7, column=0, columnspan=2)

tk.Label(root, text="Hue Low").grid(row=8, column=0)
hue_low2 = tk.Entry(root)
hue_low2.insert(0, "170")
hue_low2.grid(row=8, column=1)
canvas2_lower = Canvas(root, width=50, height=50)
canvas2_lower.grid(row=8, column=2)

tk.Label(root, text="Saturation Low").grid(row=9, column=0)
sat_low2 = tk.Entry(root)
sat_low2.insert(0, "120")
sat_low2.grid(row=9, column=1)

tk.Label(root, text="Value Low").grid(row=10, column=0)
val_low2 = tk.Entry(root)
val_low2.insert(0, "70")
val_low2.grid(row=10, column=1)

tk.Label(root, text="Hue High").grid(row=11, column=0)
hue_high2 = tk.Entry(root)
hue_high2.insert(0, "180")
hue_high2.grid(row=11, column=1)
canvas2_upper = Canvas(root, width=50, height=50)
canvas2_upper.grid(row=11, column=2)

tk.Label(root, text="Saturation High").grid(row=12, column=0)
sat_high2 = tk.Entry(root)
sat_high2.insert(0, "255")
sat_high2.grid(row=12, column=1)

tk.Label(root, text="Value High").grid(row=13, column=0)
val_high2 = tk.Entry(root)
val_high2.insert(0, "255")
val_high2.grid(row=13, column=1)

# Capture des images en continu
root.after(10, capture_frame)
root.mainloop()

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
