import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas, filedialog, colorchooser

WEIGHT = 640
HEIGHT = 480

def hsv_to_rgb(h, s, v):
    """
    Convertit une couleur HSV en un tuple RGB (0..255 chacun).

    :param h: Teinte (généralement 0..179 pour OpenCV)
    :param s: Saturation (0..255)
    :param v: Valeur/Luminosité (0..255)
    :return: Un tuple (r, g, b) avec chaque composante dans [0..255]
    """
    # Cette fonction effectue la conversion en se basant sur la décomposition de HSV
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

def rgb_to_hsv(r, g, b):
    """
    Convertit une couleur RGB en HSV, au format attendu par OpenCV (H:0..179, S:0..255, V:0..255).

    :param r: Composante rouge (0..255)
    :param g: Composante verte (0..255)
    :param b: Composante bleue (0..255)
    :return: Un tuple (h, s, v) correspondant à la teinte, saturation et valeur
    """
    # On convertit d'abord le format RGB en BGR pour OpenCV
    bgr = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[0][0]
    return int(h), int(s), int(v)

def pick_color_for_filter(is_lower, filter_number):
    """
    Ouvre une boîte de dialogue pour choisir une couleur en RGB, la convertit en HSV,
    puis l'assigne aux champs (lower ou upper) du filtre correspondant.

    :param is_lower: Booléen indiquant si l'on met à jour les valeurs "basses" (lower) ou "hautes" (upper)
    :param filter_number: Numéro du filtre (1 ou 2) pour lequel on met à jour les valeurs
    """
    chosen_color = colorchooser.askcolor(title="Choose a color")
    if chosen_color[0] is None:
        return  # L'utilisateur a annulé ou fermé la fenêtre
    r, g, b = [int(x) for x in chosen_color[0]]

    h, s, v = rgb_to_hsv(r, g, b)

    # Mise à jour des champs de saisie selon le filtre et la plage (lower/upper)
    if filter_number == 1 and is_lower:
        hue_low1.delete(0, tk.END)
        hue_low1.insert(0, str(h))
        sat_low1.delete(0, tk.END)
        sat_low1.insert(0, str(s))
        val_low1.delete(0, tk.END)
        val_low1.insert(0, str(v))
    elif filter_number == 1 and not is_lower:
        hue_high1.delete(0, tk.END)
        hue_high1.insert(0, str(h))
        sat_high1.delete(0, tk.END)
        sat_high1.insert(0, str(s))
        val_high1.delete(0, tk.END)
        val_high1.insert(0, str(v))
    elif filter_number == 2 and is_lower:
        hue_low2.delete(0, tk.END)
        hue_low2.insert(0, str(h))
        sat_low2.delete(0, tk.END)
        sat_low2.insert(0, str(s))
        val_low2.delete(0, tk.END)
        val_low2.insert(0, str(v))
    elif filter_number == 2 and not is_lower:
        hue_high2.delete(0, tk.END)
        hue_high2.insert(0, str(h))
        sat_high2.delete(0, tk.END)
        sat_high2.insert(0, str(s))
        val_high2.delete(0, tk.END)
        val_high2.insert(0, str(v))

    update_image()

