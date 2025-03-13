import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas, filedialog, colorchooser

WEIGHT = 640
HEIGHT = 480

def hsv_to_rgb(h, s, v):
    """
    Convert HSV to an RGB tuple (0..255 each).
    """
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
    Convert RGB (0..255 each) to HSV (H:0..179, S:0..255, V:0..255) for OpenCV.
    """
    bgr = np.uint8([[[b, g, r]]])  # Convert RGB -> BGR for OpenCV
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[0][0]
    return int(h), int(s), int(v)

def pick_color_for_filter(is_lower, filter_number):
    """
    Opens a color chooser, converts selected RGB to HSV,
    and sets the corresponding entries (lower or upper) for the specified filter.
    """
    chosen_color = colorchooser.askcolor(title="Choose a color")
    if chosen_color[0] is None:
        return  # User canceled or closed the dialog
    r, g, b = [int(x) for x in chosen_color[0]]  # chosen_color[0] = (r, g, b)

    h, s, v = rgb_to_hsv(r, g, b)

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
    Reads the current HSV bounds from the entry boxes,
    applies them to the currently shown image, and displays the results.
    Also updates the color-preview rectangles in the GUI.
    """
    if not image_files:
        return
    global frame

    try:
        # Grab HSV bounds for Filter 1
        lower_h1 = int(hue_low1.get())
        lower_s1 = int(sat_low1.get())
        lower_v1 = int(val_low1.get())
        upper_h1 = int(hue_high1.get())
        upper_s1 = int(sat_high1.get())
        upper_v1 = int(val_high1.get())

        # Grab HSV bounds for Filter 2
        lower_h2 = int(hue_low2.get())
        lower_s2 = int(sat_low2.get())
        lower_v2 = int(val_low2.get())
        upper_h2 = int(hue_high2.get())
        upper_s2 = int(sat_high2.get())
        upper_v2 = int(val_high2.get())

        # Convert the current frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create thresholds
        lower_color1 = np.array([lower_h1, lower_s1, lower_v1])
        upper_color1 = np.array([upper_h1, upper_s1, upper_v1])
        lower_color2 = np.array([lower_h2, lower_s2, lower_v2])
        upper_color2 = np.array([upper_h2, upper_s2, upper_v2])

        # Create masks & filtered images
        mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
        res1 = cv2.bitwise_and(frame, frame, mask=mask1)
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)

        # Display the images in resizable windows
        cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Original', WEIGHT, HEIGHT)
        cv2.imshow('Original', frame)

        cv2.namedWindow('Filtered 1', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtered 1', WEIGHT, HEIGHT)
        cv2.imshow('Filtered 1', res1)

        cv2.namedWindow('Filtered 2', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtered 2', WEIGHT, HEIGHT)
        cv2.imshow('Filtered 2', res2)

        # Update color-preview rectangles in the GUI
        lower_rgb1 = hsv_to_rgb(lower_h1, lower_s1, lower_v1)
        upper_rgb1 = hsv_to_rgb(upper_h1, upper_s1, upper_v1)
        lower_rgb2 = hsv_to_rgb(lower_h2, lower_s2, lower_v2)
        upper_rgb2 = hsv_to_rgb(upper_h2, upper_s2, upper_v2)

        canvas1_lower.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % lower_rgb1, outline="")
        canvas1_upper.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % upper_rgb1, outline="")
        canvas2_lower.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % lower_rgb2, outline="")
        canvas2_upper.create_rectangle(0, 0, 50, 50, fill='#%02x%02x%02x' % upper_rgb2, outline="")
    except ValueError:
        pass  # Ignore invalid integer inputs in the Entry boxes

def load_image(index):
    """
    Load the image at the given index from image_files into `frame`.
    Then update the displayed result.
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
    Go to the previous image in the list.
    """
    load_image(current_index - 1)

def next_image():
    """
    Go to the next image in the list.
    """
    load_image(current_index + 1)

# ---------- MAIN SCRIPT ----------

root = tk.Tk()
root.title("HSV Color Filter")

# Ask the user to pick a folder of images
image_folder = filedialog.askdirectory(title="Select a folder containing images")
if not image_folder:
    print("No folder selected. Exiting.")
    root.destroy()
    exit()

# Gather images (customize extensions if needed)
image_files = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
]
image_files.sort()

if not image_files:
    print("No images found in the selected folder.")
    root.destroy()
    exit()

current_index = 0
frame = None

# --- Filter 1 ---
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

# --- Filter 2 ---
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

# Navigation buttons
btn_prev = tk.Button(root, text="<< Previous", command=prev_image)
btn_prev.grid(row=14, column=0)
btn_next = tk.Button(root, text="Next >>", command=next_image)
btn_next.grid(row=14, column=1)

# Update button (re-applies filter if desired)
btn_update = tk.Button(root, text="Apply Filter", command=update_image)
btn_update.grid(row=14, column=2)

# Load the first image
load_image(0)

# Start the Tkinter loop
root.mainloop()

# Release windows when done
cv2.destroyAllWindows()
