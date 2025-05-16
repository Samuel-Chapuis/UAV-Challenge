'''
Projet ...... : Application Web de control d'un drone

Auteurs ..... : Samuel Chapuis
............. :

Langage ..... : Python 3.11.11           
Version ..... : 2.1.0
'''

# -------------------------------- #
# Import Locaux
from wbs.webb import app
from video.model import model

# Import Globaux
import cv2
import threading
import numpy as np
import time
import torch
from ultralytics import YOLO
# -------------------------------- #




if __name__ == '__main__':    
    app.run(debug=True, threaded=True)