def update_image():
    """
    Lit les valeurs HSV dans les champs de saisie, applique les filtres à l'image courante
    et affiche le résultat dans des fenêtres OpenCV redimensionnables.
    Met également à jour les rectangles de prévisualisation de couleur dans l'interface.
    """
    if not image_files:
        return
    global frame

    try:
        # Récupération des bornes HSV pour le Filtre 1
        lower_h1 = int(hue_low1.get())
        lower_s1 = int(sat_low1.get())
        lower_v1 = int(val_low1.get())
        upper_h1 = int(hue_high1.get())
        upper_s1 = int(sat_high1.get())
        upper_v1 = int(val_high1.get())

        # Récupération des bornes HSV pour le Filtre 2
        lower_h2 = int(hue_low2.get())
        lower_s2 = int(sat_low2.get())
        lower_v2 = int(val_low2.get())
        upper_h2 = int(hue_high2.get())
        upper_s2 = int(sat_high2.get())
        upper_v2 = int(val_high2.get())

        # Conversion de l'image courante en HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Création des seuils pour chaque filtre
        lower_color1 = np.array([lower_h1, lower_s1, lower_v1])
        upper_color1 = np.array([upper_h1, upper_s1, upper_v1])
        lower_color2 = np.array([lower_h2, lower_s2, lower_v2])
        upper_color2 = np.array([upper_h2, upper_s2, upper_v2])

        # Création des masques et des images filtrées
        mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
        res1 = cv2.bitwise_and(frame, frame, mask=mask1)
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)

        # Affichage de l'image originale et des images filtrées dans des fenêtres redimensionnables
        cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Original', WEIGHT, HEIGHT)
        cv2.imshow('Original', frame)

        cv2.namedWindow('Filtered 1', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtered 1', WEIGHT, HEIGHT)
        cv2.imshow('Filtered 1', res1)

        cv2.namedWindow('Filtered 2', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtered 2', WEIGHT, HEIGHT)
        cv2.imshow('Filtered 2', res2)

        # Mise à jour des carrés de prévisualisation (couleurs "lower" et "upper")
        lower_rgb1 = hsv_to_rgb(lower_h1, lower_s1, lower_v1)
        upper_rgb1 = hsv_to_rgb(upper_h1, upper_s1, upper_v1)
        lower_rgb2 = hsv_to_rgb(lower_h2, lower_s2, lower_v2)
        upper_rgb2 = hsv_to_rgb(upper_h2, upper_s2, upper_v2)

        canvas1_lower.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % lower_rgb1, outline="")
        canvas1_upper.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % upper_rgb1, outline="")
        canvas2_lower.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % lower_rgb2, outline="")
        canvas2_upper.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % upper_rgb2, outline="")
    except ValueError:
        # On ignore les cas où les valeurs ne sont pas des entiers valides
        pass

def load_image(index):
    """
    Charge l'image à l'index spécifié dans la variable globale 'frame'
    puis met à jour l'affichage.

    :param index: Index de l'image à charger
    """
    global frame, current_index
    if not image_files:
        return
    current_index = index % len(image_files)
    filepath = os.path.join(image_folder, image_files[current_index])
    frame = cv2.imread(filepath)
    update_image()

def prev_image():
    """
    Passe à l'image précédente dans la liste.
    """
    load_image(current_index - 1)

def next_image():
    """
    Passe à l'image suivante dans la liste.
    """
    load_image(current_index + 1)

# ---------- Début du script principal ----------

root = tk.Tk()
root.title("HSV Color Filter")

# Invite l'utilisateur à sélectionner un dossier contenant des images
image_folder = filedialog.askdirectory(title="Select a folder containing images")
if not image_folder:
    print("Aucun dossier sélectionné. Fermeture du programme.")
    root.destroy()
    exit()

# Récupère la liste des fichiers image (personnaliser l'extension si nécessaire)
image_files = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
]
image_files.sort()

if not image_files:
    print("Aucune image trouvée dans le dossier sélectionné.")
    root.destroy()
    exit()

current_index = 0
frame = None

# --- Filtre 1 ---
tk.Label(root, text="Filter 1").grid(row=0, column=0, columnspan=3)

tk.Label(root, text="Hue Low").grid(row=1, column=0)
hue_low1 = tk.Entry(root)
hue_low1.insert(0, "0")
hue_low1.grid(row=1, column=1)
canvas1_lower = Canvas(root, width=50, height=50)
canvas1_lower.grid(row=1, column=2)
btn_pick_color1_lower = tk.Button(
    root, text="Pick Color (Lower)",
    command=lambda: pick_color_for_filter(True, 1))
btn_pick_color1_lower.grid(row=1, column=3)

tk.Label(root, text="Sat Low").grid(row=2, column=0)
sat_low1 = tk.Entry(root)
sat_low1.insert(0, "120")
sat_low1.grid(row=2, column=1)

tk.Label(root, text="Val Low").grid(row=3, column=0)
val_low1 = tk.Entry(root)
val_low1.insert(0, "70")
val_low1.grid(row=3, column=1)

tk.Label(root, text="Hue High").grid(row=4, column=0)
hue_high1 = tk.Entry(root)
hue_high1.insert(0, "10")
hue_high1.grid(row=4, column=1)
canvas1_upper = Canvas(root, width=50, height=50)
canvas1_upper.grid(row=4, column=2)
btn_pick_color1_upper = tk.Button(
    root, text="Pick Color (Upper)",
    command=lambda: pick_color_for_filter(False, 1))
btn_pick_color1_upper.grid(row=4, column=3)

tk.Label(root, text="Sat High").grid(row=5, column=0)
sat_high1 = tk.Entry(root)
sat_high1.insert(0, "255")
sat_high1.grid(row=5, column=1)

tk.Label(root, text="Val High").grid(row=6, column=0)
val_high1 = tk.Entry(root)
val_high1.insert(0, "255")
val_high1.grid(row=6, column=1)

# --- Filtre 2 ---
tk.Label(root, text="Filter 2").grid(row=7, column=0, columnspan=3)

tk.Label(root, text="Hue Low").grid(row=8, column=0)
hue_low2 = tk.Entry(root)
hue_low2.insert(0, "170")
hue_low2.grid(row=8, column=1)
canvas2_lower = Canvas(root, width=50, height=50)
canvas2_lower.grid(row=8, column=2)
btn_pick_color2_lower = tk.Button(
    root, text="Pick Color (Lower)",
    command=lambda: pick_color_for_filter(True, 2))
btn_pick_color2_lower.grid(row=8, column=3)

tk.Label(root, text="Sat Low").grid(row=9, column=0)
sat_low2 = tk.Entry(root)
sat_low2.insert(0, "120")
sat_low2.grid(row=9, column=1)

tk.Label(root, text="Val Low").grid(row=10, column=0)
val_low2 = tk.Entry(root)
val_low2.insert(0, "70")
val_low2.grid(row=10, column=1)

tk.Label(root, text="Hue High").grid(row=11, column=0)
hue_high2 = tk.Entry(root)
hue_high2.insert(0, "180")
hue_high2.grid(row=11, column=1)
canvas2_upper = Canvas(root, width=50, height=50)
canvas2_upper.grid(row=11, column=2)
btn_pick_color2_upper = tk.Button(
    root, text="Pick Color (Upper)",
    command=lambda: pick_color_for_filter(False, 2))
btn_pick_color2_upper.grid(row=11, column=3)

tk.Label(root, text="Sat High").grid(row=12, column=0)
sat_high2 = tk.Entry(root)
sat_high2.insert(0, "255")
sat_high2.grid(row=12, column=1)

tk.Label(root, text="Val High").grid(row=13, column=0)
val_high2 = tk.Entry(root)
val_high2.insert(0, "255")
val_high2.grid(row=13, column=1)

# Boutons de navigation
btn_prev = tk.Button(root, text="<< Previous", command=prev_image)
btn_prev.grid(row=14, column=0)
btn_next = tk.Button(root, text="Next >>", command=next_image)
btn_next.grid(row=14, column=1)

# Bouton de mise à jour (appliquer le filtre à nouveau)
btn_update = tk.Button(root, text="Apply Filter", command=update_image)
btn_update.grid(row=14, column=2)

# Charge la première image
load_image(0)

# Démarre la boucle principale de Tkinter
root.mainloop()

# Ferme les fenêtres OpenCV une fois terminé
cv2.destroyAllWindows()
